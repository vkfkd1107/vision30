from django.db import models

# Create your models here.
class FileUpload(models.Model):
    pic=models.FileField(null=False, blank=False,upload_to='')

    def __str__(self):
        return self.title