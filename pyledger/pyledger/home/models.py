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

class Splits(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_splits")
    name = models.TextField()
    datecreated = models.DateField()

class Splitmembers(models.Model):
    splitid = models.ForeignKey(Splits, related_name="Split_members", on_delete=models.CASCADE)
    member = models.ForeignKey(User, related_name="memeber_splits", on_delete=models.CASCADE)

class Splittransactions(models.Model):
    splitid = models.ForeignKey(Splits, on_delete=models.CASCADE, related_name="split_transactions")
    spentby = models.ForeignKey(User, on_delete=models.CASCADE, related_name="split_spentby")
    amount = models.IntegerField()
    spentfor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="split_spentfor")
    datespent = models.DateField()
    spentat = models.TextField()
    mode = models.CharField(max_length=1)
