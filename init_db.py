import sqlite3

conn = sqlite3.connect("database.db")
c    = conn.cursor()

# ── USERS TABLE ───────────────────────────────
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT    UNIQUE NOT NULL,
    password TEXT    NOT NULL,
    role     TEXT    NOT NULL DEFAULT 'user'
)
""")

# ── FOOD TABLE ────────────────────────────────
c.execute("""
CREATE TABLE IF NOT EXISTS food (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name     TEXT    NOT NULL,
    category TEXT,
    price    REAL    NOT NULL,
    image    TEXT
)
""")

# ── ORDERS TABLE ──────────────────────────────
c.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id   INTEGER NOT NULL,
    item_name TEXT    NOT NULL,
    status    TEXT    DEFAULT 'Paid'
)
""")

# ── SEED DATA ─────────────────────────────────
# Default admin account
c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?,?,?)",
          ("admin", "admin123", "admin"))

# Default user account
c.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?,?,?)",
          ("user1", "user123", "user"))

# Sample food items
sample_food = [
    ("Paneer Tikka",         "Snacks",      180, "https://imgs.search.brave.com/6gbzkHA545cplU1Rhz9HctSfsdHFc8g9uMJ6uIMh0b0/rs:fit:0:180:1:0/g:ce/aHR0cHM6Ly90My5m/dGNkbi5uZXQvanBn/LzA4LzM0LzcyLzk2/LzM2MF9GXzgzNDcy/OTY1NV90YTVNRlNy/RHRMVm5aaTRRczFq/WW94UkNEMVFzckly/TC5qcGc"),
    ("Veg Biryani",      "Main Course", 280, "https://imgs.search.brave.com/4x2By9BHxQ54CUJI8DBNPDnimf1AkNjoABy8wOmw4Lk/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTI5/MjQ0Mjg1MS9waG90/by90cmFkaXRpb25h/bC1oeWRlcmFiYWRp/LXZlZ2V0YWJsZS12/ZWctZHVtLWJpcnlh/bmktd2l0aC1taXhl/ZC12ZWdnaWVzLXNl/cnZlZC13aXRoLW1p/eGVkLXJhaXRhLndl/YnA_YT0xJmI9MSZz/PTYxMng2MTImdz0w/Jms9MjAmYz1ZVFFr/ZFVmcjJQQ25jSm14/c2Fpamh4aTJ4UTdn/dGZRRkI1X0VHbUMx/TkY0PQ"),
    ("Dal Makhani",          "Main Course", 220, "https://imgs.search.brave.com/iOsKTR5Ultw8uL15ihgYSOJwDSgxwOVuNHt5l-RKZKg/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly93d3cu/Y29va3dpdGhtYW5h/bGkuY29tL3dwLWNv/bnRlbnQvdXBsb2Fk/cy8yMDE1LzAxL0Ny/ZWFteS1SZXN0YXVy/YW50LVN0eWxlLURh/bC1NYWtoYW5pLmpw/Zw"),
    ("Gulab Jamun",          "Desserts",    80,  "https://imgs.search.brave.com/HfmyXxWJgf3xOWmqD_Tb7rJ1MbykrklEM1pCVpI2REI/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly90My5m/dGNkbi5uZXQvanBn/LzE2LzQ1LzI3LzQy/LzM2MF9GXzE2NDUy/NzQyNzFfa3ZOYnRz/MWE2N2szZDBKd0Ny/bjFSSmd3dTVwY3hY/UXMuanBn"),
    ("Mango Lassi",          "Beverages",   70,  "https://imgs.search.brave.com/LlNxom1-0x2mFA0GD-jNJ5_gVvSU0SSo_27lBRdlWog/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9yYWtz/a2l0Y2hlbi5uZXQv/d3AtY29udGVudC91/cGxvYWRzLzIwMTQv/MDUvMTQwMzM2OTA5/OThfZDQ5NWI5Yzc2/Ml96LmpwZw"),
    ("Masala Dosa",          "Snacks",      120, "https://imgs.search.brave.com/crbrtbRwDMlIio0LsPGrG7wVuK1d1zD_D9iOdhEo2x4/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly90aHVt/YnMuZHJlYW1zdGlt/ZS5jb20vYi9zb3V0/aC1pbmRpYW4tbWFz/YWxhLWRvc2Etc2Ft/YmFyLWNvY29udXQt/Y2h1dG5leS1jcmlz/cHktc2VydmVkLXll/bGxvdy10cmF5LTQ0/NDM5NzcxMy5qcGc"),
    ("Chocolate Brownie",    "Desserts",    120, "https://imgs.search.brave.com/o31IAlaS1UuYv1NYt2BRVwKo92AwWZi060c6CyCMinU/rs:fit:500:0:1:0/g:ce/aHR0cHM6Ly9tZWRp/YS5pc3RvY2twaG90/by5jb20vaWQvMTE2/NDI4OTk4OS9waG90/by9jaG9jb2xhdGUt/YnJvd25pZXMtb24t/ZGFyay1icm93bi10/YWJsZS5qcGc_cz02/MTJ4NjEyJnc9MCZr/PTIwJmM9ZU80bmJX/VWdSbHRfYWdQc1BT/Q3NkSFVjeGFRbGQz/Rm8zbUdjZFp0bWpi/OD0"),
]

for item in sample_food:
    c.execute("INSERT OR IGNORE INTO food (name, category, price, image) VALUES (?,?,?,?)", item)

conn.commit()
conn.close()
print("=" * 40)
print("  Database Ready!")
print("=" * 40)
print("  Admin  → username: admin  | password: admin123")
print("  User   → username: user1  | password: user123")
print("=" * 40)