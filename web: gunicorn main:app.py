from flask import Flask

app = Flask(__name__)

app.secret_key = "mysecretkey"

from routes.auth import auth_bp
from routes.task import task_bp

app.register_blueprint(auth_bp)
app.register_blueprint(task_bp)

if __name__ == "__main__":
    app.run(debug = True)