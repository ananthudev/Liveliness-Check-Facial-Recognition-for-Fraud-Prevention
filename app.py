from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('register.html', step=0)

@app.route('/register/', methods=['POST'])
def register():
    userDetails = request.form
    step = int(userDetails.get('step', 0))

    cur = mysql.connection.cursor()
    try:
        if step == 0:
            # Assuming you have a way to uniquely identify the user/session
            # Insert user data with step set to 1
            cur.execute("""INSERT INTO liveness 
                           (name, age, phno, dob, email, username, password, step) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, 1)""", 
                        (userDetails.get('name'), userDetails.get('age'), userDetails.get('phno'), 
                         userDetails.get('dob'), userDetails.get('email'), userDetails.get('username'), 
                         userDetails.get('password')))
            mysql.connection.commit()
            return redirect(url_for('id_form'))
    except Exception as e:
        mysql.connection.rollback()
        return f"Error: {e}"
    finally:
        cur.close()
    return redirect(url_for('home'))

@app.route('/id')
def id_form():
    # Optionally handle step increment here or in another route
    return render_template('id.html')

if __name__ == '__main__':
    app.run(debug=True)
