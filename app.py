from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Define the HTML as a string
html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BFHL API Frontend</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            padding: 0;
        }
        input[type="text"], input[type="email"], input[type="number"] {
            width: 300px;
            padding: 10px;
            margin-bottom: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        input[readonly] {
            background-color: #e9ecef;
            cursor: not-allowed;
        }
        button {
            padding: 10px 20px;
            background-color: #28a745;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #218838;
        }
        pre {
            background-color: #f8f9fa;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
    </style>
</head>
<body>
    <h1>BFHL API Frontend</h1>

    <label for="user_id">User ID:</label><br>
    <input type="text" id="user_id" placeholder="Enter your user ID"><br>

    <label for="email">Email:</label><br>
    <input type="email" id="email" placeholder="Enter your email"><br>

    <label for="roll_number">Roll Number:</label><br>
    <input type="text" id="roll_number" placeholder="Enter your roll number"><br>

    <label for="json-input">Data (JSON format):</label><br>
    <input type="text" id="json-input" value='{"data":["A","B","c","1","2"]}' readonly><br>

    <button onclick="submitData()">Submit</button>

    <h3>Response:</h3>
    <pre id="response"></pre>

    <script>
        function submitData() {
            const user_id = document.getElementById('user_id').value || "default_user_id";
            const email = document.getElementById('email').value || "default_email@example.com";
            const roll_number = document.getElementById('roll_number').value || "DEFAULT123";
            const input = document.getElementById('json-input').value;
            
            try {
                const jsonData = JSON.parse(input);
                jsonData.user_id = user_id;
                jsonData.email = email;
                jsonData.roll_number = roll_number;

                console.log('Sending JSON data:', jsonData);  // Log the data being sent

                fetch('/bfhl', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(jsonData),
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('response').textContent = JSON.stringify(data, null, 2);
                })
                .catch(error => {
                    console.error('Error:', error);
                    document.getElementById('response').textContent = 'Error sending data. Check the console for details.';
                });
            } catch (error) {
                console.error('Invalid JSON:', error);
                document.getElementById('response').textContent = 'Invalid JSON input. Check the console for details.';
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_content)

@app.route('/bfhl', methods=['POST', 'GET'])
def bfhl():
    if request.method == 'POST':
        try:
            # Log the received JSON
            print("Received JSON data:", request.json)

            # Retrieve user-defined data from the request, with defaults if not provided
            user_id = request.json.get('user_id', 'default_user_id')
            email = request.json.get('email', 'default_email@example.com')
            roll_number = request.json.get('roll_number', 'DEFAULT123')
            
            # Retrieve the main data to process
            data = request.json.get('data', [])
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
            return jsonify({"is_success": False, "error": str(e)}), 400

    elif request.method == 'GET':
        return jsonify({"operation_code": 1}), 200

if __name__ == '__main__':
    app.run(debug=True)
