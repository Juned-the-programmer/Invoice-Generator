from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('backup/database', views.backup_database, name="backup")
]