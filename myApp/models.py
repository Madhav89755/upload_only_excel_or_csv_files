from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.
class filesUploadModel(models.Model):
    user = models.ForeignKey(User, related_name='file_uploaded', on_delete=models.CASCADE)
    title = models.CharField(max_length=500)
    file_uploaded = models.FileField(upload_to='csv_or_excel', validators=[FileExtensionValidator(allowed_extensions=['csv','xls','xlsx'])])
    file_name = models.CharField(max_length=500,blank=True,null=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title