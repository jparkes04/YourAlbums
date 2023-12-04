from flask import render_template, flash, request, redirect
from app import app, db, models, login_manager
from flask_login import login_user, login_required, logout_user, current_user
from .forms import FlaskForm, RegisterLoginForm, AlbumForm, TrackForm
import json

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
        # Check that the username is not already taken
        if models.User.query.filter_by(username=form.username.data).first():
            flash('That username has already been taken. Please choose another one!')
            return redirect('/login')

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
    return render_template('home.html')

# User

@app.route('/user', methods=['GET','POST'])
@login_required
def user():
    favourites = current_user.favourite_albums.all()
    return render_template('user.html',
                           favourites=favourites)

# Albums

@app.route('/albums')
def albums():
    albums = models.Album.query.all()

    return render_template('albums.html',
                            albums=albums)

# Create
@app.route('/album', methods=['GET','POST'])
@login_required
def create_album():
    form = AlbumForm()

    if form.validate_on_submit():
        album = models.Album(
            title=form.title.data,
            artist=form.artist.data,
            year=form.year.data
        )

        db.session.add(album)
        db.session.commit()

        flash(f'Album "{album.title}" added to database!')
        return redirect(f'/album/{album.id}')

    return render_template('album.html',
                            form=form)

# Edit
@app.route('/album/<int:id>', methods=['GET','POST'])
@login_required
def edit_album(id):
    album = models.Album.query.get(id)
    tracks = models.Track.query.filter_by(album_id=album.id).all()

    isFavourited = False
    for favourite in current_user.favourite_albums:
        if favourite.id == album.id:
            isFavourited = True

    form = AlbumForm(obj=album)

    if form.validate_on_submit():
        album.title=form.title.data
        album.artist=form.artist.data
        album.year=form.year.data
        db.session.commit()

        flash('Album updated!')
        return redirect(f'/album/{id}')

    return render_template('album.html',
                            form=form,
                            album=album,
                            tracks=tracks,
                            isFavourited=isFavourited)

# Delete
@app.route('/delete_album/<int:id>', methods=['GET','POST'])
@login_required
def delete_album(id):
    album = models.Album.query.get(id)
    db.session.delete(album)
    db.session.commit()
    return albums()

# Tracks

# Create
@app.route('/track/<int:albumid>', methods=['GET','POST'])
@login_required
def create_track(albumid):
    album = models.Album.query.get(albumid)

    # Generate suggestion for next position
    tracks = models.Track.query.filter_by(album_id=album.id).all()
    if (tracks):
        positions = []
        for existingTrack in tracks:
            positions.append(existingTrack.position)
        nextpos = max(positions) + 1 
    else:
        nextpos = 1

    form = TrackForm()
    form.position.data=nextpos

    if form.validate_on_submit():
        track = models.Track(
            position=form.position.data,
            trackname=form.trackname.data,
            runtime=form.runtime.data,
            album_id=albumid
        )

        db.session.add(track)
        db.session.commit()

        flash(f'Track "{track.trackname}" added to album "{album.title}"!')
        return redirect(f'/album/{album.id}')

    return render_template('track.html',
                            album=album,
                            form=form,
                            nextpos=nextpos)

# Edit
@app.route('/edit_track/<int:id>', methods=['GET','POST'])
@login_required
def edit_track(id):
    form = TrackForm()

    track = models.Track.query.get(id)
    album = models.Album.query.get(track.album_id)

    form = TrackForm(obj=track)

    if form.validate_on_submit():
        track.position=form.position.data
        track.trackname=form.trackname.data
        track.runtime=form.runtime.data

        db.session.commit()

        flash('Track updated!')
        return redirect(f'/album/{track.album_id}')

    return render_template('track.html',
                            form=form,
                            album=album)

# Delete
@app.route('/delete_track/<int:id>', methods=['GET','POST'])
@login_required
def delete_track(id):
    track = models.Track.query.get(id)
    db.session.delete(track)
    db.session.commit()
    return redirect(f'/album/{track.album_id}')

# Favourite AJAX handler

@app.route('/favourite', methods=['POST'])
def favourite():
    data = json.loads(request.data)

    user = models.User.query.get(int(data.get('user_id')))
    album = models.Album.query.get(int(data.get('album_id')))

    exists = False
    for favourite in user.favourite_albums:
        if favourite.id == album.id:
            exists = True

    if (exists):
        user.favourite_albums.remove(album)
        db.session.commit()
        favourited = False
    else:
        user.favourite_albums.append(album)
        db.session.commit()
        favourited = True

    return json.dumps({
        'status': 'OK',
        'favourited': favourited
    })
