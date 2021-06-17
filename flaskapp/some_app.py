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
    user = TextField("Введите порядок цветов (rgb, brg, grb,...)")
    submit = SubmitField('Применить')    
    
    
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
    # Из введенной строки пользователем
    # удаляем все символы кроме букв
    for i in value:
        if (i.isalpha() is False):
            value = value.replace(i, "")
    # Приводим символы к нижнему регистру
    value = value.lower()
    # Если в веденной строке пользователя встречаются символы
    # r, g, b, то картинка изменится
    if ("r" in value) and ("g" in value) and ("b" in value):
        # Заменяем символы r,g,b на соответствующие индексы
        value = value.replace("r", "0")
        value = value.replace("g", "1")
        value = value.replace("b", "2")
        # Сохраняем размерность картинки
        x,y = im.size
        # сохраняем картинку в виде массива numpy
        arr = np.asarray(im)
        # Суммируем значение каждого цвета
        eachColorSum = [0,0,0]
        for i in range(3):
            if value[i] == "0":
                eachColorSum[0] = np.sum(arr[:,:,i])
            elif value[i] == "1":
                eachColorSum[1] = np.sum(arr[:,:,i])
            elif value[i] == "2":
                eachColorSum[2] = np.sum(arr[:,:,i])
        # получаем значение каждого цвета в процентах
        colorSum = eachColorSum[0] + eachColorSum[1] + eachColorSum[2]
        # инициализируем список со значениями в процентах для каждого цвета
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
        ax.bar(colorList, colorPercent)
        # Устанавливаем цвет графика
        ax.set_facecolor('seashell')
        fig.set_facecolor('floralwhite')
        fig.set_figwidth(6)  #  ширина фигуры
        fig.set_figheight(4)  #  высота фигуры
        # Сохраняем фигуру
        plt.savefig("./static/images/myFig1.png")
#         plt.close()
		
#         avrgColor = [0,0,0]
#         # Заполняем среднимим значениями
#         for i in range (3):
#            avrgColor[i] = round(np.sum(arr[:,:,i].mean()))
#         fig2, ax2 = plt.subplots()
#         ax.pie(avrgColor, labels=colorList, colors=colorList)
#         ax.axis("equal")
#         plt.savefig("./static/images/myFig2.png")	
#         plt.close()
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
#     graphPath1 = None
    if form.validate_on_submit():
        photo = form.upload.data.filename.split('.')[-1]
        imagePath = os.path.join('./static/images', f'photo.{photo}')
        graphPath1 = os.path.join('./static/images', f'myFig1.png')
#         graphPath2 = os.path.join('./static/images', f'myFig2.png')
        # Сохраняем наше загруженное изображение
        form.upload.data.save(imagePath)
        change_pic(imagePath, form.user.data)
    return render_template('main.html', form=form, image=imagePath, graph1=graphPath1)#, graph2=graphPath2)

# Запускаем наше приложение
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
    
    
    
