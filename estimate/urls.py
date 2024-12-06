from django.urls import path
from . import views

urlpatterns = [
    path('estimatesale/', views.estimate_invoice, name='estimatesale'),
]   
