from django.db import models


class Users(models.Model):
    """
    Class describing user table
    """
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    balance = models.FloatField()


class Transactions(models.Model):
    """
    Class describing Transactions table
    """
    id = models.CharField(max_length=500, primary_key=True)
    transaction_type = models.CharField(max_length=100)
    transaction_date = models.DateTimeField()
    transaction_status = models.CharField(max_length=100)
    transaction_from = models.ForeignKey(Users, db_column='transaction_from')
    transaction_with = models.ForeignKey(Users, db_column='transaction_with')
    reason = models.CharField(max_length=200)
    transaction_amount = models.FloatField()

