# 문장 생성 함수
import os
from huggingface_hub import InferenceClient    # LLM 호출

from dotenv import load_dotenv
load_dotenv()

##### 본인 토큰으로 변경하세요! #####
token = os.getenv('HF_API_TOKEN')

# 허깅페이스에서 제공하는 beomi/KoAlpaca-Polyglot-12.8B 모델 사용하기
client = InferenceClient("mistralai/Mixtral-8x7B-Instruct-v0.1", token=token)

def generate_recommendation(text, jd):
    # 문장 추천 프롬프트 생성 + 호출
    prompt = \
        f"""다음 문장은 자기소개서의 일부입니다. 기업의 JD 내용과 더 잘 맞게 다시 작성해 주세요.

        JD: {jd}
        문장: {text}

        추천 문장:
        """
    
    response = client.text_generation(prompt,
                                      max_new_tokens=60,    # 최대 60단어까지 생성
                                      temperature=0.7,
                                      do_sample=True,
                                      top_k=50)
    return response.strip()
