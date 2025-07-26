import os
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
# For session management, a secret key is required.
# In a real app, this should be a strong, random string from environment variables.
app.secret_key = 'your_super_secret_key_here' # **CHANGE THIS IN PRODUCTION**

# Path to the flat file where user data will be saved
USERS_FILE = 'users.txt' # Format: username,password\n

# --- Helper Functions for File Operations ---

def get_users():
    """Reads users from the USERS_FILE and returns a dictionary."""
    users = {}
    if not os.path.exists(USERS_FILE):
        return users # No file yet, no users

    with open(USERS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    username, password = line.split(',', 1) # Split only on the first comma
                    users[username] = password
                except ValueError:
                    # Handle malformed lines if any
                    print(f"Skipping malformed line in {USERS_FILE}: {line}")
    return users

def save_user(username, password):
    """Appends a new user to the USERS_FILE."""
    # Check if user already exists
    users = get_users()
    if username in users:
        return False # User already exists

    try:
        with open(USERS_FILE, 'a') as f:
            f.write(f"{username},{password}\n")
        return True
    except IOError as e:
        print(f"Error saving user to file: {e}")
        return False

# --- Flask Routes ---

@app.route('/')
def root():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles user registration."""
    message = None
    message_type = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            message = "Username and password are required."
            message_type = "error"
        elif save_user(username, password):
            message = "Registration successful! Please log in."
            message_type = "success"
            # Optional: Clear form fields after successful registration
            return render_template('register.html', message=message, message_type=message_type)
        else:
            message = "Username already exists or an error occurred."
            message_type = "error"

    return render_template('register.html', message=message, message_type=message_type)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login."""
    message = None
    message_type = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = get_users()

        if username in users and users[username] == password:
            # Successful login
            session['username'] = username # Store username in session
            return redirect(url_for('dashboard'))
        else:
            message = "Invalid username or password."
            message_type = "error"

    return render_template('login.html', message=message, message_type=message_type)

@app.route('/dashboard')
def dashboard():
    """Displays the home page after successful login."""
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login')) # Redirect to login if not logged in

@app.route('/logout', methods=['POST'])
def logout():
    """Logs out the user by clearing the session."""
    session.pop('username', None)
    return redirect(url_for('login'))

# --- Main execution ---
if __name__ == '__main__':
    # Ensure the 'templates' directory exists
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Ensure the users.txt file exists (or create it if not)
    if not os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'w') as f:
                pass # Just create the file if it doesn't exist
        except IOError:
            print(f"Warning: Could not create {USERS_FILE}. Check file permissions.")

    app.run(debug=True) # debug=True allows for automatic reloading and error messages