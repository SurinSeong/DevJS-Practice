from django.shortcuts import render

from .recommendations import generate_recommendation    # LLM 추천 함수
from feedback.models import Feedback, RecommendationSentence
from coverletters.models import CoverLetter
from jds.models import JobDescription

import requests
import kss

from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
@api_view(['POST'])
def analyze_and_save(request):
    jd_id = request.data.get("jd_id")    
    cl_id = request.data.get("cl_id")    
    
    try:
        jd_obj = JobDescription.objects.get(id=jd_id)    # JD
        cl_obj = CoverLetter.objects.get(id=cl_id)    # 자소서
    except:
        return Response({"error": "JD 또는 자기소개서를 찾을 수 없습니다."}, status=400)

    sentences = kss.split_sentences(cl_obj.text_content)    # 자기소개서 문장 분리
    recommendations = []
    similarity_scores = []

    for sentence in sentences:
        try:
            # 1. 유사도 분석
            sim_response = requests.post("http://localhost:8001/similarity", json={
                "text1": sentence,
                "text2": jd_obj.text_content
            })
            
            similarity = sim_response.json()["similarity_score"]
            
        except Exception as e:
            similarity = 0.0    # 실패한 경우, 기본값
            
        similarity_scores.append(similarity)

        # 2. 유사도 낮으면 추천 문장 생성 (기준 : 유사도 < 0.5)
        if similarity >= 0 and similarity < 0.5:
            recommended = generate_recommendation(sentence, jd_obj.text_content)
            recommendations.append((sentence, recommended))
    
    avg_score = round(sum(similarity_scores) / len(similarity_scores), 4)    # 평균 유사도 계산하기
    
    # Feedback 저장
    feedback = Feedback.objects.create(
        cover_letter = cl_obj,
        job_description = jd_obj,
        matching_score = avg_score
    )
    
    # 추천 문장 저장
    for original, recommended in recommendations:
        RecommendationSentence.objects.create(
            feedback=feedback,
            sentence=recommended,
            reason='JD와 의미적 유사도가 낮음'
        )

    return Response({
        'feedback_id':feedback.id,
        'matching_score':avg_score,
        'recommendations':[rec for _, rec in recommendations]
    })