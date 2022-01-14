import sys
from email_validator import EmailNotValidError, validate_email
from flask_jwt_extended import jwt_required
from decouple import config 
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request, current_app
from pymongo import MongoClient
from db_connector import connection_string
from decouple import config
DB_NAME = config('DATABASE')
profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('getme')
@jwt_required()
def get_me():
    current_user_email = get_jwt_identity()
    db = MongoClient(connection_string)[DB_NAME]
    data = db.users.find_one(
        {"email": current_user_email},
        {"_id": {"$toString": "$_id"},"email": 1, "username": 1, "role_id": 1, "created_date": 1}
    )
    return jsonify(
        data=data,
        status=200,
        message="ok",
        success=True
    ), 200