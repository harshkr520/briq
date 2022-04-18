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
        data = json.dumps({'username': 'user1', 'password': 'pass1'})
        response = c.post('/login/', data, content_type='application/json')
        self.assertEqual(response.json(), {"message": True})

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
        self.transaction_id = ''.join([random.choice(string.ascii_lowercase) for _ in range(8)])

    def test_put_transaction(self):
        c = Client()
        data = {"transaction_id": self.transaction_id,
                "transaction_type": "borrow",
                "transaction_date": "2022-04-17",
                "transaction_status": "unpaid",
                "transaction_from_id": self.user_id1,
                "transaction_with_id": self.user_id2,
                "transaction_amount": 100,
                }
        data = json.dumps(data)
        response = c.post('/transaction/', data, content_type='application/json')
        self.assertEqual(response.json(), {"message": "Success"})

    def test_mark_paid(self):
        c = Client()
        data = json.dumps({"transaction_id": self.transaction_id})
        response = c.post('/mark_paid/', data, content_type='application/json')
        self.assertEqual(response.json(), {"message": "Transaction status updated"})

    # def tearDown(self):
    #     u = models.Users.objects.get(pk=self.user_id1)
    #     u.delete()
    #     u = models.Users.objects.get(pk=self.user_id2)
    #     u.delete()