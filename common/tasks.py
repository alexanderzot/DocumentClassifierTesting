from common.parser import *
from DoC_init.celery import app
from api.models import *
from datetime import datetime


#@app.task
def make_train(document_list, category_list, filename, algo_id):
    magic_train(document_list, category_list, filename)

    algorithm = Algorithm.get_algorithm_by_id(algorithm_id=algo_id)
    algorithm.date_train = datetime.now()
    algorithm.save()

def classify(document_path, filename, file_analize_id):
    res = classify_document(document_path, filename)
    file = FileAnalise.objects.get(id=file_analize_id)
    file.result = FileCategory.get_category_by_name(category_name=res)
    file.save()
