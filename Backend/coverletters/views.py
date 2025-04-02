from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from coverletters.models import CoverLetter
from feedback.models import RecommendationSentence

from django.shortcuts import get_object_or_404

# 추천 문장 반영 함수
class ApplyRecommendationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        # 1. 자기소개서 가져오기
        cover_letter = get_object_or_404(CoverLetter, pk=pk)
        
        # 2. 사용자 인증 체크
        if cover_letter.user != request.user:
            context = {
                'detail': '접근 권한이 없습니다.'
            }
            return Response(context, status=status.HTTP_403_FORBIDDEN)
        
        # 3. 추천 문장 ID 리스트 받기
        rec_ids = request.data.get('recommendation_ids', [])
        if not rec_ids:
            context = {
                'detail': '추천 문장 ID가 필요합니다.'
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
        # 4. 추천 문장 가져오기
        recommendations = RecommendationSentence.objects.filter(id__in=rec_ids, feedback__cover_letter=cover_letter)
        
        # 5. 추천 문장 텍스트 이어붙이기
        added_text = '\n\n' + '\n'.join([rec.sentence for rec in recommendations])
        cover_letter.text_content += added_text
        cover_letter.save()
        
        context = {
            'cover_letter_id': cover_letter.id,
            'updated_text_content': cover_letter.text_content,
            'added_sentences': [rec.sentence for rec in recommendations],
        }
        return Response(context, status=status.HTTP_200_OK)