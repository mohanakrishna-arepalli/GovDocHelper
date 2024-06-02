from flask import Flask, render_template, redirect, url_for, session, request, flash
import firebase_admin
from firebase_admin import credentials, auth
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebaseConfig.json")
firebase_admin.initialize_app(cred)

# Firebase Web API Key (found in Firebase project settings)
firebase_web_api_key = 'AIzaSyDPKO8m-t9isNnEqVqf5LnGoK2n9Kreahg'

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('adult_home' if session.get('age', 0) >= 18 else 'minor_home'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    dob = request.form['dob']

    # Use Firebase Authentication REST API to verify email and password
    login_url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebase_web_api_key}'
    login_payload = {
        'email': email,
        'password': password,
        'returnSecureToken': True
    }

    response = requests.post(login_url, json=login_payload)
    response_data = response.json()

    if response.status_code == 200:
        # User successfully logged in
        session['user'] = response_data['localId']
        
        # Calculate age based on the provided date of birth
        dob_date = datetime.strptime(dob, '%Y-%m-%d')
        age = (datetime.now() - dob_date).days // 365
        session['age'] = age

        # Redirect the user based on age
        if age >= 18:
            return redirect(url_for('adult_home'))
        else:
            return redirect(url_for('minor_home'))
    else:
        # Error occurred, display flash message
        error_message = response_data.get('error', {}).get('message', 'Unknown error')
        flash(f'Error: {error_message}', 'error')
        return redirect(url_for('index'))

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/create_account', methods=['POST'])
def create_account():
    email = request.form['email']
    password = request.form['password']

    try:
        # Create user in Firebase Authentication
        user = auth.create_user(email=email, password=password)

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('index'))
    except firebase_admin.auth.EmailAlreadyExistsError:
        flash('Email already exists.', 'error')
        return redirect(url_for('signup'))
    except firebase_admin.auth.AuthError as e:
        flash(f'Error creating user: {e}', 'error')
        return redirect(url_for('signup'))

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user', None)
    session.pop('age', None)
    return redirect(url_for('index'))

@app.route('/minor_home')
def minor_home():
    if 'user' in session:
        return render_template('minor_home.html')
    return redirect(url_for('index'))

@app.route('/adult_home')
def adult_home():
    if 'user' in session:
        return render_template('adult_home.html')
    return redirect(url_for('index'))
@app.route('/aadhaar')
def aadhaar():
    return render_template('aadhaar.html')

@app.route('/voter_id')
def voter_id():
    return render_template('voter_id.html')

@app.route('/pan_card')
def pan_card():
    return render_template('pan_card.html')

@app.route('/drivers_license')
def drivers_license():
    return render_template('drivers_license.html')

@app.route('/passport')
def passport():
    return render_template('passport.html')

@app.route('/ration_card')
def ration_card():
    return render_template('ration_card.html')

@app.route('/npr_card')
def npr_card():
    return render_template('npr_card.html')

@app.route('/employment_id')
def employment_id():
    return render_template('employment_id.html')

@app.route('/ppo')
def ppo():
    return render_template('ppo.html')

@app.route('/nrega_card')
def nrega_card():
    return render_template('nrega_card.html')

@app.route('/cghs_card')
def cghs_card():
    return render_template('cghs_card.html')

@app.route('/kisan_credit_card')
def kisan_credit_card():
    return render_template('kisan_credit_card.html')

@app.route('/posb_card')
def posb_card():
    return render_template('posb_card.html')

@app.route('/caste_certificate')
def caste_certificate():
    return render_template('caste_certificate.html')

@app.route('/income_certificate')
def income_certificate():
    return render_template('income_certificate.html')

if __name__ == '__main__':
    app.run(debug=True)