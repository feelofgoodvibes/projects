import math
from tkinter import *

def prosti_mnoj(num, i = 2):
	if ((math.sqrt(num) + 1) <= i):
		result.insert(END, str(int(num)))
		return
	while (num % i == 0):
		if type_var.get():
			result.insert(END, str(int(i)) + ", ")
		else:
			result.insert(END, str(int(i)) + " * ")
		num /= i

	prosti_mnoj(num, i + 1)

def calculate_result():
	try: number = int(n_entry.get())
	except: return

	if clearVar.get():
		result.delete("1.0", END)
	elif result.get("1.0", "1.1") != "":
		result.insert(END, ';\n')

	result.insert(END, str(number) + " = ")
	prosti_mnoj(number)


root = Tk()

settingsFrame = Frame(root)

clearVar = IntVar()
clearResult = Checkbutton(settingsFrame, text = "Очищувати результат", variable = clearVar, onvalue = 1, offvalue = 0)

type_var = IntVar()
type_var.set(0)
type1 = Radiobutton(settingsFrame, text='Запис-1', variable=type_var, value=0)
type2 = Radiobutton(settingsFrame, text='Запис-2', variable=type_var, value=1)

entryFrame = Frame(root)
number_text = Label(entryFrame, text = "Число, яке потрібно розкласти: ", font = "Arial 13")
n_entry = Entry(entryFrame, font = "Arial 13")

result = Text(width = 50)
calculate = Button(font = "Arial 13", width = 40, text = "Розкласти", command = calculate_result)

entryFrame.pack()
settingsFrame.pack()

clearResult.pack()
type1.pack()
type2.pack()

number_text.pack(side = LEFT)
n_entry.pack(side = RIGHT)

calculate.pack()
result.pack()

root.resizable(False, False)
root.title("Розклад на прості множники")
root.mainloop()