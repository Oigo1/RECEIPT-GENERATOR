from django.db import models

# Create your models here.

class Payment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    code = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account_number = models.CharField(max_length=30)
    receipt_number = models.CharField(max_length=15, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.receipt_number