from django.conf import settings
from django.db import models

from authapp.models import ShopUser
from mainapp.models import Product


class Basket(models.Model):
    # class Meta:
    #     unique_together = (key1, key2)
    #
    # key1 = models.IntegerField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_time = models.DateTimeField(verbose_name='время добавления', auto_now_add=True)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        items = Basket.objects.filter(user=self.user)
        return sum(list(map(lambda x: x.quantity, items)))

    @property
    def total_cost(self):
        items = Basket.objects.filter(user=self.user)
        return sum(list(map(lambda x: x.product_cost, items)))

