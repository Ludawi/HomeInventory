from flask import Flask, request, Response, jsonify, g, render_template
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
    return render_template('index.html')


@app.route('/inventory')
def inventory():
    return render_template('inventory.html')


@app.route('/health')
def health():
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
        'SELECT id, code_type, code, description, item_count, registered_at FROM items')
    rows = cur.fetchall()
    cur.close()

    result = [
        {
            'id': row[0],
            'code_type': row[1],
            'code': row[2],
            'description': row[3],
            'count': row[4],
            'registered_at': row[5]
        }
        for row in rows
    ]

    return jsonify(result)


def item_exists(code):
    db = get_db()
    cur = db.cursor()

    cur.execute('SELECT 1 FROM items WHERE code=? LIMIT 1', (code,))
    result = cur.fetchone()
    print("DB result:", result)
    if result is None:
        db.commit()
        cur.close()
        return False
    else:
        cur.execute(
            'SELECT item_count FROM items WHERE code=? LIMIT 1', (code,))
        result = cur.fetchone()

    if result is None:
        db.commit()
        cur.close()
        return False
    else:
        return result[0]


def add_count(code, amount, timestamp):

    count = amount + 1
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        UPDATE items
        SET item_count=?, timestamp=?
        WHERE code=?
    ''', (count, timestamp, code,))

    db.commit()
    cur.close()
    return 200


def add_item(item):

    code_type = item.get("type")
    code = item.get("data")
    timestamp_iso = datetime.strptime(
        item.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%fZ")
    timestamp = timestamp_iso.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    amount = item_exists(code)
    if amount == None:
        # Create new entry
        db = get_db()
        cur = db.cursor()
        cur.execute('''
            INSERT INTO items (code_type, code, timestamp, item_count)
            VALUES (?, ?, ?, ?)
        ''', (code_type, code, timestamp, 1))

        db.commit()
        cur.close()
        return 201
    else:
        add_count(code, amount, timestamp)
        return 200


@app.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    required_fields = {"timestamp", "type", "data"}
    if not required_fields.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    return_code = add_item(data)

    return jsonify({
        "message": "Registration successful",
        "received": data
    }), return_code


def substract_count(code, amount, timestamp):

    count = amount - 1
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        UPDATE items
        SET item_count=?, timestamp=?
        WHERE code=?
    ''', (count, timestamp, code,))

    db.commit()
    cur.close()
    return 200


def remove_item(item):

    code = item.get("data")
    timestamp_iso = datetime.strptime(
        item.get("timestamp"), "%Y-%m-%dT%H:%M:%S.%fZ")
    timestamp = timestamp_iso.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    amount = item_exists(code)

    if amount == None or amount <= 0:
        return 304
    else:
        substract_count(code, amount, timestamp)
        return 200


@app.route('/unregister', methods=['POST'])
def unregister():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # Validation
    required_fields = {"timestamp", "type", "data"}
    if not required_fields.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    return_code = remove_item(data)

    return jsonify({
        "message": "Unregistration successful",
        "received": data
    }), return_code


if __name__ == '__main__':
    app.run(debug=True)
