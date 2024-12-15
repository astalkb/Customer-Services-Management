import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from flask_jwt_extended import create_access_token
from unittest.mock import patch, MagicMock
from unittest import mock
import pytest
from werkzeug.security import generate_password_hash

# Temporary user store for testing
temp_users = {}

def load_users():
    """Load users from the temporary store for testing."""
    return temp_users

def save_users(users):
    """Save users to the temporary store for testing."""
    global temp_users
    temp_users = users

def mock_jwt_required(*args, **kwargs):
    pass

@pytest.fixture
def client():
    """Set up a test client and mock MySQL."""
    app.config["TESTING"] = True
    app.config["DEBUG"] = True
    app.config["DISABLE_BLACKLIST_CHECK"] = True

    with patch("mysql.connector") as mock_mysql:
        mock_cursor = MagicMock()
        mock_mysql.connect.return_value.cursor.return_value = mock_cursor

        with mock.patch('flask_jwt_extended.view_decorators.jwt_required', side_effect=mock_jwt_required):
            with app.app_context():
                yield app.test_client(), mock_mysql

    # Clear temp_users after each test
    temp_users.clear()

def generate_token(identity, role):
    return create_access_token(identity=identity, additional_claims={"role": role, "username": identity})

def setup_mock_db(mock_mysql, query_result=None, rowcount=0, side_effect=None):
    mock_cursor = mock_mysql.connect.return_value.cursor.return_value
    mock_cursor.fetchall.return_value = query_result or []
    mock_cursor.rowcount = rowcount
    if side_effect:
        mock_cursor.execute.side_effect = side_effect
    else:
        mock_cursor.execute.side_effect = lambda query, params=None: None

# Load users from the JSON file for authentication
users = load_users()



# AUTHENTICATION TESTING 
def test_register_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=0)

    # Ensure the testuser does not already exist
    if "testuser" in temp_users:
        del temp_users["testuser"]

    response = client.post(
        "/register",
        json={"username": "testuser", "password": "password123", "role": "admin"},
    )

    assert response.status_code == 201
    assert "User registered successfully" in response.get_json()["message"]
    print("test_register_success: Passed")

def test_login_success(client):
    client, mock_mysql = client
    hashed_password = generate_password_hash("password123")
    temp_users["testuser"] = {"password": hashed_password, "role": "admin"}

    response = client.post(
        "/login",
        json={"username": "testuser", "password": "password123"},
    )

    assert response.status_code == 200
    assert "token" in response.get_json()
    print("test_login_success: Passed")



#CRUD ROUTES TESTING
# Addresses
def test_get_addresses_success(client):
    client, mock_mysql = client
    addresses = [
        {"address_id": 1, "number_building": "123", "street": "Main St", "city": "Anytown", "zip_postcode": "12345", "state_province_county": "State", "country": "Country"},
        {"address_id": 2, "number_building": "456", "street": "Second St", "city": "Othertown", "zip_postcode": "67890", "state_province_county": "State", "country": "Country"},
    ]
    setup_mock_db(mock_mysql, query_result=addresses)

    response = client.get("/addresses")
    assert response.status_code == 200
    assert len(response.get_json()) == len(addresses)
    print("test_get_addresses_success: Passed")

def test_add_address_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=0)

    response = client.post(
        "/addresses",
        json={"number_building": "123", "street": "Main St", "city": "Anytown", "zip_postcode": "12345", "state_province_county": "State", "country": "Country"},
        headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"}
    )

    assert response.status_code == 201
    assert "Address added successfully" in response.get_json()["message"]
    print("test_add_address_success: Passed")

def test_update_address_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.put(
        "/addresses/1",
        json={"number_building": "789", "street": "Updated St", "city": "Updatedtown", "zip_postcode": "54321", "state_province_county": "Updated State", "country": "Updated Country"},
        headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"}
    )

    assert response.status_code == 200
    assert "Address updated successfully" in response.get_json()["message"]
    print("test_update_address_success: Passed")

def test_delete_address_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.delete("/addresses/1", headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert "Address deleted successfully" in response.get_json()["message"]
    print("test_delete_address_success: Passed")


# Customers
def test_get_customers_success(client):
    client, mock_mysql = client
    customers = [
        {"customer_id": 1, "address_id": 1, "customer_name": "John Doe", "customer_phone": "1234567890", "customer_email": "john@example.com"},
        {"customer_id": 2, "address_id": 2, "customer_name": "Jane Smith", "customer_phone": "0987654321", "customer_email": "jane@example.com"},
    ]
    setup_mock_db(mock_mysql, query_result=customers)

    response = client.get("/customers")
    assert response.status_code == 200
    assert len(response.get_json()) == len(customers)
    print("test_get_customers_success: Passed")

def test_add_customer_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=0)

    response = client.post(
        "/customers",
        json={"address_id": 1, "customer_name": "John Doe", "customer_phone": "1234567890", "customer_email": "john@example.com"},
        headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"}
    )

    assert response.status_code == 201
    assert "Customer added successfully" in response.get_json()["message"]
    print("test_add_customer_success: Passed")

def test_update_customer_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.put(
        "/customers/1",
        json={"address_id": 1, "customer_name": "John Updated", "customer_phone": "1234567890", "customer_email": "john_updated@example.com"},
        headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"}
    )

    assert response.status_code == 200
    assert "Customer updated successfully" in response.get_json()["message"]
    print("test_update_customer_success: Passed")

def test_delete_customer_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.delete("/customers/1", headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert "Customer deleted successfully" in response.get_json()["message"]
    print("test_delete_customer_success: Passed")


# Orders
def test_get_orders_success(client):
    client, mock_mysql = client
    orders = [
        {"order_id": 1, "customer_id": 1, "order_status": "Pending", "order_date": "2024-01-01", "start_date": "2024-01-02", "end_date": "2024-01-03"},
        {"order_id": 2, "customer_id": 2, "order_status": "Completed", "order_date": "2024-01-04", "start_date": "2024-01-05", "end_date": "2024-01-06"},
    ]
    setup_mock_db(mock_mysql, query_result=orders)

    response = client.get("/orders")
    assert response.status_code == 200
    assert len(response.get_json()) == len(orders)
    print("test_get_orders_success: Passed")

def test_add_order_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=0)

    response = client.post(
        "/orders",
        json={"customer_id": 1, "order_status": "Pending", "order_date": "2024-01-01", "start_date": "2024-01-02", "end_date": "2024-01-03"},
        headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"}
    )

    assert response.status_code == 201
    assert "Order added successfully" in response.get_json()["message"]
    print("test_add_order_success: Passed")

def test_update_order_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.put(
        "/orders/1",
        json={"customer_id": 1, "order_status": "Completed", "order_date": "2024-01-01", "start_date": "2024-01-02", "end_date": "2024-01-03"},
        headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"}
    )

    assert response.status_code == 200
    assert "Order updated successfully" in response.get_json()["message"]
    print("test_update_order_success: Passed")

def test_delete_order_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.delete("/orders/1", headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert "Order deleted successfully" in response.get_json()["message"]
    print("test_delete_order_success: Passed")


# Order Items
def test_get_order_items_success(client):
    client, mock_mysql = client
    order_items = [
        {"order_item_id": 1, "order_id": 1, "service_id": 1, "order_quantity": 2, "monthly_payment_amount": 100.0, "monthly_payment_date": "2024-01-01"},
        {"order_item_id": 2, "order_id": 2, "service_id": 2, "order_quantity": 1, "monthly_payment_amount": 50.0, "monthly_payment_date": "2024-01-02"},
    ]
    setup_mock_db(mock_mysql, query_result=order_items)

    response = client.get("/order_items")
    assert response.status_code == 200
    assert len(response.get_json()) == len(order_items)
    print("test_get_order_items_success: Passed")

def test_add_order_item_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=0)

    response = client.post(
        "/order_items",
        json={"order_id": 1, "service_id": 1, "order_quantity": 2, "monthly_payment_amount": 100.0, "monthly_payment_date": "2024-01-01"},
        headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"}
    )

    assert response.status_code == 201
    assert "Order item added successfully" in response.get_json()["message"]
    print("test_add_order_item_success: Passed")

def test_update_order_item_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.put(
        "/order_items/1",
        json={"order_id": 1, "service_id": 1, "order_quantity": 3, "monthly_payment_amount": 150.0, "monthly_payment_date": "2024-01-01"},
        headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"}
    )

    assert response.status_code == 200
    assert "Order item updated successfully" in response.get_json()["message"]
    print("test_update_order_item_success: Passed")

def test_delete_order_item_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.delete("/order_items/1", headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert "Order item deleted successfully" in response.get_json()["message"]
    print("test_delete_order_item_success: Passed")


# Payments
def test_get_payments_success(client):
    client, mock_mysql = client
    payments = [
        {"payment_id": 1, "order_id": 1, "payment_date": "2024-01-01", "payment_amount": 100.0, "payment_method": "Credit Card", "transaction_reference": "ABC123"},
        {"payment_id": 2, "order_id": 2, "payment_date": "2024-01-02", "payment_amount": 50.0, "payment_method": "PayPal", "transaction_reference": "XYZ456"},
    ]
    setup_mock_db(mock_mysql, query_result=payments)

    response = client.get("/payments")
    assert response.status_code == 200
    assert len(response.get_json()) == len(payments)
    print("test_get_payments_success: Passed")

def test_add_payment_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=0)

    response = client.post(
        "/payments",
        json={"order_id": 1, "payment_date": "2024-01-01", "payment_amount": 100.0, "payment_method": "Credit Card", "transaction_reference": "ABC123"},
        headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"}
    )

    assert response.status_code == 201
    assert "Payment added successfully" in response.get_json()["message"]
    print("test_add_payment_success: Passed")

def test_update_payment_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.put(
        "/payments/1",
        json={"order_id": 1, "payment_date": "2024-01-01", "payment_amount": 150.0, "payment_method": "Credit Card", "transaction_reference": "ABC123"},
        headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"}
    )

    assert response.status_code == 200
    assert "Payment updated successfully" in response.get_json()["message"]
    print("test_update_payment_success: Passed")

def test_delete_payment_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.delete("/payments/1", headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert "Payment deleted successfully" in response.get_json()["message"]
    print("test_delete_payment_success: Passed")


# Services
def test_get_services_success(client):
    client, mock_mysql = client
    services = [
        {"service_id": 1, "service_name": "Haircut", "price_per_period": 20.0},
        {"service_id": 2, "service_name": "Shampoo", "price_per_period": 10.0},
    ]
    setup_mock_db(mock_mysql, query_result=services)

    response = client.get("/services")
    assert response.status_code == 200
    assert len(response.get_json()) == len(services)
    print("test_get_services_success: Passed")

def test_add_service_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=0)

    response = client.post(
        "/services",
        json={"service_name": "Haircut", "price_per_period": 20.0},
        headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"}
    )

    assert response.status_code == 201
    assert "Service added successfully" in response.get_json()["message"]
    print("test_add_service_success: Passed")

def test_update_service_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.put(
        "/services/1",
        json={"service_name": "Haircut Deluxe", "price_per_period": 25.0},
        headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"}
    )

    assert response.status_code == 200
    assert "Service updated successfully" in response.get_json()["message"]
    print("test_update_service_success: Passed")

def test_delete_service_success(client):
    client, mock_mysql = client
    setup_mock_db(mock_mysql, rowcount=1)

    response = client.delete("/services/1", headers={"Authorization": f"Bearer {generate_token('testuser', 'admin')}"})
    assert response.status_code == 200
    assert "Service deleted successfully" in response.get_json()["message"]
    print("test_delete_service_success: Passed")
