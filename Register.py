from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mypassword'
app.config['MYSQL_DB'] = 'mydatabase'

mysql = MySQL(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Validate input data
        if not name or not password or not confirm_password:
            flash('Please fill in all fields')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        # Create new user record in the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (name, password) VALUES (%s, %s)", (name, password))
        mysql.connection.commit()
        cur.close()

        flash('Account created successfully')
        return redirect(url_for('login'))

    return render_template('register.html')