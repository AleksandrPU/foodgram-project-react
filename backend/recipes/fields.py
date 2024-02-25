import base64

from django.core.files.base import ContentFile
from rest_framework.serializers import ImageField


class Base64ImageField(ImageField):
    """Field for convert image to base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            type_file, image_str = data.split(';base64,')
            ext = type_file.split('/')[-1]
            data = ContentFile(base64.b64decode(image_str), name='temp.' + ext)
        return super().to_internal_value(data)
