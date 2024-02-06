from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

# For loading teh form
@app.route('/')
def form():
    return render_template('form.html')

# Action of the form
@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        username = userDetails['username']
        password = userDetails['password']
        email = userDetails['email'] 
        dob = userDetails['dob']  
        
        cur = mysql.connection.cursor()

        # Sql query

        cur.execute("INSERT INTO liveness (username, password , email, dob) VALUES(%s, %s, %s , %s)", (username, password, email, dob))
        mysql.connection.commit()
        cur.close()
        # return 'success'
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
