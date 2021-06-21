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
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# инициализируем папку с изображением 
IMAGE_FOLDER = os.path.join('static', 'images')
app = Flask(__name__)
# Визуальная составляющая страницы описывается 
# с помощью наследования нашего класса от FlaskForm
# в котором мы инициализируем поле для загрузки файла,
# поле капчи, текстовое поле и кнопку подтверждения
class MyForm(FlaskForm):
    upload = FileField('Загрузите изображение', validators = 
      [FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Только картинки!')])
    recaptcha = RecaptchaField()
    color1 = StringField("Введите порядок цветов (rgb, brg, grb,...)")
    color2 = StringField()
    color3 = StringField()
    submit = SubmitField('Применить')    
    
    
SECRET_KEY = 'secret'
app.config['UPLOAD_FOLDER'] = IMAGE_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LenXSsbAAAAABPqpQZ3RpkDt42hxynW7j7SZxpm'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LenXSsbAAAAALFvL7os3RcyzKnYADCcTW37GBPH'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
bootstrap = Bootstrap(app)

def problem(path, color1, color2, color3):
    im = Image.open(path)
    
        # Заменяем символы r,g,b на соответствующие индексы
    value = [color1, color2, color3]
    for i in range(3):
        value[i].lower()
        if "r" in value[i]:
            value[i].replace("r", "0")
        elif "g" in value[i]:
            value[i].replace("g", "1")
        elif "b" in value[i]:
            value[i].replace("b", "1")
    # Сохраняем размерность картинки
    x,y = im.size
    # сохраняем картинку в виде массива numpy
    arr = np.asarray(im)
    eachColorSum = [0,0,0]
    for i in range(3):
            if value[i] == "0":
                    eachColorSum[0] = np.sum(arr[:,:,i])
            elif value[i] == "1":
                    eachColorSum[1] = np.sum(arr[:,:,i])
            elif value[i] == "2":
                    eachColorSum[2] = np.sum(arr[:,:,i])

    colorSum = eachColorSum[0] + eachColorSum[1] + eachColorSum[2]
    colorPercent = [0,0,0]
    for i in range (3):
        # Прописываем условие, чтобы избежать ошибки деления на 0
            if colorSum != 0:
                    colorPercent[i] = eachColorSum[i] / colorSum * 100
    fig1, ax1 = plt.subplots()
    # Используем гистограмму
    # Передаем название для каждой (цвет)
    # и его соответствующее значение
    colorList = ["red", "green", "blue"]
    ax1.bar(colorList, colorPercent)
    # Устанавливаем цвет графика
    ax1.set_facecolor('seashell')
    fig1.set_facecolor('floralwhite')
    fig1.set_figwidth(6)  #  ширина фигуры
    fig1.set_figheight(4)  #  высота фигуры
# Сохраняем фигуру
    plt.savefig("./static/images/myFig1.png")
    plt.close()


    # Средний цвет
    avrgColor = [0,0,0]
    # Заполняем среднимим значениями
    for i in range (3):
        avrgColor[i] = round(np.sum(arr[:,:,i].mean()))
    fig2, ax2 = plt.subplots()
    ax2.bar(colorList, avrgColor)

    ax2.set_facecolor('floralwhite')
    fig2.set_facecolor('seashell')
    fig2.set_figwidth(6)  #  ширина фигуры
    fig2.set_figheight(4)  #  высота фигуры

    plt.savefig("./static/images/avrg.png") 
    plt.close()



# Проходясь по картинке изменяем цвета пикселей 
# в зависимости от выбранного порядка цветовых карт
    for i in range(0,y):
        for j in range(0,x):
            im.putpixel((j,i),(arr[i][j][int(value[0])],arr[i][j][int(value[1])],arr[i][j][int(value[2])]))
        # Сохраняем изображение
        im.save(path)
    
@app.route("/", methods=['GET', 'POST'])
def main():
    form = MyForm()
    imagePath = None
    graphPath1 = None
    graphPath2 = None
    if form.validate_on_submit():
        photo = form.upload.data.filename.split('.')[-1]
        imagePath = os.path.join('./static/images', f'photo.{photo}')
        graphPath1 = os.path.join('./static/images', f'myFig1.png')
        graphPath2 = os.path.join('./static/images', f'avrg.png')
        # Сохраняем наше загруженное изображение
        form.upload.data.save(imagePath)
        problem(imagePath, form.color1.data, form.color2.data, form.color3.data)
    return render_template('main.html', form=form, image=imagePath, graph1=graphPath1, graph2=graphPath2)
# Запускаем наше приложение
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
    
