from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user data (in real world scenario, this would come from a database)
users = {
    'user1': 'password1',
    'user2': 'password2',
    'user3': 'password3'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']
    
    if username in users and users[username] == password:
        return f'Welcome, {username}!'
    else:
        return 'Invalid username or password. Please try again.'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')