from django.shortcuts import render
from django.contrib import auth
from api.models import *
from api.forms import *
from django.core.files.uploadedfile import SimpleUploadedFile
from common.tasks import *
from DoC_init.settings import *

def home(request):
    args = {}
    user = auth.get_user(request)
    args['user'] = user
    args['algorithms'] = Algorithm.objects.all()
    args['user_files'] = FileAnalise.objects.filter(user__username=user.get_username())

    if user.is_anonymous:
        args['error_desc'] = "Необходимо выполнить вход"
        return render(request, 'error.html', args)

    if request.method == "POST":
        data = request.POST
        algorithm = data['select_algorithm']

        form = UploadFileForm(request.POST or None, request.FILES or None)
        file_model = form.save(commit=False)
        file_model.set_owner(user_name=user.get_username())
        file_model.save()

        analise = FileAnalise.create(file_id=file_model.get_id(),
                                     user_name=user.get_username(),
                                     algorithm_id=algorithm
                                     )
        analise.save()

        file_path_analize = os.path.join(MEDIA_ROOT, file_model.get_file_path())

        train_file_path = os.path.join(MEDIA_ROOT, analise.algorithm.get_train_file_data_name())

        classify(file_path_analize, train_file_path, analise.id)

    return render(request, 'index.html', args)


def setting(request):
    args = {}
    user = auth.get_user(request)
    args['categorys'] = FileCategory.objects.all()
    args['algorithms'] = Algorithm.objects.all()

    if not user.is_staff:
        args['error_desc'] = "Для доступа нужны права администратора"
        return render(request, 'error.html', args)

    if request.method == 'POST':
        data = request.POST
        type_form = data['type']

        if type_form == 'add_category':
            category_name = data['name']
            category  = FileCategory.create(category_name=category_name)

            if not category:
                args['error_desc'] = "Категория '%s' уже существует!" % category_name
            else:
                args['success_desc'] = "Категория успешно добавлена"
        elif type_form == 'add_algorithm':
            algorithm_name = data['name']
            algorithm = Algorithm.create(algorithm_name=algorithm_name)

            if not algorithm:
                args['error_desc2'] = "Алгоритм с названием '%s' уже существует!" % algorithm_name
            else:
                args['success_desc2'] = "Алгоритм успешно создан"
        elif type_form == 'add_file':
            select_category_id = data['select_category']
            form = UploadFileForm(request.POST or None, request.FILES or None)
            file_model = form.save(commit=False)
            file_model.set_category_by_id(category_id=select_category_id)
            file_model.save()

    return render(request, 'setting.html', args)


def setting_algorithm(request, algorithm_id):
    args = {}
    user = auth.get_user(request)
    algorithm = Algorithm.get_algorithm_by_id(algorithm_id=algorithm_id)
    args['algorithm'] = algorithm
    args['files'] = File.objects.filter(category__isnull=False).exclude(train_files__id=algorithm_id)

    if not user.is_staff:
        args['error_desc'] = "Для доступа нужны права администратора"
        return render(request, 'error.html', args)

    if request.method == 'POST':
        data = request.POST
        type_input = data['type']

        if type_input == 'start_algorithm':
            data_file_name = os.path.join(MEDIA_ROOT, algorithm.train_data_file_name)

            data_files = []
            data_categorys = []
            for file in algorithm.train_files.all():
                data_files.append(os.path.join(MEDIA_ROOT, file.get_file_path()))
                data_categorys.append(file.category.get_name())
            #print(data_file_name)
            #print(data_files)
            #print(data_categorys)
            make_train(data_files, data_categorys, data_file_name, algorithm.get_id())
        elif type_input == 'add_algorithm':
            file_id = data['file_id']
            algorithm.add_file(file_id=file_id)

    return render(request, 'setting_algorithm.html', args)