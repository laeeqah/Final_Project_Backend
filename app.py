import sqlite3
from flask import Flask,render_template, request,jsonify
from flask_cors import CORS




def initialize_database():
    conn = sqlite3.connect('database.db')

    conn.execute('CREATE TABLE if not exists  user(userid integer primary key autoincrement, fullname TEXT not null ,username TEXT not null, email TEXT not null, password TEXT not null)')
    conn.execute('CREATE TABLE if not exists  products(proid integer primary key autoincrement, images TEXT, price TEXT, description TEXT, categories TEXT, color TEXT, size TEXT)')

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

# REGISTRATION
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

# SHOW ALL RECORDS
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


# LOGIN
@app.route('/logged/', methods= ['GET'])
def logged():
    msg = None
    if request.method == 'GET':

        try:
            username = request.form['username']
            password = request.form['password']
            print(username)
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM user(username,password) VALUES (?, ?)", (username, password))
                con.commit()
                msg = str("Successfully logged")
        except Exception as e:
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            return {'msg':msg}

# PRODUCTS
@app.route('/')
@app.route('/shop/', methods= ['POST'])
def cart():
    if  request.method == "POST":
        msg = None
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Maroon Dress','https://i.postimg.cc/PqD1WnVf/cocktail-dress2.jpg','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Dress','Maroon', 'M')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size)  VALUES('Sparkly Dress','https://i.postimg.cc/dV6VgH7R/cocktail-dress3.jpg','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Dress','Light Violet', 'S')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Maroon Dress','https://i.postimg.cc/PqD1WnVf/cocktail-dress2.jpg','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Dress','Maroon', 'M')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Maroon Blouse','https://i.postimg.cc/vBkB344p/women-blouse-maroon.jpg','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Tops','Maroon', 'M')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Maroon Blouse','https://i.postimg.cc/vBkB344p/women-blouse-maroon.jpg','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Tops','Maroon', 'S')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Classy Crop-Top','https://i.postimg.cc/SQrymcBQ/black-croptop-women.jpg','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Tops','Black', 'S')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Nude Classy Pants','https://i.postimg.cc/XvNpJSMD/women-pants1.jpg','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Pants and Skirts','Nude', 'S')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Classy Black Pants','https://i.postimg.cc/Vk8Jx0Kw/women-pants2.jpg','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Pants and Skirts','Black', 'S')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Black and white Check','https://i.postimg.cc/QNKVVJPs/women-skirts2.jpg','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Pants and skirts','Black&White Check', 'S')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('PLain White Skirt','https://i.postimg.cc/j2fj9RNC/women-skirts3.jpg','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Pants and Skirts','White', 'S')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Leather Bag','https://i.postimg.cc/HkdLZDLs/women-bag2.jpg','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Accessory','Black', 'All')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Gold Earrings','https://i.postimg.cc/qBN6yTNP/accessory1.jpg','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Accessory','Gold', 'All')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('White Heels','https://i.postimg.cc/JnG0NNzN/accessory2.jpg','Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Accessory','White', '6+')")

                con.commit()
                msg = str("items added.")
        except Exception as e:
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            return {'msg':msg}


if __name__ =='__main__':
    app.run(debug=True)
