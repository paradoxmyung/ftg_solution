import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 비밀 키 설정

def init_db():
    with sqlite3.connect("users.db") as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
    print("Database Session Ready")

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

def add_user(username, password):
    print("def user starts.")
    with sqlite3.connect("users.db") as conn:
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
def get_users():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.execute('SELECT username FROM users')
        return [row[0] for row in cursor.fetchall()]

@app.route('/', methods=['GET', 'POST'])
def register():
    print("Register function called") 
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if add_user(username, password):
            flash(f'User {username} is registered successfully!', 'success')
        else:
            flash(f'Username {username} is already taken.', 'danger')
        return redirect(url_for('register'))
    users = get_users()
    return render_template('register.html', form=form, users=users)

if __name__ == '__main__':
    init_db()  
    app.run(debug=True)
