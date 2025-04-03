from django.urls import path
from .views import KakaoLoginView, GoogleLoginView, UserInfoView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("auth/kakao/", KakaoLoginView.as_view(), name="kakao-login"),
    path("auth/google/", GoogleLoginView.as_view(), name="google-login"),
    
    path("user/", UserInfoView.as_view(), name="user-info"),  # 선택 사항: 로그인된 유저 정보
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
