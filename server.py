from os import remove
from flask import Flask, request, Response, jsonify, g
import sqlite3
from datetime import datetime


app = Flask(__name__)

DATABASE = './db/database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h1>BARCODE and QRCODE based inventory</h1>
            <p>POST code data to /register</p>
            <p>POST code data to /unregister</p>
        </body>
    </html>
    '''


@app.route('/db')
def db_list():
    db = get_db()
    cur = db.cursor()
    cur.execute(
        'SELECT id, code_type, code, description, registered_at FROM items')
    rows = cur.fetchall()
    cur.close()

    result = [
        {
            'id': row[0],
            'code_type': row[1],
            'code': row[2],
            'description': row[3],
            'registered_at': row[4]
        }
        for row in rows
    ]

    return jsonify(result)


def get_amount(code):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT count(*) FROM items WHERE code=?', (code,))
    count = cur.fetchone()
    cur.close()
    count: int
    return count


def add_item(item):

    code_type = item.get("type")
    code = item.get("data")
    timestamp_iso = datetime.strptime(
        item.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%fZ")
    timestamp = timestamp_iso.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

    print("There are", get_amount(code), "of this")

    db = get_db()
    cur = db.cursor()
    cur.execute('''
        INSERT INTO items (code_type, code, timestamp)
        VALUES (?, ?, ?)
    ''', (code_type, code, timestamp))

    db.commit()
    cur.close()


def remove_item(item):
    return 'not yet'


@app.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    required_fields = {"timestamp", "type", "data"}
    if not required_fields.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    add_item(data)

    return jsonify({
        "message": "Registration successful",
        "received": data
    }), 200


@app.route('/unregister', methods=['POST'])
def unregister():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # Validation
    required_fields = {"timestamp", "type", "data"}
    if not required_fields.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    remove_item(data)

    return jsonify({
        "message": "Unregistration successful",
        "received": data
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
