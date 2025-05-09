import os
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Appointment Model
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    speciality = db.Column(db.String(50), nullable=False)
    slot = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)

# Route to render HTML form
@app.route('/')
def index():
    return render_template('form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    age = request.form['age']
    phone = request.form['phone']
    speciality = request.form['speciality']
    slot = request.form['slot']
    date = request.form['appointment_date']

    new_appointment = Appointment(
        name=name,
        age=age,
        phone=phone,
        speciality=speciality,
        slot=slot,
        date=date
    )

    db.session.add(new_appointment)
    db.session.commit()

    return redirect(url_for('confirmation'))  # Redirect to a confirmation page

# Route to display confirmation message
@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')  # You can create a 'confirmation.html' file for this page

if __name__ == '__main__':
    app.run(debug=True)
