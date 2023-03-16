from flask import Flask, render_template, request
import psycopg2
import os
from dotenv import load_dotenv
import hashlib


load_dotenv()
app = Flask(__name__)
app.debug = True


db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
db_name = os.getenv("POSTGRES_DB")
db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")

# connnecting to db
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)

# creating table if doesn't exists
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(80) UNIQUE,
        password VARCHAR(80)
    )
""")
conn.commit()

# Main page
@app.route("/")
def index():
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    return str(rows)

# Register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Recieving data from form
        username = request.form["username"]
        password = request.form["password"]

        password_bytes = password.encode('utf-8')

        # Hash the password bytes using the SHA-256 algorithm
        hashed_bytes = hashlib.sha256(password_bytes)

        # Convert the hashed bytes to a hexadecimal string
        hashed_password = hashed_bytes.hexdigest()

        # input values to db
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        """, (username, hashed_password))
        conn.commit()

        # relocate to confirming registration page
        return render_template("register_success.html")
    else:
        return render_template("register.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')