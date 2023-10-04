import os
import pytest
import sys
import configparser

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from etl.etl import load_data_from_json, process_data, calculate_net_merchandise_value

# Get the directory of the current script
current_dir = os.path.dirname(__file__)
print(f"current_dir {current_dir}")

# Construct the absolute path to config.ini using the current script's directory
config_path = ("./config.ini")

# Load the configuration file
config = configparser.ConfigParser()
config.read(config_path)

FILE_PATH = config['FILE_PATH']['test_data_file']

# Test the existence of the data file
def test_data_file_existence():
    assert os.path.exists(FILE_PATH)

# Define test functions
def test_load_data_from_json():
    # Test if the function successfully loads JSON data
    data = load_data_from_json(FILE_PATH)
    assert isinstance(data, list)
    assert len(data) > 0
    assert isinstance(data[0], dict)

# Test the calculation of net merchandise value
@pytest.mark.parametrize(
    "product_type, gross_value, expected_net_value",
    [
        ("hot food", 10.24, 10.24 * 0.85),  # 15% VAT
        ("cold food", 10.21, 10.21 * 0.93),  # 7% VAT
        ("beverage", 10.28, 10.28 * 0.91),  # 9% VAT
    ],
)
def test_calculate_net_merchandise_value(product_type, gross_value, expected_net_value):
    net_value = calculate_net_merchandise_value([{"productType": product_type, "grossMerchandiseValueEur": gross_value}])
    assert net_value == pytest.approx(expected_net_value, rel=1e-2)  

# Test data processing
def test_process_data():
    # Load JSON data
    json_data = load_data_from_json(FILE_PATH)

    # Process data
    processed_data = process_data(json_data)
    assert len(processed_data) == 5  

    # Check if processed data has the expected keys
    for item in processed_data:
        assert "customerId" in item
        assert "orderId" in item
        assert "netMerchandiseValueEur" in item