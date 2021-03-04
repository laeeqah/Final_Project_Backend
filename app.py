import sqlite3
from flask import Flask, request,jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)


def initialize_database():
    conn = sqlite3.connect('database.db')

    conn.execute('CREATE TABLE if not exists  user(userid integer primary key autoincrement, fullname TEXT not null ,username TEXT not null, email TEXT not null, password TEXT not null)')
    conn.execute('CREATE TABLE if not exists  products(proid integer primary key autoincrement, name TEXT, images TEXT, price TEXT, description TEXT, categories TEXT, color TEXT, size TEXT)')

    print("user table created succesfully")
    print("product table created succesfully")

    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
    print(cur.fetchall())

initialize_database()




def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] =row[idx]
    return d

# REGISTRATION
@app.route('/')
@app.route('/register/', methods=['POST'])
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

@app.route('/add_product/', methods=['POST'])
def add_Product():
    if  request.method == "POST":
        msg = None
        try:
            post_data = request.get_json()
            p_name = post_data['p_name']
            img_links = post_data['img_links']
            p_rice = post_data['p_rice']
            des = post_data['description']
            color = post_data['color']
            size = post_data['size']
            print(p_name,img_links, p_rice, des, color, size)
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES (?, ?, ?, ?)", (p_name, img_links, p_rice, des, color, size))
                con.commit()
                msg = str("Product successfully added.")
        except Exception as e:
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            return {'msg':msg}
# SHOW ALL RECORDS
@app.route('/list-records/', methods=['GET'])
def listUsers():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM user")
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
            post_data = request.get_json()
            username = post_data['username']
            password = post_data['password']
            print(username,password)
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM user ")
                con.commit()
                con.close()
                msg = str("Successfully logged")
        except Exception as e:
            msg = "Error occurred in insert operation: " + str(e)

        finally:
            return jsonify('msg',msg)

# PRODUCTS
@app.route('/')
@app.route('/shop/', methods = ['GET', 'POST'])
def cart():
    if  request.method == "POST":
        msg = None
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                # WOMEN PRODUCTS
                # DRESSES
                cur.execute("INSERT into products(name, images, price, description, categories, color , size) VALUES('Maroon Dress','https://i.postimg.cc/PqD1WnVf/cocktail-dress2.jpg','R800', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Dress','Maroon', 'M')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size)  VALUES('Sparkly Dress','https://i.postimg.cc/dV6VgH7R/cocktail-dress3.jpg','R950', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Dress','Light Violet', 'S')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Maroon Dress','https://i.postimg.cc/PqD1WnVf/cocktail-dress2.jpg','R950', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Dress','Maroon', 'M')")
                # TOPS
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Maroon Blouse','https://i.postimg.cc/vBkB344p/women-blouse-maroon.jpg','R500', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Tops','Maroon', 'M')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Maroon Blouse','https://i.postimg.cc/vBkB344p/women-blouse-maroon.jpg','R500', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Tops','Maroon', 'S')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Classy Crop-Top','https://i.postimg.cc/SQrymcBQ/black-croptop-women.jpg','R300', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Tops','Black', 'S')")
                # PANTS&SKIRTS
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Nude Classy Pants','https://i.postimg.cc/XvNpJSMD/women-pants1.jpg','R300', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Pants and Skirts','Nude', 'S')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Classy Black Pants','https://i.postimg.cc/Vk8Jx0Kw/women-pants2.jpg','R300', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Pants and Skirts','Black', 'S')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Black and white Check','https://i.postimg.cc/QNKVVJPs/women-skirts2.jpg','R200', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Pants and skirts','Black&White Check', 'S')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('PLain White Skirt','https://i.postimg.cc/j2fj9RNC/women-skirts3.jpg','R200', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Pants and Skirts','White', 'S')")
                # ACCESSORY
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Leather Bag','https://i.postimg.cc/HkdLZDLs/women-bag2.jpg','R250', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Accessory','Black', 'All')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Gold Earrings','https://i.postimg.cc/qBN6yTNP/accessory1.jpg','R400', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Accessory','Gold', 'All')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('White Heels','https://i.postimg.cc/JnG0NNzN/accessory2.jpg','R600', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Accessory','White', '6+')")

                # MEN PRODUCTS
                # SHIRTS
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Blue Long sleeve shirt','https://i.postimg.cc/G34z26d2/shirt4.jpg','R300', Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Men Tops','Blue', 'M')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Maroon Shirt','https://i.postimg.cc/jqBcJvSh/men-shirts1.jpg','R400', Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Men Tops','Maroon', 'M')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Blue Short sleeve shirt','https://i.postimg.cc/DysgQsW3/shirt3.jpg','R250', Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Men Tops','Blue', 'M')")
                # PANTS
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Black Pants','https://i.postimg.cc/PqD1WnVf/cocktail-dress2.jpg','R300', Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Pants','Black', 'M')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Black Dress Pants','https://i.postimg.cc/PqD1WnVf/cocktail-dress2.jpg','R400', Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Pants','Black', 'M')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Brown Pants','https://i.postimg.cc/PqD1WnVf/cocktail-dress2.jpg','R300', Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Pants','Black', 'M')")
                # ACCESSORY
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Maroon Dress','https://i.postimg.cc/PqD1WnVf/cocktail-dress2.jpg','R150', Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Accessory','Black', 'All')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Maroon Dress','https://i.postimg.cc/PqD1WnVf/cocktail-dress2.jpg','R50', Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Accessory','Black', 'All')")
                cur.execute("INSERT INTO products(name, images, price, description, categories, color , size) VALUES('Maroon Dress','https://i.postimg.cc/PqD1WnVf/cocktail-dress2.jpg','R150', Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard.', 'Accessory','Brown', 'All')")


                con.commit()
                msg = str("items added.")
        except Exception as e:
            msg = "Error occurred in insert operation: " + str(e)
        finally:
            return {'msg':msg}




@app.route('/list-products/', methods=['GET'])
def listProducts():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("select * from products")
            data = cur.fetchall()
            print(data)

    except Exception as e:
        con.rollback()
        print("Something happened when getting data from db: " + str(e))
    finally:
        con.close()
        return jsonify(data)



# if __name__ =='__main__':
#     app.run(debug=True)
