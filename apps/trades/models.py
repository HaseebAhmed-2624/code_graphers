from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.utils.enum import TransactionType
from apps.utils.mixins import BaseModel
from apps.utils.exceptions import CustomException

from django.db.models import Sum

# Create your models here.
class Stocks(
    BaseModel,
):
    """
    """
    owner = models.ForeignKey(
        "auth_.User",
        on_delete=models.CASCADE,
        null=False,
        related_name="stock_as_owner",
        verbose_name=_("User")
    )
    name = models.CharField(
        _("Name"), max_length=255,
        null=False,
        blank=False,
        unique=True,
    )
    quantity = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name=_("Quantity"),
    )
    price = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name=_("Price"),
    )

    @property
    def remaining_quantity(self):
        quantity_sold = Transactions.objects.filter(stock=self.id, type=TransactionType.SELL.value).aggregate(sold = Sum('quantity'))['sold'] or 0
        quantity_bought = Transactions.objects.filter(stock=self.id, type=TransactionType.SELL.value).aggregate(bought = Sum('quantity'))['bought'] or 0
        return self.quantity - quantity_sold + quantity_bought

    def stock_quantity_a_user_owns(self,user_id):
        quantity_sold = Transactions.objects.filter(stock=self.id, type=TransactionType.SELL.value, owner = user_id).aggregate(sold=Sum('quantity'))[
            'sold'] or 0
        quantity_bought = Transactions.objects.filter(stock=self.id, type=TransactionType.SELL.value, owner = user_id).aggregate(bought=Sum('quantity'))[
            'bought'] or 0
        return quantity_bought - quantity_sold

    def __str__(self):
        return f"{self.owner} - {self.name}"

    # def save(self,*args):

class Transactions(
    BaseModel,
):
    """
    """
    owner = models.ForeignKey(
        "auth_.User",
        on_delete=models.CASCADE,
        null=False,
        related_name="transaction_as_owner",
        verbose_name=_("User")
    )
    type = models.CharField(
        verbose_name=_("Transaction Type"),
        null=False,
        blank=False,
        max_length=TransactionType.max_length(),
        choices=TransactionType.choices(),
    )
    quantity = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name=_("Quantity"),
        validators=[MinValueValidator(1)],
    )
    price_per_stock = models.PositiveIntegerField(
        null=False,
        blank=False,
        verbose_name=_("Price"),
    )
    stock = models.ForeignKey(
        "Stocks",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="transaction_as_stock",
        verbose_name=_("Stock")
    )

    def __str__(self):
        return f"{self.owner} - {self.type} - {self.quantity} - {self.price_per_stock}"

    def save(self, *args, **kwargs):
        self.price_per_stock = self.stock.price
        ttl_amount = self.price_per_stock * self.quantity
        if self.type == "BUY":
            if ttl_amount > self.owner.balance:
                raise CustomException("Insufficient balance")
            elif self.quantity > self.stock.remaining_quantity:
                raise CustomException("Insufficient quantity in stock")
            self.owner.balance -= ttl_amount
            self.stock.quantity -= self.quantity
        elif self.type == "SELL":
            if self.quantity > self.stock.stock_quantity_a_user_owns(self.owner):
                raise CustomException("You've insufficient quantity in stock")
            self.stock.quantity += self.quantity
            self.owner.balance += ttl_amount
        self.owner.save()
        self.stock.save()
        return super().save(*args, **kwargs)