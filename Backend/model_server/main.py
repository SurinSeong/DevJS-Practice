from fastapi import FastAPI
from models import AnalyzeRequest, AnalyzeResponse
from analyze import analyze_similarity

app = FastAPI()

@app.post('/analyze/', response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    print(f'[분석 요청] ID: {request.analysis_id}')
    
    feedbacks = analyze_similarity(
        request.cover_letter,
        request.job_description
    )
    
    print(f'[분석 완료] 총 {len(feedbacks)}개의 문장 분석됨.')
    
    return {'feedbacks': feedbacks}