from tkinter import *
from tkinter.ttk import *
f = Tk()

def prin():
    print(choix.get())
choix = StringVar()
nom = ("Yavan","Rémi","Valentin")
w = Combobox(f, textvariable = choix,values = nom, state = 'readonly')
w.pack(side=LEFT)
b = Button(f,text="V",command=prin)
b.pack(side=LEFT)


f.mainloop()