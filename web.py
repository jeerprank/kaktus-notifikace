# Import Flask and SQLite
from flask import Flask, render_template
import sqlite3

# Import your code as a module
import main

# Create a Flask app
app = Flask(__name__)

# Create a SQLite database connection
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Create a table to store the email history
cursor.execute("""CREATE TABLE IF NOT EXISTS email_history (
    id INTEGER PRIMARY KEY,
    subject TEXT,
    body TEXT,
    timestamp TEXT
)""")
conn.commit()

# Define a route for the home page
@app.route("/")
def index():
    # Get the server status from your code
    server_status = main.check_server_status()
    # Get the last email from the database
    cursor.execute("SELECT * FROM email_history ORDER BY id DESC LIMIT 1")
    last_email = cursor.fetchone()
    # Render the index.html template with the data
    return render_template("index.html", server_status=server_status, last_email=last_email)

# Define a function to run the check_new_posts function as a background task
def run_check_new_posts():
    # Use the APScheduler library to schedule the check_new_posts function every 10 seconds
    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(main.check_new_posts, 'interval', seconds=10)
    scheduler.start()

# Run the app in debug mode and start the background task
if __name__ == "__main__":
    run_check_new_posts()
    app.run(debug=True)
