from django.db import models
from users.models import User

# Create your models here.
class JobDescription(models.Model):
    # 작성자
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # JD 업로드 파일
    file = models.FileField(upload_to='jds/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    # JD 텍스트 내용
    text_content = models.TextField(blank=True)

class ExtractedKeyword(models.Model):
    jd = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)