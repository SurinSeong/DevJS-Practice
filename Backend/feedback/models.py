from django.db import models
from coverletters.models import CoverLetter
from jds.models import JobDescription

# Create your models here.
# Feedback 모델
    # 자기소개서 전체에 대한 피드백
    # JD와 Coverletter를 참조하고, matching_score(= 유사도), 문법/가독성 점수 등 포함
class Feedback(models.Model):
    cover_letter = models.ForeignKey(CoverLetter, on_delete=models.CASCADE)
    job_description = models.ForeignKey(JobDescription, on_delete=models.SET_NULL, null=True)
    matching_score = models.FloatField(help_text="JD와의 일치도 (0~1)")
    grammar_score = models.FloatField(null=True, blank=True)
    clarity_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# RecommendationSentence 모델
    # Feedback과 연결된 문장 단위 추천 결과 저장용
    # 어떤 문장을 왜 추천했는지 이유까지 저장 가능
class RecommendationSentence(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name='recommendations')
    sentence = models.TextField()
    reason = models.CharField(max_length=255, help_text="추천 이유 또는 강조 키워드")