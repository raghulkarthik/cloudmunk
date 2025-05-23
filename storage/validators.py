# storage/validators.py

from django.core.exceptions import ValidationError
import os

from django.conf import settings

def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = getattr(settings, 'ALLOWED_FILE_EXTENSIONS', [])
    if ext.lower() not in valid_extensions:
        raise ValidationError(f'Unsupported file extension.')

