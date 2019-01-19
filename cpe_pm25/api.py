import mysql.connector
from flask import Blueprint, render_template, abort, jsonify, request
from jinja2 import TemplateNotFound
from os import getenv
from dotenv import load_dotenv
from datetime import timedelta
from cpe_pm25.air_condition import get_air_condition

load_dotenv()

api = Blueprint('api', __name__,
                template_folder='templates')


class DustDatabase:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host=getenv("MYSQL_HOST"),
            user=getenv("MYSQL_USERNAME"),
            passwd=getenv("MYSQL_PASSWORD"),
            database=getenv("MYSQL_DB")
        )
        self.cursor = self.conn.cursor()

    def query(self, n=100):
        if n > 200:
            n = 200
        sql = '''
        SELECT convert_tz(`timestamp`,@@session.time_zone,'+00:00'), `pm10`, `pm2.5`, `pm1`
        FROM logs
        ORDER BY timestamp DESC
        '''
        self.cursor.execute(sql)
        res = []
        for _ in range(n):
            latest_data = self.cursor.fetchone()
            if latest_data == None:
                break
            res.append({
                "timestamp": latest_data[0],
                "PM10": latest_data[1],
                "PM2.5": latest_data[2],
                "PM1": latest_data[3]
            })
        return res

    def insert(self, pm10, pm25, pm1):
        sql = "INSERT INTO logs (`pm10`, `pm2.5`, `pm1`) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (pm10, pm25, pm1))
        self.conn.commit()
        return True


@api.route("/")
def api_manual():
    return render_template("api.html")


@api.route("/latest")
def return_latest_dust():
    db = DustDatabase()
    data = db.query(n=1)[0]
    data["description"] = get_air_condition(data["PM2.5"])
    return jsonify(data)


@api.route("/history")
def return_amounted_dust():
    try:
        amount = int(request.args.get('amount'))
    except ValueError:
        return jsonify({
            "error": "wrong parameter"
        })
    except TypeError:
        amount = 10
    db = DustDatabase()
    data = db.query(n=amount)
    return jsonify(data)


@api.route("/insert")
def insert():
    secret = str(request.args.get('secret'))
    if secret != getenv("SECRET"):
        return jsonify({
            "error": "invalid secret"
        })
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
    db = DustDatabase()
    db.insert(values[0], values[1], values[2])
    return jsonify({
        "status": "done"
    })
