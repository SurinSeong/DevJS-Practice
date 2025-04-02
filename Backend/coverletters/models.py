from django.db import models
from users.models import User

# Create your models here.
class CoverLetter(models.Model):
    # 작성자
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 업로드된 자소서 파일
    file = models.FileField(upload_to='coverletters/', null=True, blank=True)
    # 자소서 텍스트 본문
    text_content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # 최신 피드백과 연결
    latest_feedback = models.OneToOneField(
        'feedback.Feedback',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='latest_for'
    )