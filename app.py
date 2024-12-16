from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager, create_access_token
import mysql.connector
import json
import jwt
from werkzeug.security import check_password_hash, generate_password_hash, check_password_hash
from functools import wraps
import datetime
import logging
from decimal import Decimal


app = Flask(__name__)
app.config['SECRET_KEY'] = "keinth123"
app.config['TESTING'] = False

# Initialize JWTManager
jwt_manager = JWTManager(app)

auth = HTTPBasicAuth()
USER_DATA_FILE = "users.json"

# Database Connection Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'elective'
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    """Execute a database query with optional parameters"""
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = cursor.rowcount
        
        cursor.close()
        connection.close()
        return result
    except mysql.connector.Error as e:
        logging.error(f"Database error: {e}")
        if connection:
            connection.close()
        return None
    

def load_users():
    """Load users from JSON file or return an empty dict if in testing mode"""
    if app.config['TESTING']:
        return {}
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    """Save users to JSON file only if not in testing mode"""
    if app.config['TESTING']:
        return
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file)

users = load_users()


@auth.verify_password
def verify_password(username, password):
    """Verify user password"""
    if username in users and check_password_hash(users[username]['password'], password):
        return username

def generate_token(identity, role):
    return create_access_token(identity=identity, additional_claims={"role": role, "username": identity})


def token_required(f):
    """Decorator to require JWT token for route access"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        
        if not token:
            logging.warning("Token is missing")
            return jsonify({"error": "Token is missing"}), 401

        # Extract the token from the "Bearer" prefix
        token = token.split(" ")[1] if " " in token else token

        try:
            decoded_token = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            request.username = decoded_token["username"]
            logging.debug(f"Decoded token: {decoded_token}")
        except jwt.ExpiredSignatureError:
            logging.warning("Token has expired")
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError as e:
            logging.error(f"Invalid token: {e}")
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return wrapper

def role_required(required_roles):
    """Decorator for role-based access control"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            username = getattr(request, "username", None)
            user_role = users.get(username, {}).get("role")
            if not user_role or user_role not in required_roles:
                return jsonify({"error": "Access forbidden: insufficient permissions"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

# Register Route
@app.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "admin")

    if username in users:
        return jsonify({"error": "User already exists"}), 400

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Hash the password and save the user
    hashed_password = generate_password_hash(password)
    users[username] = {"password": hashed_password, "role": role}
    save_users(users)

    return jsonify({"message": "User registered successfully"}), 201

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Login Route
@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    if username not in users or not check_password_hash(users[username]['password'], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(username, users[username]['role'])
    return jsonify({"token": token}), 200


# CRUD operations for Addresses
@app.route("/addresses", methods=["GET"])
def get_all_addresses():
    query = "SELECT * FROM addresses"
    addresses = execute_query(query, fetch=True)
    
    if not addresses:
        return jsonify({"error": "No addresses found"}), 404
    
    formatted_addresses = [
        {
            "address_id": address["address_id"],
            "number_building": address["number_building"],
            "street": address["street"],
            "city": address["city"],
            "zip_postcode": address["zip_postcode"],
            "state_province_county": address["state_province_county"],
            "country": address["country"]
        }
        for address in addresses
    ]
    return app.response_class(
        response=json.dumps(formatted_addresses, separators=(', ', ': ')),
        status=200,
        mimetype='application/json'
    )

@app.route("/addresses", methods=["POST"])
@token_required
@role_required(["staff", "admin"])
def add_address():
    data = request.get_json()
    number_building = data.get("number_building")
    street = data.get("street")
    city = data.get("city")
    zip_postcode = data.get("zip_postcode")
    state_province_county = data.get("state_province_county")
    country = data.get("country")

    if not number_building or not street or not city or not zip_postcode or not state_province_county or not country:
        return jsonify({"error": "Required fields missing"}), 400

    query = """
    INSERT INTO addresses (number_building, street, city, zip_postcode, state_province_county, country) 
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    params = (number_building, street, city, zip_postcode, state_province_county, country)

    try:
        result = execute_query(query, params)

        if result is not None and result >= 0:
            return jsonify({"message": "Address added successfully"}), 201
        else:
            return jsonify({"error": "Failed to add address"}), 500
    except Exception as e:
        logging.error(f"Error adding address: {e}")
        return jsonify({"error": "An error occurred while adding address"}), 500
    

@app.route("/addresses/<int:address_id>", methods=["PUT"])
@token_required
@role_required(["staff", "admin"])
def update_address(address_id):
    data = request.get_json()
    number_building = data.get("number_building")
    street = data.get("street")
    city = data.get("city")
    zip_postcode = data.get("zip_postcode")
    state_province_county = data.get("state_province_county")
    country = data.get("country")

    query = """
    UPDATE addresses SET number_building=%s, street=%s, city=%s, zip_postcode=%s, 
    state_province_county=%s, country=%s WHERE address_id=%s
    """
    params = (number_building, street, city, zip_postcode, state_province_county, country, address_id)
    
    result = execute_query(query, params)
    
    if result:
        return jsonify({"message": "Address updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update address"}), 500

@app.route("/addresses/<int:address_id>", methods=["DELETE"])
@token_required
@role_required(["staff", "admin"])
def delete_address(address_id):
    query = "DELETE FROM addresses WHERE address_id=%s"
    params = (address_id,)
    
    result = execute_query(query, params)
    
    if result:
        return jsonify({"message": "Address deleted successfully"}), 200
    else:
        return jsonify({"error": "Failed to delete address"}), 500
    

# CRUD operations for Customers
@app.route("/customers", methods=["GET"])
def get_all_customers():
    query = "SELECT * FROM customers"
    customers = execute_query(query, fetch=True)
    
    if not customers:
        return jsonify({"error": "No customers found"}), 404
    
    formatted_customers = [
        {
            "customer_id": customer["customer_id"],
            "address_id": customer["address_id"],
            "customer_name": customer["customer_name"],
            "customer_phone": customer["customer_phone"],
            "customer_email": customer["customer_email"]
        }
        for customer in customers
    ]
    return app.response_class(
        response=json.dumps(formatted_customers, separators=(', ', ': ')),
        status=200,
        mimetype='application/json'
    )

@app.route("/customers", methods=["POST"])
@token_required
@role_required(["staff", "admin"])
def add_customer():
    data = request.get_json()
    address_id = data.get("address_id")
    customer_name = data.get("customer_name")
    customer_phone = data.get("customer_phone")
    customer_email = data.get("customer_email")

    # Validation
    if not address_id or not customer_name or not customer_phone:
        return jsonify({"error": "Required fields missing"}), 400

    query = """
    INSERT INTO customers (address_id, customer_name, customer_phone, customer_email) 
    VALUES (%s, %s, %s, %s)
    """
    params = (address_id, customer_name, customer_phone, customer_email)
    
    try:
        result = execute_query(query, params)
        
        if result is not None and result >= 0:
            return jsonify({"message": "Customer added successfully"}), 201
        else:
            return jsonify({"error": "Failed to add customer"}), 500
    except Exception as e:
        logging.error(f"Error adding customer: {e}")
        return jsonify({"error": "An error occurred while adding customer"}), 500

@app.route("/customers/<int:customer_id>", methods=["PUT"])
@token_required
@role_required(["staff", "admin"])
def update_customer(customer_id):
    data = request.get_json()
    address_id = data.get("address_id")
    customer_name = data.get("customer_name")
    customer_phone = data.get("customer_phone")
    customer_email = data.get("customer_email")

    query = """
    UPDATE customers SET address_id=%s, customer_name=%s, customer_phone=%s, 
    customer_email=%s WHERE customer_id=%s
    """
    params = (address_id, customer_name, customer_phone, customer_email, customer_id)
    
    result = execute_query(query, params)
    
    if result:
        return jsonify({"message": "Customer updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update customer"}), 500

@app.route("/customers/<int:customer_id>", methods=["DELETE"])
@token_required
@role_required(["staff", "admin"])
def delete_customer(customer_id):
    query = "DELETE FROM customers WHERE customer_id=%s"
    params = (customer_id,)
    
    result = execute_query(query, params)
    
    if result:
        return jsonify({"message": "Customer deleted successfully"}), 200
    else:
        return jsonify({"error": "Failed to delete customer"}), 500
    

# CRUD operations for Services
@app.route("/services", methods=["GET"])
def get_all_services():
    query = "SELECT * FROM services"
    services = execute_query(query, fetch=True)
    
    if not services:
        return jsonify({"error": "No services found"}), 404
    
    formatted_services = [
        {
            "service_id": service["service_id"],
            "service_name": service["service_name"],
            "price_per_period": float(service["price_per_period"])
        }
        for service in services
    ]
    return app.response_class(
        response=json.dumps(formatted_services, separators=(', ', ': ')),
        status=200,
        mimetype='application/json'
    )

@app.route("/services", methods=["POST"])
@token_required
@role_required(["staff", "admin"])
def add_service():
    data = request.get_json()
    service_name = data.get("service_name")
    price_per_period = data.get("price_per_period")

    if not service_name or price_per_period is None:
        return jsonify({"error": "Required fields missing"}), 400

    query = """
    INSERT INTO services (service_name, price_per_period) 
    VALUES (%s, %s)
    """
    params = (service_name, price_per_period)
    
    try:
        result = execute_query(query, params)
        
        if result is not None and result >= 0:
            return jsonify({"message": "Service added successfully"}), 201
        else:
            return jsonify({"error": "Failed to add service"}), 500
    except Exception as e:
        logging.error(f"Error adding service: {e}")
        return jsonify({"error": "An error occurred while adding service"}), 500

@app.route("/services/<int:service_id>", methods=["PUT"])
@token_required
@role_required(["staff", "admin"])
def update_service(service_id):
    data = request.get_json()
    service_name = data.get("service_name")
    price_per_period = data.get("price_per_period")

    query = """
    UPDATE services SET service_name=%s, price_per_period=%s WHERE service_id=%s
    """
    params = (service_name, price_per_period, service_id)
    
    result = execute_query(query, params)
    
    if result:
        return jsonify({"message": "Service updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update service"}), 500

@app.route("/services/<int:service_id>", methods=["DELETE"])
@token_required
@role_required(["staff", "admin"])
def delete_service(service_id):
    query = "DELETE FROM services WHERE service_id=%s"
    params = (service_id,)
    
    result = execute_query(query, params)
    
    if result:
        return jsonify({"message": "Service deleted successfully"}), 200
    else:
        return jsonify({"error": "Failed to delete service"}), 500


# CRUD operations for Customer_Orders
@app.route("/orders", methods=["GET"])
def get_all_orders():
    query = "SELECT * FROM customer_orders"
    orders = execute_query(query, fetch=True)
    
    if not orders:
        return jsonify({"error": "No orders found"}), 404
    
    formatted_orders = [
        {
            "order_id": order["order_id"],
            "customer_id": order["customer_id"],
            "order_status": order["order_status"],
            "order_date": order["order_date"].isoformat() if isinstance(order["order_date"], datetime.date) else str(order["order_date"]),
            "start_date": order["start_date"].isoformat() if isinstance(order["start_date"], datetime.date) else str(order["start_date"]),
            "end_date": order["end_date"].isoformat() if isinstance(order["end_date"], datetime.date) else str(order["end_date"])
        }
        for order in orders
    ]
    return app.response_class(
        response=json.dumps(formatted_orders, separators=(', ', ': ')),
        status=200,
        mimetype='application/json'
    )

@app.route("/orders", methods=["POST"])
@token_required
@role_required(["staff", "admin"])
def add_order():
    data = request.get_json()
    customer_id = data.get("customer_id")
    order_status = data.get("order_status")
    order_date = data.get("order_date")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    if not customer_id or not order_status or not order_date or not start_date:
        return jsonify({"error": "Required fields missing"}), 400

    query = """
    INSERT INTO customer_orders (customer_id, order_status, order_date, start_date, end_date) 
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (customer_id, order_status, order_date, start_date, end_date)
    
    try:
        result = execute_query(query, params)
        
        if result is not None and result >= 0:
            return jsonify({"message": "Order added successfully"}), 201
        else:
            return jsonify({"error": "Failed to add order"}), 500
    except Exception as e:
        logging.error(f"Error adding order: {e}")
        return jsonify({"error": "An error occurred while adding order"}), 500
    
@app.route("/orders/<int:order_id>", methods=["PUT"])
@token_required
@role_required(["staff", "admin"])
def update_order(order_id):
    data = request.get_json()
    customer_id = data.get("customer_id")
    order_status = data.get("order_status")
    order_date = data.get("order_date")
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    query = """
    UPDATE customer_orders SET customer_id=%s, order_status=%s, order_date=%s, 
    start_date=%s, end_date=%s WHERE order_id=%s
    """
    params = (customer_id, order_status, order_date, start_date, end_date, order_id)
    
    result = execute_query(query, params)
    
    if result:
        return jsonify({"message": "Order updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update order"}), 500

@app.route("/orders/<int:order_id>", methods=["DELETE"])
@token_required
@role_required(["staff", "admin"])
def delete_order(order_id):
    query = "DELETE FROM customer_orders WHERE order_id=%s"
    params = (order_id,)
    
    result = execute_query(query, params)
    
    if result:
        return jsonify({"message": "Order deleted successfully"}), 200
    else:
        return jsonify({"error": "Failed to delete order"}), 500


# CRUD operations for Order_Items
@app.route("/order_items", methods=["GET"])
def get_all_order_items():
    query = "SELECT * FROM order_items"
    order_items = execute_query(query, fetch=True)
    
    if not order_items:
        return jsonify({"error": "No order items found"}), 404
    
    formatted_order_items = [
        {
            "order_item_id": item["order_item_id"],
            "order_id": item["order_id"],
            "service_id": item["service_id"],
            "order_quantity": item["order_quantity"],
            "monthly_payment_amount": float(item["monthly_payment_amount"]) if isinstance(item["monthly_payment_amount"], Decimal) else item["monthly_payment_amount"],
            "monthly_payment_date": item["monthly_payment_date"].isoformat() if isinstance(item["monthly_payment_date"], datetime.date) else str(item["monthly_payment_date"])
        }
        for item in order_items
    ]
    return app.response_class(
        response=json.dumps(formatted_order_items, separators=(', ', ': ')),
        status=200,
        mimetype='application/json'
    )

@app.route("/order_items", methods=["POST"])
@token_required
@role_required(["staff", "admin"])
def add_order_item():
    data = request.get_json()
    order_id = data.get("order_id")
    service_id = data.get("service_id")
    order_quantity = data.get("order_quantity")
    monthly_payment_amount = data.get("monthly_payment_amount")
    monthly_payment_date = data.get("monthly_payment_date")

    if not order_id or not service_id or not order_quantity:
        return jsonify({"error": "Required fields missing"}), 400

    query = """
    INSERT INTO order_items (order_id, service_id, order_quantity, monthly_payment_amount, monthly_payment_date) 
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (order_id, service_id, order_quantity, monthly_payment_amount, monthly_payment_date)
    
    try:
        result = execute_query(query, params)
        
        if result is not None and result >= 0:
            return jsonify({"message": "Order item added successfully"}), 201
        else:
            return jsonify({"error": "Failed to add order item"}), 500
    except Exception as e:
        logging.error(f"Error adding order item: {e}")
        return jsonify({"error": "An error occurred while adding order item"}), 500

@app.route("/order_items/<int:order_item_id>", methods=["PUT"])
@token_required
@role_required(["staff", "admin"])
def update_order_item(order_item_id):
    data = request.get_json()
    order_id = data.get("order_id")
    service_id = data.get("service_id")
    order_quantity = data.get("order_quantity")
    monthly_payment_amount = data.get("monthly_payment_amount")
    monthly_payment_date = data.get("monthly_payment_date")

    query = """
    UPDATE order_items SET order_id=%s, service_id=%s, order_quantity=%s, 
    monthly_payment_amount=%s, monthly_payment_date=%s WHERE order_item_id=%s
    """
    params = (order_id, service_id, order_quantity, monthly_payment_amount, monthly_payment_date, order_item_id)
    
    result = execute_query(query, params)
    
    if result:
        return jsonify({"message": "Order item updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update order item"}), 500

@app.route("/order_items/<int:order_item_id>", methods=["DELETE"])
@token_required
@role_required(["staff", "admin"])
def delete_order_item(order_item_id):
    query = "DELETE FROM order_items WHERE order_item_id=%s"
    params = (order_item_id,)
    
    result = execute_query(query, params)
    
    if result:
        return jsonify({"message": "Order item deleted successfully"}), 200
    else:
        return jsonify({"error": "Failed to delete order item"}), 500


# CRUD operations for Customer_Payment_Details
@app.route("/payments", methods=["GET"])
def get_all_payments():
    query = "SELECT * FROM customer_payment_details"
    payments = execute_query(query, fetch=True)
    
    if not payments:
        return jsonify({"error": "No payments found"}), 404
    
    formatted_payments = [
        {
            "payment_id": payment["payment_id"],
            "order_id": payment["order_id"],
            "payment_date": payment["payment_date"].isoformat() if isinstance(payment["payment_date"], datetime.date) else str(payment["payment_date"]),
            "payment_amount": float(payment["payment_amount"]) if isinstance(payment["payment_amount"], Decimal) else payment["payment_amount"],
            "payment_method": payment["payment_method"],
            "transaction_reference": payment["transaction_reference"]
        }
        for payment in payments
    ]
    return app.response_class(
        response=json.dumps(formatted_payments, separators=(', ', ': ')),
        status=200,
        mimetype='application/json'
    )

@app.route("/payments", methods=["POST"])
@token_required
@role_required(["staff", "admin"])
def add_payment():
    data = request.get_json()
    order_id = data.get("order_id")
    payment_date = data.get("payment_date")
    payment_amount = data.get("payment_amount")
    payment_method = data.get("payment_method")
    transaction_reference = data.get("transaction_reference")

    if not order_id or not payment_date or payment_amount is None or not payment_method:
        return jsonify({"error": "Required fields missing"}), 400

    query = """
    INSERT INTO customer_payment_details (order_id, payment_date, payment_amount, payment_method, transaction_reference) 
    VALUES (%s, %s, %s, %s, %s)
    """
    params = (order_id, payment_date, payment_amount, payment_method, transaction_reference)
    
    try:
        result = execute_query(query, params)
        
        if result is not None and result >= 0:
            return jsonify({"message": "Payment added successfully"}), 201
        else:
            return jsonify({"error": "Failed to add payment"}), 500
    except Exception as e:
        logging.error(f"Error adding payment: {e}")
        return jsonify({"error": "An error occurred while adding payment"}), 500

@app.route("/payments/<int:payment_id>", methods=["PUT"])
@token_required
@role_required(["staff", "admin"])
def update_payment(payment_id):
    data = request.get_json()
    order_id = data.get("order_id")
    payment_date = data.get("payment_date")
    payment_amount = data.get("payment_amount")
    payment_method = data.get("payment_method")
    transaction_reference = data.get("transaction_reference")

    query = """
    UPDATE customer_payment_details SET order_id=%s, payment_date=%s, payment_amount=%s, 
    payment_method=%s, transaction_reference=%s WHERE payment_id=%s
    """
    params = (order_id, payment_date, payment_amount, payment_method, transaction_reference, payment_id)
    
    result = execute_query(query, params)
    
    if result:
        return jsonify({"message": "Payment updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update payment"}), 500

@app.route("/payments/<int:payment_id>", methods=["DELETE"])
@token_required
@role_required(["staff", "admin"])
def delete_payment(payment_id):
    query = "DELETE FROM customer_payment_details WHERE payment_id=%s"
    params = (payment_id,)
    
    result = execute_query(query, params)
    
    if result:
        return jsonify({"message": "Payment deleted successfully"}), 200
    else:
        return jsonify({"error": "Failed to delete payment"}), 500

@app.route("/")
def hello_world():
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Customer & Services Management System</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #121212;
            color: #e0e0e0;
        }
        .container {
            background-color: #1e1e1e;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
            padding: 30px;
            border: 1px solid #333;
        }
        h1 {
            color: #4da6ff;
            text-align: center;
            border-bottom: 2px solid #3498db;
            padding-bottom: 15px;
        }
        h2 {
            color: #4da6ff;
            margin-top: 25px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background-color: #2c2c2c;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid #404040;
        }
        li a {
            display: block;
            padding: 12px 15px;
            text-decoration: none;
            color: #e0e0e0;
            transition: all 0.3s ease;
        }
        li a:hover {
            background-color: #3498db;
            color: white;
            border-radius: 5px;
        }
        .footer {
            text-align: center;
            margin-top: 20px;
            color: #888;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Customer & Services Management System</h1>
        
        <h2>Available Tables</h2>
        <ul>
            <li><a href="/addresses">Addresses</a></li>
            <li><a href="/customers">Customers</a></li>
            <li><a href="/services">Services</a></li>
            <li><a href="/orders">Orders</a></li>
            <li><a href="/order_items">Order Items</a></li>
            <li><a href="/payments">Payments</a></li>
        </ul>
        
        <div class="footer">
            © 2024 Customer Management API
        </div>
    </div>
</body>
</html>
    """

if __name__ == "__main__":
    app.run(debug=True)