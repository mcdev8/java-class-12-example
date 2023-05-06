from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

def init_db():
    os.makedirs('db', exist_ok=True)
    conn = sqlite3.connect('db/example.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')

    c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'secret-password')")
    c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (2, 'Eddard', 'st@yAl1v3ForSsn2')")
    c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (3, 'Joffrey', 'aSuP3r$3cuR3P@ssW0rD')")
    c.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (3, 'Tyroin', 'NeverForgetWhatYouAre')")

    conn.commit()
    conn.close()


def query_db(query):
    conn = sqlite3.connect('db/example.db')
    cur = conn.cursor()
    cur.execute(query)
    results = cur.fetchall()
    conn.close()
    return results

# def query_db(query, args=(), one=False):
    conn = sqlite3.connect('db/example.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        results = query_db(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")

        if results:
            # Return user information as JSON for demonstration purposes
            if len(results) == 1:
                return render_template('home.html', userName=results[0][1])
            return render_template('hacked.html', userInfo=results)
            # return jsonify(results)
        else:
                return render_template('index.html', error='🔒 Login Failed')

    return render_template('index.html')



if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)


@app.route('/', methods=['POST'])
def login():
    # Get the username and password from the login form:
    username = request.form['username']
    password = request.form['password']
    # Check if there is a match in the database:
    results = query_db(f"SELECT * FROM users WHERE username='{username}' AND password='{password}'")
    # If there is a match, let the user login:
    if results:
        return render_template('home.html', userInfo=results)
    # If there is not a match re-render the login page with a message saying login failed
    else:
            return render_template('login.html', error='🔒 Login Failed')


