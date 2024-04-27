from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    password = request.form['password']

    if len(username) == 0 or len(password)==0:
        return "Invalid Input"
    
    with open('data/usernames.json','r') as file:
        data = json.load(file)
    row = {'username':username,'password':password}
    data.append(row)
    with open('data/usernames.json','w') as file:
        json.dump(data,file)
        
    return f"Your registration is sucessful {username}"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')