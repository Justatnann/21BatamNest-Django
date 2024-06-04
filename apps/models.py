from django.db import models

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, null=True)
    price = models.IntegerField()
    

class Event(models.Model):
    event_name = models.CharField(max_length=100)
    description = models.TextField(max_length=300, null=True)
    
class Invoice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()
    date = models.DateField(auto_now=True,)
    discount = models.IntegerField()
    payment_method = models.CharField(max_length=100)
    customer = models.CharField(max_length=100)
    sales = models.CharField(max_length=100)

class Payment_Method(models.Model):
    payment_method = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
