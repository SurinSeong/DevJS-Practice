from typing import List
from models import FeedbackItem
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('jhgan/ko-sbert-nli')

def split_sentence(text: str) -> List[str]:
    return [s.strip() for s in text.split('.') if s.strip()]


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
            recommendation = f'{sentence} (이 문장을 좀 더 구체적으로 써보세요.)'
            reason = 'JD와 유사도가 낮아 개선이 필요합니다.'
            
        feedbacks.append(FeedbackItem(
            original_sentence=sentence,
            similarity_score=score,
            is_weak=is_weak,
            recommendation=recommendation,
            reason=reason
        ))
        
        return feedbacks