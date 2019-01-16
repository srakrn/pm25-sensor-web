import mysql.connector
from flask import Blueprint, render_template, abort, jsonify, request
from jinja2 import TemplateNotFound
from os import getenv
from dotenv import load_dotenv
load_dotenv()

web = Blueprint('web', __name__,
                template_folder='templates')


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
def render_index():
    return render_template("index.html")
