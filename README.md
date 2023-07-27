# api_yamdb
api_yamdb


## Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как "Книги", "Фильмы", "Музыка". Например, в категории "Книги" могут быть произведения "Винни-Пух и все-все-все" и "Марсианские хроники", а в категории "Музыка" — песня "Давеча" группы "Жуки" и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или "Ювелирка"). 
Произведению может быть присвоен жанр из списка предустановленных (например, "Сказка", "Рок" или "Артхаус"). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

Проект API для приложениея Api_yamdb. Документация к API доступна http://127.0.0.1:8000/redoc/

## Инструкция по запуску проекта
1. Склонируйте проект «Api_yamdb» себе на компьютер.
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
## Примеры запросов к API
# Список возможных эндпоинтов смотри в документации http://127.0.0.1:8000/redoc/.

Примеры некоторых запросов API
Регистрация пользователя:
POST /api/v1/auth/signup/
Получение данных своей учетной записи:
GET /api/v1/users/me/
Добавление новой категории:
POST /api/v1/categories/
Удаление жанра:
DELETE /api/v1/genres/{slug}
Частичное обновление информации о произведении:
PATCH /api/v1/titles/{titles_id}
Получение списка всех отзывов:
GET /api/v1/titles/{title_id}/reviews/
Добавление комментария к отзыву:
POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/

Полный список запросов API находятся в документации