from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ganti dengan kunci rahasia yang aman

client = MongoClient('mongodb://localhost:27017/')
db = client['Showroom_Mobil']
collection = db['test_drive_booking']
users_collection = db['user']

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return render_template('index(blmlogin).html')

@app.route('/byd')
def byd():
    return render_template('BYD.html')

@app.route('/show_byd')
def show_byd():
    list_data_schedule = collection.find()
    return render_template("ShowBYD.html", data_schedule=list_data_schedule)

@app.route('/BMWF82')
def BMWF82():
    return render_template('BMWF82.html')

@app.route('/LamborghiniSián')
def LamborghiniSián():
    return render_template('LamborghiniSián.html')

@app.route('/LamborghiniCountach')
def LamborghiniCountach():
    return render_template('LamborghiniCountach.html')

@app.route('/schedule_drive', methods=['POST'])
def schedule_drive():
    username = request.form['i_username']
    email = request.form['i_email']
    car = request.form['i_cars']
    scheduleDateTime = request.form['i_scheduleDateTime']
    data = {
        'username': username,
        'email': email,
        'car': car,
        'scheduleDateTime': scheduleDateTime
    }
    collection.insert_one(data)
    return redirect('/show_byd')

@app.route('/edit_BYD/<id>')
def edit_BYD(id):
    schedule = collection.find_one({'_id': ObjectId(id)})
    return render_template('edit_BYD.html', schedule=schedule)

@app.route('/update_schedule/<id>', methods=['POST'])
def update_schedule(id):
    username = request.form['username']
    email = request.form['email']
    car = request.form['car']
    scheduleDateTime = request.form['scheduleDateTime']
    data = {
        'username': username,
        'email': email,
        'car': car,
        'scheduleDateTime': scheduleDateTime
    }
    collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    return redirect('/show_byd')

@app.route('/delete_schedule/<id>', methods=['POST'])
def delete_schedule(id):
    collection.delete_one({'_id': ObjectId(id)})
    return redirect('/show_byd')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        user_data = {
            'username': username,
            'email': email,
            'password': hashed_password
        }
        users_collection.insert_one(user_data)
        flash('Registrasi berhasil, silakan login.')
        return redirect(url_for('login'))
    return render_template('registrasi.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Login berhasil.')
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    print("Logout route accessed.")
    if 'username' in session:
        session.pop('username', None)
        flash('Logout berhasil.')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
