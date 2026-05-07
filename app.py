from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "foodrush_secret_2024"

DB = "database.db"

def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ── AUTH HELPERS ─────────────────────────────
def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            flash("Please login first.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        if session.get("role") != "admin":
            flash("Admin access required.", "error")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return decorated

# ── ROUTES ───────────────────────────────────

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("home"))
    return redirect(url_for("login"))

# ── REGISTER ─────────────────────────────────
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        role     = request.form.get("role", "user")

        if not username or not password:
            flash("All fields are required.", "error")
            return redirect(url_for("register"))

        db = get_db()
        existing = db.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
        if existing:
            flash("Username already taken. Try another.", "error")
            db.close()
            return redirect(url_for("register"))

        db.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)",
                   (username, password, role))
        db.commit()
        db.close()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

# ── LOGIN ─────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        db   = get_db()
        user = db.execute("SELECT * FROM users WHERE username=? AND password=?",
                          (username, password)).fetchone()
        db.close()

        if user:
            session["user_id"]  = user["id"]
            session["username"] = user["username"]
            session["role"]     = user["role"]
            session["cart"]     = session.get("cart", [])
            flash(f"Welcome back, {user['username']}!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

# ── LOGOUT ────────────────────────────────────
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

# ── HOME / DASHBOARD ──────────────────────────
@app.route("/home")
@login_required
def home():
    return render_template("home.html",
                           username=session["username"],
                           role=session["role"])

# ── MENU ──────────────────────────────────────
@app.route("/menu")
@login_required
def menu():
    search = request.args.get("search", "").strip()
    db     = get_db()
    if search:
        items = db.execute(
            "SELECT * FROM food WHERE name LIKE ?", (f"%{search}%",)
        ).fetchall()
    else:
        items = db.execute("SELECT * FROM food").fetchall()
    db.close()
    return render_template("menu.html", items=items, search=search,
                           cart_count=len(session.get("cart", [])))

# ── CART ──────────────────────────────────────
@app.route("/add_to_cart/<int:item_id>")
@login_required
def add_to_cart(item_id):
    db   = get_db()
    item = db.execute("SELECT * FROM food WHERE id=?", (item_id,)).fetchone()
    db.close()
    if item:
        cart = session.get("cart", [])
        cart.append({
            "id":    item["id"],
            "name":  item["name"],
            "price": item["price"]
        })
        session["cart"] = cart
        flash(f'"{item["name"]}" added to cart!', "success")
    return redirect(url_for("menu"))

@app.route("/cart")
@login_required
def cart():
    cart  = session.get("cart", [])
    total = sum(i["price"] for i in cart)
    return render_template("cart.html", cart=cart, total=total)

@app.route("/remove_from_cart/<int:index>")
@login_required
def remove_from_cart(index):
    cart = session.get("cart", [])
    if 0 <= index < len(cart):
        removed = cart.pop(index)
        session["cart"] = cart
        flash(f'"{removed["name"]}" removed from cart.', "success")
    return redirect(url_for("cart"))

@app.route("/clear_cart")
@login_required
def clear_cart():
    session["cart"] = []
    flash("Cart cleared.", "success")
    return redirect(url_for("cart"))

# ── CHECKOUT / PAYMENT ────────────────────────
@app.route("/checkout", methods=["GET", "POST"])
@login_required
def checkout():
    cart  = session.get("cart", [])
    total = sum(i["price"] for i in cart)
    if not cart:
        flash("Your cart is empty!", "error")
        return redirect(url_for("cart"))
    return render_template("checkout.html", cart=cart, total=total)

@app.route("/pay", methods=["POST"])
@login_required
def pay():
    cart = session.get("cart", [])
    if not cart:
        return redirect(url_for("cart"))

    db = get_db()
    for item in cart:
        db.execute(
            "INSERT INTO orders (user_id, item_name, status) VALUES (?,?,?)",
            (session["user_id"], item["name"], "Paid ✅")
        )
    db.commit()
    db.close()

    session["cart"] = []
    flash("Payment successful! Your order has been placed. 🎉", "success")
    return redirect(url_for("orders"))

# ── ORDERS ────────────────────────────────────
@app.route("/orders")
@login_required
def orders():
    db     = get_db()
    orders = db.execute(
        "SELECT * FROM orders WHERE user_id=? ORDER BY id DESC",
        (session["user_id"],)
    ).fetchall()
    db.close()
    return render_template("orders.html", orders=orders)

# ── ADMIN PANEL ───────────────────────────────
@app.route("/admin", methods=["GET", "POST"])
@admin_required
def admin():
    if request.method == "POST":
        name     = request.form["name"].strip()
        category = request.form["category"].strip()
        price    = request.form["price"].strip()
        image    = request.form["image"].strip()

        if not name or not price:
            flash("Name and price are required.", "error")
            return redirect(url_for("admin"))

        try:
            price = float(price)
        except ValueError:
            flash("Price must be a number.", "error")
            return redirect(url_for("admin"))

        db = get_db()
        db.execute("INSERT INTO food (name, category, price, image) VALUES (?,?,?,?)",
                   (name, category, price, image))
        db.commit()
        db.close()
        flash(f'"{name}" added to menu!', "success")
        return redirect(url_for("admin"))

    db    = get_db()
    items = db.execute("SELECT * FROM food ORDER BY id DESC").fetchall()
    db.close()
    return render_template("admin.html", items=items)

@app.route("/delete/<int:item_id>")
@admin_required
def delete_item(item_id):
    db = get_db()
    item = db.execute("SELECT name FROM food WHERE id=?", (item_id,)).fetchone()
    db.execute("DELETE FROM food WHERE id=?", (item_id,))
    db.commit()
    db.close()
    if item:
        flash(f'"{item["name"]}" deleted.', "success")
    return redirect(url_for("admin"))

if __name__ == "__main__":
    if not os.path.exists(DB):
        print("Run init_db.py first!")
    app.run(debug=True)