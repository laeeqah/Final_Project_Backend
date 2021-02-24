import sqlite3
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def initialize_database():
    conn = sqlite3.connect('database.db')

    conn.execute('CREATE TABLE if not exists  user(userid integer primary key autoincrement, fullname TEXT ,username TEXT, email TEXT, password TEXT)')
    print("user table created succesfully")


initialize_database()

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] =row[idx]
    return d

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sign_up/')
def enter_new_user():
    return render_template('sign_up.html')

@app.route('/add-record/', methods=['POST'])
def add_new_record():
    try:
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email_address']
        password = request.form['password']

        with sqlite3.connect('database.db') as con:
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


@app.route('/list-records/')
def listUsers():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            con = sqlite3.connect("database.db")
            cur = con.cursor()
            cur.execute("select * from user")

            rows = cur.fetchall()

    except Exception as e:
        print("Something happened when getting data from db: " + str(e))
    return jsonify(rows)

if __name__ =='__main__':
    app.run(debug=True)

# @app.route('/show_records/', methods=["GET"])
# def show_records():
#     with sqlite3.connect("mywebsite.db") as conn:
#         conn.cursor()
#
#         conn.commit()
#     try:
#         with sqlite3.connect('mywebsite.db') as con:
#             cur = con.cursor()
#             cur.execute("SELECT * FROM user")
#             records = cur.fetchall()
#     except Exception as e:
#         con.rollback()
#         print("There was an error fetching results from the database.") + str(e)
#     finally:
#         con.close()
#         return jsonify(records)
#
# @app.route('/delete-user/<int:userid>/', methods=["GET"])
# def delete_student(userid):
#
#     msg = None
#     try:
#         with sqlite3.connect('mywebsite.db') as con:
#             cur = con.cursor()
#             cur.execute("DELETE FROM user WHERE userid=" + str(userid))
#             con.commit()
#             msg = "A record was deleted successfully from the database."
#     except Exception as e:
#         con.rollback()
#         msg = "Error occurred when deleting a user in the database: " + str(e)
#     finally:
#         con.close()
#         return render_template('delete-success.html', msg=msg)
