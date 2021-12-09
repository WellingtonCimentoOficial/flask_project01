from datetime import datetime
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired
from flask_migrate import Migrate
import os
import functions

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
PROFILES = 'static\\img\\profiles\\'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SECRET_KEY'] = 'djadjadajskj'
app.config['UPLOAD_FOLDER'] = PROFILES
login_manager = LoginManager(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()

class Users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    perm = db.Column(db.Integer, nullable=False, default=0)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.now())
    last_update_date = db.Column(db.DateTime, default=datetime.now())
    image_profile = db.relationship('Images', backref='user', uselist=False)
    
    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def __repr__(self):
        return str(self.id)

class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

    def __init__(self, id_user, name, mimetype):
        self.id_user = id_user
        self.name = name
        self.mimetype = mimetype

    def __repr__(self):
        return str(self.id)

class FormRegister(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class FormLogin(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = FormRegister()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data
        email_query = Users.query.filter_by(email=email).first()
        if email_query:
            flash('This email already exists.')
            return redirect(url_for('register'))
        else:
            user_query = Users.query.filter_by(username=username).first()
            if user_query:
                flash('The user already exists.')
                return redirect(url_for('register'))
            else:
                db.session.add(Users(name=name, email=email, username=username, password=password))
                db.session.commit()
                try:
                    os.makedirs(PROFILES + 'user' + str(Users.query.all().pop().id) + '\\profile')
                except Exception as e:
                    print('Erro na criação da pasta do usuario')
                    print(e)
                flash('Account created successfully!')
                return redirect(url_for('register'))
    else:
        return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = FormLogin()
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    else:
        if request.method == 'POST':
            user = Users.query.filter_by(username=form.username.data).first()
            if user:
                password = user.verify_password(form.password.data)
                if password:
                    login_user(user)
                    return redirect(url_for('dashboard'))
                else:
                    flash('Incorrect username or password.')
            else:
                flash('Incorrect username or password.')
        return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return redirect(url_for('login'))
    else:
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    all_users = Users.query.order_by(Users.id).all()
    if current_user.is_authenticated:
        return render_template('dashboard.html', users=all_users)
    else:
        return redirect(url_for('login'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    form = FormRegister()
    if request.method == 'POST':
        file = request.files['file']
        user = current_user.id
        password = form.password.data
        last_update_date = datetime.now()
        if password == '':
            if not file:
                if form.username.data == current_user.username:
                    Users.query.get(user).name = form.name.data
                    Users.query.get(user).username = form.username.data
                    Users.query.get(user).last_update_date = last_update_date
                    db.session.commit()
                    flash('Data updated successfully')
                    return redirect(url_for('profile'))
                if Users.query.filter_by(username=form.username.data).first():
                    flash('This username already exists')
                    return redirect(url_for('profile'))

                Users.query.get(user).name = form.name.data
                Users.query.get(user).username = form.username.data
                Users.query.get(user).last_update_date = last_update_date
                db.session.commit()
                flash('Data updated successfully')
                return redirect(url_for('profile'))
                
            if file and allowed_file(file.filename):
                if current_user.image_profile:
                    db.session.delete(Images.query.filter_by(id_user=current_user.id).first())
                    db.session.commit()

                    #filename = secure_filename(file.filename)
                    mimetype = file.mimetype
                    filename = functions.renameprofile(mimetype)
                    try:
                        file.save(os.path.join(PROFILES + 'user' + str(current_user.id) + '\\profile', filename))
                    except Exception as e:
                        print('erro na hora de armazenar a imagem de perfil na pasta do usuario')

                    image = Images(id_user=current_user.id, name=filename, mimetype=mimetype)
                    db.session.add(image)

                    if form.username.data == current_user.username:
                        Users.query.get(user).name = form.name.data
                        Users.query.get(user).username = form.username.data
                        Users.query.get(user).last_update_date = last_update_date
                        db.session.commit()
                        flash('Data updated successfully')
                        return redirect(url_for('profile'))
                    if Users.query.filter_by(username=form.username.data).first():
                        flash('This username already exists')
                        return redirect(url_for('profile'))

                    Users.query.get(user).name = form.name.data
                    Users.query.get(user).username = form.username.data
                    Users.query.get(user).last_update_date = last_update_date
                    db.session.commit()
                    flash('Data updated successfully')
                    return redirect(url_for('profile'))

                #filename = secure_filename(file.filename)
                mimetype = file.mimetype
                filename = functions.renameprofile(mimetype)
                try:
                    file.save(os.path.join(PROFILES + 'user' + str(current_user.id) + '\\profile', filename))
                except Exception as e:
                    print('erro na hora de armazenar a imagem de perfil na pasta do usuario')

                image = Images(id_user=current_user.id, name=filename, mimetype=mimetype)
                db.session.add(image)

                if form.username.data == current_user.username:
                    Users.query.get(user).name = form.name.data
                    Users.query.get(user).username = form.username.data
                    Users.query.get(user).last_update_date = last_update_date
                    db.session.commit()
                    flash('Data updated successfully')
                    return redirect(url_for('profile'))
                if Users.query.filter_by(username=form.username.data).first():
                    flash('This username already exists')
                    return redirect(url_for('profile'))

                Users.query.get(user).name = form.name.data
                Users.query.get(user).username = form.username.data
                Users.query.get(user).last_update_date = last_update_date
                db.session.commit()
                flash('Data updated successfully')
                return redirect(url_for('profile'))
            
            flash('data not updated as it is only allowed *png *jpg *jpeg')
            return redirect(url_for('profile'))

        if not file:
            if form.username.data == current_user.username:
                Users.query.get(user).name = form.name.data
                Users.query.get(user).username = form.username.data
                Users.query.get(user).password = generate_password_hash(password)
                Users.query.get(user).last_update_date = last_update_date
                db.session.commit()
                flash('Data updated successfully')
                return redirect(url_for('profile'))
            if Users.query.filter_by(username=form.username.data).first():
                flash('This username already exists')
                return redirect(url_for('profile'))

            Users.query.get(user).name = form.name.data
            Users.query.get(user).username = form.username.data
            Users.query.get(user).password = generate_password_hash(password)
            Users.query.get(user).last_update_date = last_update_date
            db.session.commit()
            flash('Data updated successfully')
            return redirect(url_for('profile'))
        
        if file and allowed_file(file.filename):
            if current_user.image_profile:
                db.session.delete(Images.query.filter_by(id_user=current_user.id).first())
                db.session.commit()

                #filename = secure_filename(file.filename)
                mimetype = file.mimetype
                filename = functions.renameprofile(mimetype)
                try:
                    file.save(os.path.join(PROFILES + 'user' + str(current_user.id) + '\\profile', filename))
                except Exception as e:
                    print('erro na hora de armazenar a imagem de perfil na pasta do usuario')

                image = Images(id_user=current_user.id, name=filename, mimetype=mimetype)
                db.session.add(image)

                if form.username.data == current_user.username:
                    Users.query.get(user).name = form.name.data
                    Users.query.get(user).username = form.username.data
                    Users.query.get(user).password = generate_password_hash(password)
                    Users.query.get(user).last_update_date = last_update_date
                    db.session.commit()
                    flash('Data updated successfully')
                    return redirect(url_for('profile'))
                if Users.query.filter_by(username=form.username.data).first():
                    flash('This username already exists')
                    return redirect(url_for('profile'))

                Users.query.get(user).name = form.name.data
                Users.query.get(user).username = form.username.data
                Users.query.get(user).password = generate_password_hash(password)
                Users.query.get(user).last_update_date = last_update_date
                db.session.commit()
                flash('Data updated successfully')
                return redirect(url_for('profile'))

            #filename = secure_filename(file.filename)
            mimetype = file.mimetype
            filename = functions.renameprofile(mimetype)
            try:
                file.save(os.path.join(PROFILES + 'user' + str(current_user.id) + '\\profile', filename))
            except Exception as e:
                print('erro na hora de armazenar a imagem de perfil na pasta do usuario')

            image = Images(id_user=current_user.id, name=filename, mimetype=mimetype)
            db.session.add(image)

            if form.username.data == current_user.username:
                Users.query.get(user).name = form.name.data
                Users.query.get(user).username = form.username.data
                Users.query.get(user).password = generate_password_hash(password)
                Users.query.get(user).last_update_date = last_update_date
                db.session.commit()
                flash('Data updated successfully')
                return redirect(url_for('profile'))
            if Users.query.filter_by(username=form.username.data).first():
                flash('This username already exists')
                return redirect(url_for('profile'))

            Users.query.get(user).name = form.name.data
            Users.query.get(user).username = form.username.data
            Users.query.get(user).password = generate_password_hash(password)
            Users.query.get(user).last_update_date = last_update_date
            db.session.commit()
            flash('Data updated successfully')
            return redirect(url_for('profile'))
        
        flash('data not updated as it is only allowed *png *jpg *jpeg')
        return redirect(url_for('profile'))
    else:
        return render_template('profile.html', form=form)

@app.route('/deleteuser/<int:id>')
def delete_user(id):
    if current_user.is_authenticated and current_user.perm == 1:
        try:
            os.system('rd /S /Q ' + PROFILES + 'user' + str(id))
        except Exception as e:
            print('erro ao excluir a pasta do usuario')
            print(e)
        db.session.delete(Users.query.get(str(id)))
        db.session.commit()
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('dashboard'))

@app.route('/deleteimageprofile/<int:id>')
def delete_image_profile(id):
    if current_user.is_authenticated and id == current_user.id:
        if current_user.image_profile:
            mimetype = functions.renameprofile(Images.query.filter_by(id_user=current_user.id).first().mimetype)
            try:
                os.remove(PROFILES + 'user' + str(current_user.id) + '\\profile\\' + mimetype)
            except Exception as e:
                print('erro na hora de excluir a foto de perfil da pasta do usuario')
                print(e)

            image = Images.query.filter_by(id_user=current_user.id).first()
            db.session.delete(image)
            db.session.commit()

            flash('successfully deleted image')
            return redirect(url_for('profile'))

        return redirect(url_for('profile'))

    return redirect(url_for('login'))

@app.route('/activities')
def activities():
    if current_user.is_authenticated:
        return render_template('activities.html')
    else:
        return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)