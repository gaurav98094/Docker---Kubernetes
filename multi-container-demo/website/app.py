from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://mongodb:27017/")  
db = client["instagram"]
users_collection = db["users"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    
    user = users_collection.find_one({'username': username, 'password': password})
    if user:
        return f'Welcome, {username}!'
    else:
        return 'Invalid username or password. Please try again.'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username already exists
        if users_collection.find_one({'username': username}):
            return 'Username already exists. Please choose another one.'
        
        # Insert new user into the database
        users_collection.insert_one({'username': username, 'password': password})
        return redirect(url_for('index'))
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
