from flask import Flask
from flask_jwt_extended import JWTManager
from decouple import config
from itsdangerous import URLSafeTimedSerializer

from auth import auth_bp
from profile import profile_bp

app= Flask(__name__)
version_api = "v1"
app.config['JWT_AUTH_HEADER_NAME'] = 'JWTAuthorization'
app.config['JWT_AUTH_HEADER_PREFIX'] = 'Bearer'
app.secret_key=config('JWT_SECRET_KEY')
app.serializerURL = URLSafeTimedSerializer(app.secret_key)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix=f'/api/{version_api}/auth')
app.register_blueprint(profile_bp, url_prefix=f'/api/{version_api}/profile')
if __name__ == "__main__":
    app.run(debug=True)
