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

class MyForm(FlaskForm):
    upload = FileField('Load image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    recaptcha = RecaptchaField()
    user = TextField()
    submit = SubmitField('OK')    
    
    
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LenXSsbAAAAABPqpQZ3RpkDt42hxynW7j7SZxpm'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LenXSsbAAAAALFvL7os3RcyzKnYADCcTW37GBPH'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

bootstrap = Bootstrap(app)
    

@app.route("/", methods=['GET', 'POST'])
def main():
    form = MyForm()
    filename = None
    if form.validate_on_submit():
        photo = form.upload.data.filename.split('.')[-1]
        filename = os.path.join('./static', f'photo.{photo}')
        form.upload.data.save(filename)
#         show_image(filename)
    return render_template('main.html', form=form, image_name=filename)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
    
# @app.route("/i")
# def show_image():
@app.route('/index')
def show_index():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'picture.png')
    return render_template("index.html", user_image = full_filename)
#     myImage = Image.open(filename)
#     fig = plt.figure(figsize=(6,4))
#     ax = fig.add_subplot()
#     ax.imshow(myImage)
    




    
    
