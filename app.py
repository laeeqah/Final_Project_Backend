import sqlite3
from flask import Flask,render_template, request,jsonify
from flask_cors import CORS




def initialize_database():
    conn = sqlite3.connect('database.db')

    conn.execute('CREATE TABLE if not exists  user(userid integer primary key autoincrement, fullname TEXT ,username TEXT, email TEXT, password TEXT)')
    # conn.execute('CREATE TABLE if not exists  products(proid integer primary key autoincrement, description TEXT, color TEXT, size TEXT) ')

    print("user table created succesfully")
    print("product table created succesfully")

    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
    print(cur.fetchall())

initialize_database()

app = Flask(__name__)
CORS(app)
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] =row[idx]
    return d

@app.route('/')
def register():
    return render_template('sign_up.html')


@app.route('/')
@app.route('/main/', methods=['POST'])
def main_page():
    if  request.method == "POST":
        msg = None
        try:
            post_data = request.get_json()
            fullname = post_data['fullname']
            username = post_data['username']
            email = post_data['email']
            password = post_data['password']
            print(fullname,username)
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO user (fullname, username, email, password) VALUES (?, ?, ?, ?)", (fullname, username, email, password))
                con.commit()
                msg = str("Record successfully added.")
        except Exception as e:
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            return {'msg':msg}


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

# @app.route('/logged/', methods= ['GET','POST'])
# def logged():
#     error = None
#     if request.method == 'POST':
#
#         try:
#             username = request.form['username']
#             password = request.form['password']
