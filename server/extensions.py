#from flask import Flask, make_response, jsonify, request, session as browser_session
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy
#from chat_gpt_controller import chat_gpt_route_path, chat_gpt_route


#import os 
#import openai

migrate = Migrate()
bcrypt = Bcrypt()
db = SQLAlchemy()