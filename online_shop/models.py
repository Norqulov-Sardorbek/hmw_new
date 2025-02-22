from decimal import Decimal

from django.db import models

# Create your models here.

class Product(models.Model):
    class RatingChoices(models.IntegerChoices):
        one = 1
        two = 2
        three = 3
        four = 4
        five = 5
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.DecimalField(decimal_places=2,max_digits=10)
    quantity=models.IntegerField()
    image=models.ImageField(upload_to='images/')
    discount=models.PositiveIntegerField(max_length=2)
    rating=models.IntegerField(choices=RatingChoices.choices,default=RatingChoices.one.value)


    @property
    def discounted_price(self):
        if self.discount >0:
            self.price=self.price*Decimal(1- self.discount/100)
        return Decimal(self.price).quantize(Decimal('.01'))

class Comment(models.Model):
    name=models.CharField(max_length=100)
    comment=models.TextField()
    commented_date=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(Product,on_delete=models.CASCADE)