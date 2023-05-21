from concurrent.futures import process
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import requests
import json
from flask_login import login_required, current_user
from .models import User, Prompt
from . import db
from dotenv.main import load_dotenv
import os
load_dotenv()



views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        pass 

    if request.method == 'POST':
        pass
    
    return render_template('index.html')

@views.route('/chat/<name>', methods=['GET', 'POST'])
@login_required
def solve(name):
    chars = {
        'Chandu':os.environ['Chandu'], 
        'Golu': os.environ['Golu'], 
        'Ravi': os.environ['Ravi'], 
        'Bhola': os.environ['Bhola'], 
        'Gopal': os.environ['Gopal'],
        'Ramu': os.environ['Ramu']
    }

    m_names = {
            "Chandu":['Chandu: Hi there! My name is Chandu. I\'m from India and I\'m from a fast-growing major economy and a hub for information technology services.'], 
            "Golu":['Golu: Hi! I\'m Golu. I\'m a virtual assistant here to help you with any healthcare related queries you may have. How may I help you?'],
            "Ravi":['Ravi: I am Ravi, I can answer anything on IPL and cricket in general.'],
            "Bhola":['Bhola: I can answer your queries regarding The Taj.'],
            "Gopal":['Gopal: Hi, my name is Gopal. Ask me anything about Bollywood!'],
            'Ramu':['Ramu: My name is Ramu, I am a banking expert. Come after lunch time!']
            }

    favorite_language = os.environ['API_KEY']

    for i in m_names.keys():
        t = Prompt.query.filter_by(user_id=current_user.id, char_name=i)
        for j in t:
            if j.content not in m_names[i]:
                print(f"{i}----{j.content}")
                m_names[i].append(j.content)
    
    if request.method == 'POST':
        url = "https://api.convai.com/character/getResponse"
        prompt = request.form.get('message')
        if prompt is not "":
            payload={'userText': prompt,
            'charID': chars[name],
            'sessionID': '-1',
            'voiceResponse': 'False'}
            headers = {
            'CONVAI-API-KEY': favorite_language
            }
            
            response = requests.request("POST", url, headers=headers, data=payload)
            data = response.json()
            character_response = data["text"]

            user_prompt = current_user.name+": "+prompt
            character_response = name+": "+character_response
            
            new_prompt1 = Prompt(char_name=name,user_id=current_user.id, content=user_prompt)
            new_prompt2 = Prompt(char_name=name,user_id=current_user.id, content=character_response)
            db.session.add(new_prompt1)
            db.session.add(new_prompt2)
            db.session.commit()
            
            m_names[name].append(user_prompt)
            m_names[name].append(character_response)

    l = m_names[name][::-1]
    return render_template('chat.html', messages=l, name=name)
