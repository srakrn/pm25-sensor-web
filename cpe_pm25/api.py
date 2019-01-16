import mysql.connector
from flask import Blueprint, render_template, abort, jsonify, request
from jinja2 import TemplateNotFound
from os import getenv
from dotenv import load_dotenv
load_dotenv()

api = Blueprint('api', __name__,
                template_folder='templates')


@api.before_request
def generate_conn():
    global conn, cursor
    conn = mysql.connector.connect(
        host=getenv("MYSQL_HOST"),
        user=getenv("MYSQL_USERNAME"),
        passwd=getenv("MYSQL_PASSWORD"),
        database=getenv("MYSQL_DB")
    )

    cursor = conn.cursor()


@api.route("/latest")
def return_latest_dust():
    sql = '''
    SELECT *
    FROM logs
    ORDER BY timestamp DESC
    '''
    cursor.execute(sql)
    latest_data = cursor.fetchone()
    return jsonify({
        "timestamp": latest_data[0],
        "PM10": latest_data[1],
        "PM2.5": latest_data[2],
        "PM1": latest_data[3]
    })


@api.route("/query")
def return_amounted_dust():
    try:
        amount = int(request.args.get('amount'))
    except ValueError:
        return jsonify({
            "error": "wrong parameter"
        })
    except TypeError:
        amount = 10
    sql = '''
    SELECT *
    FROM logs
    ORDER BY timestamp DESC
    '''
    cursor.execute(sql)
    res = []
    for _ in range(amount):
        latest_data = cursor.fetchone()
        if latest_data == None:
            break
        res.append({
            "timestamp": latest_data[0],
            "PM10": latest_data[1],
            "PM2.5": latest_data[2],
            "PM1": latest_data[3]
        })
    return jsonify(res)


@api.route("/insert")
def insert():
    secret = str(request.args.get('secret'))
    if secret != getenv("SECRET"):
        return jsonify({
            "error": "invalid secret"
        })
    sql = "INSERT INTO logs (`pm10`, `pm2.5`, `pm1`) VALUES (%s, %s, %s)"
    try:
        values = [int(i) for i in request.args.get('values').split(",")]
    except AttributeError:
        return jsonify({
            "error": "invalid values"
        })
    if len(values) != 3:
        return jsonify({
            "error": "invalid values length"
        })
    cursor.execute(sql, values)
    conn.commit()
    return jsonify({
        "status": "done"
    })
