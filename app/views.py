from flask import render_template, flash, request, redirect
from app import app, db, models, login_manager
from flask_login import login_user, login_required, logout_user, current_user
from .forms import FlaskForm, RegisterLoginForm

# Authentication

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)
    # check this returns none and not an exception if the user does not exist
    #return User.get(user_id)

@app.route('/login', methods=['GET','POST'])
def login():
    form = RegisterLoginForm()
    if form.validate_on_submit():

        user = models.User.query.filter_by(username=form.username.data).first()

        if user is None:
            flash('User account not found! Please register an account first.')
            return redirect('/login')

        if user.password != form.password.data:
            flash('Incorrect password, please try again.')
            return redirect('/login')

        login_user(user)
        flash('Successfully logged in!')
        return redirect('/')

    return render_template('login.html',
                           form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterLoginForm()
    if form.validate_on_submit():

        # Add new user to db
        user = models.User(
            username=form.username.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Account registered successfully!')
        return redirect('/login')

    return render_template('register.html',
                           form=form)


@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')

# Views

@app.route('/')
def home():
    if current_user.is_authenticated:
        return user()
    return render_template('home.html', title='Home')

@app.route('/user', methods=['GET','POST'])
@login_required
def user():
    return render_template('user.html')

@app.route('/albums')
def albums():
    albums = models.Album.query.all()

    return render_template('albums.html',
                            albums=albums)