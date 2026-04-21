from flask import Flask

def create_app():

    app = Flask(__name__)

    app.secret_key = "mysecretkey"

    from routes.auth import auth_bp
    from routes.task import task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app
