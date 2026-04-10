from flask import Blueprint, render_template, request, flash, session
from .model_db import Client
from . import db, mail, Message
from config import ConfigDetails
from datetime import datetime


home_page = Blueprint('home', __name__)

@home_page.route('/', methods=['GET', 'POST'],)
def home():
    """data = ['''For him who has conquered the mind, the mind is the best of friends;
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
    #return render_template("home.html", items=data)"""
    return render_template("home.html")

@home_page.route('/fee')
def fee():
    return render_template('fee.html')

#def get_html():
 
#    return render_template("email.html")

def send_email(name, last, email, phone, country):
    msg = Message(
        subject="New Client Submission",
        sender=ConfigDetails.MAIL_USERNAME,
        recipients=[email]
    )

    msg.html = render_template(
    "email.html",
    firstName=name,
    lastName=last,
    email=email,
    phone=phone,
    country=country
)
    mail.send(msg)
    return "Email sent successfully!"

@home_page.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@home_page.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        email = request.form['email'].strip(),
        firstName = request.form['firstName'].strip(),
        lastName = request.form['lastName'].strip(),
        phone = request.form['phone'].strip(),
        resident = request.form['resident']
        if resident == "No":
            country = request.form['country']
            data = Client(
                email = request.form['email'],
                firstName = request.form['firstName'],
                lastName = request.form['lastName'],
                age = request.form['age'],
                occupation = request.form['occupation'],
                phone = request.form['phone'],
                alt_phone = request.form['alt_phone'],
                resident = request.form['resident'],
                country = request.form['country'],
                insurance = request.form['insurance'],
                reason = request.form['reason'],
                past = request.form['past'],
                message = request.form['message'],
                created_at = datetime.now()
            )
        else:
            country = "India"
            data = Client(
                email = request.form['email'],
                firstName = request.form['firstName'],
                lastName = request.form['lastName'],
                age = request.form['age'],
                occupation = request.form['occupation'],
                phone = request.form['phone'],
                alt_phone = request.form['alt_phone'],
                resident = request.form['resident'],
                country = "India",
                insurance = request.form['insurance'],
                reason = request.form['reason'],
                past = request.form['past'],
                message = request.form['message'],
                created_at = datetime.now()
            )

        db.session.add(data)
        db.session.commit()
        
        #clients = Client.query.all()
        #return render_template('user_data.html', clients=clients)
        send_email(firstName[0], lastName[0], email[0], phone[0], country)
        return render_template('submit_ack.html')
        
    return render_template('booking.html')

@home_page.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['password']
        if username == "mini" and password == "mini_123":
            clients = Client.query.all()
            return render_template('user_data.html', clients=clients)
    return render_template('admin.html')

@home_page.route('/consent', methods=['GET', 'POST'])
def consent():
    return render_template('consent.html')


