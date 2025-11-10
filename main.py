import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import factory


env = os.getenv("FLASK_ENV", "development")
config = factory(env)


app = Flask(__name__)
app.config.from_object(config)


db = SQLAlchemy(app)

if __name__ == "__main__":
    # Inicia la app para pruebas locales 
    app.run(host="0.0.0.0", port=5005)
