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
    return " <html><head></head> <body>Hello World!</body></html>"
  
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
