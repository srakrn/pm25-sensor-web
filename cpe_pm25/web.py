import mysql.connector
from flask import Blueprint, render_template, abort, jsonify, request, url_for
from jinja2 import TemplateNotFound
import os.path
from os import getenv
from dotenv import load_dotenv
import markdown
from cpe_pm25.air_condition import get_air_condition
load_dotenv()

web = Blueprint('web', __name__, template_folder='templates')


@web.before_request
def generate_conn():
    global conn, cursor
    conn = mysql.connector.connect(
        host=getenv("MYSQL_HOST"),
        user=getenv("MYSQL_USERNAME"),
        passwd=getenv("MYSQL_PASSWORD"),
        database=getenv("MYSQL_DB")
    )

    cursor = conn.cursor()


@web.route("/")
def index():
    sql = '''
    SELECT *
    FROM logs
    ORDER BY timestamp DESC
    '''
    cursor.execute(sql)
    latest_data = cursor.fetchone()
    data = {
        "timestamp": latest_data[0],
        "PM10": latest_data[1],
        "PM2.5": latest_data[2],
        "PM1": latest_data[3],
        "description": get_air_condition(latest_data[2])
    }
    return render_template("index.html", data=data, alert=getenv("ALERT"))


@web.route("/about")
def sensor_info():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    about_path = os.path.join(BASE_DIR, "static/about.md")
    with open(about_path, encoding='utf-8') as f:
        contents_md = "".join(f.readlines())
        contents = markdown.markdown(contents_md)
    return render_template("about.html", contents=contents)


@web.route("/manifest.json")
def json_webpack():
    json_data = {
        "short_name": "PM2.5@KU",
        "name": "PM2.5@KU",
        "icons": [
            {
                "src": url_for('static', filename='logo-192px.png'),
                "type": "image/png",
                "sizes": "192x192"
            },
            {
                "src": url_for('static', filename='logo-512px.png'),
                "type": "image/png",
                "sizes": "512x512"
            }
        ],
        "start_url": '/',
        "background_color": "#FFFFFF",
        "display": "standalone",
        "scope": '/',
        "theme_color": "#FFA000"
    }
    return jsonify(json_data)
