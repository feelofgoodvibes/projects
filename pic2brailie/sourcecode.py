#!/usr/bin/python
# -*- coding: utf-8 -*-

# by ecyc
# ecyccc@gmail.com

import clipboard
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageGrab
from sys import exc_info, exit


# Таблица Брайля
braillie = {'blank': '​⠀','12345678':'⣿' ,'1': '⠁', '2': '⠂', '12': '⠃', '3': '⠄', '13': '⠅', '23': '⠆', '123': '⠇', '4': '⠈', '14': '⠉', '24': '⠊', '124': '⠋', '34': '⠌', '134': '⠍', '234': '⠎', '1234': '⠏', '5': '⠐', '15': '⠑', '25': '⠒', '125': '⠓', '35': '⠔', '135': '⠕', '235': '⠖', '1235': '⠗', '45': '⠘', '145': '⠙', '245': '⠚', '1245': '⠛', '345': '⠜', '1345': '⠝', '2345': '⠞', '12345': '⠟', '6': '⠠', '16': '⠡', '26': '⠢', '126': '⠣', '36': '⠤', '136': '⠥', '236': '⠦', '1236': '⠧', '46': '⠨', '146': '⠩', '246': '⠪', '1246': '⠫', '346': '⠬', '1346': '⠭', '2346': '⠮', '12346': '⠯', '56': '⠰', '156': '⠱', '256': '⠲', '1256': '⠳', '356': '⠴', '1356': '⠵', '2356': '⠶', '12356': '⠷', '456': '⠸', '1456': '⠹', '2456': '⠺', '12456': '⠻', '3456': '⠼', '13456': '⠽', '23456': '⠾', '123456': '⠿', '7': '⡀', '17': '⡁', '27': '⡂', '127': '⡃', '37': '⡄', '137': '⡅', '237': '⡆', '1237': '⡇', '47': '⡈', '147': '⡉', '247': '⡊', '1247': '⡋', '347': '⡌', '1347': '⡍', '2347': '⡎', '12347': '⡏', '57': '⡐', '157': '⡑', '257': '⡒', '1257': '⡓', '357': '⡔', '1357': '⡕', '2357': '⡖', '12357': '⡗', '457': '⡘', '1457': '⡙', '2457': '⡚', '12457': '⡛', '3457': '⡜', '13457': '⡝', '23457': '⡞', '123457': '⡟', '67': '⡠', '167': '⡡', '267': '⡢', '1267': '⡣', '367': '⡤', '1367': '⡥', '2367': '⡦', '12367': '⡧', '467': '⡨', '1467': '⡩', '2467': '⡪', '12467': '⡫', '3467': '⡬', '13467': '⡭', '23467': '⡮', '123467': '⡯', '567': '⡰', '1567': '⡱', '2567': '⡲', '12567': '⡳', '3567': '⡴', '13567': '⡵', '23567': '⡶', '123567': '⡷', '4567': '⡸', '14567': '⡹', '24567': '⡺', '124567': '⡻', '34567': '⡼', '134567': '⡽', '234567': '⡾', '1234567': '⡿', '8': '⢀', '18': '⢁', '28': '⢂', '128': '⢃', '38': '⢄', '138': '⢅', '238': '⢆', '1238': '⢇', '48': '⢈', '148': '⢉', '248': '⢊', '1248': '⢋', '348': '⢌', '1348': '⢍', '2348': '⢎', '12348': '⢏', '58': '⢐', '158': '⢑', '258': '⢒', '1258': '⢓', '358': '⢔', '1358': '⢕', '2358': '⢖', '12358': '⢗', '458': '⢘', '1458': '⢙', '2458': '⢚', '12458': '⢛', '3458': '⢜', '13458': '⢝', '23458': '⢞', '123458': '⢟', '68': '⢠', '168': '⢡', '268': '⢢', '1268': '⢣', '368': '⢤', '1368': '⢥', '2368': '⢦', '12368': '⢧', '468': '⢨', '1468': '⢩', '2468': '⢪', '12468': '⢫', '3468': '⢬', '13468': '⢭', '23468': '⢮', '123468': '⢯', '568': '⢰', '1568': '⢱', '2568': '⢲', '12568': '⢳', '3568': '⢴', '13568': '⢵', '23568': '⢶', '123568': '⢷', '4568': '⢸', '14568': '⢹', '24568': '⢺', '124568': '⢻', '34568': '⢼', '134568': '⢽', '234568': '⢾', '1234568': '⢿', '78': '⣀', '178': '⣁', '278': '⣂', '1278': '⣃', '378': '⣄', '1378': '⣅', '2378': '⣆', '12378': '⣇', '478': '⣈', '1478': '⣉', '2478': '⣊', '12478': '⣋', '3478': '⣌', '13478': '⣍', '23478': '⣎', '123478': '⣏', '578': '⣐', '1578': '⣑', '2578': '⣒', '12578': '⣓', '3578': '⣔', '13578': '⣕', '23578': '⣖', '123578': '⣗', '4578': '⣘', '14578': '⣙', '24578': '⣚', '124578': '⣛', '34578': '⣜', '134578': '⣝', '234578': '⣞', '1234578': '⣟', '678': '⣠', '1678': '⣡', '2678': '⣢', '12678': '⣣', '3678': '⣤', '13678': '⣥', '23678': '⣦', '123678': '⣧', '4678': '⣨', '14678': '⣩', '24678': '⣪', '124678': '⣫', '34678': '⣬', '134678': '⣭', '234678': '⣮', '1234678': '⣯', '5678': '⣰', '15678': '⣱', '25678': '⣲', '125678': '⣳', '35678': '⣴', '135678': '⣵', '235678': '⣶', '1235678': '⣷', '45678': '⣸', '145678': '⣹', '245678': '⣺', '1245678': '⣻', '345678': '⣼', '1345678': '⣽', '2345678': '⣾'}


# Функция выбора файла
def getfile(event = None): 
	temptext = filedialog.askopenfilename(initialdir = "/",title = "Выберите файл",filetypes = (("All files",("*.*")),("JPG","*.jpg"),("JPEG","*.jpeg"),("GIF","*.gif"),("PNG","*.png")))
	imgpathEntry.delete('0', END)
	imgpathEntry.insert(END, temptext)


# Синхронизация SCROLL и ENTRY размера и уровня цвета
def scrollListener(val, target):
	if target == 'size':
		sizeEntry.delete(0, END)
		sizeEntry.insert(0, val)
	if target == 'lvl':
		lvlEntry.delete(0, END)
		lvlEntry.insert(0, val)


def change_var(a,b,c):
	if styleVar.get() == 'По цвету':
		lvlLabel.config(text='Уровень цвета:')
		lvlScroll.config(to=765)
	else:
		lvlLabel.config(text='Уровень яркости:')
		lvlScroll.config(to=255)


# Изменение активности компонентов GUI
def toggler(target):
	if target == 'clip':
		if clipVar.get():
			imgpathLabel.config(state='disable')
			imgpathEntry.config(state='disable')
			imgpathButton.config(state='disable')
		else:
			imgpathLabel.config(state='normal')
			imgpathEntry.config(state='normal')
			imgpathButton.config(state='normal')
	if target == 'crit':
		if critVar.get():
			lvlLabel.config(state='disable')
			lvlEntry.config(state='disable')
			lvlScroll.config(state='disable')
			styleMenu.config(state='disable')
		else:
			lvlLabel.config(state='normal')
			lvlEntry.config(state='normal')
			lvlScroll.config(state='normal')
			styleMenu.config(state='normal')



# 1. Получение всех параметров из интерфейса
# 2. Вызов функции конвертирования
# 3. Перенос ретурна конвертирования в текстовое поле
def generate(event = None):
	if clipVar.get(): IMGPATH = 'clip'
	else: IMGPATH = imgpathEntry.get()

	try: 
		RESIZE = int(sizeEntry.get())
	except:
		messagebox.showerror('!','Размер принимает только числовые значения')
		return None

	try:
		LVL = int(lvlEntry.get())
	except:
		messagebox.showerror('!','Уровень цвета принимает только числовые значения')
		return None

	if invVar.get(): INVERT = True
	else: INVERT = False
	if replVar.get():
		braillie['blank'] = '⠁'
	else:
		braillie['blank'] = '​⠀'
	art = img_to_brailie(IMGPATH, LVL, RESIZE, INVERT)
	if art == None: return
	mainText.delete('0.0', END)
	mainText.insert('0.0', art)



# Вся магия тут
def img_to_brailie(img_path, level, resize = False, invert = False):
	# Изображение из буфера обмена
	if img_path == 'clip':
		img = ImageGrab.grabclipboard()
		if type(img) == type(None):
			messagebox.showerror('!','В буфере обмена нету изображения!')
			return None
	
	# Изображение из указаного пути
	else:
		try: img = Image.open(img_path)
		except:
			messagebox.showerror('!','Что-то не так с изображением. Либо по указаному пути нету изображения\nСкорее всего, исходный файл - не изображение, либо его тип не поддерживается')
			return None

	# Конвертирование
	if critVar.get(): img = img.convert('1')
	else: 
		if styleVar.get() == 'По цвету': 
			img = img.convert('RGB')
		else:
			img = img.convert('RGB').convert('HSV')

	# Изменение размера изображения
	if resize:
		img.thumbnail((resize,resize))
	data =list(img.getdata())
	# Превращение цветного изображения в массив из нулей и едениц
	# основываясь на параметре "Уровень цвета"
	for i,x in enumerate(data):
		if critVar.get():
			if invert:
				if x == 0: data[i] = 0
				else: data[i] = 1
			else:
				if x == 0: data[i] = 1
				else: data[i] = 0
			continue

		summa = 0
		if styleVar.get() == 'По цвету': 
			for v in x: summa += v
		else: summa = x[2]

		if invert:
			if summa > level: data[i] = 1
			else: data[i] = 0
		else:
			if summa < level: data[i] = 1
			else: data[i] = 0
	# Формирование 2D матрицы
	art = ''
	OX = img.size[0]
	OY = img.size[1]
	matrix = []
	for x in range(0,OX*OY,OX):
		matrix.append(list(data[x:x+OX]))

	curX = 0
	curY = 0

	# Оптимизация
	if optVar.get():
		try:
			while 1 not in matrix[0]:
				matrix.pop(0)

			while 1 not in matrix[-1]:
				matrix.pop(len(matrix)-1)


			while True:
				clearFlag = True
				for x in matrix:
					if x[0] == 1: 
						clearFlag = False
						break

				if not clearFlag: break
				for i,x in enumerate(matrix):
					matrix[i] = x[1:]

			while True:
				clearFlag = True
				for x in matrix:
					if x[-1] == 1: 
						clearFlag = False
						break

				if not clearFlag: break
				for i,x in enumerate(matrix):
					matrix[i] = x[:-1]



			while 0 not in matrix[0]:
				matrix.pop(0)

			while 0 not in matrix[-1]:
				matrix.pop(len(matrix)-1)


			while True:
				clearFlag = True
				for x in matrix:
					if x[0] == 0: 
						clearFlag = False
						break

				if not clearFlag: break
				for i,x in enumerate(matrix):
					matrix[i] = x[1:]

			while True:
				clearFlag = True
				for x in matrix:
					if x[-1] == 0: 
						clearFlag = False
						break

				if not clearFlag: break
				for i,x in enumerate(matrix):
					matrix[i] = x[:-1]
		except:
			if len(matrix) == 0:
				matrix = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
			else:
				messagebox.showerror('!','Во время оптимизации все было удалено\nЭто значит, что нужно изменить размер, или уровень цвета\n(Если фото приемущественно из светлых цветов - нужно увеличить уровень цвета при выключеной инверсии\nЕсли фото приемущественно из темных цветов - нужно уменьшить уровень цвета)\n\nКроме того, размер цвета не должен быть выше 765!')
				return None

		OX = len(matrix[0])
		OY = len(matrix)

	# Формирование конечного результата
	while curX < OY:
		cur = ''
		try:
			if matrix[curX][curY]: cur += '1'
		except: pass
		try:
			if matrix[curX+1][curY]: cur += '2'
		except: pass
		try:
			if matrix[curX+2][curY]: cur += '3'
		except: pass

		try:
			if matrix[curX][curY+1]: cur += '4'
		except: pass
		try:
			if matrix[curX+1][curY+1]: cur += '5'
		except: pass
		try:
			if matrix[curX+2][curY+1]: cur += '6'
		except: pass

		try:
			if matrix[curX+3][curY]: cur += '7'
		except: pass
		try:
			if matrix[curX+3][curY+1]: cur += '8'
		except: pass

		if cur == '': cur = 'blank'
		art += braillie[cur]

		curY += 2
		if curY >= OX:
			art += '\n'
			curY = 0
			curX += 4

	return art

# GUI
root = Tk()
clipVar = IntVar()
invVar = IntVar()
replVar = IntVar()
optVar = IntVar()
critVar = IntVar()
styleVar = StringVar()

mainText = Text()
imgpathLabel = Label(text='Путь к фото:', font = 'Arial 11')
imgpathEntry = Entry()
imgpathButton = Button(text='Open...', command = getfile)
clipboardCheck=Checkbutton(text='Из буфера',variable=clipVar,onvalue=1,offvalue=0, command = lambda: toggler('clip'))

sizeLabel = Label(text='Размер:', font = 'Arial 13')
sizeScroll = Scale(orient=HORIZONTAL,from_=0,to=500,tickinterval=100,resolution=1, command = lambda x: scrollListener(x,'size'))
sizeEntry = Entry()
sizeEntry.insert(0,100)
sizeScroll.set(100)
choices = {'По цвету', 'По яркости'}
styleMenu = OptionMenu(root,styleVar, *choices)
styleVar.set('По цвету')

lvlLabel = Label(text='Уровень цвета:', font = 'Arial 13')
lvlScroll = Scale(orient=HORIZONTAL,from_=0,to=765,tickinterval=100,resolution=1, command = lambda x: scrollListener(x,'lvl'))
lvlEntry  = Entry()
lvlEntry.insert(0,200)
lvlScroll.set(200)

invertCheck = Checkbutton(text='Инверсия',variable=invVar,onvalue=1,offvalue=0)
replCheck = Checkbutton(text='Заменить пустые пиксели на [⠁]\n(отметить, если результат кривой)',variable=replVar,onvalue=1,offvalue=0)
optCheck = Checkbutton(text='Оптимизация',variable=optVar,onvalue=1,offvalue=0)
critCheck = Checkbutton(text='Критический контраст',variable=critVar,onvalue=1,offvalue=0, command = lambda: toggler('crit'))
generateButton = Button(text='Старт', font = 'Arial 18', command = generate)
copyButton = Button(text='Скопировать', font = 'Arial 18', command = lambda: clipboard.copy(mainText.get('0.0',END)[:-1]))

mainText.place(relx=0.6,rely=0.01, relwidth = 0.6, relheight = 1, anchor = 'ne')
imgpathLabel.place(relx = 0.61, rely = 0.01, width = 84)
imgpathEntry.place(relx = 0.67, rely = 0.013, relwidth = 0.072)
imgpathButton.place(relx = 0.75, rely = 0.01)
clipboardCheck.place(relx = 0.61, rely = 0.04)

sizeLabel.place(relx = 0.61, rely = 0.09)
sizeScroll.place(relx = 0.61, rely = 0.115, relwidth = 0.2)
sizeEntry.place(relx = 0.66, rely = 0.094)
styleMenu.place(relx = 0.61, rely = 0.198)
lvlLabel.place(relx = 0.61, rely = 0.25)
lvlScroll.place(relx = 0.61, rely = 0.278, relwidth = 0.2)
lvlEntry.place(relx = 0.7, rely = 0.255)

invertCheck.place(relx = 0.61, rely = 0.35)
replCheck.place(relx = 0.61, rely = 0.38)
optCheck.place(relx = 0.61, rely = 0.43)
critCheck.place(relx = 0.61, rely = 0.47)

generateButton.place(relx = 0.61, rely = 0.53, relwidth = 0.2)
copyButton.place(relx = 0.61, rely = 0.59, relwidth = 0.2)

styleVar.trace('w', change_var)

root.state('zoomed')
root.bind('<Up>', lambda x: sizeScroll.set(sizeScroll.get()+1))
root.bind('<Down>', lambda x: sizeScroll.set(sizeScroll.get()-1))
root.bind('<Left>', lambda x: lvlScroll.set(lvlScroll.get()-1))
root.bind('<Right>', lambda x: lvlScroll.set(lvlScroll.get()+1))
root.bind('<Return>', generate)
root.title('pic2txt')
root.iconbitmap('ico.ico')
root.mainloop()