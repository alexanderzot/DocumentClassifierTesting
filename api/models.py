from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import uuid


class FileCategory(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)

    @staticmethod
    def is_category_by_name(category_name):
        return FileCategory.objects.filter(name=category_name).exists()

    @staticmethod
    def is_category_by_id(category_id):
        return FileCategory.objects.filter(id=category_id).exists()

    @staticmethod
    def get_category_by_name(category_name):
        if not FileCategory.is_category_by_name(category_name=category_name):
            return False
        return FileCategory.objects.get(name=category_name)

    @staticmethod
    def get_category_by_id(category_id):
        if not FileCategory.is_category_by_id(category_id=category_id):
            return False
        return FileCategory.objects.get(id=category_id)

    @staticmethod
    def create(category_name):
        if FileCategory.is_category_by_name(category_name=category_name):
            return False
        file = FileCategory(name=category_name)
        file.save()
        return file

    @staticmethod
    def remove(category_name):
        if not FileCategory.is_category_by_name(category_name=category_name):
            return False

        FileCategory.objects.filter(name=category_name).delete()
        return True

    @staticmethod
    def remove_all():
        FileCategory.objects.all().delete()

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    if ext == filename:
        ext = "txt"
    new_filename = "%s.%s" % (uuid.uuid4(), ext)
    folder_name = datetime.now().strftime("%Y_%m_%d")
    return '%s/%s' % (folder_name, new_filename)


class File(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    loaded_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    file = models.FileField(upload_to=get_file_path, null=False, blank=False)
    user_owner = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    category = models.ForeignKey(FileCategory, on_delete=models.PROTECT, null=True, blank=True)

    @staticmethod
    def create(file_name, file, user_name):
        f = File(name=file_name,
                 file=file,
                 user_owner=User.objects.get(username=user_name))
        f.save()
        return f

    @staticmethod
    def create_admin(file_name, file):
        f = File(name=file_name, file=file)
        f.save()
        return f

    @staticmethod
    def get_user_owner_files(user_id):
        return File.objects.filter(user_owner__id=user_id)

    def get_file_path(self):
        return str(self.file)

    def get_ext(self):
        filename = self.get_file_path()
        return filename.split('.')[-1]

    def set_owner(self, user_name):
        self.user_owner = User.objects.get(username=user_name)

    def set_category_by_name(self, category_name):
        file_category = FileCategory.get_category_by_name(category_name=category_name)
        if file_category:
            self.category = file_category

    def set_category_by_id(self, category_id):
        file_category = FileCategory.get_category_by_id(category_id=category_id)
        if file_category:
            self.category = file_category

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_loaded_date(self):
        return self.loaded_date

    def get_owner(self):
        return self.user_owner

    def get_category(self):
        return self.category

    @staticmethod
    def is_file_id(file_id):
        return File.objects.filter(id=file_id).exists()

    @staticmethod
    def get_file_by_id(file_id):
        if not File.is_file_id(file_id=file_id):
            return False
        return File.objects.get(id=file_id)

    def __str__(self):
        return "%d__%s.%s" % (self.id, self.name, self.get_ext())

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"


class Algorithm(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)
    train_files = models.ManyToManyField(File, related_name='train_files', blank=True)
    date_train = models.DateTimeField(null=True, blank=True)
    train_data_file_name = models.CharField(max_length=255, null=False, blank=False)

    @staticmethod
    def is_algorithm_name(algorithm_name):
        return Algorithm.objects.filter(name=algorithm_name).exists()

    @staticmethod
    def is_algorithm_id(algorithm_id):
        return Algorithm.objects.filter(id=algorithm_id).exists()

    @staticmethod
    def get_algorithm_by_id(algorithm_id):
        if not Algorithm.is_algorithm_id(algorithm_id=algorithm_id):
            return False
        return Algorithm.objects.get(id=algorithm_id)

    @staticmethod
    def get_algorithm_by_name(algorithm_name):
        if not Algorithm.is_algorithm_name(algorithm_name=algorithm_name):
            return False
        return Algorithm.objects.get(name=algorithm_name)

    @staticmethod
    def create(algorithm_name):
        if Algorithm.is_algorithm_name(algorithm_name=algorithm_name):
            return False
        algorithm = Algorithm(name=algorithm_name)
        algorithm.train_data_file_name = '%s/%s' % ('__train__', uuid.uuid4())
        algorithm.save()
        return algorithm

    def add_file(self, file_id):
        file_object = File.get_file_by_id(file_id=file_id)
        if file_object:
            self.train_files.add(file_object)

    def get_train_file_data_name(self):
        return self.train_data_file_name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_date_train(self):
        return self.date_train


class FileAnalise(models.Model):
    file = models.ForeignKey(File, on_delete=models.PROTECT, null=False, blank=False)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.PROTECT)
    result = models.ForeignKey(FileCategory, on_delete=models.PROTECT, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    @staticmethod
    def create (file_id, user_name, algorithm_id):
        file_object = File.get_file_by_id(file_id=file_id)
        if not file_object:
            return False

        algorithm_object = Algorithm.get_algorithm_by_id(algorithm_id=algorithm_id)
        if not algorithm_object:
            return False

        is_user_object = User.objects.filter(username=user_name).exists()
        if not is_user_object:
            return False
        user_object = User.objects.get(username=user_name)

        file_analise = FileAnalise(file=file_object,
                                   algorithm=algorithm_object,
                                   user=user_object
                                   )
        file_analise.save()
        return file_analise

    def set_result(self, category_name):
        category_object = FileCategory.get_category_by_name(category_name=category_name)
        if category_object:
            self.result = category_object

    def save_result(self, category_name):
        self.set_result(category_name=category_name)
        self.save()

