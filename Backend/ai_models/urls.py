from django.urls import path
from .views import analyze_and_save

urlpatterns = [
    path('analyze/', analyze_and_save),
]