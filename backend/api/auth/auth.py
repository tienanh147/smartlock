from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token
from flask_jwt_extended.utils import get_jwt_identity
from email_validator import validate_email, EmailNotValidError
import traceback
import bcrypt
from datetime import datetime
from .query import get_user
from _validators import validate_request
import sys
from errors import RequestBodyError
from datetime import timedelta
from pymongo import MongoClient
from db_connector import connection_string
from decouple import config
auth_bp = Blueprint("auth", __name__)
DB_NAME = config('DATABASE')
@auth_bp.route("login", methods=["POST"])
@validate_request(request=request, required_fields=["username", "password"])
def login():
    try: 
        db = MongoClient(connection_string)[DB_NAME]
        body_data = request.get_json()
        username = body_data['username']
        password = body_data['password']

        user = get_user(db, username=username)

        access_token = ""
        if not user: 
            return jsonify(
                errors="người dùng không tồn tại",
                success=False,
                message="thông tin đăng nhập sai",
                status=400), 200
        password_in_db = user["password"]
        password_checker = bcrypt.checkpw(password.encode('utf-8'), password_in_db)
        if password_checker:
            access_token = create_access_token(identity=user["email"], expires_delta=timedelta(minutes=60))
            return jsonify(
                success=True,            
                errors=[],
                data=access_token,
                status=200), 200
            # save log user login
        else:
            return jsonify(
                errors="Sai mật khẩu hoặc tên đăng nhập",
                success=False,
                message="thông tin đăng nhập sai",
                status=400), 200
    except Exception: 
        return jsonify(
            errors=traceback.format_exception(*sys.exc_info()),
            message="Internal Server Error",
            success=False,
            status=500), 500
        
@auth_bp.route("signup", methods=["POST"])
@validate_request(request=request, required_fields=["username", "email", "password1", "password2"])
def signup():
    fail_msg_errors = []
    try:
        body_data = request.get_json()
        email=body_data["email"]
        username=body_data["username"]
        password1=body_data["password1"]
        password2=body_data["password2"]
       
        if password1 != password2:
            fail_msg_errors.append("mật khẩu xác nhận không trùng khớp")
        try: 
            validate_email(email)
        except EmailNotValidError: 
            fail_msg_errors.append("Định dạng email không phù hợp") 
        db = MongoClient(connection_string)[DB_NAME]
        exist_in_db = db.users.find_one({"email": email})
        
        if exist_in_db != None:
            return jsonify(
                errors="email đã tồn tại trong hệ thống",
                message="Bad request", 
                success=False,
                status=400
            ), 200
        if fail_msg_errors: 
            raise RequestBodyError
        hashed = bcrypt.hashpw(password2.encode('utf-8'), bcrypt.gensalt())
        user_info = dict(
            username=username,
            email=email,
            password=hashed,
            role_id=None,
            created_date=datetime.now()
        )
        try:
            db.users.insert_one(user_info)
        except Exception:
            raise Exception
        return jsonify(
            errors=[],
            success=True,
            message="Tài khoản đã tạo thành công"
        ), 200
    except RequestBodyError:
        return jsonify(
                errors=fail_msg_errors,
                message="Bad request", 
                success=False,
                status=400
            ), 200
    except Exception:
        return jsonify(
            errors=traceback.format_exception(*sys.exc_info()),
            message="Internal Server Error",
            success=False,
            status=500), 500
 
   