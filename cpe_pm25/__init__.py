import mysql.connector
from flask import Flask, jsonify, request
from os import getenv
from dotenv import load_dotenv
from cpe_pm25.web import web
from cpe_pm25.api import api
from babel.dates import format_datetime
load_dotenv()

app = Flask(__name__)

app.register_blueprint(web, url_prefix='/')
app.register_blueprint(api, url_prefix='/api')


def datetime(value, format='medium'):
    if format == 'full':
        format = "EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format = "DD/MM/YYYY HH:mm"
    return format_datetime(value, format)


app.jinja_env.filters['datetime'] = datetime
