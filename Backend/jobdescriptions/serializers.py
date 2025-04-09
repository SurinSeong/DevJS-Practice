from rest_framework import serializers
from .models import JobDescription

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = ['id', 'user', 'file', 'content', 'created_at']    # 기존 필드
        read_only_fields = ['id', 'user', 'created_at']    # 사용자에게 보이는 필드