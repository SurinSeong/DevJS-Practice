# 폴더별 기능

```
Backend/
├── manage.py
├── Devjs/                 # 프로젝트 디렉토리
│   ├── __init__.py
│   ├── settings.py        # 'from decouple import config' 사용함.
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                # 사용자 인증 관련 앱
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py            # CustomUser 정의
│   ├── serializers.py       # (선택) 사용자 직렬화
│   ├── urls.py              # /auth/kakao, /auth/google URL 라우팅
│   ├── views.py             # 카카오, 구글 로그인 뷰
│   └── utils.py             # 사용자 생성 및 JWT 발급 함수
│
└── requirements.txt
```

---

## 🗂️ 각 파일 역할 요약

| 파일명 | 설명 |
|--------|------|
| `accounts/models.py` | `CustomUser` 모델 정의 (`AbstractUser` 상속) |
| `accounts/views.py` | 카카오/구글 로그인 처리를 위한 APIView 정의 |
| `accounts/urls.py` | `/auth/kakao/`, `/auth/google/` 등의 URL 연결 |
| `accounts/utils.py` | 소셜 사용자 생성 및 JWT 발급 로직 모듈화 |
| `backend/settings.py` | 앱 등록, OAuth 키 설정, 인증 설정 등 |
| `backend/urls.py` | 전체 API 라우팅 설정 (accounts.urls 포함) |

---

### accounts

- `models.py`
    - `CustomUser` 모델 정의 (`AbstractUser` 상속)
    - 추가 필드
        - `provider` : 소셜 로그인 제공자 이름
        - `social_id` : 소셜 로그인 제공자 보내주는 고유 사용자 ID  
        => 해당 유저의 소셜 로그인 계정을 유일하게 식별한다.

- `views.py`
    - `KakaoLoginView`, `GoogleLoginView`, `UserInfoView` 작성
    - 로직 흐름
        1. 프론트에서 받은 code 값을 받는다.
        2. 해당 code로 Access Token 요청
        3. Access Token으로 사용자 정보 요청 (email, id 등)
        4. 사용자 DB에 등록 or 이미 존재하면 로그인
        5. JWT 토큰 발급 후 프론트에 응답


- `urls.py`
    - `api/` 하위로 연결
    - URL 동작 방법
        - POST : `api/auth/kakao` (카카오 로그인) , `api/auth/google` (구글 로그인)
        - GET : `api/user/` (JWT 필요) 현재 로그인된 사용자 정보


**로그인 완료** 0403
✅ 카카오 소셜 로그인  
✅ JWT 기반 인증  
✅ access/refresh 토큰 관리  
✅ 토큰 자동 갱신  
✅ 로그인 후 유저 정보 조회  
✅ 로그인 유지 기능  


### 보완 사항

- 로그인 후, 닉네임을 받아야 할 듯 함.
---

## ✨ 다음에 할 수 있는 것들 (선택 옵션)

| 기능 | 설명 |
|------|------|
| 🔓 로그아웃 기능 | localStorage 초기화 + `/login`으로 이동 |
| 👤 유저 프로필 사진, 닉네임 표시 | 카카오에서 `nickname`, `profile_image_url` 가져오기 |
| ⚠️ 로그인 안 된 상태에서 `/dashboard` 접근 제한 | access_token 없으면 리디렉트 |
| 📦 axios 인스턴스로 인증 공통 처리 | 요청마다 헤더 설정 중복 줄이기 |
| 🛡 실제 배포 환경용 보안 설정 | CORS, HTTPS, 토큰 저장 방식 등 |

---

