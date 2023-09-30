import json
import psycopg2
import logging

# Configure logging
logging.basicConfig(filename='./logs/etl.log', level=logging.INFO)

# Load JSON data from file
def load_data_from_json(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            data.append(json.loads(line))
    return data

# Process the data and return processed data
def process_data(data):
    processed_data = []
    for entry in data:
        customer_id = entry['customerId']
        for order in entry['orders']:
            order_id = order['orderId']
            net_value = sum(item['grossMerchandiseValueEur'] * 0.93 if item['productType'] == 'beverage' else
                            item['grossMerchandiseValueEur'] * 0.85 if item['productType'] == 'hot food' else
                            item['grossMerchandiseValueEur'] for item in order['basket'])
            processed_data.append({
                'customerId': customer_id,
                'orderId': order_id,
                'netMerchandiseValueEur': net_value
            })
    return processed_data

# Establish PostgreSQL connection
def connect_to_postgres():
    try:
        connection = psycopg2.connect(
            host="postgres",  # Docker container name
            database="mydb",
            user="myuser",
            password="mypassword",
            port="5432"
        )
        return connection
    except Exception as e:
        logging.error(f"Error connecting to PostgreSQL: {e}")
        raise

# Store the processed data in PostgreSQL
def insert_data_into_postgres(connection, data):
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
    print("Before loading Json")
    json_data = load_data_from_json('./resources/data.json')
    print("Before processing Json")
    processed_data = process_data(json_data)
    print("Before database connectionnnnn")
    # Establish PostgreSQL connection
    db_connection = connect_to_postgres()
    print("Before insertinggggggg data")
    try:
        # Insert data into PostgreSQL
        insert_data_into_postgres(db_connection, processed_data)
    except Exception as e:
        logging.error(f"ETL process failed: {e}")
    finally:
        db_connection.close()
    print("Operation done")
# docker exec -it postgres bash
# psql -h localhost -U myuser -d mydb
# SELECT * FROM merchandise;

