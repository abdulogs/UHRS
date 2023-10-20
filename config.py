from flask import Flask, url_for, render_template, request, redirect, session, jsonify, flash
from flask_mail import Mail, Message
from helpers import fetchDisease
from database import Listing, Create, Delete, Update


app = Flask(__name__, template_folder='public', static_folder="src")

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'abdulhannanzarrar88@gmail.com'
app.config['MAIL_PASSWORD'] = 'kbkwrghyjprlrnqo'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
