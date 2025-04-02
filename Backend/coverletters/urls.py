from django.urls import path

from .views import ApplyRecommendationView

app_name = 'coverletters'

urlpatterns = [
    path('<int:pk>/apply-recommendations/', ApplyRecommendationView.as_view(), name='apply-recommendations'),
    
]
