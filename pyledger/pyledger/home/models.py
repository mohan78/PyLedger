from django.db import models
from django.contrib.auth.models import User

class Expenses(models.Model):
    username = models.ForeignKey(User, related_name="user_expenses", on_delete=models.CASCADE)
    category = models.CharField(max_length=30)
    spentat = models.CharField(max_length=40)
    amount = models.IntegerField()
    modeofpayment = models.CharField(max_length=20)
    datespent = models.DateField('Date Spent')

    def __str__(self):
        return self.spentat
