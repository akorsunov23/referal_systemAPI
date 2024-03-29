# Реферальная система и API.

### Настройка проекта:
- Создать проект на локальном компьютере.
- Склонировать репозиторий
```angular2html
$ git clone https://github.com/akorsunov23/referal_systemAPI
```
- Перейти в папку склонированного проекта
```angular2html
$ cd referal_systemAPI
```
- Добавить в корень проекта файл '.env' и указать в нём переменные согласно инструкциям '.env.temp' 
- Установить зависимости:
````angular2html
$ pip install -r req.txt
````
- Выполнить миграции в БД:
```angular2html
$ python manage.py migrate
```
- Запустить локальный сервер:
````angular2html
$ python manage.py runserver
````
### Docker
- Запустить контейнеризацию, командой
````
$ docker-compose build 
````
- Запустить проект
````
$ docker-compose up -d #в фоновом режиме
$ docker-compose up    #в детальном режиме 
````
- Для остановки проекта, использовать следующую команду.
````
$ docker-compose down
````

После проделанных действий, проект будет доступен по адресу http://localhost:8000/.

Также проект доступен на удалённом сервере http://akorsunov.pythonanywhere.com/.

Проект представляем собой простую имитацию реферальной системы.
При входе, сервис предлагает пользователю аутентифицироваться по номеру телефона, 
после чего ему приходит код подтверждения по СМС (использован сервис отправки СМС [SMSC.RU](https://www.smsc.ru/)). 
При верном вводе кода, пользователь попадает на страницу профиля, где он может наблюдать пользователей воспользовавшихся его инвайт-кодом, а также сам может единоразово ввести чужой инвайт-код.

## Доступные АPI методы:
Документация к API:
```angular2html
/api/v1/schema/redoc/
```
На локальном и удалённом сервере доступны следующие API методы:
- POST (запрос номера телефона)

После ввода номера телефона, он проходит проверку на валидность, и в случае успеха пользователю отправляется код с подтверждением по СМС.
Если такого номера нет в БД, он добавляется и присваивается уникальный 6 значный инвайт-код.
```angular2html
/api/v1/auth/
```
- POST (проверка кода подтверждения и аутентификация пользователя)

Код подтверждения после отправки по СМС, сохраняется в БД. После ввода кода пользователем, он сравнивается с БД и в случае успеха аутентифицирует.
```angular2html
/api/v1/auth/<phone_number>/verification_code/
```
- GET (запрос на профиль пользователя)

В профиле имеется вывод всех пользователей, добавивших инвайт-код текущего. 

```angular2html
/api/v1/users/profile/
```
- PUT (запрос на добавление реферала)

В профиле пользователя доступен PUT запрос, добавление чужого инвайт-кода, с проверкой на существование такого пользователя и повторного ввода.
````angular2html
/api/v1/profile/<pk>/set_invite_code/
````