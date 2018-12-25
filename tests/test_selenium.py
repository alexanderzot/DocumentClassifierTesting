from django.test import TestCase
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time


class LoginTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox(executable_path='C:/Develop/Projects/Git/document_classifier/driver/geckodriver.exe',
                                        firefox_binary='C:/Program Files/Mozilla Firefox/firefox.exe')

    def tearDown(self):
        self.driver.close()

    def testGetHomePage(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        time.sleep(2)
        self.assertIn("Document Classifier", driver.title)

    def testGetSettingPage(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/setting/")
        time.sleep(2)
        try:
            driver.find_element_by_class_name("alert.alert-danger")
        except NoSuchElementException:
            self.assertTrue(False)
        self.assertTrue(True)

    def testLogin(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        elem = driver.find_element_by_name("nameLogIn")
        elem.click()
        time.sleep(3)
        driver.find_element_by_id("inputSignInEmail").send_keys("admin@example.com")
        driver.find_element_by_id("inputSignInPassword").send_keys("admin")
        driver.find_element_by_id("buttonSignIn").click()
        time.sleep(3)
        self.assertIn("admin", driver.find_element_by_class_name("font-weight-bold").text)

    def testBadLogin(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        elem = driver.find_element_by_name("nameLogIn")
        elem.click()
        time.sleep(3)
        driver.find_element_by_id("inputSignInEmail").send_keys("admin@example.com")
        driver.find_element_by_id("inputSignInPassword").send_keys("123qwe")
        driver.find_element_by_id("buttonSignIn").click()
        time.sleep(3)
        self.assertNotIn("admin", driver.find_element_by_class_name("font-weight-bold").text)

    def testRegistration(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        elem = driver.find_element_by_name("nameLogIn")
        elem.click()
        time.sleep(3)
        driver.find_element_by_id("inputSignInEmail").send_keys("admin@example.com")
        driver.find_element_by_id("inputSignInPassword").send_keys("123qwe")
        driver.find_element_by_id("buttonSignIn").click()
        time.sleep(3)
        self.assertNotIn("admin", driver.find_element_by_class_name("font-weight-bold").text)

    def testLogout(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        elem = driver.find_element_by_name("nameLogIn")
        elem.click()
        driver.find_element_by_id("inputSignInEmail").send_keys("admin@example.com")
        driver.find_element_by_id("inputSignInPassword").send_keys("admin")
        driver.find_element_by_id("buttonSignIn").click()
        time.sleep(3)

        driver.find_element_by_id("singOut").click()
        time.sleep(3)
        self.assertIn("Войти", driver.find_element_by_name("nameLogIn").text)

    def testSettingWithLogin(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        elem = driver.find_element_by_name("nameLogIn")
        elem.click()
        driver.find_element_by_id("inputSignInEmail").send_keys("admin@example.com")
        driver.find_element_by_id("inputSignInPassword").send_keys("admin")
        driver.find_element_by_id("buttonSignIn").click()
        time.sleep(3)

        driver.get("http://127.0.0.1:8000/setting/")
        time.sleep(2)
        self.assertIn("ДОБАВИТЬ", driver.find_element_by_id("id_button_add").text)

    def testSettingCategoryAdd(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        elem = driver.find_element_by_name("nameLogIn")
        elem.click()
        driver.find_element_by_id("inputSignInEmail").send_keys("admin@example.com")
        driver.find_element_by_id("inputSignInPassword").send_keys("admin")
        driver.find_element_by_id("buttonSignIn").click()
        time.sleep(3)

        driver.get("http://127.0.0.1:8000/setting/")

        driver.find_element_by_id("id_category_name").send_keys("Test" + str(datetime.now()))
        driver.find_element_by_id("id_button_add").click()
        time.sleep(3)

        self.assertIn("Категория успешно добавлена", driver.find_element_by_class_name("alert.alert-success.my-2").text)

    def testSettingCategoryBad(self):
        driver = self.driver
        driver.get("http://127.0.0.1:8000/")
        elem = driver.find_element_by_name("nameLogIn")
        elem.click()
        driver.find_element_by_id("inputSignInEmail").send_keys("admin@example.com")
        driver.find_element_by_id("inputSignInPassword").send_keys("admin")
        driver.find_element_by_id("buttonSignIn").click()
        time.sleep(3)

        driver.get("http://127.0.0.1:8000/setting/")

        time.sleep(3)
        elem = driver.find_element_by_tag_name("td")
        driver.find_element_by_id("id_category_name").send_keys(elem.text)
        driver.find_element_by_id("id_button_add").click()
        time.sleep(3)

        try:
            driver.find_element_by_class_name("alert.alert-danger.my-2").text
        except NoSuchElementException:
            self.assertTrue(False)
        self.assertTrue(True)
