from django.db import models
from accounts.models import CustomUser


# Create your models here.

# class Users(models.Model):
#     name = models.CharField(max_length=200)
#     role = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

#     def __str__(self) -> str:
#         return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    image = models.ImageField(upload_to='', null=True, blank=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    ACTION = (
        ('NEW', 'NEW'),
        ('PROCESS', 'PROCESS'),
        ('DONE', 'DONE'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, choices=ACTION, default='NEW')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderProduct')

    # def __str__(self):
    #     return self.created_by.username


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=1)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, default=1)
    quantity = models.IntegerField(default=0)
    price = models.FloatField(default=0)

    # def __str__(self):

    #     return self.order_id
