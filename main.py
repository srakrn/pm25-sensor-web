import mysql.connector
from flask import Flask, jsonify, request
from os import getenv
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


conn = mysql.connector.connect(
    host=getenv("MYSQL_HOST"),
    user=getenv("MYSQL_USERNAME"),
    passwd=getenv("MYSQL_PASSWORD"),
    database=getenv("MYSQL_DB")
)

cursor = conn.cursor()


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/latest")
def return_latest_dust():
    sql = '''
    SELECT *
    FROM logs
    WHERE timestamp = (SELECT MAX(timestamp) FROM logs)
    '''
    cursor.execute(sql)
    latest_data = cursor.fetchone()
    return jsonify({
        "timestamp": latest_data[0],
        "PM10": latest_data[1],
        "PM2.5": latest_data[2],
        "PM1": latest_data[3]
    })


@app.route("/query")
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
