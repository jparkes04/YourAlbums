from flask import render_template, flash, request, redirect
from app import app, db, models, login_manager
from flask_login import login_user, login_required, logout_user, current_user
from .forms import FlaskForm, RegisterLoginForm, AlbumForm, TrackForm
import json
import logging

# Authentication


@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegisterLoginForm()
    if form.validate_on_submit():
        # Validate that username and password were entered
        if form.username.data == "":
            flash('Please enter a username to login.')
            return redirect('/login')
        if form.password.data == "":
            flash('Please enter a password to login.')
            return redirect('/login')

        # Find user with matching username
        user = models.User.query.filter_by(username=form.username.data).first()

        # No user
        if user is None:
            flash('User account not found! Please register an account first.')
            app.logger.info(f'User attempted to log into account which does not exist.')
            return redirect('/login')

        # Wrong password
        if user.password != form.password.data:
            flash('Incorrect password, please try again.')
            app.logger.info(f'User "{user.username}" entered the incorrect password.')
            return redirect('/login')

        login_user(user)
        flash('Successfully logged in!')
        app.logger.info(f'User "{user.username}" logged in successfully.')
        return redirect('/')

    return render_template('login.html',
                           form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterLoginForm()
    if form.validate_on_submit():
        # Validate that username and password were entered
        if form.username.data == "":
            flash('Please enter a username to register.')
            return redirect('/register')
        if form.password.data == "":
            flash('Please enter a password to register.')
            return redirect('/register')

        # Check that the username is not already taken
        if models.User.query.filter_by(username=form.username.data).first():
            flash('That username has already been taken. Please choose another one!')
            app.logger.info(f'User failed to register account with existing userame "{form.username.data}".')
            return redirect('/register')

        # Add new user to db
        user = models.User(
            username=form.username.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()

        flash('Account registered successfully!')
        app.logger.info(f'New user "{form.username.data}" registered account.')
        return redirect('/login')

    return render_template('register.html',
                           form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    app.logger.info(f'User logged out.')
    return redirect('/')

# Views

# Homepage


@app.route('/')
def home():
    # Show user page if user is logged in
    # Otherwise, show home page.
    if current_user.is_authenticated:
        return user()
    return render_template('home.html')

# User


@app.route('/user', methods=['GET', 'POST'])
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


@app.route('/album', methods=['GET', 'POST'])
@login_required
def create_album():
    form = AlbumForm()

    if form.validate_on_submit():
        # Validate that title and artist are present
        if form.title.data == "":
            flash('Please enter the album\'s title.')
            return redirect('/album')
        if form.artist.data == "":
            flash('Please enter the artist name.')
            return redirect('/album')
        # Validate that year exists and is at least zero
        if not form.year.data:
            flash('Please enter a year of release.')
            return redirect('/album')
        if form.year.data < 0:
            flash('Please enter a year of release of at least 0.')
            return redirect('/album')

        # Create album and add to db
        album = models.Album(
            title=form.title.data,
            artist=form.artist.data,
            imgurl=form.imgurl.data,
            year=form.year.data
        )

        db.session.add(album)
        db.session.commit()

        flash(f'Album "{album.title}" added to database!')
        app.logger.info(f'Album "{album.title}" added to database.')

        return redirect(f'/album/{album.id}')

    return render_template('album.html',
                           form=form)

# Edit


@app.route('/album/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_album(id):
    # Get album and its tracks
    album = models.Album.query.get(id)
    tracks = models.Track.query.filter_by(album_id=album.id).all()

    # Determine if album is favourited to display correct
    # state on favourite button on page load
    isFavourited = False
    for favourite in current_user.favourite_albums:
        if favourite.id == album.id:
            isFavourited = True

    form = AlbumForm(obj=album)

    if form.validate_on_submit():
        # Validate that title and artist are present
        if form.title.data == "":
            flash('Please enter the album\'s title.')
            return redirect(f'/album/{id}')
        if form.artist.data == "":
            flash('Please enter the artist name.')
            return redirect(f'/album/{id}')
        # Validate that year exists and is at least zero
        if not form.year.data:
            flash('Please enter a year of release.')
            return redirect('/album')
        if form.year.data < 0:
            flash('Please enter a year of release of at least 0.')
            return redirect('/album')

        album.title = form.title.data
        album.artist = form.artist.data
        album.imgurl = form.imgurl.data
        album.year = form.year.data
        db.session.commit()

        flash('Album updated!')
        app.logger.info(f'Album "{album.title}" updated.')
        return redirect(f'/album/{id}')

    return render_template('album.html',
                           form=form,
                           album=album,
                           tracks=tracks,
                           isFavourited=isFavourited)

# Delete


@app.route('/delete_album/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_album(id):
    album = models.Album.query.get(id)
    app.logger.info(f'Album "{album.title}" deleted.')
    db.session.delete(album)
    db.session.commit()
    return albums()

# Tracks

# Create


@app.route('/track/<int:albumid>', methods=['GET', 'POST'])
@login_required
def create_track(albumid):
    album = models.Album.query.get(albumid)

    # Generate suggestion for next position
    # By finding current max and adding 1
    tracks = models.Track.query.filter_by(album_id=album.id).all()
    if (tracks):
        positions = []
        for existingTrack in tracks:
            positions.append(existingTrack.position)
        nextpos = max(positions) + 1
    else:
        nextpos = 1

    form = TrackForm()
    form.position.data = nextpos

    if form.validate_on_submit():
        # Validate that title was entered
        if form.trackname.data == "":
            flash('Please enter the track name.')
            return redirect(f'/track/{albumid}')
        # Validate that position exists and is greater than 0
        if not form.position.data:
            flash('Please enter track position.')
            return redirect(f'/track/{albumid}')
        if form.position.data <= 0:
            flash('Please enter a position greater than 0.')
            return redirect(f'/track/{albumid}')
        # Validate that runtime exists and is at least 0
        if not form.runtime.data:
            flash('Please enter a runtime.')
            return redirect(f'/track/{albumid}')
        if form.runtime.data < 0:
            flash('Please enter a runtime of at least 0.')
            return redirect(f'/track/{albumid}')

        # Create track and add to db
        track = models.Track(
            position=form.position.data,
            trackname=form.trackname.data,
            runtime=form.runtime.data,
            album_id=albumid
        )

        db.session.add(track)
        db.session.commit()

        flash(f'Track "{track.trackname}" added to album "{album.title}"!')
        app.logger.info(f'Track "{track.trackname}" added to album "{album.title}"')
        return redirect(f'/album/{album.id}')

    return render_template('track.html',
                           album=album,
                           form=form,
                           nextpos=nextpos)

# Edit


@app.route('/edit_track/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_track(id):
    form = TrackForm()

    track = models.Track.query.get(id)
    album = models.Album.query.get(track.album_id)

    form = TrackForm(obj=track)

    if form.validate_on_submit():
        # Validate that title was entered
        if form.trackname.data == "":
            flash('Please enter the track name.')
            return redirect(f'/edit_track/{id}')
        # Validate that position exists and is greater than 0
        if not form.position.data:
            flash('Please enter track position.')
            return redirect(f'/edit_track/{id}')
        if form.position.data <= 0:
            flash('Please enter a position greater than 0.')
            return redirect(f'/edit_track/{id}')
        # Validate that runtime exists and is at least 0
        if not form.runtime.data:
            flash('Please enter a runtime.')
            return redirect(f'/edit_track/{id}')
        if form.runtime.data < 0:
            flash('Please enter a runtime of at least 0.')
            return redirect(f'/edit_track/{id}')

        track.position = form.position.data
        track.trackname = form.trackname.data
        track.runtime = form.runtime.data

        db.session.commit()

        flash('Track updated!')
        app.logger.info(f'Track "{track.trackname}" updated.')
        return redirect(f'/album/{track.album_id}')

    return render_template('track.html',
                           form=form,
                           album=album)

# Delete


@app.route('/delete_track/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_track(id):
    track = models.Track.query.get(id)
    app.logger.info(f'Track "{track.trackname}" deleted.')
    db.session.delete(track)
    db.session.commit()
    return redirect(f'/album/{track.album_id}')

# Favourite AJAX handler


@app.route('/favourite', methods=['POST'])
def favourite():
    data = json.loads(request.data)

    user = models.User.query.get(int(data.get('user_id')))
    album = models.Album.query.get(int(data.get('album_id')))

    # Determine if album is already favourited by this user
    exists = False
    for favourite in user.favourite_albums:
        if favourite.id == album.id:
            exists = True

    if (exists):
        # If it does, remove favourite and save
        user.favourite_albums.remove(album)
        db.session.commit()
        favourited = False
        app.logger.info(f'User "{user.username}" removed favourite album "{album.title}"')
    else:
        # If it doesn't, add favourite and save
        user.favourite_albums.append(album)
        db.session.commit()
        favourited = True
        app.logger.info(f'User "{user.username}" added favourite album "{album.title}"')

    # Return new state
    return json.dumps({
        'status': 'OK',
        'favourited': favourited
    })
