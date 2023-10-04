import json
import psycopg2
import logging
import configparser

# Get VAT rate based on product type
def get_vat_rate(product_type):
    """
    Get VAT rate based on product type.

    Args:
        product_type (str): Type of the product.

    Returns:
        float: VAT rate as a decimal.
    """
    vat_rates = {
        'hot food': 0.15,     # 15% VAT
        'cold food': 0.07,    # 7% VAT
        'beverage': 0.09      # 9% VAT
    }
    return vat_rates.get(product_type, 0.0)

# Calculate net merchandise value based on VAT rates
def calculate_net_merchandise_value(basket):
    """
    Calculate net merchandise value based on VAT rates.

    Args:
        basket (list): List of items in the basket.

    Returns:
        float: Total net merchandise value.
    """
    total_net_value = 0.0
    for item in basket:
        vat_rate = get_vat_rate(item['productType'])
        net_value = item['grossMerchandiseValueEur'] * (1 - vat_rate)
        total_net_value += net_value
    return round(total_net_value, 2)

# Load JSON data from file
def load_data_from_json(file_path):
    """
    Load JSON data from a file.

    Args:
        file_path (str): Path to the JSON data file.

    Returns:
        list: List of JSON data entries.
    """
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

# Process the data and return processed data
def process_data(data):
    """
    Process JSON data and return processed data.

    Args:
        data (list): List of JSON data entries.

    Returns:
        list: Processed data entries.
    """
    processed_data = []
    for entry in data:
        customer_id = entry['customerId']
        for order in entry['orders']:
            order_id = order['orderId']
            net_value = calculate_net_merchandise_value(order['basket'])
            processed_data.append({
                'customerId': customer_id,
                'orderId': order_id,
                'netMerchandiseValueEur': net_value
            })
    return processed_data

# Establish PostgreSQL connection
def connect_to_postgres():
    """
    Establish a connection to PostgreSQL.

    Returns:
        psycopg2.extensions.connection: PostgreSQL database connection.
    """
    try:
        connection = psycopg2.connect(
            host=HOST, 
            database=DATABASE,
            user=USER,
            password=PASSWORD,
            port=PORT,
        )
        return connection
    except Exception as e:
        logging.error(f"Error connecting to PostgreSQL: {e}")
        raise 

# Store the processed data in PostgreSQL
def insert_data_into_postgres(connection, data):
    """
    Insert processed data into PostgreSQL.

    Args:
        connection (psycopg2.extensions.connection): PostgreSQL database connection.
        data (list): List of processed data entries.
    """    
    try:
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS merchandise (
            customerId TEXT,
            orderId TEXT,
            netMerchandiseValueEur DECIMAL(10, 2)
        )
        """)

        for item in data:
            cursor.execute("""
            INSERT INTO merchandise (customerId, orderId, netMerchandiseValueEur)
            VALUES (%s, %s, %s)
            """, (item['customerId'], item['orderId'], item['netMerchandiseValueEur']))

        connection.commit()
    except Exception as e:
        logging.error(f"Error inserting data into PostgreSQL: {e}")
        raise
    finally:
        cursor.close()


if __name__ == "__main__":

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

    # File Paths
    FILE_PATH = config['FILE_PATH']['data_file']
    ETL_LOG_FILE = config['FILE_PATH']['etl_log_file']

    # Configure logging
    logging.basicConfig(filename=ETL_LOG_FILE, level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Initialize db_connection
    db_connection = None

    try:
        # Load JSON data
        json_data = load_data_from_json(FILE_PATH)

        # Process data
        processed_data = process_data(json_data)

        # Establish PostgreSQL connection
        db_connection = connect_to_postgres()

        # Insert data into PostgreSQL
        insert_data_into_postgres(db_connection, processed_data)
        logging.info("Data Entered in Database Successfully!")
    except Exception as e:
        logging.error(f"ETL process failed: {e}")
    finally:
        if db_connection:
            db_connection.close()
        
# docker exec -it postgres bash
# psql -h localhost -U myuser -d mydb
# SELECT * FROM merchandise;

