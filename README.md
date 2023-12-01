# api_comment_composition

[![License MIT](https://img.shields.io/badge/licence-MIT-green)](https://opensource.org/license/mit/)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![SQLite](https://img.shields.io/badge/-SQLite-464646?style=flat-square&logo=SQLite)](https://www.sqlite.org/index.html)


## Описание
REST API (DRF) платформы отзывов пользователей на произведения.
Произведения делятся на категории, такие как "Книги", "Фильмы", "Музыка". Список категорий может быть расширен. 
Добавлять произведения, категории и жанры может только администратор.
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от 1 до 10. Из пользовательских оценок формируется усреднённая оценка произведения — рейтинг. 
Пользователи могут оставлять комментарии к отзывам.

Технологии
Python 3.9
Django 3.2
Django Rest Framework 3.12.4
Simple JWT




## Инструкция по запуску проекта
1. Склонируйте проект  себе на компьютер.
2. Создайте  virtual environment для папки с проектом: 

   - Linux/macOS
    
    ```bash
    python3 -m venv venv
    ```
    
- Windows
    
    ```python
    python -m venv venv
    ```

3. Активируйте виртуального окружения

- Linux/macOS
    
    ```bash
    source venv/bin/activate
    ```
    
- Windows
    
    ```bash
    source venv/Scripts/activate
    ```
4. Все дальнейшие команды в терминале надо выполнять с активированным виртуальным окружением.

Обновите pip:

```bash
python -m pip install --upgrade pip
```

5. Установите зависимостей из файла *requirements.txt*:
команда в терминале **pip install -r requirements.txt** (Windows).

```bash
pip install -r requirements.txt
```

6. Применете миграцию

    
В директории с файлом manage.py выполните команду: 

```bash
python manage.py migrate
```
7. Для теста можно автоматически наполнить БД данными из csv файлов (BASE_DIR/static/data).
   Для этого нужно выполнить команду
```bash
python manage.py upload_csv
```
   !!!Будьте внимательны существующие данные из БД будут утеряны!!!

## Примеры запросов к API (полный список см. в документации http://127.0.0.1:8000/redoc/)

<ul>
<li>Регистрация пользователя:
POST /api/v1/auth/signup/</li>
<li>Получение данных своей учетной записи:
GET /api/v1/users/me/</li>
<li>Добавление новой категории:
POST /api/v1/categories/</li>
<li>Удаление жанра:
DELETE /api/v1/genres/{slug}</li>
<li>Частичное обновление информации о произведении:
PATCH /api/v1/titles/{titles_id}</li>
<li>Получение списка всех отзывов:
GET /api/v1/titles/{title_id}/reviews/</li>
<li>Добавление комментария к отзыву:
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/</li>
</ul>



## Авторы
<ul>
<li>Тыртычный Сергей - https://github.com/TSergey1</li>
<li>Леденев Виктор - https://github.com/brasavarius</li>
<li>Баранов Дмитрий - https://github.com/dvkab</li>
</ul>
