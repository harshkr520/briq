import json

from django.views import View
from django.http import JsonResponse
from django.db.models import Q, Sum

from . import models


class Login(View):
    def post(self, request) -> JsonResponse:
        """
        Checks whether the passed username and password in the json body exists in users
        """
        status = 200
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            data = {"message": "Input is not json"}
            status = 400
            print(f"Error login:{e}")
            return JsonResponse(data, status=status)
        if 'username' not in payload or 'password' not in payload:
            data = {"message": "username or password not present in body"}
            status = 400
            return JsonResponse(data, status=status)
        queryset = models.Users.objects.filter(username=payload['username'], password=payload['password'])
        if [record for record in queryset]:
            data = {"message": True}
        else:
            data = {"message": False}
        return JsonResponse(data, status=status)


class Transaction(View):
    def get(self, request) -> JsonResponse:
        """
        :param request: user_id
        :return: JsonResponse with list of transactions
        """
        user_id = request.GET.get('user_id')
        if user_id:
            query_set = models.Transactions.objects.filter(Q(transaction_from=user_id)
                                                           | Q(transaction_with=user_id))
            data = [dict(row) for row in query_set]
            status = 200
        else:
            data = {"message": "User_id not present in query params"}
            status = 400
        return JsonResponse(data, status=status, safe=False)

    def post(self, request) -> JsonResponse:
        """
        Add a transaction
        """
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except Exception as e:
            data = {"message": "Input is not json"}
            status = 400
            return JsonResponse(data, status=status)
        try:
            print(payload)
            t = models.Transactions.objects.create(**payload)
            t.save()
            data = {"message": "Success"}
            status = 200
            return JsonResponse(data, status=status)
        except Exception as e:
            data = {"message": "Failed"}
            status = 400
            print(f"Post transaction failed {e}")
            return JsonResponse(data, status=status)


class MarkPaid(View):
    """
    Update transaction with transaction status
    """
    def post(self, request) -> JsonResponse:
        try:
            payload = json.loads(request.body.decode('utf-8'))
        except:
            data = {"message": "Input is not json"}
            status = 400
            return JsonResponse(data, status=status)
        if 'transaction_id' not in payload:
            data = {"message": "transaction_id not present in body"}
            status = 400
            return JsonResponse(data, status=status)
        try:
            t = models.Transactions.objects.get(transaction_id=payload['transaction_id'])
            t.transaction_status = 'paid'
            t.save()
            data = {"message": "Transaction status updated"}
            status = 200
        except Exception as e:
            data = {"message": f"Failed: {e}"}
            status = 500
        return JsonResponse(data, status=status)


class CreditScore(View):
    def get(self, request) -> JsonResponse:
        """
        :param request: user_id
        :return: {"message": credit_score}
        """
        user_id = request.GET.get('user_id')
        if user_id:
            query_set = (models.Transactions.objects.filter(transaction_from=user_id,
                                                            transaction_type='borrow')
                         .aggregate(Sum('transaction_amount')))
            borrow_amt = query_set.items()[0][1]
            query_set = (models.Transactions.objects.filter(transaction_from=user_id,
                                                            transaction_type='lend')
                         .aggregate(Sum('transaction_amount')))
            lend_amt = query_set.items()[0][1]
            borrow_percent = borrow_amt*100/(borrow_amt + lend_amt)
            lend_percent = 100 - borrow_percent
            borrow_score = (100 - (borrow_percent//10)*10)*10
            lend_score = 1000 + (lend_percent//10 + 1)*100
            data = {"message": lend_score + borrow_score}
            status = 200
        else:
            data = {"message": "User_id not present in query params"}
            status = 400
        return JsonResponse(data, status=status, safe=False)