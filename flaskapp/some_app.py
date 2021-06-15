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

# инициализируем папку с изображением 
IMAGE_FOLDER = os.path.join('static', 'images')

app = Flask(__name__)

# Визуальная составляющая страницы описывается 
# с помощью наследования нашего класса от FlaskForm
# в котором мы инициализируем поле для загрузки файла,
# поле капчи, текстовое поле и кнопку подтверждения
class MyForm(FlaskForm):
    upload = FileField('Load image', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    recaptcha = RecaptchaField()
    user = TextField("\tInput")
    submit = SubmitField('OK')    
    
    
SECRET_KEY = 'secret'
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LenXSsbAAAAABPqpQZ3RpkDt42hxynW7j7SZxpm'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LenXSsbAAAAALFvL7os3RcyzKnYADCcTW37GBPH'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

bootstrap = Bootstrap(app)

def change_pic(path, value):
    im = Image.open(path)
    x,y = im.size
    a = np.asarray(im)
    
    for i in range(0,x):
        for j in range(0,y):
            im.putpixel((i,j),(int(a[i][j][0]),int(a[i][j][2]),int(a[i][j][1])))
#     pic_arr = np.asarray(im)
#     im = Image.fromarray(a)
    im.save(path)


@app.route("/", methods=['GET', 'POST'])
def main():
    form = MyForm()
    filename = None
    if form.validate_on_submit():
        photo = form.upload.data.filename.split('.')[-1]
        filename = os.path.join('./static/images', f'photo.{photo}')
        form.upload.data.save(filename)
        change_contrast(filename, form.user.data)
    return render_template('main.html', form=form, image_name=filename)

# Запускаем наше приложение
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
    
    
    
