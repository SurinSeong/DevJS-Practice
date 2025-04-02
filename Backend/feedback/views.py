from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Feedback, RecommendationSentence
from .serializers import FeedbackSerializer
from .permissions import IsOwner

from coverletters.models import CoverLetter

# 전체 피드백 목록
    # 로그인한 사용자만 접근 가능
    # 본인 피드백만 리스트로 받아온다.
class FeedbackListView(ListAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Feedback.objects.filter(cover_letter__user=self.request.user).order_by('-created_at')


# 인증된 사용자인지 확인해서 "자기 소유 피드백만 조회 가능하게 하는 보안 기능 포함"
class FeedbackDetailView(RetrieveAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsOwner]
    
    # GET /api/feedback/<pk>/ 요청을 처리하는 클래스 기반 뷰
    def get_object(self):
        feedback = get_object_or_404(Feedback, pk=self.kwargs['pk'])
        if feedback.cover_letter.user != self.request.user:
            raise PermissionDenied('접근 권한이 없습니다.')
        return feedback
    

# 선택한 추천 문장을 자소서 본문에 추가하기
    # 해당 자소서 작성자만 가능
class ApplyRecommendationsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        feedback = get_object_or_404(Feedback, pk=pk)
        
        # 권한 확인
        if feedback.cover_letter.user != request.user:
            raise PermissionDenied('자신의 자소서에만 추천 문장을 반영할 수 있습니다.')
        
        sentence_ids = request.data.get('sentence_ids', [])
        if not sentence_ids:
            context = {
                'error': 'senetence_ids는 필수입니다.'
            }
            return Response(context, status=400)
        
        rec_sentences = RecommendationSentence.objects.filter(
            feedback=feedback,
            id__in=sentence_ids,
        )
        
        if not rec_sentences.exists():
            context = {
                'error': '추천 문장을 찾을 수 없습니다.'
            }
            return Response(context, status=404)
        
        cover_letter = feedback.cover_letter
        for rec in rec_sentences:
            cover_letter.text_content += f'\n\n{rec.sentence}'
            
        cover_letter.save()
        context = {
            'message': '추천 문장이 성공적으로 반영되었습니다.',
            'updated_content': cover_letter.text_content,
        }
        return Response(context)
