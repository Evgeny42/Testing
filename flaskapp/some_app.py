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
    user = TextField()
    submit = SubmitField('OK')    
    
    
SECRET_KEY = 'secret'
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LenXSsbAAAAABPqpQZ3RpkDt42hxynW7j7SZxpm'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LenXSsbAAAAALFvL7os3RcyzKnYADCcTW37GBPH'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

bootstrap = Bootstrap(app)
  
    
def show(file_name):
    im = Image.open(file_name)
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot()
    data = np.random.randint(0, 255, (100, 100))
    ax.imshow(im, cmap='plasma')
    b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
    fig.colorbar(b, ax=ax)
    gr_path = "./static/picture.png"
    sns.displot(data)
    #plt.show()
    plt.savefig(gr_path)
    plt.close()
    im = Image.open(file_name)
    x, y = im.size
    im.save(file_name)    

    
    
@app.route("/", methods=['GET', 'POST'])
def main():
    form = MyForm()
    filename = None
    if form.validate_on_submit():
        photo = form.upload.data.filename.split('.')[-1]
        filename = os.path.join('./static', f'photo.{photo}')
        form.upload.data.save(filename)
        show(filename)
    return render_template('main.html', form=form, image_name=filename)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
    

@app.route('/index')
def show_image(filename):
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'picture.png')
    return render_template("index.html", user_image = full_filename)
#     myImage = Image.open(filename)
#     fig = plt.figure(figsize=(6,4))
#     ax = fig.add_subplot()
#     ax.imshow(myImage)
    




    
    
