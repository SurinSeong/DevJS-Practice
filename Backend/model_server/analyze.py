import re
from typing import Tuple
from typing import List

from models import FeedbackItem
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline


# 1. 모델 로딩 (FastAPI 시작 시 1회)
model = SentenceTransformer('jhgan/ko-sbert-nli')
generator = pipeline('text-generation', model='EleutherAI/polyglot-ko-1.3b', tokenizer='EleutherAI/polyglot-ko-1.3b')    # 파이프 라인 사용


# 2. 문장 단위로 분리하는 함수
def split_sentences(text: str) -> List[str]:
    return [s.strip() for s in text.split('.') if s.strip()]


# 3. 생성된 LLM 결과에서 추천 문장 + 이유 추출

def parse_generated_result(text: str) -> Tuple[str, str]:
    recommendation, reason = '', ''

    try:
        rec_match = re.search(r"추천 문장[:：]\s*(.+)", text)
        reason_match = re.search(r"이유[:：]\s*(.+)", text)

        if rec_match:
            recommendation = rec_match.group(1).strip()
        if reason_match:
            reason = reason_match.group(1).strip()

    except Exception as e:
        print("[❌ 파싱 오류]", e)
        print("[📄 원본 응답]", text)

    return recommendation, reason




# 4. 최종 분석 함수
def analyze_similarity(cover_letter: str, job_description: str) -> List[FeedbackItem]:
    sentences = split_sentences(cover_letter)
    jd_embedding = model.encode(job_description, convert_to_tensor=True)
    
    feedbacks = []
    prompts = []
    weak_indexes = []
    
    for i, sentence in enumerate(sentences):
        sentence_embedding = model.encode(sentence, convert_to_tensor=True)
        score = float(util.cos_sim(sentence_embedding, jd_embedding)[0][0])
        is_weak = score < 0.7    # 기준 값 조정 가능

        feedback = FeedbackItem(
            original_sentence=sentence,
            similarity_score=score,
            is_weak=is_weak,
            recommendation="",
            reason=""
        )
        
        if is_weak:    # 유사도가 낮으면
            prompt = f"""
                    [직무 설명]
                    {job_description}
                    
                    [자기소개서 문장]
                    {sentence}
                    
                    이 문장이 직무에 적합하지 않다면, 더 적절한 문장으로 고쳐주시고 그 이유도 설명해주세요.

                    다음 형식에 맞춰서 답변해주세요:

                    추천 문장:
                    이유:
                    """
        
            # 위의 추천 문장 받는 포맷을 문장 마다 생성할 수 있도록 리스트에 넣어주기
            prompts.append(prompt)
            weak_indexes.append(len(feedbacks))    # 고친 문장 위치 추적
        
        feedbacks.append(feedback)
        
    # 약한 문장만 LLM으로 추천 생성
    if prompts:
        results = generator(
            prompts,
            max_new_tokens=80,
            do_sample=True,
            temperature=0.8,
            truncation=True
        )

        for idx, result in zip(weak_indexes, results):
            # generator(...) 결과에서 텍스트 추출
            gen_text = result[0]["generated_text"]
            print(gen_text)

            # JSON 형태로 파싱
            rec, reason = parse_generated_result(gen_text)

            # 해당 위치의 feedback 객체에 저장
            feedbacks[idx].recommendation = rec
            feedbacks[idx].reason = reason

    return feedbacks