import pytest
import requests

# API base URL (assuming your API container is running locally)
BASE_URL = 'http://localhost:8080'

def test_get_customer_data():
    # Make a GET request to the API endpoint
    response = requests.get(f'{BASE_URL}/spend/5b6950c008c899c1a4caf2a1')
    
    # Check the HTTP status code and response content
    assert response.status_code == 200
    data = response.json()
    assert data['customerId'] == '5b6950c008c899c1a4caf2a1'
    assert data['orders'] == 5
    assert data['totalNetMerchandiseValueEur'] == 88.65

def test_get_customer_data_no_id():
    # Make a GET request to the API endpoint without a customer_id
    response = requests.get(f'{BASE_URL}/spend')
    
    # Check the HTTP status code and response content
    assert response.status_code == 400
    data = response.json()
    assert data['error'] == 'Customer ID is required'

def test_get_customer_data_not_found():
    # Make a GET request to the API endpoint with a customer_id that does not exist
    response = requests.get(f'{BASE_URL}/spend/2')
    
    # Check the HTTP status code and response content
    assert response.status_code == 404
    data = response.json()
    assert data['error'] == 'Customer data not found'

if __name__ == '__main__':
    pytest.main()

