from django.db import models
from django.core.exceptions import ValidationError

def file_size(value): 
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Archivo excede los 2MB')

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
