from flask import render_template, flash, request, redirect
from app import app, db, models, login_manager
from .forms import FlaskForm

@login_manager.user_loader
def load_user(user_id):
    return db.User.get(user_id)

@app.route('/')
def home():
    return render_template('base.html', title='Home')