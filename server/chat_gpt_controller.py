from flask import Blueprint, request, jsonify
from chat_gpt_service import ChatGptService 
from extensions import *
from models import MessageRequestDTO

chat_gpt_route_path = 'chat-gpt-ai'
chat_gpt_route = Blueprint(chat_gpt_route_path, __name__)


@chat_gpt_route.route('/message', methods=['POST'])
def get_ai_model_answer():
    body = request.json
    return jsonify({
        'result': ChatGptService.get_ai_model_answer(MessageRequestDTO.new_instance_from_flask_body(body))
    })
 