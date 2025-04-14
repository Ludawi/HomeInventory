from flask import Flask, request, Response, jsonify, g, render_template, redirect, send_from_directory
from db import Db

app = Flask(__name__)


@app.teardown_appcontext
def close_connection(exception):
    Db.close_connection(exception)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


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


@app.route('/api')
def db_list():
    # return jsonify(Db.list_items())
    result = Db.list_items()
    if result is None:
        return jsonify({"error": "Resource not found"}), 404
    else:
        return jsonify(result)


@app.route('/api/record', methods=['POST'])
def show_record():  # returns single record by code
    code = None

    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    required_fields = {"code"}

    if not required_fields.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    code = data.get("code")

    result = Db.get_record(code)
    if result is None:
        return jsonify({"error": "Resource not found"}), 404
    else:
        return jsonify(result)


@app.route('/inventory')
def inventory():
    return render_template('inventory.html')


@app.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    required_fields = {"timestamp", "type", "data"}

    if not required_fields.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    return_code = Db.add_item(data)

    return jsonify({
        "message": "Registration successful",
        "received": data
    }), return_code


@app.route('/unregister', methods=['POST'])
def unregister():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    required_fields = {"timestamp", "type", "data"}

    if not required_fields.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    return_code = Db.remove_item(data)

    return jsonify({
        "message": "Unregistration successful",
        "received": data
    }), return_code


if __name__ == '__main__':
    app.run(debug=True)
