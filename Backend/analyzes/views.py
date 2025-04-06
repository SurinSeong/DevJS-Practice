from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Analysis
from coverletters.models import CoverLetter
from jobdescriptions.model import JobDescription

# 새로운 자소서 + JD 조합으로 분석 요청을 만드는 API
class AnalysisCreateView(APIView):
    def post(self, request):
        cover_letter_id = request.data.get('cover_letter_id')
        job_description_id = request.data.get('job_description_id')
        
        try:
            cover_letter = CoverLetter.objects.get(id=cover_letter_id)
            job_description = JobDescription.objects.get(id=job_description_id)
        except (CoverLetter.DoesNotExist, JobDescription.DoesNotExist):
            return Response({'error': 'Invalid ID provided.'}, status=status.HTTP_400_BAD_REQUEST)
        
        analysis = Analysis(cover_letter=cover_letter, job_description=job_description, status='pending')
        analysis.save()    # 저장
        
        # TODO: 여기서 Celery 또는 FastAPI 연동 로직 들어감
        
        return Response({'message': '분석 요청이 등록되었습니다.', 'analysis_id': analysis.id}, status=status.HTTP_201_CREATED)


# 이미 존재하는 자소서에 대해 재분석 요청을 하는 API
class AnalysisRetryView(APIView):
    def post(self, request, coverletter_id):
        try:
            cover_letter = CoverLetter.objects.get(id=coverletter_id)
            job_description = cover_letter.job_description    # 커버레터에 JD가 연결되어 있다면
        except CoverLetter.DoesNotExist:
            return Response({'error': 'Cover letter not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        analysis = Analysis(cover_letter=cover_letter, job_description=job_description, status='pending')
        analysis.save()    # 저장
        
        # TODO: 여기서 재분석 AI 요청 처리
        
        return Response({'message': '재분석 요청이 등록되었습니다.', 'analysis_id': analysis.id}, status=status.HTTP_201_CREATED)
    
