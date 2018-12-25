# Document Classifier

## API

### Авторизация
```
url: /api/user/sign_in/
method: POST
json: {"email": "admin@example.com", "password": "admin"}
```

**Результат:**

1. Успешная авторизация
```
status: 200
json: {'status': 'OK', 'username': $username$}
```
2. Ошибка авторизации
```
status: 204
json: {'status': 'FAIL'}
```

### Деавторизация
```
url: /api/user/sign_out/
method: POST
```

**Результат:**

1. Успешная авторизация
```
status: 200
json: {'status': 'OK'}
```
2. Ошибка авторизации
```
status: 204
json: {'status': 'FAIL'}
```





## Пакеты Python:
```ssh
Django	2.1.3	2.1.3
djangorestframework	3.9.0	3.9.0

python-docx 0.8.7
striprtf 0.0.3

pymorphy2 0.8
pymorphy2-dicts-ru 2.4.404381.4453942

nltk 3.4
celery 4.2.1

Testing:
coverage  4.5.2
#WebTest 2.0.32
#django-webtest 1.9.4
django-coverage 1.2.4

pip install git+git://github.com/jwaschkau/pyrtf

selenium 3.141.0

```





## Администрирование

### Активация виртуальной среды
**Windows: **
```
source venv/Scripts/activate
```

**Linux: **
```
source venv/bin/activate
```

### Миграция
```
python manage.py makemigrations
python manage.py migrate
```

### Создание суперпользователя
**Windows: **

```ssh
winpty python manage.py createsuperuser
```

**Linux: **

```ssh
winpty python manage.py createsuperuser
```

## Тестирование

coverage run --source='.' manage.py test api

Удаление временного  файла
coverage erase

coverage report
coverage html


coverage run manage.py test api -v 2
coverage html

## Selenium установка

https://selenium-python.readthedocs.io/installation.html
geckodriver (32 bit) https://github.com/mozilla/geckodriver/releases
install FireFox

Плагины
https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd
https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/


## Запуск тестов
python manage.py test

python manage.py test --verbosity 2