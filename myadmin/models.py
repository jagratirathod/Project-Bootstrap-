from django.db import models

# Create your models here.

class Category(models.Model):
    catid=models.AutoField(primary_key=True)
    catnm=models.CharField(unique=True , max_length=100)
    caticonname=models.CharField(max_length=100)

class Subcategory(models.Model):
    scatid=models.AutoField(primary_key=True)
    catnm=models.CharField(max_length=100)
    subcatnm=models.CharField(max_length=100)
    subcaticon=models.CharField(max_length=1000)
    sprice=models.IntegerField()
    description=models.CharField(max_length=1000)
    
