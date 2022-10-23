import os
import shutil
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
from PIL import Image

# Запрос директории
def insert_text():
    path = fd.askdirectory()
    return path

# Проверка безопасности PIN
def checking_PIN(pin):
    if pin == current_PIN:
        label1.config(text='Успешно!', fg='green')
        Label(root, text="Выберете длину в пикселях:", bg='#4cf5ae', font="Verdana 12").pack(side=TOP, pady=0)
        scale = Scale(root, orient=HORIZONTAL, length=241, from_=5000, to=30000, tickinterval=25000, resolution=5000, highlightthickness=0, bg='#4cf5ae', font='Verdana 10', variable=px)
        scale.pack(side=TOP, pady=0)
        scale.set(30000)
        button2 = Button(text='Выбрать папку\nс изображениями', font='Verdana 14', width=18, height=2, command= lambda: paste(insert_text()))
        button2.pack(side=TOP, pady=15)
    else:
        label1.config(text='Неверный PIN!', fg='red')

# Процесс склеивания
def paste(pics_path = '.'):
    
    # Чистка и создание новой result папки
    result_path = os.path.join(pics_path, 'result')
    if os.path.exists(result_path):
        shutil.rmtree(result_path)
    os.mkdir(result_path)

    # Расчет длины результирующего изображения
    counter = 0
    img_width = 720
    bg_size = [0]
    pathways = []
    total_pictures_list = []
    for file in os.listdir(pics_path):
        if file.endswith(pictures_format):
            total_pictures_list.append(file)

    for pic in total_pictures_list:
        img = Image.open(pics_path + '/' + pic)
        if img.size[0] < img_width:
            coef = img_width / (img.size[0] - (0.1 * img.size[0]))
            img = img.resize([round(img.size[0]*coef), round(img.size[1]*coef)])
        img.thumbnail((img_width, img.size[1]))
        bg_size[counter] += img.size[1]
        pathways.append(pic)

        if bg_size[counter] > px.get()-1000 or pic == total_pictures_list[-1]:
            # Создание фона нужного размера
            #print(px.get())
            bg = Image.new('RGBA', (img_width, bg_size[counter]), 'black')
            if pic != total_pictures_list[-1]:
                bg_size.append(0)
            
            # Склеивание (накладывание) последовательности изображений на фон
            y = [0]
            for picpath in pathways:
                image = Image.open(pics_path + '/' + picpath)
                if image.size[0] < img_width:
                    coef = img_width / (image.size[0] - (0.1 * image.size[0]))
                    image = image.resize([round(image.size[0]*coef), round(image.size[1]*coef)])
                image.thumbnail((img_width, image.size[1]))
                bg.paste(image, (0, sum(y)))
                y.append(image.size[1])

            # Сохранение результата
            bg.save(result_path + f'/result{counter+1}.png')
            #print(pathways)
            pathways = []
            #root.destroy()
            counter += 1

    #print(bg_size)

    # Диалоговое окно с результатами
    answer = messagebox.askyesno(title="Успешно!", 
                        message=f"Результат сохранен в папке result в указанной директории.\n\n  Всего скомпановано изображений: {len(total_pictures_list)}\n  Создано сканов: {counter}.\n\nОткрыть папку с результатами?")
    if answer:
        os.startfile(result_path)

# main
current_PIN = '1994'
pictures_format = ('.jpg', '.png')
root = Tk()
px = IntVar()
PIN = StringVar()
root.title('Image Editor')
root.geometry('350x350')
root['bg'] = '#4cf5ae'
Label(root, text="Введите PIN", bg='#4cf5ae', font="Verdana 16").pack(side=TOP, pady=3)
e1 = Entry(root, font='Verdana 16', width=18, justify=CENTER, textvariable=PIN)
e1.pack(side=TOP, pady=3)
button1 = Button(text='Войти', width=18, height=1, font='Verdana 16', command= lambda: checking_PIN(PIN.get()))
button1.pack(side=TOP, pady=3)
label1 = Label(root, text="", bg='#4cf5ae', font="Verdana 12")
label1.pack_forget()
label1.pack(side=TOP, pady=3)



root.mainloop()