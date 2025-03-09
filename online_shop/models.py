from decimal import Decimal
from phonenumber_field.modelfields import PhoneNumberField

from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order=models.PositiveIntegerField(default=0,null=True,blank=True)


    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product(BaseModel):
    class RatingChoices(models.IntegerChoices):
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(decimal_places=2,max_digits=10)
    quantity=models.IntegerField()
    image=models.ImageField(upload_to='images/')
    discount=models.PositiveIntegerField(max_length=3)
    rating=models.IntegerField(choices=RatingChoices.choices,default=RatingChoices.one.value)

    def __str__(self):
        return self.name
    @property
    def discounted_price(self):
        if self.discount >0:
            self.price=self.price*Decimal(1- self.discount/100)
        return Decimal(self.price).quantize(Decimal('.01'))
    class Meta:
        ordering = ['order']

class Comment(models.Model):
    name=models.CharField(max_length=100)
    comment=models.TextField()
    commented_date=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(Product,on_delete=models.CASCADE)
    def __str__(self):
        return self.name


class Order(BaseModel):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone = PhoneNumberField(region='UZ')
    quantity = models.PositiveIntegerField(default=1)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f'{self.phone} - {self.product.name}'