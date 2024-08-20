from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ACCOUNT_TYPE = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employees', 'employees'),
    ]
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE,)
    email = models.CharField(max_length=100)
    phone=models.CharField(max_length=100 , default="")
    last_login=models.CharField(max_length=100 ,default="")
    password =models.CharField(max_length=100,default="CBTUSER1234")

    def __str__(self):
        return self.username
    

class Product(models.Model):
    batch_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    expirydate = models.DateField(max_length=100)
    price = models.IntegerField(default=0)
    tquantity= models.IntegerField(default=0)
    rquantity = models.IntegerField(default=0)
    category=models.CharField(max_length=100)
    description=models.CharField(max_length=500, default="this is the decription for this product")

    class Meta:
        db_table= 'Products'

class categories(models.Model):
    name = models.CharField(max_length=100 )
    description = models.CharField(max_length=100)

    class Meta:
        db_table= 'categories'

class documents(models.Model):
    companyname =  models.CharField(max_length=100, default='THE OFE COMPANY')
    companyaddress =  models.CharField(max_length=100, default='THE OFE ADDRESS' )
    quantity = models.IntegerField(default=0)
    amount =  models.IntegerField(default=0)
    document_type = models.CharField(max_length=100 )
    document_number =models.CharField(max_length=100 )
    description = models.CharField(max_length=500)

    class Meta:
        db_table= 'documents'
    

