from extensions import * 
from models import MessageRequestDTO
import os
import openai
openai.organization = os.getenv('ORGANIZATION_ID')
openai.api_key = os.getenv('OPENAI_API_KEY')




DEFAULT_MODEL = 'text-davinci-003'
DEFAULT_TEMPERATURE = 0.9
DEFAULT_MAX_TOKENS = 1024

class ChatGptService:

    @classmethod
    def get_ai_model_answer(cls, data:MessageRequestDTO):
        return openai.Completion.create(
            prompt=data.question, 
            model=DEFAULT_MODEL,
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=DEFAULT_MAX_TOKENS
        )