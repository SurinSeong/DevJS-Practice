from rest_framework import serializers
from .models import Feedback, RecommendationSentence

class RecommendationSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationSentence
        fields = ['id', 'sentence', 'reason']

class FeedbackSerializer(serializers.ModelSerializer):
    recommendations = RecommendationSentenceSerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'cover_letter', 'job_description', 'matching_score', 'created_at', 'recommendations']