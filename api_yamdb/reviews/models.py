from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator)

from api_yamdb.settings import CONST
from .validators import validate_username, validate_year


class User(AbstractUser):
    """Модель пользователей."""

    ROLES = [
        (CONST['ADMIN'], 'Администратор'),
        (CONST['MODERATOR'], 'Модератор'),
        (CONST['USER'], 'Пользователь'),
    ]
    username = models.CharField(
        max_length=CONST['MAX_LENGTH_USERNAME'],
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        max_length=CONST['MAX_LENGTH_EMAIL'],
        unique=True
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(
        max_length=CONST['MAX_LENGTH_ROLE'],
        choices=ROLES,
        default=CONST['USER'],
        verbose_name='Роль'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == CONST['ADMIN']

    @property
    def is_moderator(self):
        return self.role == CONST['MODERATOR']

    @property
    def is_user(self):
        return self.role == CONST['USER']


class BaseCategoryGenre(models.Model):
    """Базовый класс категорий и жанров произведений."""

    name = models.CharField(
        max_length=CONST['MAX_LENGTH_NAME'],
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        max_length=CONST['MAX_LENGTH_SLUG'],
        unique=True,
        verbose_name='Slug'
    )

    class Meta:
        abstract = True


class Category(BaseCategoryGenre):
    """Модель категорий произведений."""

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(BaseCategoryGenre):
    """Модель жанров произведений."""

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""

    name = models.CharField(
        max_length=CONST['MAX_LENGTH_NAME'],
        db_index=True,
        verbose_name='Название'
    )
    year = models.IntegerField(
        db_index=True,
        validators=[validate_year],
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Slug категории'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Slug жанра'
    )

    class Meta:
        ordering = ('name',)
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class BaseReviewComment(models.Model):
    """Базовый класс отзывов и комментариев."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )
    text = models.TextField(
        'Текст',
        help_text='Введите текст',
    )

    class Meta:
        ordering = ('pub_date',)
        abstract = True


class Review(BaseReviewComment):
    """Модель отзывов к произведениям."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение на которое пишется отзыв',
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг произведения',
        help_text='Поставьте вашу оценку произведению 1-10',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_title_author'
            )
        ]

    def __str__(self):
        return (
            f'{self.title.name} ({self.author.username})'
        )


class Comment(BaseReviewComment):
    """Модель комментариев к отзывам."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв к произведению (автор отзыва)',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'

    def __str__(self):
        return (
            f'{self.title.name} ({self.author.username})'
        )
