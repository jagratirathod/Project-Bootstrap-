from django.db import models

class Register(models.Model):
    regid=models.AutoField(primary_key=True)
    firstnm=models.CharField(max_length=100)
    lastnm=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=10)
    mobile=models.CharField(max_length=12)
    info=models.CharField(max_length=100)
    status=models.IntegerField()
    role=models.CharField(max_length=10)