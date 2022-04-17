from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('transaction/', views.Transaction.as_view(), name='transaction'),
    path('mark_paid/', views.MarkPaid.as_view(), name='mark_paid'),
    path('credit_score/', views.CreditScore.as_view(), name='credit_score'),
]