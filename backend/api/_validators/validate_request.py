from errors import RequestBodyError
from functools import wraps
from flask import jsonify, Request
from copy import deepcopy
def validate_request(request: Request, required_fields: list = []):
    '''
    Decorator to check the request has parsed required fields and in json format? 
    @param: 
    - request: flask request to get body data
    - required_fields: list of required fields
    '''
    def decorator(fn): 
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try: 
                body_data = request.get_json()
                if not body_data: raise RequestBodyError 
                missing_fields = [field for field in required_fields \
                    if (field not in body_data) or (body_data.get(field) is None)]
                if missing_fields: 
                    return jsonify(
                        message="Thiếu các trường cần thiết",
                        missing_fields=missing_fields,
                        success=False,
                        status=400
                    ), 400
            except RequestBodyError:
                return jsonify(
                    message="Thiếu body data",
                    success=False,
                    status=400), 400
            return fn(*args, **kwargs)
        return wrapper 
    return decorator