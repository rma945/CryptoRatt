from django.db.models import FileField, ImageField

class SizedImageFileField(FileField):
    def __init__(self, *args, **kwargs):
        super(SizedImageFileField, self).__init__(*args, **kwargs)
        return None