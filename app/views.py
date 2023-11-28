from flask import render_template, flash, request, redirect
from app import app, db, models
from .forms import FlaskForm


@app.route('/')
def home():
    return render_template('base.html', title='Home')