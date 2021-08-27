from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import os
from twilio.rest import Client


STATE_CHOICE=(('Maharashtra','Maharashtra'),
              ('Gujrat','Gujrat'))


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    contact = models.CharField(max_length=13)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICE, max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICE=(
    ('oil','c'),
    ('jag','organic jaggery'),
    ('salt','Rock salt'),
    ('honey','Raw honey')
)

class Product(models.Model):
    title = models.CharField(max_length=50)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=50)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=50)
    product_image = models.ImageField(upload_to='productimg')


    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICE =(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date= models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICE, default='Pending', max_length=50)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    def save(self, *args, **kwargs):
        if self.status == 'Pending':
            account_sid = 'AC32344962b328200c5cba65a558f9895e'
            auth_token = 'bb96b5d6bacfe452e3071cd71d687549'
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                body=f"you have new order from {self.user}, of {self.product}",
                from_='+12562875021',
                to='+917020244683'
            )

            print(message.sid)
        return super().save(*args,**kwargs)


