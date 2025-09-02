from flask import Flask, render_template, request, redirect, flash, session
import sqlite3  # Use MySQL if needed
import os

app = Flask(__name__, template_folder='templates')  # Ensure templates folder is correctly set
app.secret_key = "secret_key"

# Database Connection
def connect_db():
    return sqlite3.connect("voting.db")

# Initialize database & create tables if they don't exist
def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS voters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            voter_id TEXT UNIQUE NOT NULL,
            has_voted BOOLEAN DEFAULT FALSE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            votes INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Run database initialization
initialize_db()

# Home Page (Registration)
@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        voter_id = request.form["voter_id"]

        conn = connect_db()
        cursor = conn.cursor()
        
        # Check if voter already registered
        cursor.execute("SELECT * FROM voters WHERE voter_id = ?", (voter_id,))
        if cursor.fetchone():
            flash("Voter ID already registered!", "error")
            return redirect("/")
        
        cursor.execute("INSERT INTO voters (name, voter_id) VALUES (?, ?)", 
                       (name, voter_id))
        conn.commit()
        conn.close()

        flash("Registration successful! You can now vote.", "success")
        return redirect("/vote")

    return render_template("index.html")

# Voting Page
@app.route("/vote", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        voter_id = request.form["voter_id"]
        candidate_id = request.form["candidate_id"]

        conn = connect_db()
        cursor = conn.cursor()

        # Check if voter exists and has already voted
        cursor.execute("SELECT has_voted FROM voters WHERE voter_id = ?", (voter_id,))
        voter = cursor.fetchone()
        
        if not voter:
            flash("You need to register before voting!", "error")
            return redirect("/vote")
        if voter[0]:  # If has_voted is True
            flash("You have already voted!", "error")
            return redirect("/vote")

        # Update vote count
        cursor.execute("UPDATE candidates SET votes = votes + 1 WHERE id = ?", (candidate_id,))
        cursor.execute("UPDATE voters SET has_voted = TRUE WHERE voter_id = ?", (voter_id,))
        conn.commit()
        conn.close()

        flash("Vote cast successfully!", "success")
        return redirect("/success")

    # Get candidates list
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()
    conn.close()

    return render_template("vote.html", candidates=candidates)

# Success Page
@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    # Ensure templates folder exists
    if not os.path.exists("templates"):
        os.makedirs("templates")

    # Ensure necessary template files exist
    for template in ["index.html", "vote.html", "success.html"]:
        template_path = os.path.join("templates", template)
        if not os.path.exists(template_path):
            with open(template_path, "w") as f:
                f.write(f"<h1>{template.replace('.html', '').capitalize()} Page</h1>")

    app.run(debug=True)
