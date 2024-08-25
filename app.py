from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bfhl', methods=['POST', 'GET'])
def bfhl():
    if request.method == 'POST':
        try:
            # Log the received JSON
            print("Received JSON data:", request.json)

            # Ensure request.json is not None
            if request.json is None:
                raise ValueError("Request JSON is None")

            # Retrieve user-defined data from the request, with defaults if not provided
            user_id = request.json.get('user_id', 'default_user_id')
            email = request.json.get('email', 'default_email@example.com')
            roll_number = request.json.get('roll_number', 'DEFAULT123')
            
            # Retrieve the main data to process
            data = request.json.get('data', [])
            if not isinstance(data, list):
                raise ValueError("Data should be a list")

            numbers = [x for x in data if x.isdigit()]
            alphabets = [x for x in data if x.isalpha()]
            highest_lowercase = max([x for x in alphabets if x.islower()], default=None)

            # Prepare the response
            response = {
                "is_success": True,
                "user_id": user_id,
                "email": email,
                "roll_number": roll_number,
                "numbers": numbers,
                "alphabets": alphabets,
                "highest_lowercase_alphabet": [highest_lowercase] if highest_lowercase else []
            }
            return jsonify(response), 200
        except Exception as e:
            print(f"Error: {str(e)}")  # Log the error
            return jsonify({"is_success": False, "error": str(e)}), 400

    elif request.method == 'GET':
        return jsonify({"operation_code": 1}), 200

if __name__ == '__main__':
    app.run(debug=True)

