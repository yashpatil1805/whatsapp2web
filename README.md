# WhatsApp2Web

A Flask-based web application for managing customers, products, and orders with a PostgreSQL database backend.

## Features

- **Customer Management**: Add, edit, and delete customer information
- **Product Management**: Manage product catalog with details like product number, name, size, price, and description
- **Order Management**: Create, edit, and track orders with status updates
- **Admin Dashboard**: Secure admin interface for managing all aspects of the system

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript

## Installation

### Prerequisites

- Python 3.7 or higher
- PostgreSQL database
- pip (Python package installer)

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/whatsapp2web.git
cd whatsapp2web
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up PostgreSQL database:
   - Create a database named `whatsapp2web_db`
   - Update database credentials in `config.py`

5. Configure the application:
   - Update database connection settings in `config.py`
   - Change the admin credentials in `app.py` (default: admin/adminpassword123)
   - Update the secret key in `app.py` for production use

6. Run the application:
```bash
python app.py
```

7. Access the application:
   - Open your browser and navigate to `http://localhost:5000`
   - Login with admin credentials

## Project Structure

```
whatsapp2web/
├── app.py                 # Main Flask application
├── config.py              # Database configuration
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── templates/            # HTML templates
│   ├── login.html
│   ├── dashboard.html
│   ├── customers.html
│   ├── products.html
│   ├── orders.html
│   ├── edit_customer.html
│   ├── edit_product.html
│   └── edit_order.html
└── static/               # Static files
    ├── css/              # Stylesheets
    └── images/           # Image assets
```

## Configuration

### Database Configuration

Edit `config.py` to set your PostgreSQL connection details:

```python
DB_HOST = "localhost"
DB_NAME = "whatsapp2web_db"
DB_USER = "postgres"
DB_PASSWORD = "your_password"
DB_PORT = 5432
```

### Admin Credentials

Default admin credentials are set in `app.py`. **Change these before deploying to production:**

```python
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "adminpassword123"
```

## Usage

1. **Login**: Access the admin login page and enter your credentials
2. **Dashboard**: View the main dashboard after successful login
3. **Customers**: Manage customer information including name, email, phone, and address
4. **Products**: Add and manage products with details like price, size, and description
5. **Orders**: Create orders by selecting customers and products, track order status

## Database Schema

The application uses the following main tables:
- `customers`: Customer information
- `products`: Product catalog
- `orders`: Order headers
- `order_items`: Order line items

## Development

To run in development mode with auto-reload:

```bash
python app.py
```

The application will run with `debug=True` enabled.

## Security Notes

- Change default admin credentials before deployment
- Use a strong secret key for session management
- Store database credentials securely (consider using environment variables)
- Enable HTTPS in production

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

