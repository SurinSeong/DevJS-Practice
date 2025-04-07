import re
from typing import List

from models import FeedbackItem
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
from concurrent.futures import ThreadPoolExecutor


# 1. 모델 로딩 (FastAPI 시작 시 1회)
model = SentenceTransformer('jhgan/ko-sbert-nli')
generator = pipeline('text-generation', model='skt/kogpt2-base-v2')    # 파이프 라인 사용 EleutherAI/polyglot-ko-1.3b


def split_sentences(text: str) -> List[str]:
    return [s.strip() for s in text.split('.') if s.strip()]


def parse_generated_result(text: str) -> tuple[str, str]:
    rec, reason = '', ''
    try:
        rec_match = re.search(r"추천 문장[:：]\s*(.+)", text)
        reason_match = re.search(r"이유[:：]\s*(.+)", text)

        if rec_match:
            rec = rec_match.group(1).strip()
        if reason_match:
            reason = reason_match.group(1).strip()
            
        # 💡 조건 강화: 의미 없는 텍스트는 제거
        if rec.lower() in ["이유:", "", "내용 없음"] or rec.startswith("이유"):
            rec = ""
        if reason.strip().startswith("#") or len(reason.strip()) < 5:
            reason = ""    
            
    except Exception as e:
        print(f"[❌ 파싱 오류] {e}")
        print(f"[📄 원본 응답] {text}")
        
    return rec, reason


def generate_prompt(original: str, jd: str) -> str:
    return f"""
    [자기소개서 문장]
    {original}

    [직무 설명]
    {jd}

    위 자기소개서 문장이 직무 설명과 잘 맞지 않는다면, 다음 형식으로 답해주세요.

    [추천 문장]
    (직무 설명과 잘 맞도록 문장을 고쳐주세요)

    [이유]
    (왜 고쳐야 하는지 설명해주세요)
    """


def generate_feedback(prompt: str) -> tuple[str, str]:
    try:
        result = generator(prompt, max_new_tokens=150, do_sample=True, temperature=0.9)[0]["generated_text"]
        print(result)
        
        rec, reason = parse_generated_result(result)

        # ✅ fallback 값 적용 (이 부분!)
        if not rec:
            rec = "JD에 맞게 구체적인 프로젝트 경험을 작성해보세요."
        if not reason:
            reason = "직무 연관성이 부족하거나 너무 추상적인 표현입니다."
            
        if not rec or not reason:
            print(f"[⚠️ 추천 생성 부족] rec: '{rec}', reason: '{reason}'")

        print("[📥 LLM 응답]", result)
        print("[✅ 파싱된 결과]", rec, reason)
        
        return rec, reason

    except Exception as e:
        print(f"[LLM 생성 실패] {e}")
        return "JD에 맞게 구체적인 프로젝트 경험을 작성해보세요.", "직무 연관성이 부족하거나 너무 추상적인 표현입니다."



def analyze_similarity(cover_letter: str, job_description: str) -> List[FeedbackItem]:
    sentences = split_sentences(cover_letter)
    jd_embedding = model.encode(job_description, convert_to_tensor=True)

    feedbacks = []
    weak_prompts = []
    weak_indexes = []

    # 1. 유사도 계산 & 약한 문장 추리기
    for idx, sent in enumerate(sentences):
        sent_embedding = model.encode(sent, convert_to_tensor=True)
        score = float(util.cos_sim(sent_embedding, jd_embedding)[0][0])
        is_weak = score < 0.7

        feedback = FeedbackItem(
            original_sentence=sent,
            similarity_score=score,
            is_weak=is_weak,
            recommendation="",
            reason=""
        )

        feedbacks.append(feedback)

        if is_weak:
            prompt = generate_prompt(sent, job_description)
            weak_prompts.append(prompt)
            weak_indexes.append(idx)

    # 2. 병렬로 LLM 호출
    if weak_prompts:
        with ThreadPoolExecutor() as executor:
            results = list(executor.map(generate_feedback, weak_prompts))

        for idx, (rec, reason) in zip(weak_indexes, results):
            feedbacks[idx].recommendation = rec
            feedbacks[idx].reason = reason

    return feedbacks


# # 2. 문장 단위로 분리하는 함수
# def split_sentences(text: str) -> List[str]:
#     return [s.strip() for s in text.split('.') if s.strip()]


# # 3. 생성된 LLM 결과에서 추천 문장 + 이유 추출
# def parse_generated_result(text: str) -> tuple[str, str]:
#     rec, reason = '', ''
#     try:
#         rec_match = re.search(r"추천 문장[:：]\s*(.+)", text)
#         reason_match = re.search(r"이유[:：]\s*(.+)", text)

#         if rec_match:
#             rec = rec_match.group(1).strip()
#         if reason_match:
#             reason = reason_match.group(1).strip()
#     except Exception as e:
#         print(f"[파싱 오류] {e}")
#         print(f"[원본 응답] {text}")

#     return rec, reason


# # 4. LLM 기반 추천 문장 + 이유 생성 함수
# def generate_feedback(original: str, jd: str) -> tuple[str, str]:
#     prompt = f"""
#     자기소개서 문장: "{original}"
#     직무 설명: "{jd}"

#     이 자기소개서 문장이 JD에 잘 맞지 않는다면, 고친 문장과 그 이유를 알려주세요.

#     다음 형식에 맞춰 주세요:

#     추천 문장: ...
#     이유: ...
#     """

#     try:
#         result = generator(prompt, max_new_tokens=150, do_sample=True, temperature=0.9)[0]["generated_text"]
#         return parse_generated_result(result)
    
#     except Exception as e:
#         print(f"[LLM 생성 실패] {e}")
#         return "JD와 관련된 구체적인 경험으로 보완해보세요.", "직무 연관성이 부족합니다."



# # 4. 최종 분석 함수
# def analyze_similarity(cover_letter: str, job_description: str) -> List[FeedbackItem]:
#     cl_sentences = split_sentences(cover_letter)
#     jd_embedding = model.encode(job_description, convert_to_tensor=True)

#     feedbacks = []
#     for sent in cl_sentences:
#         sent_embedding = model.encode(sent, convert_to_tensor=True)
#         score = float(util.cos_sim(sent_embedding, jd_embedding)[0][0])
#         is_weak = score < 0.7

#         recommendation = ""
#         reason = ""

#         if is_weak:
#              recommendation, reason = generate_feedback(sent, job_description)

#         feedbacks.append(FeedbackItem(
#             original_sentence=sent,
#             similarity_score=score,
#             is_weak=is_weak,
#             recommendation=recommendation,
#             reason=reason
#         ))

#     return feedbacks
