from django.urls import path
from . import views

urlpatterns = [
    path('GSTsale/', views.GST_Invoice, name='GST_Invoice'),
]
