import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8MB
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    from .routes import bp
    app.register_blueprint(bp)

    return app
