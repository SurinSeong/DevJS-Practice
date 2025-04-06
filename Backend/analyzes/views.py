from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Analysis
from .serializers import AnalysisSerializer

from coverletters.models import CoverLetter
from jobdescriptions.model import JobDescription

# 새로운 자소서 + JD 조합으로 분석 요청을 만드는 API
class AnalysisCreateView(APIView):
    def post(self, request):
        serializer = AnalysisSerializer(data=request.data)
        if serializer.is_valid():    # 유효성 검사
            analysis = serializer.save(status='pending')
            
            # TODO: 여기서 Celery 또는 FastAPI 연동 로직 들어감
        
            return Response({'message': '분석 요청이 등록되었습니다.', 'analysis_id': analysis.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 이미 존재하는 자소서에 대해 재분석 요청을 하는 API
class AnalysisRetryView(APIView):
    def post(self, request, coverletter_id):
        try:
            cover_letter = CoverLetter.objects.get(id=coverletter_id)
            job_description = cover_letter.job_description    # 커버레터에 JD가 연결되어 있다면
        except CoverLetter.DoesNotExist:
            return Response({'error': 'Cover letter not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        except AttributeError:
            return Response({'error': 'Cover letter does not have a job description.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # serializer를 통한 생성
        data = {
            'cover_letter_id': cover_letter.id,
            'job_description_id': job_description.id,
        }
        serializer = AnalysisSerializer(data=data)
        if serializer.is_valid():    # 유효성 검사
            analysis = serializer.save(status='pending')
        
            # TODO: 여기서 재분석 AI 요청 처리
        
            return Response({'message': '재분석 요청이 등록되었습니다.', 'analysis_id': analysis.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
