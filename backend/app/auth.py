# backend/app/auth.py
from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    return "Login endpoint"