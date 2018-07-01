from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Code(models.Model):
    language=models.CharField(max_length=10)
    content=models.CharField(max_length=100000000)
    expire=models.CharField(max_length=20)
    slug=models.CharField(max_length=10)

    def __str__(self):
        return str(self.id)+' - '+self.language+' - '+self.slug+'\n\nCode : \n'+self.content+'\n'
