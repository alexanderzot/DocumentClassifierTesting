from django.test import TestCase

# Create your tests here.
from common.parser import *

import PyRTF.Elements
import PyRTF.Renderer

class TestDocumentParser(TestCase):
    def setUp(self):
        self.texts = [
            " ",
            "Привет, мир!",
            "Привет, мир!\n Привет, мир!",
        ]
        self.filename = 'test'

    def compare_text(self, text1, text2):
        text1 = re.sub(r'\s+', ' ', text1.replace('\n', ' '))
        text2 = re.sub(r'\s+', ' ', text2.replace('\n', ' '))
        if text1 and text1[0] == ' ':
                text1 = text1[1:]
        if text1 and text1[-1] == ' ':
                text1 = text1[:-1]
        if text2 and text2[0] == ' ':
                text2 = text2[1:]
        if text2 and text2[-1] == ' ':
                text2 = text2[:-1]
        return text1 == text2

    def create_file(self, type, text):
        if type == 'txt':
          with open(self.filename + '.txt', 'w') as f:
              f.write(text)
        elif type == 'docx':
            doc = docx.Document()
            doc.add_paragraph(text)
            doc.add_page_break()
            doc.save(self.filename + '.docx')
        elif type == 'rtf':
            doc = PyRTF.Elements.Document()
            section = PyRTF.Elements.Section()
            doc.Sections.append(section)
            section.append(text)
            DR = PyRTF.Renderer.Renderer()
            DR.Write(doc, open('%s.rtf' % self.filename, 'w'))
        elif type == 'out':
            with open(self.filename + '.out', 'w') as f:
                f.write(text)


    def test_parser_texts(self):
        for text in self.texts:
            for file_type in list_of_parse_type:
                self.create_file(file_type, text)
                parsed_text = parse_document(self.filename + '.' + file_type)
                #print(parsed_text)
                self.assertTrue(self.compare_text(text, parsed_text))

    def test_parser_texts_docx(self):
        for text in self.texts:
            file_type = 'docx'
            self.create_file(file_type, text)
            parsed_text = get_text_from_docx(self.filename + '.' + file_type)
            self.assertTrue(self.compare_text(text, parsed_text))

    def test_parser_texts_rtf(self):
        for text in self.texts:
            file_type = 'rtf'
            self.create_file(file_type, text)
            parsed_text = get_text_from_rtf(self.filename + '.' + file_type)
            self.assertTrue(self.compare_text(text, parsed_text))

    def test_parser_texts_txt(self):
        for text in self.texts:
            file_type = 'txt'
            self.create_file(file_type, text)
            parsed_text = get_text_from_txt(self.filename + '.' + file_type)
            self.assertTrue(self.compare_text(text, parsed_text))


    def test_error_format(self):
        text = self.texts[2]
        file_type = 'out'
        self.create_file(file_type, text)
        parsed_text = parse_document(self.filename + '.' + file_type)
        self.assertEqual("", parsed_text)


class TestWords(TestCase):
    def setUp(self):
        self.texts = [
            " ",
            "Привет, мир!",
            "Привет, мир!\n Привет, мир! Делающему нет пока в",
            "Привет миру!\n Привет, мир! Делает, Делать нет пока в",
        ]
        self.words = [
            {},
            {'мир': 1, 'привет': 1},
            {'привет': 2, 'мир': 2, 'делающему': 1, 'нет': 1, 'пока': 1, 'в': 1},
            {'привет': 2, 'миру': 1, 'мир': 1, 'делает': 1, 'делать': 1, 'нет': 1, 'пока': 1, 'в': 1}
        ]
        self.key_words_ALL = [
            {},
            {'мир': 1, 'привет': 1},
            {'привет': 2, 'мир': 2, 'делать': 1, 'нет': 1, 'пока': 1, 'в': 1},
            {'привет': 2, 'мир': 2, 'делать': 2, 'нет': 1, 'пока': 1, 'в': 1}
        ]
        self.key_words_NOUN = [
            {},
            {'мир': 1, 'привет': 1},
            {'привет': 2, 'мир': 2},
            {'привет': 2, 'мир': 2}
        ]
        self.key_words_NOUN_INFN = [
            {},
            {'мир': 1, 'привет': 1},
            {'привет': 2, 'мир': 2},
            {'привет': 2, 'мир': 2, 'делать': 1}
        ]

        self.filename = 'test'

    def create_file(self, text):
        with open(self.filename + '.txt', 'w') as f:
            f.write(text)


    def test_get_words(self):
        for i in range(len(self.texts)):
            text = self.texts[i]
            parsed_words = get_words_from_text(text)
            self.assertDictEqual(parsed_words, self.words[i])

    def test_get_words_from_document(self):
        for i in range(len(self.texts)):
            text = self.texts[i]
            self.create_file(text)
            parsed_words = get_words_from_document(self.filename + '.txt')
            self.assertDictEqual(parsed_words, self.words[i])

    def test_get_key_words_ALL(self):
        for i in range(len(self.words)):
            key_words = get_key_words(self.words[i])
            self.assertDictEqual(key_words, self.key_words_ALL[i])

    def test_get_key_words_NOUN(self):
        for i in range(len(self.words)):
            key_words = get_key_words(self.words[i], ['NOUN'])
            self.assertDictEqual(key_words, self.key_words_NOUN[i])

    def test_get_key_words_NOUN_INFN(self):
        for i in range(len(self.words)):
            key_words = get_key_words(self.words[i], ['NOUN', 'INFN'])
            self.assertDictEqual(key_words, self.key_words_NOUN_INFN[i])


class TestGetFeatures(TestCase):
    def setUp(self):
        self.all_words = [
            {},
            {'привет': None, 'мир': None},
            {'привет': None, 'миру': None, 'мир': None, 'делает': None, 'делать': None, 'нет': None, 'пока': None, 'в': None}
        ]
        self.words = [
            {},
            {'мир': 1, 'привет': 1},
            {'привет': 2, 'мир': 2, 'делающему': 1, 'нет': 1, 'пока': 1, 'в': 1, 'солнце': None},
        ]
        self.results = [
            {'count(привет)': 1, 'count(мир)': 1},
            {'count(привет)': 2, 'count(мир)': 2},
            {'count(привет)': 2, 'count(миру)': 0, 'count(мир)': 2, 'count(делает)': 0, 'count(делать)': 0,
             'count(нет)': 1, 'count(пока)': 1, 'count(в)': 1},

        ]


    def test_empty_all_words(self):
        for i in range (len(self.words)):
            f = get_features(self.words[i], self.all_words[0])
            self.assertDictEqual({}, f)

    def test_all_words_in_words(self):
        for i in range (1, len(self.words)):
            f = get_features(self.words[i], self.all_words[1])

    def test_equal_all_words(self):
        f = get_features(self.words[1], self.all_words[1])
        self.assertDictEqual(f, self.results[0])

    def test_with_diff_all_words(self):
        f = get_features(self.words[2], self.all_words[2])
        self.assertDictEqual(f, self.results[2])

    def test_more_than_all_words(self):
        f = get_features(self.words[2], self.all_words[1])
        self.assertDictEqual(f, self.results[1])

class TestPrepareTrain(TestCase):
    def setUp(self):
        self.texts = [
            [
                ''
            ],
            [
                "Привет мир"
            ],
            [
                'Кино',
                'Привет мир'
            ],
            [
                'Привет мир',
                'Привет мир'
            ]
        ]
        self.all_words = [
            {},
            {'привет': None, 'мир': None},
            {'кино': None, 'привет': None, 'мир': None},
            {'привет': None, 'мир': None},
        ]
        self.train_list = [
            [{}],
            [{'count(привет)': 1, 'count(мир)': 1}],
            [{'count(кино)': 1, 'count(привет)': 0, 'count(мир)': 0},
             {'count(кино)': 0, 'count(привет)': 1, 'count(мир)': 1}],
            [{'count(привет)': 1, 'count(мир)': 1}, {'count(привет)': 1, 'count(мир)': 1}]
        ]

        self.filename = 'test'

    def create_files(self, texts):
        document_list = []
        for i in range(len(texts)):
            filename = self.filename + str(i) + '.txt'
            with open(filename, 'w') as f:
                f.write(texts[i])
            document_list.append(filename)
        return document_list

    def compare_train(self, train1, train2):
        for i in range(len(train1)):
            self.assertDictEqual(train1[i], train2[i])
        return True


    def test_empty(self):
        document_list = self.create_files(self.texts[0])
        all_words, train_list = get_all_train_words_and_train_list(document_list)
        self.assertEqual(self.all_words[0], all_words)
        self.assertEqual(self.train_list[0], train_list)

    def test_one_file(self):
        document_list = self.create_files(self.texts[1])
        all_words, train_list = get_all_train_words_and_train_list(document_list)
        self.assertEqual(self.all_words[1], all_words)
        self.assertEqual(self.train_list[1], train_list)


    def test_different_files(self):
        document_list = self.create_files(self.texts[2])
        all_words, train_list = get_all_train_words_and_train_list(document_list)
        self.assertEqual(self.all_words[2], all_words)
        self.assertEqual(self.train_list[2], train_list)

    def test_equal_files(self):
        document_list = self.create_files(self.texts[3])
        all_words, train_list = get_all_train_words_and_train_list(document_list)
        self.assertEqual(self.all_words[3], all_words)
        self.assertEqual(self.train_list[3], train_list)

