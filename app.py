import os
from flask import Flask
from model.model import setup_db
from flask_cors import CORS

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        greeting = "Hello!" 
        return greeting

    @app.route('/coolkids')
    def be_cool():
        return "Be cool, man, be coooool!"

    return app

app = create_app()

if __name__ == '__main__':
    app.run()
