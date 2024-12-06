from django.urls import path
from . import views

urlpatterns = [
    path('addproduct/', views.addproduct, name='addproduct'),
    path('viewproduct/', views.viewproduct, name='viewproduct'),
]
