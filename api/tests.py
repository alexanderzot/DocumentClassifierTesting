from audioop import add

from django.test import TestCase
from random import randint
from api.models import *
from api.threads import Threads


class FileCategoryTest(TestCase):
    def setUp(self):
        self.Category = FileCategory.create("test_category")

    def tearDown(self):
        FileCategory.remove_all()

    def testCreate(self):
        self.assertTrue(isinstance(self.Category, FileCategory))
        self.assertFalse(FileCategory.create("test_category"))

    def testIsCategoryId(self):
        self.assertTrue(FileCategory.is_category_by_id(1))

    def testIsCategoryName(self):
        self.assertTrue(FileCategory.is_category_by_name("test_category"))

    def testGetCategoryName(self):
        self.assertFalse(FileCategory.get_category_by_name(""))
        category = FileCategory.get_category_by_name("test_category")
        self.assertEqual(category.get_id(), 1)
        self.assertEqual(category.get_name(), "test_category")

    def testGetCategoryId(self):
        self.assertFalse(FileCategory.get_category_by_id(2))
        category = FileCategory.get_category_by_id(1)
        self.assertEqual(category.get_id(), 1)
        self.assertEqual(category.get_name(), "test_category")


class CreatePathTest(TestCase):
    def testFilePath(self):
        path = get_file_path(None, "filename")
        self.assertEqual(path.split('.')[-1], "txt")


class UserTest(TestCase):
    def setUp(self):
        self.User = User(username='admin', password='admin')
        self.User.save()

    def tearDown(self):
        User.objects.all().delete()

    def testIsUser(self):
        self.assertTrue(User.objects.filter(username='admin').exists())

    def testGetUser(self):
        user = User.objects.get(username='admin')
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user, self.User)
        self.assertEqual(user.get_username(), 'admin')


class AlgorithmTest(TestCase):
    def setUp(self):
        self.algorithm = Algorithm.create('algo')

    def testCreate(self):
        self.assertFalse(Algorithm.create('algo'))
        self.assertTrue(isinstance(self.algorithm, Algorithm))

    def testIsAlgorithm(self):
        self.assertTrue(Algorithm.is_algorithm_name('algo'))
        self.assertFalse(Algorithm.is_algorithm_name('none'))
        self.assertTrue(Algorithm.is_algorithm_id(1))
        self.assertFalse(Algorithm.is_algorithm_id(2))

    def testGetAlgorithmData(self):
        algo = Algorithm.get_algorithm_by_name('algo')
        self.assertEqual(algo.get_name(), 'algo')
        self.assertEqual(algo.get_id(), 1)
        self.assertEqual(algo.get_date_train(), None)
        self.assertNotEqual(algo.get_train_file_data_name(), "")

    def testAlgorithmId(self):
        self.assertFalse(Algorithm.get_algorithm_by_id(2))
        self.assertTrue(Algorithm.get_algorithm_by_id(1))
        self.assertEqual(Algorithm.get_algorithm_by_id(1), self.algorithm)

    def testGetAlgorithm(self):
        self.assertFalse(Algorithm.get_algorithm_by_name('none'))


    # def testLogoutAndLogin(self):
    #     page = self.app.get('/', user='admin')
    #     page = page.click(u'Выйти').follow()
    #     assert u'Выйти' not in page
    #     login_form = page.click(u'Войти', index=0).form
    #     login_form['email'] = 'example@example.com'
    #     login_form['password'] = '123'
    #     result_page = login_form.submit().follow()
    #     assert u'Войти' not in result_page
    #     assert u'Выйти' in result_page
    #
    # def testEmailRegister(self):
    #     register_form = self.app.get('/').click(u'Регистрация').form
    #
    #     self.assertEqual(len(mail.outbox), 0)
    #     register_form['email'] = 'example2@example.com'
    #     register_form['password'] = '123'
    #     assert u'Регистрация завершена' in register_form.submit().follow()
    #     self.assertEqual(len(mail.outbox), 1)
    #
    #     # активируем аккаунт и проверяем, что после активации
    #     # пользователь сразу видит свои покупки
    #     mail_body = unicode(mail.outbox[0].body)
    #     activate_link = re.search('(/activate/.*/)', mail_body).group(1)
    #     activated_page = self.app.get(activate_link).follow()
    #     assert u'


class ThreadFileCategoryTest(TestCase):
    @classmethod
    def setUpClass(cls):
        def create_category(category_list, num, step):
            for i in range(num - 1, len(category_list), step):
                FileCategory.create(cls.category_list[i])

        def create_category_list(count):
            return ["category_%s" % i for i in range(1, count)]

        cls.category_list = create_category_list(1000)
        thread_count = 4
        threads = [Threads(target=create_category, args=(cls.category_list, i, thread_count)) for i in range(1, thread_count + 1)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    @classmethod
    def tearDownClass(cls):
        FileCategory.remove_all()

    def testThreadFileCategoryCreating(self):
        self.assertEqual(len(self.category_list), FileCategory.objects.all().count())

    def testThreadFileCategoryHasElement(self):
        rand_index = randint(0, len(self.category_list))
        rand_category_name = self.category_list[rand_index]
        self.assertTrue(FileCategory.is_category_by_name(rand_category_name))

    def testThreadFileCategoryHasNotElement(self):
        self.assertFalse(FileCategory.is_category_by_name("bad_category"))

    def testThreadFileCategoryBadId(self):
        self.assertTrue(FileCategory.is_category_by_id(0))
        self.assertTrue(FileCategory.is_category_by_id(len(self.category_list) - 1))

    def testThreadFileCategoryBadId(self):
        self.assertFalse(FileCategory.is_category_by_id(len(self.category_list) + 1))


class ThreadUserTest(TestCase):
    @classmethod
    def setUpClass(cls):
        def create_users(category_list, num, step):
            for i in range(num - 1, len(category_list), step):
                user = User(username=cls.user_list[i][0], password=cls.user_list[i][1])
                user.save()

        def create_user_list(count):
            return [("user_%s" % i, "pass_%d" % i) for i in range(1, count)]

        cls.user_list = create_user_list(10000)
        thread_count = 4
        threads = [Threads(target=create_users, args=(cls.user_list, i, thread_count)) for i in
                   range(1, thread_count + 1)]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()

    def testThreadUserCount(self):
        self.assertEqual(User.objects.all().count(), len(self.user_list))

    def testThreadUserIsUser(self):
        rand_index = randint(0, len(self.user_list))
        rand_user_name = self.user_list[rand_index][0]
        self.assertTrue(User.objects.filter(username=rand_user_name).exists())

    def testThreadUserIsNotUser(self):
        self.assertFalse(User.objects.filter(username='user_bad_name').exists())

    def testThreadUserIsId(self):
        rand_index = randint(0, len(self.user_list))
        self.assertTrue(User.objects.filter(id=rand_index).exists())

    def testThreadUserIsNotId(self):
        index = len(self.user_list)
        self.assertTrue(User.objects.filter(id=index).exists())