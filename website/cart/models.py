from django.db import models
from home.models import *
from django.forms import ModelForm


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, null=True, blank=True,default=None)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username


class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']
