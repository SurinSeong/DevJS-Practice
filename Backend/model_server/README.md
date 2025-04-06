# FastAPI

- JD + 자소서를 받아서 → 유사도 분석 + 추천 문장 생성

## 구조

```

model-server/
├── main.py               ← FastAPI 엔트리포인트
├── models.py             ← Pydantic 데이터 구조
├── analyze.py            ← 유사도 분석 + 추천 생성 함수
└── client.py             ← 여기서 request_analysis 함수 정의

```

### analyze.py

- 유사도 기반 분석 + 간단한 추천 문장 생성
    
    - `sentence-transformers` 사용
    - `KoSimCSE`, `KLUE`, `KoBERT`, 등 벡터 기반 유사도 분석에 최적
    - 문장 단위 유사도 계산 (`util.cos_sim`)이 매우 직관적
    - 속도 빠르고 문장 나누기 & 추천도 쉽게 가능

- 응답 형식

```
{
  "feedbacks": [
    {
      "original_sentence": "...",
      "similarity_score": 0.63,
      "is_weak": true,
      "recommendation": "...",
      "reason": "..."
    },
    ...
  ]
}
```
