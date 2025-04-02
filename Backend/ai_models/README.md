# ai_model 서빙

- 한국어 중심 LLM in HuggingFace : beomi/KoAlpaca-Polyglot-12.8B
    - 기반 : Polyglot-ko (한국어 중심 GPT 모델)
    - 특징: 한국어 인스트럭션 튜닝된 모델로, 프롬프트 기반 질답 및 생성에 매우 적합 / 자기소개서 리라이팅 작업에도 잘 맞음



## 0401

- **자기소개서 문장 <-> JD 비교 -> 추천 문장 받기**

- 순서
    1. 자기소개서 업로드 (CoverLetter)
    2. JD 업로드 (JobDescription)
    3. 분석 요청 (POST /api/analyze/)
    4. 문장 분리 + 유사도 계산 + 추천 생성
    5. Feedback, RecommendationSentence 저장
    6. GET /api/feedback/<id>/으로 확인