import re

from rest_framework.exceptions import ValidationError


def validate_username(username):
    pattern = re.compile(r'^[\w.@+-]+\Z')
    if username == 'me' or not bool(pattern.match(username)):
        raise ValidationError(
            {'errors': 'Имя пользователя не может '
             'быть me, может содержать латинские '
             'буквы в верхнем и нижнем регистре, '
             'цифры и знаки .@+-'}
        )
    return username
