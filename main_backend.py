# important
import os

import pymysql
from flask_sqlalchemy import SQLAlchemy

from database.Domain.BaseClass import Base

pymysql.install_as_MySQLdb()
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = (f'mysql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASSWORD")}'
                                         f'@{os.getenv("DATABASE_HOST")}/{os.getenv("DATABASE_NAME")}')

db.init_app(app)


@app.route('/api/hello')
def hello_world():
    return jsonify(message="Hello from Flask! :)")


if __name__ == '__main__':
    app.run(debug=not bool(int(os.getenv("PRODUCTION"))), host='0.0.0.0', port=8000)
