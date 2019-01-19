import mysql.connector
from flask import Blueprint, render_template, abort, jsonify, request
from jinja2 import TemplateNotFound
from os import getenv
from dotenv import load_dotenv
from datetime import timedelta

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


def get_air_condition(pm25):
    lower_bound = [0, 26, 38, 51, 91]
    brief_description = [
        "ดี",
        "ปกติ",
        "ปานกลาง",
        "เริ่มมีผลกระทบต่อสุขภาพ",
        "มีผลกระทบต่อสุขภาพ"
    ]
    description = [
        "คุณภาพอากาศดีมาก เหมาะสำหรับกิจกรรมกลางแจ้งและการท่องเที่ยว",
        "คุณภาพอากาศดี สามารถทำกิจกรรมกลางแจ้งและการท่องเที่ยวได้ตามปกติ",
        "ผู้ที่ต้องดูแลสุขภาพ หากมีอาการเบื้องต้น ควรลดระยะเวลาการทำกิจกรรมกลางแจ้ง",
        "ควรเฝ้าระวังสุขภาพ หากมีอาการเบื้องต้นควรงดกิจกรรมกลางแจ้ง ใช้อุปกรณ์ป้องกันหากจำเป็น",
        "ทุกคนควรหลีกเลี่ยงกิจกรรมกลางแจ้ง หลีกเลี่ยงพื้นที่ที่มีมลพิษทางอากาศสูง และใช้อุปกรณ์ป้องกันตนเองหากมีความจำเป็น"
    ]
    condition = [pm25 > i for i in lower_bound]
    i = condition.count(True)
    return {
        "level": i,
        "brief_description": brief_description[i-1],
        "description": description[i-1]
    }


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
