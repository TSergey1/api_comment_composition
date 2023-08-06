import re
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

from api_yamdb.settings import CONST


def validate_username(value):
    regex = r"^[\w.@+-]+\Z"
    if re.search(regex, value) is None:
        result = set(re.findall(r"[^\w.@+-]", value))
        raise ValidationError(
            f'Использовать символов {result} запрещено.'
        )
    if value.lower() == CONST['FORBIDDEN_USERNAME']:
        raise ValidationError(
            f'Использовать имя {CONST["FORBIDDEN_USERNAME"]} запрещено.'
        )


def validate_year(value):
    today = now().year
    if value > today:
        raise ValidationError('Дата из будущего.')
