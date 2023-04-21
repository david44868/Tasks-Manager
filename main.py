from flask import Flask, render_template, request, session, redirect, url_for
import pymysql
import mysql.connector


app = Flask(__name__)
app.secret_key = 'secret_key'

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('tasks'))
    else:
        return render_template('index.html')

@app.route('/signin', methods=['POST'])
def signin():
    username = request.form['username']
    session['username'] = username
    with get_connection() as conn, conn.cursor() as cursor:
        sql = "SELECT * FROM users WHERE username = %s"
        cursor.execute(sql, (session['username'],))
        result = cursor.fetchone()
        if result:
            print("wow")
        else:
            sql = "INSERT INTO users (username) VALUES (%s)"
            cursor.execute(sql, (session['username'],))
            conn.commit()

    return redirect('/')
    
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/add_tasks')
def add_tasks():
    if 'username' in session:
        return render_template('add_tasks.html')
    else:
        return redirect(url_for('index'))
    
@app.route('/get_db', methods=['POST', 'GET'])
def get_db():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        due_date = request.form['due_date']
        with get_connection() as conn, conn.cursor() as cursor:
            sql = "SELECT user_id FROM users WHERE username = %s"
            cursor.execute(sql, (session['username'],))
            result = cursor.fetchone()
            user_id = result[0]

            sql = "INSERT INTO tasks (user_id, title, description, status, due_date) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (user_id, title, description, status, due_date))
            conn.commit()

        return redirect(url_for('index'))
    return render_template('add_tasks.html')

def get_connection():
    # Establish a connection to the database
    conn = mysql.connector.connect(
        host='aws.connect.psdb.cloud',
        user='igsmntjrbaguthodb6uc',
        password='pscale_pw_CDaSfKpFCSfgmkV7NSA0vCoAFkruicoyZjSUu47yaMt',
        database='tasks_db',
        ssl_ca = "/etc/ssl/cert.pem",
        #cursorclass = pymysql.cursors.DictCursor
    )
    return conn

@app.route('/tasks')
def tasks():
    if 'username' in session:
        with get_connection() as conn, conn.cursor() as cursor:
            sql = "SELECT user_id FROM users WHERE username = %s"
            cursor.execute(sql, (session['username'],))
            result = cursor.fetchone()
            user_id = result[0]
            
            sql = "SELECT * FROM tasks WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            tasks = cursor.fetchall()

        return render_template('tasks.html', tasks=tasks)
    else:
        return render_template('index.html')

@app.route('/sort')
def sort():
    if 'username' in session:
        with get_connection() as conn, conn.cursor() as cursor:
            sql = "SELECT user_id FROM users WHERE username = %s"
            cursor.execute(sql, (session['username'],))
            result = cursor.fetchone()
            user_id = result[0]

            sort = request.args.get('sort')
            sql = f"SELECT * FROM tasks WHERE user_id = %s ORDER BY {sort}"
            cursor.execute(sql, (user_id,))
            tasks = cursor.fetchall()
        return render_template('tasks.html', tasks=tasks)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)