from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import get_db_connection
import psycopg2.extras

# ---------------------------
# Flask App Setup
# ---------------------------
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key in production

# Dummy admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "adminpassword123"

# ---------------------------
# Helpers
# ---------------------------
def get_first_value(row):
    if row is None:
        return None
    return list(row.values())[0] if isinstance(row, dict) else row[0]

def reset_sequence_if_table_empty(conn, cursor, table_name, id_column):
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count_row = cursor.fetchone()
    count_val = get_first_value(count_row)
    try:
        count_val = int(count_val)
    except Exception:
        count_val = 0

    if count_val == 0:
        cursor.execute("SELECT pg_get_serial_sequence(%s, %s)", (table_name, id_column))
        seq_row = cursor.fetchone()
        seq_name = get_first_value(seq_row)
        if seq_name:
            cursor.execute(f"ALTER SEQUENCE {seq_name} RESTART WITH 1")
            conn.commit()

# ---------------------------
# ROUTES
# ---------------------------
@app.route("/")
def home():
    return redirect(url_for("login"))

# LOGIN / LOGOUT
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid credentials", "error")
            return redirect(url_for("login"))
    return render_template("login.html", css_file="login.css")

@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("login"))

# DASHBOARD
@app.route("/dashboard")
def dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    return render_template("dashboard.html", css_file="admin_styles.css")

# ---------------------------
# CUSTOMERS
# ---------------------------
@app.route("/customers")
def customers():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    customers_list = []
    if conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT customerid, name, email, phone_number, address, landmark, pincode FROM customers ORDER BY customerid ASC")
            customers_list = cur.fetchall()
        conn.close()
    return render_template("customers.html", customers=customers_list, css_file="admin_styles.css")

@app.route("/add_customer", methods=["POST"])
def add_customer():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    name = request.form.get("name")
    email = request.form.get("email")
    address = request.form.get("address")
    landmark = request.form.get("landmark")
    pincode = request.form.get("pincode")
    phone_number = request.form.get("phone_number")

    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for("customers"))

    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO customers (name, email, address, landmark, pincode, phone_number) VALUES (%s, %s, %s, %s, %s, %s)",
                        (name, email, address, landmark, pincode, phone_number))
            conn.commit()
        flash(f"Customer '{name}' added successfully.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Failed to add customer: {e}", "error")
    finally:
        conn.close()
    return redirect(url_for("customers"))

@app.route("/delete_customer/<int:customerid>")
def delete_customer(customerid):
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for("customers"))

    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM order_items WHERE orderid IN (SELECT orderid FROM orders WHERE customerid=%s)", (customerid,))
            cur.execute("DELETE FROM orders WHERE customerid=%s", (customerid,))
            cur.execute("DELETE FROM customers WHERE customerid=%s", (customerid,))
            conn.commit()
            reset_sequence_if_table_empty(conn, cur, "customers", "customerid")
        flash(f"Customer ID {customerid} deleted successfully.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Failed to delete customer: {e}", "error")
    finally:
        conn.close()
    return redirect(url_for("customers"))

@app.route("/edit_customer/<int:customerid>", methods=["GET", "POST"])
def edit_customer(customerid):
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for("customers"))

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if request.method == "POST":
                name = request.form.get("name")
                email = request.form.get("email")
                address = request.form.get("address")
                landmark = request.form.get("landmark")
                pincode = request.form.get("pincode")
                phone_number = request.form.get("phone_number")
                cur.execute("""UPDATE customers SET name=%s, email=%s, address=%s, landmark=%s, pincode=%s, phone_number=%s
                               WHERE customerid=%s""",
                            (name, email, address, landmark, pincode, phone_number, customerid))
                conn.commit()
                flash("Customer updated successfully.", "success")
                return redirect(url_for("customers"))
            cur.execute("SELECT * FROM customers WHERE customerid=%s", (customerid,))
            customer = cur.fetchone()
    finally:
        conn.close()
    return render_template("edit_customer.html", customer=customer, css_file="admin_styles.css")

# ---------------------------
# PRODUCTS
# ---------------------------
@app.route("/products")
def products():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    products_list = []
    if conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT productid, product_no, name, size, price, description FROM products ORDER BY productid ASC")
            products_list = cur.fetchall()
        conn.close()
    return render_template("products.html", products=products_list, css_file="admin_styles.css")

@app.route("/add_product", methods=["POST"])
def add_product():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    product_no = request.form.get("product_no")
    name = request.form.get("name")
    price = request.form.get("price")
    size = request.form.get("size")
    description = request.form.get("description")

    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for("products"))

    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO products (product_no, name, size, price, description) VALUES (%s, %s, %s, %s, %s)",
                        (product_no, name, size, price, description))
            conn.commit()
        flash(f"Product '{name}' added successfully.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Failed to add product: {e}", "error")
    finally:
        conn.close()
    return redirect(url_for("products"))

@app.route("/delete_product/<int:productid>")
def delete_product(productid):
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for("products"))

    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM products WHERE productid=%s", (productid,))
            conn.commit()
            reset_sequence_if_table_empty(conn, cur, "products", "productid")
        flash(f"Product ID {productid} deleted successfully.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Failed to delete product: {e}", "error")
    finally:
        conn.close()
    return redirect(url_for("products"))

@app.route("/edit_product/<int:productid>", methods=["GET", "POST"])
def edit_product(productid):
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for("products"))

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if request.method == "POST":
                product_no = request.form.get("product_no")
                name = request.form.get("name")
                price = request.form.get("price")
                size = request.form.get("size")
                description = request.form.get("description")
                cur.execute("""UPDATE products SET product_no=%s, name=%s, price=%s, size=%s, description=%s
                               WHERE productid=%s""",
                            (product_no, name, price, size, description, productid))
                conn.commit()
                flash("Product updated successfully.", "success")
                return redirect(url_for("products"))
            cur.execute("SELECT * FROM products WHERE productid=%s", (productid,))
            product = cur.fetchone()
    finally:
        conn.close()
    return render_template("edit_product.html", product=product, css_file="admin_styles.css")

# ---------------------------
# ORDERS
# ---------------------------
@app.route("/orders")
def orders():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    orders_list = []
    customers = []
    products = []

    if conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""SELECT o.orderid, o.customerid, o.order_date, o.total_amount, o.status,
                                  c.name AS customer_name
                           FROM orders o
                           LEFT JOIN customers c ON o.customerid = c.customerid
                           ORDER BY o.orderid ASC""")
            orders_data = cur.fetchall()

            for order in orders_data:
                cur.execute("""SELECT oi.itemid, oi.productid, p.name AS name, p.size, oi.quantity, oi.price
                               FROM order_items oi
                               LEFT JOIN products p ON oi.productid = p.productid
                               WHERE oi.orderid=%s ORDER BY oi.itemid ASC""", (order["orderid"],))
                items_raw = cur.fetchall() or []
                items_list = []
                for item in items_raw:
                    items_list.append({
                        "name": item["name"],
                        "size": item["size"],
                        "quantity": item["quantity"],
                        "price": item["price"]
                    })
                orders_list.append({
                    "orderid": order["orderid"],
                    "customer_name": order["customer_name"],
                    "order_date": order["order_date"],
                    "total_amount": order["total_amount"],
                    "status": order["status"],
                    "order_items": items_list
                })

            cur.execute("SELECT customerid, name FROM customers ORDER BY customerid ASC")
            customers = cur.fetchall() or []

            cur.execute("SELECT productid, name, size, price FROM products ORDER BY productid ASC")
            products = cur.fetchall() or []

        conn.close()
    return render_template("orders.html", orders=orders_list, customers=customers, products=products, css_file="admin_styles.css")

@app.route("/add_order", methods=["POST"])
def add_order():
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))

    try:
        customer_id = int(request.form.get("customerid", 0))
        if customer_id <= 0:
            flash("Please select a valid customer.", "error")
            return redirect(url_for("orders"))
    except ValueError:
        flash("Invalid customer ID.", "error")
        return redirect(url_for("orders"))

    product_ids = request.form.getlist("productid[]")
    quantities = request.form.getlist("quantity[]")
    items = []

    for pid_str, qty_str in zip(product_ids, quantities):
        try:
            pid = int(pid_str)
            qty = int(qty_str)
            if pid > 0 and qty > 0:
                items.append((pid, qty))
        except ValueError:
            continue

    if not items:
        flash("No valid items selected.", "error")
        return redirect(url_for("orders"))

    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for("orders"))

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("INSERT INTO orders (customerid, order_date, total_amount, status) VALUES (%s, NOW(), %s, %s) RETURNING orderid",
                        (customer_id, 0, "Accepted"))
            order_id_row = cur.fetchone()
            order_id = order_id_row["orderid"]

            total_amount = 0
            for pid, qty in items:
                cur.execute("SELECT name, size, price FROM products WHERE productid=%s", (pid,))
                product = cur.fetchone()
                if product:
                    price = product["price"]
                    subtotal = price * qty
                    total_amount += subtotal
                    cur.execute("INSERT INTO order_items (orderid, productid, quantity, price) VALUES (%s, %s, %s, %s)",
                                (order_id, pid, qty, price))
            cur.execute("UPDATE orders SET total_amount=%s WHERE orderid=%s", (total_amount, order_id))
            conn.commit()
        flash("Order added successfully.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Failed to add order: {e}", "error")
    finally:
        conn.close()
    return redirect(url_for("orders"))

@app.route("/delete_order/<int:order_id>")
def delete_order(order_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for("orders"))

    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM order_items WHERE orderid=%s", (order_id,))
            cur.execute("DELETE FROM orders WHERE orderid=%s", (order_id,))
            conn.commit()
            reset_sequence_if_table_empty(conn, cur, "orders", "orderid")
        flash(f"Order ID {order_id} deleted successfully.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Failed to delete order: {e}", "error")
    finally:
        conn.close()
    return redirect(url_for("orders"))

@app.route("/update_order_status/<int:order_id>", methods=["POST"])
def update_order_status(order_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    new_status = request.form.get("status")
    if not new_status:
        flash("Invalid status.", "error")
        return redirect(url_for("orders"))
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for("orders"))
    try:
        with conn.cursor() as cur:
            cur.execute("UPDATE orders SET status = %s WHERE orderid = %s", (new_status, order_id))
            conn.commit()
        flash(f"Order #{order_id} status updated to {new_status}.", "success")
    except Exception as e:
        conn.rollback()
        flash(f"Failed to update status: {e}", "error")
    finally:
        conn.close()
    return redirect(url_for("orders"))

# ---------------------------
# EDIT ORDER
# ---------------------------
@app.route("/edit_order/<int:order_id>", methods=["GET", "POST"])
def edit_order(order_id):
    if not session.get("admin_logged_in"):
        return redirect(url_for("login"))
    conn = get_db_connection()
    if not conn:
        flash("Database connection failed.", "error")
        return redirect(url_for("orders"))

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            if request.method == "POST":
                customer_id = int(request.form.get("customerid"))
                product_ids = request.form.getlist("productid[]")
                quantities = request.form.getlist("quantity[]")

                # Remove old items
                cur.execute("DELETE FROM order_items WHERE orderid=%s", (order_id,))

                total_amount = 0
                for pid, qty in zip(product_ids, quantities):
                    pid_int = int(pid)
                    qty_int = int(qty)
                    cur.execute("SELECT price FROM products WHERE productid=%s", (pid_int,))
                    price = cur.fetchone()["price"]
                    subtotal = price * qty_int
                    total_amount += subtotal
                    cur.execute("INSERT INTO order_items (orderid, productid, quantity, price) VALUES (%s,%s,%s,%s)",
                                (order_id, pid_int, qty_int, price))

                cur.execute("UPDATE orders SET customerid=%s, total_amount=%s WHERE orderid=%s",
                            (customer_id, total_amount, order_id))
                conn.commit()
                flash("Order updated successfully.", "success")
                return redirect(url_for("orders"))

            # GET: fetch order info
            cur.execute("SELECT * FROM orders WHERE orderid=%s", (order_id,))
            order = cur.fetchone()
            cur.execute("SELECT * FROM order_items WHERE orderid=%s", (order_id,))
            items = cur.fetchall()
            cur.execute("SELECT customerid, name FROM customers")
            customers = cur.fetchall()
            cur.execute("SELECT productid, name, size, price FROM products")
            products = cur.fetchall()
    finally:
        conn.close()

    return render_template("edit_order.html", order=order, items=items,
                           customers=customers, products=products, css_file="admin_styles.css")

# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
