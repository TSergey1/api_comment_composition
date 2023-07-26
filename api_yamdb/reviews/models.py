from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    ROLES = [
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
    ]
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Имя пользователя'
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(
        max_length=100,
        choices=ROLES,
        default='user',
        verbose_name='Роль'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Review(models.Model):
    """Модель отзывов к произведениям."""

    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение на которое пишется отзыв',
    )
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
    )
    pub_date = models.DateTimeField(
        'Дата добавления отзыва',
        auto_now_add=True,
        db_index=True,
    )
    score = models.IntegerField(
        verbose_name='Рейтинг произведения',
        help_text='Поставьте вашу оценку произведению 1-10',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comment(models.Model):
    """Модель комментариев к отзывам."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария',
    )
    pub_date = models.DateTimeField(
        'Дата добавления комментария',
        auto_now_add=True,
        db_index=True,
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария',
    )
    review_id = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментируемый отзыв',
    )

    class Meta:
        ordering = ('pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
