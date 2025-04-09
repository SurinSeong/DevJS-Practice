from django.shortcuts import render

# Create your views here.
# jobdescriptions/views.py
from rest_framework import viewsets, permissions
from .models import JobDescription
from .serializers import JobDescriptionSerializer


class JobDescriptionViewSet(viewsets.ModelViewSet):
    queryset = JobDescription.objects.all()    # 모델의 모든 인스턴스 가져오기
    serializer_class = JobDescriptionSerializer    # 직렬화
    permission_classes = [permissions.IsAuthenticated]    # 인증증 관련

    def perform_create(self, serializer):    # 저장 메소드
        serializer.save(user=self.request.user)

    def get_queryset(self):    # 사용자가 등록한 JD 가져오는 메소드
        return JobDescription.objects.filter(user=self.request.user)
