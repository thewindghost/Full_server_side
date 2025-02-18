from flask import Flask, render_template, render_template_string, request, jsonify, session, redirect, url_for
import json
import os
# bleach not import bleach clean, can secure attack xss but not clear regex 
from bleach import clean
import subprocess
from flask_login import LoginManager


app = Flask(__name__, static_url_path="/", static_folder="static")

app.config['SECRET_KEY'] = os.urandom(32)

data_file_user = "json_information/users.json"
data_file_admin = "json_information/admins.json"

#credetial login users
def valid_login_user(username, password):
    valid_user = {
        "guest": "guest123",
        "bug hunter": "bughunter",
        "john hardler": "john4115151",
        "<script>alert(1)</script>": "test",
        "{{cycler.__init__.__globals__.os.popen('whoami').read()}}" : "test"
    }
    return username in valid_user and valid_user[username] == password

def valid_login_admin(username, password):
    valid_admin = {
        "admin": "admin123",
        "john hardler": "john4115151",
        "root": "root123"
    }
    return username in valid_admin and valid_admin[username] == password

def load_data(file_path):

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return 'Not Found 404', 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update-balance', methods=['GET', 'POST'])
def update_balance():

    error = None
    balances = request.form.get('balance', '')

    if request.method == 'GET' and 'username' in session:
        return render_template('wallet.html')
    
    try:
        if request.method == 'POST' and 'username' in session:
            wallet = clean(balances)
            balance = clean(wallet)
            # Remote Code Execution Basic(RCE)
            #exec(balance)
            eval(balance)
            #subprocess.run(balance, shell=True)
            return render_template(f'wallet.html', balance=balance) 
        
    except 'username' in session and Exception as e :
            error = str(e)
            return render_template(f'wallet.html', error=error)

    return redirect(url_for('index'))

@app.route('/my-profile', methods=['GET', 'POST'])
def my_profile():

    # Server-Side Template Injection Attack Basic(SSTI) but defen scanner bug
    if request.method == 'GET' and 'username' in session:
        username = request.args.get('path', '')
        return render_template('profile_user.html', template_rendered=clean(render_template_string(session['username'])) , username=username)

    if request.method == 'POST' and 'username' in session:
        data = request.form.get('path', '')
        return render_template('profile_user.html', data=data)
    else:
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = clean(request.form.get('password', ''))
    
        if valid_login_user(username, password):
            session['username'] = username
            return redirect(url_for('dashboard'))
        
        if valid_login_admin(username, password):
            session['username'] = username
            return redirect(url_for('admin_panel'))

        else:
            error = 'Invalid Username/Password'
    # if not using method POST
    return render_template('login.html', error=error) 

@app.get('/dashboard')
def dashboard():

    name_user = request.args.get('name', '')
    data = load_data(data_file_user)
    username = data.get(name_user)

    if username:
        return jsonify(username)
    
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])

    return redirect(url_for('index'))

@app.get('/admin-panel-131315315211')
def admin_panel():
        
    # brute force attack IDOR
    id = request.args.get('id', '')
    data = load_data(data_file_admin)
    admin_id = data.get(str(id))

    if 'username' in session:
        return render_template('control_panel.html')

    try:
        if admin_id:
            return jsonify(admin_id)
    
    except Exception as e:
        error = str(e)
        return redirect(url_for(admin_panel, error=error))

    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():

    error = None

    if request.method == 'POST':
        try:
            username = request.form.get('username', '').strip()
            password = clean(request.form.get('password', '')).strip()
            email = clean(request.form.get('email', ''))
            first_name = clean(request.form.get('first_name', ''))
            last_name = clean(request.form.get('last_name', ''))
            number_phone = clean(request.form.get('number_phone', ''))
            website_company = clean(request.form.get('website_company', ''))
            birth_year = clean(request.form.get('birth_year', ''))
            success = True
            return render_template('register.html', username=username, password=password, email=email, first_name=first_name, last_name=last_name, number_phone=number_phone, website_company=website_company, birth_year=birth_year, success=success)

        except Exception as e:
            error = str(e)
            return render_template('register.html', error=error)

    return render_template('register.html')

@app.get('/logout')
def logout():

    session.clear()
    response = redirect(url_for('index'))
    response.delete_cookie('session')
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4100)
