from django.urls import path
from . import views

urlpatterns = [
    path('addcustomer/', views.addcustomer, name='addcustomer'),
    path('viewcustomer/', views.viewcustomer, name='viewcustomer'),
]
