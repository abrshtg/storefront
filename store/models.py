from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    class Membership(models.TextChoices):
        Gold = "G", _("Gold")
        Silver = "S", _("Silver")
        Bronze = "B", _("Bronze")

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=Membership, default=Membership.Bronze
    )


class Order(models.Model):
    class PaymentStatus(models.TextChoices):
        Complete = "C", _("Complete")
        Pending = "P", _("Pending")
        Failed = "F", _("Failed")

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PaymentStatus, default=PaymentStatus.Pending
    )
