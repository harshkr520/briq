from django.db import models


class Users(models.Model):
    """
    Class describing user table
    """
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    balance = models.FloatField(null=True)


class Transactions(models.Model):
    """
    Class describing Transactions table
    """
    transaction_id = models.CharField(max_length=500, primary_key=True)
    transaction_type = models.CharField(max_length=100)
    transaction_date = models.DateTimeField()
    transaction_status = models.CharField(max_length=100, null=True)
    transaction_from = models.ForeignKey(Users, db_column='transaction_from',
                                         related_name='transaction_from', on_delete=models.SET(0))
    transaction_with = models.ForeignKey(Users, db_column='transaction_with',
                                         related_name='transaction_with', on_delete=models.SET(0))
    reason = models.CharField(max_length=200, null=True)
    transaction_amount = models.FloatField()

