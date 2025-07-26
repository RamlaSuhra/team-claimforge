import os
import sys
from flask import Flask, render_template, request, redirect, url_for, session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.db_client import (
    SessionLocal,
    create_user,
    get_user_by_username,
    get_all_users,
    update_user_email,
    delete_user,
)

app = Flask(__name__)
app.secret_key = 'your_super_secret_key_here'  # 🔐 Change this in production

# --- Flask Routes ---

@app.route('/')
def root():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    message_type = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']   
        email = f"{username}"     

        db = SessionLocal()
        try:
            if get_user_by_username(db, username):
                message = "Username already exists."
                message_type = "error"
            else:
                create_user(db, username, email)
                message = "Registration successful! Please log in."
                message_type = "success"
        except Exception as e:
            db.rollback()
            message = f"Error during registration: {str(e)}"
            message_type = "error"
        finally:
            db.close()

    return render_template('register.html', message=message, message_type=message_type)


@app.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    message_type = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Not validated in this demo

        db = SessionLocal()
        try:
            user = get_user_by_username(db, username)
            if user:
                session['username'] = username
                return redirect(url_for('dashboard'))
            else:
                message = "Invalid username."
                message_type = "error"
        finally:
            db.close()

    return render_template('login.html', message=message, message_type=message_type)


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# --- Main Execution ---

if __name__ == '__main__':
    app.run(debug=True)
