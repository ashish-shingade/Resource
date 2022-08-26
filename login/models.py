from django.db import models

# Create your models here.

class Anamoly(models.Model):
    id = models.AutoField(primary_key= True)
    ip = models.CharField(max_length=1000)

