**Тестовое задание для  компании "Строительный Двор"**

Порядок установки на сервере Linux, система работает с базой данных Postgres.

1) Склонировать репозиторий, установить виртуальное окружение и пакеты

`git clone https://github.com/gaichikov/sdvor.git`
`cd sdvor`
`virtualenv -p python3 venv`
`source venv/bin/activate`
`pip install -r requirements.txt`

2) Файл конфигурации sdvor/__local_settings.py  переименовать в sdvor/local_settings.py, поправить в нем реквизиты доступа к БД Postgres . 

3) Создать базу данных Postgres
 
`su postgres`
`psql `
`> create database sdvor;`

4) Применить миграции

./manage.py makemigrations order_api
./manage.py migrate
 
5) Загрузить фикстуры из fixtures/items.json

./manage.py loaddata fixtures/users.json
./manage.py loaddata fixtures/items.json

6) Запустить сервер

./manage.py runserver 0.0.0.0:8000 

Поскольку нельзя пользоваться django restframework сделаны view которые обрабатывают запросы POST/GET и возвращают JSONResponse с соответствующим статусом.

Добавлено два приложения: orders_api, для api запросов и orders_site - с формой авторизации и простой формой добавления заказа с использованием vue.js, и axios для отправки get и post запросов.

По ссылке server_ip_addr:8000 доступна авторизация (реализована через нативные  view из django.contrib.auth ), после авторизации редирект на форму заказа.

Доступ: 
логин: test
пароль: sdvor12345

Авторизация по JWT токену доступна через роут /api/login_jwt - тут получаем токен (в post request указываем username и password), далее полученный токен подставляем в хедер Authorization. Время жизни токена 10 минут.

доступные api endpoint`ы:

/api/orders/pk  - детали заказа с полной суммой заказа
/api/items  - список товаров

/api/orders  - список заказов (GET) или создание нового заказа (POST) в формате:
{phone: 'номер телефона'
address: 'адрес'
full_name: 'ФИО'
email: 'Email'
items: [{"quantity":4,"item":{"id":2}}, {"quantity":2,"item":{"id":1}}] }


Тесты доступны для API и авторизации, в том числе JWT авторизации.
`/order_site/test.py`
`/order_api/test.py`

Запуск через 

`./manage.py test`

Админский интерфейс сильно не кастомизировал, но создать заказы, товары через него можно.