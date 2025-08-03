from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",  # Remove ":3306"
    user="root",
    password="",
    database=""
)
cursor = conn.cursor()


@app.route('/')
def index():
    return render_template('index.html')

# Route to insert data 
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    print(f"Received data: {data}")

    if not data:
        return jsonify({"message": "No data recieved!"}), 400
    

    name = data['name']
    email = data['email']
    phone = data['phone']
    address = data['address']
    cityState = data['cityState']
    zip = data['zip']
    package = data['package']
    details = data['details']


    try:
        # New connection to make sure no time out during data transport
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database=""
        )
        cursor = conn.cursor()

        # Insert into MySQL
        cursor.execute("INSERT INTO Customer (name, email, phone, address, cityState, zip, package, details) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                        (name, email, phone, address, cityState, zip, package, details))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Data inserted successfully!"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  
