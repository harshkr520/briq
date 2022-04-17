import json
import random
import string

from django.test import TestCase, Client
from . import models


class LoginTestCase(TestCase):
    def setUp(self):
        user_record = {"username": "user1",
                       "password": "pass1",
                       "balance": 0}
        u = models.Users.objects.create(**user_record)
        u.save()
        self.user_id = u.id

    def test_user_login(self):
        c = Client()
        response = c.post('/login/', {'username': 'user1', 'password': 'pass1'})
        self.assertEqual(json.loads(response.body), {"message": True})

    def tearDown(self):
        u = models.Users.objects.get(pk=self.user_id)
        u.delete()


class TransactionTestCase(TestCase):
    def setUp(self):
        user_record = {"username": "user1",
                       "password": "pass1",
                       "balance": 0}
        u = models.Users.objects.create(**user_record)
        u.save()
        self.user_id1 = u.id
        user_record = {"username": "user2",
                       "password": "pass2",
                       "balance": 0}
        u = models.Users.objects.create(**user_record)
        u.save()
        self.user_id2 = u.id

    def test_put_transaction(self):
        c = Client()
        self.transaction_id = ''.join([random.choice(string.ascii_lowercase) for _ in range(8)])
        data = {"id": self.transaction_id,
                "transaction_type": "borrow",
                "transaction_date": "2022-04-17",
                "transaction_status": "unpaid",
                "transaction_from": self.user_id1,
                "transaction_with": self.user_id2,
                "transaction_amount": 100,
                }
        response = c.post('/transaction/', data)
        self.assertEqual(json.loads(response.body), {"message": "Success"})

    def test_mark_paid(self):
        c = Client()
        response = c.post('/transaction/', {"transaction_id": self.transaction_id})
        self.assertEqual(json.loads(response.body), {"message": "Transaction status updated"})

    def tearDown(self):
        u = models.Users.objects.get(pk=self.user_id1)
        u.delete()
        u = models.Users.objects.get(pk=self.user_id2)
        u.delete()