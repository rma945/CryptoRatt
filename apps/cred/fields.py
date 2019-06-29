from django.db.models import FileField

class SizedImageFileField(FileField):
    def __init__(self, *args, **kwargs):
        return None