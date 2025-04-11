from flask import Flask, request, Response, jsonify


app = Flask(__name__)


@app.route('/')
def index():
    return '''
    <html>
        <body>
            <h1>Send new item to /register</h1>
            <p>POST MJPEG video stream to /video</p>
        </body>
    </html>
    '''


app = Flask(__name__)


@app.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    required_fields = {"timestamp", "type", "data"}
    if not required_fields.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    # add more validation here if needed

    return jsonify({
        "message": "Registration successful",
        "received": data
    }), 200


@app.route('/unregister', methods=['POST'])
def unregister():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # Validate the expected keys
    required_fields = {"timestamp", "type", "data"}
    if not required_fields.issubset(data):
        return jsonify({"error": "Missing required fields"}), 400

    return jsonify({
        "message": "Unregistration successful",
        "received": data
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
