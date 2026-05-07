# Online Food Ordering System

A web-based application that allows users to browse food items, add them to a cart, and place orders. The system implements role-based access control, where administrators manage food items and users interact with the ordering process.

---

## Overview

This project demonstrates core software engineering concepts such as authentication, database design, and modular backend development using Flask. It provides a structured approach to handling food ordering workflows in a simple and efficient manner.

---

## Features

### User
- User registration and login
- Browse food items with images
- Search food by name
- Add items to cart
- View cart with total price
- Place orders (payment simulation)
- View order history

### Admin
- Add food items with image URL
- Delete food items
- Manage menu dynamically

---

## Technology Stack

- Backend: Flask (Python)
- Frontend: HTML, CSS (Jinja2 Templates)
- Database: SQLite
- Authentication: Session-based

---

## Project Structure

food-ordering/
│
├── app.py              # Main Flask application
├── init_db.py          # Database initialization
├── database.db         # SQLite database
│
├── static/
│   └── style.css       # Styling
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── admin.html
│   ├── menu.html
│   ├── cart.html
│   └── orders.html

---

## Installation and Setup

1. Clone the repository

git clone https://github.com/rishi-1510/online_food_ordering.git  
cd online_food_ordering

2. Install dependencies

pip install flask

3. Initialize database

python init_db.py

4. Run the application

python app.py

5. Open in browser

http://127.0.0.1:5000

---

## Usage

- Register as admin to add food items  
- Register as user to browse and order food  
- Add items to cart and proceed to checkout  
- Simulate payment to place order  

---

## Limitations

- Payment system is simulated  
- Basic authentication (no encryption)  
- No real-time order tracking  

---

## Future Improvements

- Integration with real payment gateway  
- Improved authentication (password hashing, JWT)  
- Real-time order tracking  
- Mobile responsive UI  




