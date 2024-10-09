import mysql.connector
from flask import Flask, request, jsonify, make_response, url_for
from settings import *

# configure database
config = {
  'user': DB_USER,
  'password': DB_PASS,
  'database': 'products',
}
db_connection = mysql.connector.connect(**config)
cursor = db_connection.cursor(dictionary=True)

cursor.execute("CREATE TABLE IF NOT EXISTS products ( \
        id INT unsigned NOT NULL AUTO_INCREMENT, \
        name             VARCHAR(150) NOT NULL, \
        description      VARCHAR(150) NOT NULL, \
        version          INT, \
        PRIMARY KEY (id) \
        );")


app = Flask(__name__)


@app.route("/")
@app.route("/<name>")
def index(name=None):
    if name:
        return f"<h1>Hello, {name}</h1>"
    else:
        return "<h1>Hello, World</h1>"


@app.route("/products/<id>", methods=["GET", "PUT", "DELETE"])
def products_id(id):
    if request.method == "GET":             # get a resourse
        cursor.execute("SELECT * FROM products WHERE id=%s;", params=(id,))
        return jsonify(cursor.fetchone())
    
    elif request.method == "PUT":
        pass

    elif request.method == "DELETE":        # delete a resourse
        cursor.execute("DELETE FROM products WHERE id = %s;", params=(id,))
        return make_response("", 204)
    


@app.route("/products/", methods=["GET", "POST", "OPTIONS"])
def products():
    
    if request.method == "GET":             # get all resourses
        cursor.execute("SELECT * FROM products;")
        print(cursor)
        return jsonify(cursor.fetchall()), 200
    
    elif request.method == "POST":          # create a resourse
        data = request.get_json()
        name = data['name']
        desc = data['description']
        ver = data['version']

        cursor.execute("INSERT INTO products (name, description, version) VALUES (%s, %s, %s);", \
                        params=(name, desc, ver))
        cursor.execute("SELECT * FROM products WHERE name=%s AND description=%s AND version=%s;", \
                        params=(name, desc, ver))
        query = cursor.fetchone()
        id = query['id']
        print(f"Created product id: {id}")
        response = jsonify(dict(location='YET NONE', product=query))
        return response, 201
