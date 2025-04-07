from typing import List
from models import FeedbackItem
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline

model = SentenceTransformer('jhgan/ko-sbert-nli')

generator = pipeline('text-generation', model='EleutherAI/polyglot-ko-1.3b')    # 파이프 라인 사용


# 문장 단위로 분리하는 함수
def split_sentence(text: str) -> List[str]:
    return [s.strip() for s in text.split('.') if s.strip()]


# 자기소개서 추천 문장 생성 함수
def generate_better_sentence(original: str, jd: str) -> str:
    prompt = f"""
              자기소개서 문장: '{original}'
              직무 설명: '{jd}'
              이 자기소개서 문장을 직무에 맞게 고쳐주세요.:
              """
    
    response = generator(prompt, max_length=100, do_sample=True, temperature=0.9)
    return response[0]['generated_text'].split('고쳐주세요:')[-1].strip().split('\n')[0]


# 이 문장을 개선해야 하는 이유 생성 함수
def generate_reason_for_feedback(original: str, jd: str) -> str:
    prompt = f"""
              자기소개서 문장: '{original}'
              직무 설명: '{jd}'
              왜 이 문장을 개선해야 할까요?
              """
    
    response = generator(prompt, max_length=100, do_sample=True, temperature=0.9)
    return response[0]['generated_text'].split('왜 이 문장을 개선해야 할까요?')[-1].strip().split('\n')[0]


def analyze_similarity(cover_letter: str, job_description: str) -> List[FeedbackItem]:
    cl_sentences = split_sentence(cover_letter)
    jd_embedding = model.encode(job_description, convert_to_tensor=True)
    
    feedbacks = []
    
    for sentence in cl_sentences:
        sentence_embedding = model.encode(sentence, convert_to_tensor=True)
        score = float(util.cos_sim(sentence_embedding, jd_embedding)[0][0])
        is_weak = score < 0.7
        
        recommendation = ''
        reason = ''
        
        if is_weak:
            recommendation = generate_better_sentence(sentence, job_description)
            reason = generate_reason_for_feedback(sentence, job_description)
            
        feedbacks.append(FeedbackItem(
            original_sentence=sentence,
            similarity_score=score,
            is_weak=is_weak,
            recommendation=recommendation,
            reason=reason
        ))
        
        return feedbacks