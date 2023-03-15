from flask import Flask, render_template, request
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.debug = True
# connecting to db, i don't ave something important there :)
db_host = os.getenv("POSTGRES_HOST")
db_port = "5432"
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

        # input values to db
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        """, (username, password))
        conn.commit()

        # relocate to confirming registration page
        return render_template("register_success.html")
    else:
        return render_template("register.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0')