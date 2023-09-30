from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Function to fetch data from PostgreSQL
def get_data_from_postgres(customer_id):
    try:
        connection = psycopg2.connect(
            host="postgres",  # Docker container name
            database="mydb",
            user="myuser",
            password="mypassword"
        )

        cursor = connection.cursor()

        # Execute SQL query to fetch data for the specified customer_id
        cursor.execute("""
        SELECT customerid, orderid, netmerchandisevalueeur
        FROM merchandise
        WHERE customerid = %s
        """, (customer_id,))

        data = cursor.fetchall()

        return data

    except Exception as e:
        return None
    finally:
        cursor.close()
        connection.close()

@app.route('/spend/<string:customer_id>', methods=['GET'])
def get_customer_spend(customer_id):
    data = get_data_from_postgres(customer_id)
    if data is not None:
        response = {
            "customerId": customer_id,
            "orders": len(data),
            "totalNetMerchandiseValueEur": float(sum(row[2] for row in data))
        }
        return jsonify(response), 200
    else:
        return jsonify({"error": "Customer data not found"}), 404

if __name__ == '__main__':
    print("Before running")
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
    print("After running")
