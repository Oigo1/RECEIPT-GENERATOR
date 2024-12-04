from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_form, name='payment_form'),
]