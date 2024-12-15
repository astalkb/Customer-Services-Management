# Customer & Services Management System API

The Customer & Services Management System API is a Flask-based application designed to manage customer data, services, and orders. This project aims to streamline the management of customer interactions and service offerings.

## Features

- **Customer Management:** Track customer details, including contact information and associated addresses.
- **Service Management:** Maintain a catalog of services offered, including pricing and descriptions.
- **Order Management:** Manage customer orders, including status tracking and order history.

## Project Setup

Follow these steps to set up and run the project locally.

### 1. Create a Virtual Environment

First, create a virtual environment to manage your project dependencies:
```bash
python -m venv .venv
```

Activate the virtual environment:

-   **On Windows:**

    ```bash
    .venv\Scripts\activate
    ```

-   **On macOS/Linux:**

    ```bash
    source .venv/bin/activate
    ```

### 2. Install Dependencies

Install the required dependencies by running the following command:
```bash
pip install -r requirements.txt
```

### 3. Configure Database Connection

Modify the database connection settings in the `app.py` file. Look for the `DB_CONFIG` dictionary and update the values with your actual database credentials:
```python
DB_CONFIG = {
'host': 'localhost',
'user': 'your_username',
'password': 'your_password',
'database': 'elective'
}
```

### 4. Run the Application

Start the Flask application with the following command:
```bash
flask --app app.py run
```

### Running Tests

To run the tests, use `test_app.py` and run the following command:
```bash
pytest -s tests/test_app.py
```

File Structure
--------------

The project has the following structure:
```bash
customer_services/
├── .venv/ # Virtual environment folder
├── database/ # Database for the Flask application
│ └── elective.sql # MySQL schema
├── tests/ # Test cases for the Flask application
│ └── test_app.py # API test cases
├── .gitignore # List of files/folders ignored by Git
├── app.py # Flask application (main file)
├── README.md # Project documentation
└── requirements.txt # List of project dependencies
```


## API Endpoints
### Authentication Endpoints

| **Method** | **Endpoint** | **Description** | **Roles Required** |
| --- | --- | --- | --- |
| POST | /auth/register | Register a new user (provide username, password, and role). | - |
| POST | /auth/login | Login with credentials (username and password) and receive a JWT token. | - |

### Address CRUD Endpoints

| **Method** | **Endpoint** | **Description** | **Roles Required** |
| --- | --- | --- | --- |
| GET | /addresses | Fetch all addresses. | - |
| POST | /addresses | Add a new address to the database. | `admin`, `staff` |
| PUT | /addresses/<int:address_id> | Update details of a specific address by ID. | `admin`, `staff` |
| DELETE | /addresses/<int:address_id> | Delete an address by ID. | `admin`, `staff` |

### Customer CRUD Endpoints

| **Method** | **Endpoint** | **Description** | **Roles Required** |
| --- | --- | --- | --- |
| GET | /customers | Fetch all customers. | - |
| POST | /customers | Add a new customer to the database. | `admin`, `staff` |
| PUT | /customers/<int:customer_id> | Update details of a specific customer by ID. | `admin`, `staff` |
| DELETE | /customers/<int:customer_id> | Delete a customer by ID. | `admin`, `staff` |

### Service CRUD Endpoints

| **Method** | **Endpoint** | **Description** | **Roles Required** |
| --- | --- | --- | --- |
| GET | /services | Fetch all services. | - |
| POST | /services | Add a new service to the database. | `admin`, `staff` |
| PUT | /services/<int:service_id> | Update details of a specific service by ID. | `admin`, `staff` |
| DELETE | /services/<int:service_id> | Delete a service by ID. | `admin`, `staff` |

### Order CRUD Endpoints

| **Method** | **Endpoint** | **Description** | **Roles Required** |
| --- | --- | --- | --- |
| GET | /orders | Fetch all orders. | - |
| POST | /orders | Add a new order to the database. | `admin`, `staff` |
| PUT | /orders/<int:order_id> | Update details of a specific order by ID. | `admin`, `staff` |
| DELETE | /orders/<int:order_id> | Delete an order by ID. | `admin`, `staff` |

### Order Item CRUD Endpoints

| **Method** | **Endpoint** | **Description** | **Roles Required** |
| --- | --- | --- | --- |
| GET | /order_items | Fetch all order items. | - |
| POST | /order_items | Add a new order item to the database. | `admin`, `staff` |
| PUT | /order_items/<int:order_item_id> | Update details of a specific order item by ID. | `admin`, `staff` |
| DELETE | /order_items/<int:order_item_id> | Delete an order item by ID. | `admin`, `staff` |

### Payment CRUD Endpoints

| **Method** | **Endpoint** | **Description** | **Roles Required** |
| --- | --- | --- | --- |
| GET | /payments | Fetch all payments. | - |
| POST | /payments | Add a new payment to the database. | `admin`, `staff` |
| PUT | /payments/<int:payment_id> | Update details of a specific payment by ID. | `admin`, `staff` |
| DELETE | /payments/<int:payment_id> | Delete a payment by ID. | `admin`, `staff` |

## Troubleshooting

-   **Database Connection Error:**\
    Ensure that the database credentials in `app.py` are correct and that the MySQL server is running and accessible.

-   **Missing Dependencies:**\
    If any required package is missing, run `pip install -r requirements.txt` again.

## Git Commit Guidelines
Use conventional commits:
```bash
feat: add user authentication
fix: resolve database connection issue
docs: update API documentation
test: add user registration tests
```