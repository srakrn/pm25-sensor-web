import mysql.connector
from flask import Flask, jsonify, request
from os import getenv
from dotenv import load_dotenv
from cpe_pm25.api import api
load_dotenv()

app = Flask(__name__)

app.register_blueprint(api, url_prefix='/api')
