from django.contrib import admin
from django.urls import path
from .views import create_checkout_session,payment_cancelled,payment_success,payment_successful_webhook



app_name = 'paymentsApp'


urlpatterns = [
    path('',create_checkout_session,name = 'create-checkout'),
    path('payment_success/',payment_success,name = 'payment-success'),
    path('payment_cancelled/',payment_cancelled,name = 'payment-cancellled'),
    path('payment_success_webhook/',payment_successful_webhook,name='payment-success-webhook')
]