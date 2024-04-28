Here's a complete setup for a Flask application with MongoDB, using Docker containers and a user-defined network for communication.

**Folder Structure:**
```
website/
├── app.py
├── Dockerfile
├── requirements.txt
└── templates/
    ├── index.html
    └── register.html
database/
└── Dockerfile

```

**1. `app.py`**:
```python
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://mongodb:27017/")  # "mongodb" is the name of the MongoDB service in the Docker Compose file
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
```

**2. `Dockerfile` for Flask App:**
```Dockerfile
# Use the official Python image as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask and other dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]
```

**3. `Dockerfile.mongodb` for MongoDB Container:**
```Dockerfile
# Use the official MongoDB image
FROM mongo

# Expose MongoDB port
EXPOSE 27017

# Create a directory to store MongoDB data
RUN mkdir -p /data/db
```

**4. `requirements.txt`** (for Flask dependencies):
```
Flask
pymongo
```

**5. `index.html` (inside `templates` folder):**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Sign In</title>
    <!-- CSS styles here -->
</head>
<body>
    <form action="/signin" method="post">
        <h2>Instagram Sign In</h2>
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <input type="submit" value="Sign In">
    </form>
    <p>Don't have an account? <a href="/register">Register</a></p>
</body>
</html>
```

**6. `register.html` (inside `templates` folder):**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Register</title>
    <!-- CSS styles here -->
</head>
<body>
    <form action="/register" method="post">
        <h2>Register</h2>
        <input type="text" name="username" placeholder="Username" required>
        <input type="password" name="password" placeholder="Password" required>
        <input type="submit" value="Register">
    </form>
    <p>Already have an account? <a href="/">Sign In</a></p>
</body>
</html>
```

**Build and Run Commands:**
1. Build the MongoDB container and attach it to the user-defined network:
    ```bash
    docker build -t mongodb -f Dockerfile.mongodb .
    docker network create instagram_network
    docker run -d --name mongodb -v mongodb_data:/data/db --network instagram_network mongodb
    ```

2. Build the Flask app container and attach it to the user-defined network:
    ```bash
    docker build -t flaskapp .
    docker run -d -p 5000:5000 --name flaskapp --network instagram_network flaskapp
    ```

Now, both containers are connected through the `instagram_network` network, and they can communicate with each other without using the deprecated `--link` flag. Your Flask application should be accessible at `http://localhost:5000`, and you can register new users and sign in with existing ones. All user data will be stored in the MongoDB container.