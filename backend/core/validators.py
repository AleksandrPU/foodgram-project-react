import re

from rest_framework.exceptions import ValidationError


def validate_username(username):
    pattern = re.compile(r'^[\w.@+-]+\Z')
    if username == 'me' or not bool(pattern.match(username)):
        raise ValidationError()
    return username
