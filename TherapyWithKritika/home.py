from flask import Blueprint, render_template, request, flash, session, url_for, redirect
from .model_db import Client, Users, Notes
from . import db, mail, Message
from config import ConfigDetails
from datetime import datetime
from markupsafe import escape
import os
from pathlib import Path


home_page = Blueprint('home', __name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(BASE_DIR, "static", "downloads", "Client_Note.txt")

#file_path = Path(home_page.static_folder)
#print(file_path) #/ "downloads"
#file_path.parent.mkdir(parents=True, exist_ok=True)

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

def send_email(**kwargs):#name, last, email, phone, country, filename):
    name = kwargs.get('name')
    last = kwargs.get('last')
    email = kwargs.get('email')
    phone = kwargs.get('phone')
    country = kwargs.get('country')
    email_file = kwargs.get('email_file')
    filename = kwargs.get('filename')
    subject = kwargs.get('subject')

    msg = Message(
        subject=subject,
        sender="therapywithkritikazutshi@gmail.com", #ConfigDetails.MAIL_USERNAME,
        recipients=[email],
        bcc=['puneet1234bhat@gmail.com'] #ConfigDetails.MAIL_BCC
    )

    msg.html = render_template(
    email_file,
    firstName=name,
    lastName=last,
    email=email,
    phone=phone,
    country=country
)
    if filename:
        with home_page.open_resource(filename) as f:
            msg.attach(
                filename=filename,
                content_type="application/csv",
                data=f.read()
                )
    mail.send(msg)
    return "Email sent successfully!"

@home_page.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@home_page.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        try:
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            email = request.form['email']
            phone = request.form['phone']
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
        
            add_user()
        
            #return render_template('user_data.html', clients=clients)
            send_email(name=firstName, subject="New User Registered - {} {}".format(firstName, lastName), last=lastName, email=email, phone=phone, country=country, email_file='email_booking.html') #firstName, lastName, email, phone, country, '')
            return render_template('submit_ack.html')
        except:
            return render_template('booking.html', error=True, email=email)
    return render_template('booking.html')

def add_user():
    clients = Client.query.all()
    for c in clients:
        exist = Users.query.filter_by(email=c.email).first()
        if not exist:
            user = Users(
                email=c.email,
                firstName=c.firstName,
                lastName=c.lastName,
                phone=c.phone,
                created_at=c.created_at
                )
            db.session.add(user)

        db.session.commit()


@home_page.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['password']
        table = request.form['table']
        if username == "mini" and password == "mini_123":
            if table == "Clients":
                val = Client.query.all()
                return render_template('user_data.html', clients=val)
            elif table == "Users":
                val = Users.query.all()
                return render_template('user_data.html', users=val)
            elif table == 'Notes':
                val = Notes.query.all()
                return render_template('user_data.html', notes=val)
    return render_template('admin.html', reqd='YES')

@home_page.route('/consent', methods=['GET', 'POST'])
def consent():
    return render_template('consent.html')

@home_page.route('/note', methods=['GET', 'POST'])
def note():
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['password']
        if username == "mini" and password == "mini_123":
            return redirect(url_for('home.add_note'))
    return render_template('admin.html', reqd="NO")

@home_page.route('/view', methods=['GET', 'POST'])
def view():
    if request.method == "POST":
        username = request.form['uname']
        password = request.form['password']
        if username == "mini" and password == "mini_123":
            return redirect(url_for('home.view_note'))
    return render_template('admin.html', reqd="NO")

@home_page.route('/add_note', methods=['GET', 'POST'])
def add_note():        
    if request.method == 'POST':
        user_id = request.form['user'].split('-')[0]
        email = request.form['user'].split('-')[1]
        return redirect(url_for('home.add_notes', id=user_id, email=email))
    val = Client.query.all()
    return render_template('add_notes.html', content=val)

@home_page.route('/add_notes/id=<int:id>/<email>', methods=['GET', 'POST'])
def add_notes(id,email):
    if request.method == 'POST':
        id = id
        email = email
        note = request.form['note']
        data = Notes(
            email = email.strip(),
            note = note
            )
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('home.add_note'))
    return render_template('add_note.html', id=id, email=email)

@home_page.route('/view_note', methods=['GET', 'POST'])
def view_note():        
    if request.method == 'POST':
        user_id = request.form['user'].split('-')[0]
        email = request.form['user'].split('-')[1]
        return redirect(url_for('home.view_notes', id=user_id, email=email))
    val = Client.query.all()
    return render_template('view_notes.html', content=val)


@home_page.route('/view_notes/id=<int:id>/<email>', methods=['GET', 'POST'])
def view_notes(id,email):
    content = Notes.query.all()
    id = id
    email = email.strip()
    content = Notes.query.all() #filter_by(email=email).first()
    return render_template('view_note.html', notes=content, id=id, email=email)

@home_page.route('/download', methods=['GET', 'POST'])
def download():
    content = Client.query.all()
    if request.method == 'POST':
        notes = Notes.query.all()
        data = request.form['download']
        email = data.split("-")[1].strip()
        name = data.split("-")[2].strip()

        if os.path.exists(file_path):
            os.remove(file_path)
        line = 1
        for note in notes:
            if note.email.strip() == email:
                with open(file_path, "a") as f:
                    f.write('{}. {}\n'.format(line, note.note))
                    line += 1
        send_email(email_file='email_download.html', subject='File request - {}'.format(name), email='puneet1234bhat@gmail.com', filename=file_path)
        return render_template('success.html')
    return render_template('download.html', content=content)

