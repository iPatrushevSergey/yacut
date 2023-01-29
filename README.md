![Python](https://img.shields.io/pypi/pyversions/scrapy?color=brightgreen&style=plastic) ![Flask](https://img.shields.io/badge/flask-2.0.2-brightgreen>)  ![Flask-SQLAlchemy](https://img.shields.io/badge/flask_sqlalchemy-2.5.1-brightgreen>) ![Flask-Migrate](https://img.shields.io/badge/flask_migrate-3.1.0-brightgreen>) ![Flask-WTF](https://img.shields.io/badge/flask_wtf-2.0.2-brightgreen>) ![Jinja2](https://img.shields.io/badge/jinja2-3.0.3-brightgreen>) ![Click](https://img.shields.io/badge/click-8.0.3-brightgreen>)

# Проект 21-го спринта "Сервис YaCut"

## Описание

В проекте реализована возможность:
- укорачивания ссылок - ассоциировать длиную пользовательскую ссылку с короткой,
которую предлагает сам пользователь.
На большинстве сайтов адреса страниц довольно длинные. Делиться такими ссылками
не всегда удобно, а иногда и вовсе невозможно. Удобнее использовать короткие ссылки.

Например, **http://<ваш домен>.ru/ya** и **http://<ваш домен>.ru/777** воспринимаются
лучше, чем **https://yandex.ru/trainer/backend/12e07d96-31f3-449f-abcf-e468b6a39061/**. 

В проекте также реализована функция логирования с помощью модуля **logging** (логи
сохраняются по адресу: **YACUT/logs**)

## Технологии

- Python 3.7
- Flask 2.0.2
- Flask-SQLAlchemy 2.5.1
- Flask-Migrate 3.1.0
- Flask-WTF 1.0.0
- Jinja2 3.0.3
- Click 8.0.3

## Подготовка проекта

1. Необходимо сделать **Fork** репозитория:
```
https://github.com/iPatrushevSergey/yacut.git
```
2. Далее нужно клонировать проект:
```
git clone git@github.com:<ваш_username>/yacut.git
```
3. Создать и активировать виртуальное окружение:

- MacOS и Linux
```
python3 -m venv venv && . venv/bin/activate
```
- Windows
```
python -m venv venv && . venv/bin/activate
```
4. Установить зависимости:
```
pip install -r requirements.txt 
```

## Запуск проекта

```
flask run
```

## URL адреса

### 1. Создание короткой ссылки:

**http://<ваш домен>/**

### 2. Переход по короткой ссылке на оринальный url адрес:

**http://<ваш домен>/{ваша короткая ссылка}**

## Примеры API запросов

### 1. Создание короткой ссылки:
POST-запрос /api/id/

*Обязательное поле*: **url**

> Тело запроса:
>```json
>{
>  "url": "string",
>  "custom_id": "string"
>}
>```

> Ответ:
>```json
>{
>  "url": "string",
>  "short_link": "string"
>}
>```

### 2. Получение длинной ссылки используя короткую ссылку:
GET-запрос /api/id/{short_id}/

*Обязательные параметры*: **short_id**

> Тело запроса:
>```json
>{
>  "short_id": "string"
>}
>`

> Ответ:
>```json
>{
>  "url": "string",
>}
>```

+ **Author**: Patrushev Sergey
+ **Mail**: PatrushevSergeyVal@yandex.ru
+ **GitHub**: [iPatrushevSergey](https://github.com/iPatrushevSergey)
