#import magic
import docx
import re
from striprtf.striprtf import rtf_to_text

list_of_parse_type = [
    'docx',
    'txt',
    'rtf'
]


def get_text_from_docx(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


def get_text_from_txt(filename):
    f = open(filename)
    #print(filename)
    text = f.read()
    return text


def get_text_from_rtf(filename):
    with open(filename) as source:
        result = rtf_to_text(source.read())
    return result


def get_file_type(filename):
    extension = filename.split('.')[-1]
    return [extension]


def get_words_from_text(text):
    words = re.findall(r"[\w']+", text)
    words = [w.lower() for w in words]
    result = dict.fromkeys(words, 0)
    for word in words:
        result[word] = result[word] + 1
    return result

def parse_document(path):
    '''
    import subprocess
    import shlex

    filename = path
    cmd = shlex.split('file --mime-type {0}'.format(filename))
    result = subprocess.check_output(cmd)
    mime_type = result.split()[-1]
    print(mime_type)

    import fleep

    with open(path, "rb") as file:
        info = fleep.get(file.read(128))
    print(info)

    print(info.type)  # prints ['image']
    print(info.extension)  # prints ['png']
    print(info.mime)  # prints ['image/png']

    print(info.extension_matches("txt"))
    print(info.extension_matches("docx"))

    print(magic.from_file(path))
    print(magic.from_file(path, mime = True))
    '''
    file_type = get_file_type(path)
    #parse document
    text = ''
    if 'docx' in file_type:
        text = get_text_from_docx(path)
    elif 'txt' in file_type:
        text = get_text_from_txt(path)
    elif 'rtf' in file_type:
        text = get_text_from_rtf(path)
    return text

#/home/moskov/Docs/doc.txt
#/home/moskov/Docs/doc.docx

def get_words_from_document(path):
    text = parse_document(path)
    #print(text)
    #text analiz
    result = get_words_from_text(text)
    return result


import pymorphy2
morph = pymorphy2.MorphAnalyzer()


# filter
# [] - all words
# NOUN	имя существительное	хомяк
# ADJF	имя прилагательное (полное)	хороший
# INFN	глагол (инфинитив)	говорить, сказать
# NUMR	числительное	три, пятьдесят
# ADVB	наречие	круто

# NPRO	местоимение-существительное	он
# PRED	предикатив	некогда
# PREP	предлог	в
# CONJ	союз	и
# PRCL	частица	бы, же, лишь
# INTJ	междометие	ой

####### не используются
# COMP	компаратив	лучше, получше, выше
# VERB	глагол (личная форма)	говорю, говорит, говорил
# ADJS	имя прилагательное (краткое)	хорош
# PRTF	причастие (полное)	прочитавший, прочитанная
# PRTS	причастие (краткое)	прочитана
# GRND	деепричастие	прочитав, рассказывая

def get_key_words(words, filter = []):
    key_words = {}
    for word in words.keys():
        parsed = morph.parse(word)[0]
        normal_form = parsed.normal_form
        flag_add = False
        if not filter:
            flag_add = True
        else:
            for f in filter:
                if parsed.tag.POS == f:
                    flag_add = True
        if flag_add:
            if not normal_form in key_words:
                key_words[normal_form] = 0
            key_words[normal_form] = key_words[normal_form] + words[word]

    return key_words

def get_features(doc, all_words):
    doc_features = {}
    for word in all_words.keys():
        if word in doc:
            doc_features['count({})'.format(word)] = doc[word]
        else:
            doc_features['count({})'.format(word)] = 0
    return doc_features


def get_all_train_words_and_train_list(document_list):
    documents_words = [get_words_from_document(doc) for doc in document_list]
    filter = ['NOUN']
    documents_normal_words = [get_key_words(doc, filter) for doc in documents_words]
    all_words = {}
    for words in documents_normal_words:
        all_words.update(dict.fromkeys(words.keys()))

    train_list = [get_features(doc, all_words) for doc in documents_normal_words]

    return all_words, train_list
    #print(all_words)


def get_set_for_classifier(doc_path, all_words):
    #print(doc_path)
    documents_words = get_words_from_document(doc_path)
    #filter = ['NOUN', 'ADJF', 'INFN', 'NUMR', 'ADVB']
    filter = ['NOUN']
    print(documents_words)
    documents_normal_words = get_key_words(documents_words, filter)
    print(documents_normal_words)
    return get_features(documents_normal_words, all_words)


def get_train_set_and_all_words(document_list, category_list):
    all_words, train_list = get_all_train_words_and_train_list(document_list)
    set_trains = [(train_list[i], category_list[i]) for i in range(len(document_list))]
    return set_trains, all_words

import pickle
from nltk.classify import NaiveBayesClassifier

#save classifier to filename
def magic_train(document_list, category_list, filename):
    train, all_words = get_train_set_and_all_words(document_list, category_list)
    classifier = NaiveBayesClassifier.train(train)
    #print(all_words)
    #print(train)
    with open(filename, 'wb') as f:
        pickle.dump(classifier, f)
        pickle.dump(all_words, f)

#classify document from path by train data from filename
def classify_document(document_path, filename):
    #print('classify')
    with open(filename, 'rb') as f:
        classifier = pickle.load(f)
        all_words = pickle.load(f)
    print(document_path)
    test_data = get_set_for_classifier(document_path, all_words)
    print(test_data)
    return classifier.classify(test_data)



def test_run ():
    words = get_words_from_document('/home/moskov/Docs/doc.docx')
    print(words)
    res = get_key_words(words)
    print(res)
    res = get_key_words(words, ['NOUN'])
    print(res)

    words = get_words_from_document('/home/moskov/Docs/doc.txt')
    print(words)
    res = get_key_words(words)
    print(res)
    res = get_key_words(words, ['NOUN'])
    print(res)

    words = get_words_from_document('/home/moskov/Docs/test.txt')
    print(words)
    res = get_key_words(words)
    print(res)
    res = get_key_words(words, ['NOUN'])
    print(res)


    documents = [
        '/home/moskov/Docs/doc.docx',
        '/home/moskov/Docs/doc.txt'
    ]
    categories = [
        'a',
        'b'
    ]
    magic_train(documents, categories, 'train.bin')
    print(classify_document('/home/moskov/Docs/test.txt', 'train.bin'))

    '''
    train, all_words = get_train_set_and_all_words(documents, categories)
    print(train)
    print(all_words)

    classifier = NaiveBayesClassifier.train(train)

    test_data = get_set_for_classifier('/home/moskov/Docs/test.txt', all_words)
    print(classifier.classify(test_data))
    '''


#test_run()



