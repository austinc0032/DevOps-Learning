import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (LoginManager, UserMixin, current_user, login_required,
                         login_user, logout_user)
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash, generate_password_hash
from wtforms import PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('TICKET_SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('TICKET_DATABASE_URI', 'sqlite:///tickets.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'localhost')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 25))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'false').lower() in ('true', '1', 'yes')
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'false').lower() in ('true', '1', 'yes')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@example.com')
app.config['ADMIN_NOTIFICATION_EMAILS'] = [email.strip() for email in os.environ.get('ADMIN_NOTIFICATION_EMAILS', 'admin@example.com').split(',') if email.strip()]

mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'warning'

STATUS_CHOICES = [
    ('New', 'New'),
    ('In Progress', 'In Progress'),
    ('More Info Required', 'More Info Required'),
    ('Escalated to CTO', 'Escalated to CTO'),
    ('Resolved', 'Resolved'),
    ('Closed', 'Closed'),
]


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(240), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    tickets = db.relationship('Ticket', backref='creator', lazy=True)
    comments = db.relationship('TicketComment', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role in ('admin', 'it', 'cto')


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(40), nullable=False, default='New')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('TicketComment', backref='ticket', lazy=True, cascade='all, delete-orphan')


class TicketComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=240)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=240)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')


class TicketForm(FlaskForm):
    title = StringField('Ticket Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=3000)])
    submit = SubmitField('Submit Ticket')


class TicketUpdateForm(FlaskForm):
    status = SelectField('Status', choices=STATUS_CHOICES, validators=[DataRequired()])
    comment = TextAreaField('Update / Request Info', validators=[Length(max=3000)])
    submit = SubmitField('Save Update')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def send_email(subject, recipients, body):
    if not recipients:
        return
    if isinstance(recipients, str):
        recipients = [recipients]

    msg = Message(subject=subject, recipients=recipients, body=body)
    try:
        mail.send(msg)
        app.logger.info('Email sent to %s', recipients)
    except Exception as err:
        app.logger.warning('Email notification failed: %s', err)


def get_admin_emails():
    emails = list(app.config['ADMIN_NOTIFICATION_EMAILS'])
    admins = User.query.filter(User.role.in_(['admin', 'it', 'cto'])).all()
    for admin in admins:
        if admin.email not in emails:
            emails.append(admin.email)
    return emails


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Welcome back.', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data.lower()).first()
        if existing:
            flash('An account with that email already exists.', 'warning')
        else:
            user = User(name=form.name.data, email=form.email.data.lower(), role='user')
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        tickets = Ticket.query.order_by(Ticket.updated_at.desc()).all()
    else:
        tickets = Ticket.query.filter_by(user_id=current_user.id).order_by(Ticket.updated_at.desc()).all()
    return render_template('dashboard.html', tickets=tickets)


@app.route('/tickets/new', methods=['GET', 'POST'])
@login_required
def create_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            title=form.title.data,
            description=form.description.data,
            status='New',
            creator=current_user,
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Your ticket has been created.', 'success')

        admin_emails = get_admin_emails()
        send_email(
            subject=f'New ticket submitted: {ticket.title}',
            recipients=admin_emails,
            body=(
                f'A new ticket was submitted by {current_user.name} ({current_user.email}).\n\n'
                f'Ticket ID: {ticket.id}\nTitle: {ticket.title}\n\n'
                f'View the ticket after logging in to respond or update the status.'
            ),
        )
        return redirect(url_for('dashboard'))
    return render_template('ticket_form.html', form=form)


@app.route('/tickets/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if not current_user.is_admin() and ticket.user_id != current_user.id:
        flash('You are not authorized to view that ticket.', 'danger')
        return redirect(url_for('dashboard'))

    update_form = TicketUpdateForm(status=ticket.status)
    if update_form.validate_on_submit():
        if not current_user.is_admin():
            flash('Only IT or admin users can update ticket status.', 'danger')
            return redirect(url_for('ticket_detail', ticket_id=ticket_id))

        original_status = ticket.status
        ticket.status = update_form.status.data
        if update_form.comment.data:
            comment = TicketComment(
                ticket=ticket,
                author=current_user,
                body=update_form.comment.data,
            )
            db.session.add(comment)
        db.session.commit()

        if ticket.creator.email:
            send_email(
                subject=f'Ticket #{ticket.id} status changed to {ticket.status}',
                recipients=ticket.creator.email,
                body=(
                    f'Hello {ticket.creator.name},\n\n'
                    f'Your ticket "{ticket.title}" has changed status from {original_status} to {ticket.status}.\n\n'
                    f'Comments:\n{update_form.comment.data or "No additional comments."}\n\n'
                    'Please log in to view the ticket details.'
                ),
            )

        flash('Ticket updated successfully.', 'success')
        return redirect(url_for('ticket_detail', ticket_id=ticket.id))

    comments = TicketComment.query.filter_by(ticket_id=ticket.id).order_by(TicketComment.created_at.desc()).all()
    return render_template('ticket_detail.html', ticket=ticket, update_form=update_form, comments=comments)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


def create_default_admin():
    if User.query.filter(User.role.in_(['admin', 'it', 'cto'])).first():
        return
    admin_email = os.environ.get('ADMIN_EMAIL')
    admin_password = os.environ.get('ADMIN_PASSWORD')
    if admin_email and admin_password:
        admin = User(
            name=os.environ.get('ADMIN_NAME', 'IT Admin'),
            email=admin_email.lower(),
            role='admin',
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()
        app.logger.info('Default admin account created for %s', admin_email)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_admin()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
