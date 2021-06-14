from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import os
from flask import request
from flask import Response
import base64
from PIL import Image
from io import BytesIO
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

app = Flask(__name__)

# декоратор для вывода страницы по умолчанию
@app.route("/")
def hello():
    return " <html><head></head><body>Hello World!</body></html>"
  
@app.route("/pic")
def pic():
    return " <html><head></head><body><img src="https://media.istockphoto.com/photos/business-man-pushing-large-stone-up-to-hill-business-heavy-tasks-and-picture-id825383494?k=6&amp;m=825383494&amp;s=612x612&amp;w=0&amp;h=pamh6qxyNPCnNAVru4BrAHt2qTHAGCD9lDiN_6MbaNY=" alt="66,296 Struggle Stock Photos, Pictures &amp;amp; Royalty-Free Images - iStock" jsname="HiaYvf" jsaction="load:XAeZkd;" class="n3VNCb" data-noaft="1" style="width: 383px; height: 217.784px; margin: 0px;"></body></html>"  
  
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
