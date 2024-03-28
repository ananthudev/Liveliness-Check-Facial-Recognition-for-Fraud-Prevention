import datetime
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from PIL import Image # pillow for image manipulatipon, converting to image to base 64 and vice versa
import io
import os
import random
import base64 # module for converting raw image into base64 string
import pytesseract


from image_convert import convert_image_to_base64, save_base64_to_image
#imported image_converted module 

# Import the face extraction function
from face_extractor import extract_face_and_return_filepath

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






#App route for registration and save into database liveness and javascript for phone number exists
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
   
    return render_template('id.html')


# Image Upload route
@app.route('/id', methods=['POST'])
def upload_id():
    if 'username' not in session:
        return "User not logged in", 403

    username = session['username']
    files = request.files.getlist("id_images")

    if len(files) != 2:
        return jsonify({'success': False, 'message': "Please upload exactly two images."}), 400

    cur = mysql.connection.cursor()
    try:
        file_paths = []
        for index, file in enumerate(files):
            image = Image.open(file.stream)
            base64_str = convert_image_to_base64(image)
            image_type = 'front' if index == 0 else 'back'
            file_path = save_base64_to_image(base64_str, username, image_type)
            file_paths.append(file_path)

        #Insert into idcards table front, back and username
        cur.execute("""INSERT INTO idcards (username, front, back) VALUES (%s, %s, %s)
                       ON DUPLICATE KEY UPDATE front = VALUES(front), back = VALUES(back)""", 
                    (username, file_paths[0], file_paths[1]))
        
         # Extract, convert and save the face image from the front ID image
        profile_image_base64 = extract_face_and_return_filepath(file_paths[0], username)
        if profile_image_base64:
            profile_image_path = save_base64_to_image(profile_image_base64, username, "profile")
            # Update database with the profile image path
            cur.execute("""UPDATE idcards SET userprofileimage = %s WHERE username = %s""", (profile_image_path, username))
            



             # Retrieve phno for the username from the liveness table
            cur.execute("SELECT phno FROM liveness WHERE username = %s", [username])
            phno_result = cur.fetchone()

            if phno_result:
                phno = phno_result[0]
                # Update the step in the liveness table using the retrieved phno
                cur.execute("UPDATE liveness SET step = 2 WHERE phno = %s", [phno])
            else:
                mysql.connection.rollback()
                return jsonify({'success': False, 'message': "No phone number found for the given username."}), 400


            mysql.connection.commit()
            return jsonify({
                'success': True, 
                'message': "ID card and profile image uploaded successfully.",
                'frontImageUrl': url_for('static', filename=f'uploaded_images/{username}_front.png'),
                'backImageUrl': url_for('static', filename=f'uploaded_images/{username}_back.png')
            }), 200
        else:
            for path in file_paths:
                os.remove(path)  # Assuming the path is absolute
            mysql.connection.rollback()
            return jsonify({'success': False, 'message': "No face detected in the uploaded ID card. Please upload a clear ID card image with a visible face."}), 400
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'success': False, 'message': f"Error: {e}"}), 500
    finally:
        cur.close()





# Login Route
        
@app.route('/login/', methods=['POST'])
def login():
    phno = request.form['phno'] 
    password = request.form['password']
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM liveness WHERE phno = %s AND password = %s", (phno, password))
    
    if result > 0:
        userDetails = cur.fetchone()
        session['logged_in'] = True
        session['username'] = userDetails[5]

        # Redirect to the ID upload page upon successful login
        return jsonify({'success': 'Successfully logged in'}), 200
    else:
        return jsonify({'error': 'Invalid login credentials'}), 401


# Flask route that takes a mobile number, checks the current step for that number in your database, and returns the step to the client.
    
@app.route('/check_step', methods=['POST'])
def check_step():
    data = request.json
    phno = data.get('phno')
    
    if not phno:
        return jsonify({'error': 'Mobile number is required'}), 400
    
    cur = mysql.connection.cursor()
    cur.execute("SELECT step FROM liveness WHERE phno = %s", [phno])
    result = cur.fetchone()
    
    if result:
        step = result[0]
        return jsonify({'step': step})
    else:
        return jsonify({'error': 'Mobile number not found'}), 404


#Liveness flask route
@app.route('/generate_otp')
def generate_otp():
    # Generate a random 4-digit OTP
    otp = random.randint(1000, 1001)
    # Store the OTP in the session for later verification
    session['otp'] = otp

    # Assume 'username' is available in the session
    username = session.get('username')
    if username:
        cur = mysql.connection.cursor()
        try:
            # Save the OTP in the database for the given user
            cur.execute("UPDATE liveness SET otp = %s WHERE username = %s", (otp, username))
            mysql.connection.commit()
        except Exception as e:
            print(e)
            mysql.connection.rollback()

    return render_template('otp_display.html', otp=otp)



@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    username = session.get('username')
    if not username:
        return jsonify({'error': 'Session or username missing'}), 400

    image_file = request.files['image']
    image_base64 = convert_image_to_base64(Image.open(image_file.stream))
    # Save in the 'liveness' directory
    image_path = save_base64_to_image(image_base64, username, 'liveliness', directory="liveness")

    if not image_path:
        return jsonify({'error': 'Image saving failed'}), 500

    # Save the image path to the database immediately after it's generated
    cur = mysql.connection.cursor()
    try:
        cur.execute("UPDATE liveness SET liveness_image_path = %s WHERE username = %s", (image_path, username))
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({'error': 'Failed to update image path in database'}), 500

    # Proceed with OTP verification
    try:
        extracted_text = pytesseract.image_to_string(Image.open(os.path.join('static', image_path)))
        otp = session.get('otp')

        if str(otp) in extracted_text:
            # Update status to 'OTP verified' if OTP matches
            cur.execute("UPDATE liveness SET status = 'OTP verified' WHERE username = %s", [username])
            mysql.connection.commit()
            return jsonify({'success': True, 'message': 'Liveliness check passed.'})
        else:
            # Update status to 'OTP failed' if OTP does not match
            cur.execute("UPDATE liveness SET status = 'OTP failed' WHERE username = %s", [username])
            mysql.connection.commit()
            return jsonify({'success': False, 'message': 'OTP does not match.'})
    except Exception as e:
        mysql.connection.rollback()  # Roll back in case of any exception
        return jsonify({'error': str(e)}), 500









if __name__ == '__main__':
    app.run(debug=True)









