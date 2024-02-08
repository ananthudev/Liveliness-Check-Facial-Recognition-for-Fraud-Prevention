from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import os

app = Flask(__name__)


# Secret key for session management
app.secret_key = os.urandom(24)

# MySQL connection configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'project'

mysql = MySQL(app)

@app.route('/')
def home():
    # Initial landing page
    return render_template('register.html', step=0)


#App route for registration


@app.route('/register/', methods=['POST'])
def register():
    userDetails = request.form
    
    phno = userDetails.get('phno')
    cur = mysql.connection.cursor()
    cur.execute("SELECT COUNT(*) FROM liveness WHERE phno = %s", [phno])
    if cur.fetchone()[0] > 0:
        # Phone number exists, return an error message for the frontend to catch
        return jsonify({'error': 'User with this phone number already exists'}), 400

    username = userDetails.get('username')
    session['username'] = username  
    
    try:
        cur.execute("""INSERT INTO liveness 
                       (name, age, phno, dob, email, username, password, step) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, 1)""", 
                    (userDetails.get('name'), userDetails.get('age'), phno, 
                     userDetails.get('dob'), userDetails.get('email'), username, 
                     userDetails.get('password')))
        mysql.connection.commit()
        return jsonify({'success': True})
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/id')
def id_form():
    #  image upload
    return render_template('id.html')

@app.route('/id', methods=['POST'])
def upload_id():
    if 'username' not in session:
        return "User not logged in", 403

    username = session['username']
    files = request.files.getlist("id_images")

    if len(files) != 2:
        return "Please upload exactly two images.", 400

    front_image = files[0].read()
    back_image = files[1].read()

    cur = mysql.connection.cursor()
    try:
        cur.execute("""INSERT INTO idcards (front, back, username) 
                       VALUES (%s, %s, %s)
                       ON DUPLICATE KEY UPDATE front = VALUES(front), back = VALUES(back)""", 
                    (front_image, back_image, username))
        
         # Update the step in the liveness table for the username
        cur.execute("""UPDATE liveness SET step = 2 
                       WHERE username = %s""", [username])
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        return f"Error: {e}"
    finally:
        cur.close()

    return "Images uploaded successfully."


if __name__ == '__main__':
    app.run(debug=True)

# #New new for phone number validation
# @app.route('/validate_phno', methods=['POST'])
# @app.route('/validate_phno', methods=['POST'])
# def validate_phno():
#     phno = request.json['phno']  # Adjusted to handle JSON request
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT COUNT(1) FROM liveness WHERE phno = %s", [phno])
#     exists = cur.fetchone()[0] > 0
#     return jsonify({'exists': exists})  # Correctly return JSON response







