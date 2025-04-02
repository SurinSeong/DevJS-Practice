from django.urls import path
from .views import FeedbackDetailView, FeedbackListView, ApplyRecommendationsView

urlpatterns = [
    path('<int:feedback_pk>/', FeedbackDetailView.as_view(), name='feedback-detail'),
    path('', FeedbackListView.as_view(), name='feedback-list'),
    path('<int:feedback_pk>/apply-recommendations/', ApplyRecommendationsView.as_view(), name='apply-recommendations'),
]
