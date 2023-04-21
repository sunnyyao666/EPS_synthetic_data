from django.urls import path
from service import service

urlpatterns = [
    # Get results
    path('result', service.get_result, name='result')
]
