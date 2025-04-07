from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import AnalysisSerializer

from coverletters.models import CoverLetter
from feedbacks.models import Feedback, RecommendationSentence
from model_server.client import request_analysis

# AnalysisCreateView와 AnalysisRetryView가 거의 같음 → 공통 로직 함수로 분리
def run_analysis_and_save(analysis):
    cl_text = analysis.cover_letter.content
    jd_text = analysis.job_description.content

    result = request_analysis(analysis.id, cl_text, jd_text)

    if result is None:
        analysis.status = 'failed'
        analysis.error_message = 'FastAPI 호출 실패'
        analysis.save()
        return None

    # 결과 저장
    for feedback_data in result.get('feedbacks', []):
        feedback = Feedback.objects.create(
            analysis=analysis,
            original_sentence=feedback_data['original_sentence'],
            similarity_score=feedback_data['similarity_score'],
            is_weak=feedback_data['is_weak'],
        )
        if feedback_data['is_weak'] and feedback_data.get('recommendation'):
            RecommendationSentence.objects.create(
                feedback=feedback,
                content=feedback_data['recommendation'],
                reason=feedback_data.get('reason', '')
            )

    analysis.status = 'done'
    analysis.save()
    return analysis


# 새로운 자소서 + JD 조합으로 분석 요청을 만드는 API
class AnalysisCreateView(APIView):
    def post(self, request):
        serializer = AnalysisSerializer(data=request.data)
        if serializer.is_valid():
            analysis = serializer.save(status='pending')
            saved = run_analysis_and_save(analysis)

            if not saved:
                return Response({'error': 'FastAPI 호출 실패'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'message': '분석 및 결과 저장 완료', 'analysis_id': analysis.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 이미 존재하는 자소서에 대해 재분석 요청을 하는 API
class AnalysisRetryView(APIView):
    def post(self, request, coverletter_id):
        try:
            cover_letter = CoverLetter.objects.get(id=coverletter_id)
            job_description = cover_letter.job_description
        except CoverLetter.DoesNotExist:
            return Response({'error': 'Cover letter not found.'}, status=status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return Response({'error': 'Cover letter does not have a job description.'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'cover_letter_id': cover_letter.id,
            'job_description_id': job_description.id,
        }
        serializer = AnalysisSerializer(data=data)
        if serializer.is_valid():
            analysis = serializer.save(status='pending')
            saved = run_analysis_and_save(analysis)

            if not saved:
                return Response({'error': 'FastAPI 호출 실패'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'message': '재분석 완료.', 'analysis_id': analysis.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
