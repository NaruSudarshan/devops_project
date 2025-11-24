from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/submit', methods=['POST'])
def submit_form():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    if not name or not email:
        return jsonify({'error': 'Name and Email are required'}), 400

    print(f"Received submission: Name={name}, Email={email}, Message={message}")
    
    # In a real app, you might save this to a database
    return jsonify({'message': 'Form submitted successfully!', 'data': {'name': name, 'email': email, 'message': message}}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
