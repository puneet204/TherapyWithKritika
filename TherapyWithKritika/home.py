from flask import Blueprint, render_template, request, flash, session
from .model_db import Client, New_User
from . import db

home_page = Blueprint('home', __name__)

@home_page.route('/', methods=['GET', 'POST'],)
def home():
    data = ['''For him who has conquered the mind, the mind is the best of friends;
but for one who has failed to do so, the mind will remain the greatest enemy. \n - Bhagavad Gita (Chapter 6, Verse 6)''',
            'A person is made by their belief. As they believe, so they become. \n - Bhagavad Gita (Chapter 17, Verse 3)',
            'One who has controlled the mind and senses finds peace.\n - Bhagavad Gita (Chapter 17)',
            'You have a right to perform your duties, but not to the fruits of your actions.\n - Bhagavad Gita (Chapter 2, Verse 47)',
            'The good life is a process, not a state of being. It is a direction, not a destination. \n- Carl Rogers',
            'In any given moment, we have two options: to step forward into growth or to step back into safety.\n- Abraham Maslow',
            'What lies behind us and what lies before us are tiny matters compared to what lies within us.\n- Ralph Waldo Emerson',
            'I am not what happened to me, I am what I choose to become. - Carl Jung',
            'When we are no longer able to change a situation, we are challenged to change ourselves. - Viktor Frankl',
            'Between stimulus and response there is a space. In that space is our power to choose our response. - Viktor Frankl',
            'The curious paradox is that when I accept myself just as I am, then I can change. - Carl Rogers',
            'The best years of your life are the ones in which you decide your problems are your own. - Albert Ellis',
            'The act of revealing oneself fully to another and still being accepted may be the major vehicle of therapeutic help. - Irvin Yalom'
            ]
    return render_template("home.html", items=data)

@home_page.route('/fee')
def fee():
    return render_template('fee.html')

@home_page.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@home_page.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        data1 = New_User(
            email = request.form['email'],
            name = request.form['name'],
            uname = request.form['uname'],
            password1 = request.form['password1'],
            password2 = request.form['password2']
        )

        if data1.password1 == data1.password2:
            db.session.add(data1)
            db.session.commit()

            return render_template('user_login.html')        
    
    return render_template('sign_up.html')

@home_page.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        return render_template('login.html')

@home_page.route('/individual_booking', methods=['GET', 'POST'],)
def individual_booking():
    if request.method == 'POST':
        data = Client(
            email = request.form['email'],
            name = request.form['name'],
            age = request.form['age'],
            occupation = request.form['occupation'],
            phone = request.form['phone'],
            alt_phone = request.form['alt_phone'],
            resident = request.form['resident'],
            insurance = request.form['insurance'],
            concern = request.form['concern'],
            goal = request.form['goal'],
            past = request.form['past']
        )

        db.session.add(data)
        db.session.commit()

        return render_template('submit_ack.html')

    return render_template("individual_booking.html")

@home_page.route('/user_data', methods=['GET', 'POST'])
def user_data():
    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('password')

        if username == "Mini" and password == "Mini_12345":
            clients = Client.query.all()
            return render_template('user_data.html', clients=clients)
        else:
            return render_template('login.html')
    return render_template('login.html')
