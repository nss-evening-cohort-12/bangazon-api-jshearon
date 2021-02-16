from django.db import models
from .customer import Customer
from .product import Product


class ProductLike(models.Model):

    customer = models.ForeignKey(Customer, related_name='product_likes', on_delete=models.DO_NOTHING,)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING,)
