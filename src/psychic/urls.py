import os
from django.urls import path
from .views import index

app_name = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    path('', index, name='index'),
]