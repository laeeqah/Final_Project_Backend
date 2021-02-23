import sqlite3
from flask import Flask, render_template, request, jsonify



app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sign_up/')
def enter_new_student():
    return render_template('sign_up.html')

@app.route('/add-record/', methods=['POST'])
def add_new_record():
    try:
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email_address']
        password = request.form['password']

        with sqlite3.connect('mywebsite.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO user (fullname, username, email, password) VALUES (?, ?, ?, ?)", (fullname, username, email, password))
            con.commit()
            msg = "Record successfully added."
    except Exception as e:
        con.rollback()
        msg = "Error occurred in insert operation: " + str(e)
    finally:
        con.close()
        return render_template('results.html', msg=msg)


@app.route('/show_records/', methods=["GET"])
def show_records():
    with sqlite3.connect("mywebsite.db") as conn:
        conn.cursor()
        conn.execute('CREATE TABLE if not exists  user(userid auto_increment, fullname TEXT , username TEXT, email TEXT, password TEXT)')
        conn.commit()
    try:
        with sqlite3.connect('mywebsite.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM user")
            records = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database.") + str(e)
    finally:
        con.close()
        return jsonify("mywebsite.db")



