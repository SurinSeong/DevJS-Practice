import os
from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()

HF_TOKEN = os.getenv('HF_API_TOKEN')

messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="google/gemma-2-9b-it", token=HF_TOKEN)
answer = pipe(messages)
print(answer)