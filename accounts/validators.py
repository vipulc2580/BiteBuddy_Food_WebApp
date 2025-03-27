from django.core.exceptions import ValidationError
import os
def allow_only_images_validator(value):
    ext=os.path.splitext(value.name)[1] # this returns file name and extension
    allowed_extensions=['.jpg','.jpeg','.png']
    if not ext.lower() in allowed_extensions:
        raise ValidationError(f'Unsupported file Extension,Allowed Extension {str(allowed_extensions)}')

def validate_file_size(file):
    max_size = 5 * 1024 * 1024  # 5MB in bytes
    if file.size > max_size:
        raise ValidationError("File size must be less than 5MB.")