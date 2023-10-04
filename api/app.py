from flask import Flask, request, jsonify
from flask_restful import Api
import psycopg2
from flasgger.utils import swag_from
import logging
import configparser

# Initialize Flask application
app = Flask(__name__)
api = Api(app)

# Configure logging
logging.basicConfig(filename='api.log', level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a configuration object
config = configparser.ConfigParser()

# Load the configuration file using a relative path
config.read('config.ini') 

# Access variables from the configuration file
HOST = config['Database']['host']
DATABASE = config['Database']['database']
USER = config['Database']['user']
PASSWORD = config['Database']['password']
PORT = config['Database']['port']

# Function to fetch data from PostgreSQL
def get_data_from_postgres(customer_id):
    """
    Fetch data from PostgreSQL for a specific customer.

    Args:
        customer_id (str): Customer ID to fetch data for.

    Returns:
        list: List of data rows for the customer.
    """    
    try:
        connection = psycopg2.connect(
            host=HOST,  # Docker container name
            database=DATABASE,
            user=USER,
            password=PASSWORD
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

# Decorate the route with Swagger documentation
@swag_from('api_doc.yml')
@app.route('/spend/<string:customer_id>', methods=['GET'])
def get_spend(customer_id):
    try:
        if not customer_id:
            return {"error": "Customer ID is required"}, 400

        data = get_data_from_postgres(customer_id)
        if data is not None:
            response = {
                "customerId": customer_id,
                "orders": len(data),
                "totalNetMerchandiseValueEur": float(sum(row[2] for row in data))
            }
            return response, 200
        else:
            return {"error": "Customer data not found"}, 404
    except Exception as e:
        return {"error": str(e)}, 500

# Entry point for running the Flask application
if __name__ == '__main__':
    try:
        # Enable debugging mode for development
        app.debug = True
        app.run(host='0.0.0.0', port=8080)
    except Exception as e:
        logger.error(f"Error starting Flask app: {e}")

# http://localhost:8080/spend/5b6950c008c899c1a4caf2a1