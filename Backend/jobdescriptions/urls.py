# jobdescriptions/urls.py
from rest_framework.routers import DefaultRouter
from .views import JobDescriptionViewSet

# router 이용해서 한번에 url 등록할 수 있도록
router = DefaultRouter()
router.register(r'job-descriptions', JobDescriptionViewSet, basename='jobdescription')

urlpatterns = router.urls
