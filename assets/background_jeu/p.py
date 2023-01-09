from tkinter import *
from PIL import Image, ImageTk

# Création de la fenêtre principale
root = Tk()

# Création de la Frame
frame = Frame(root)

# Chargement de l'image
image = Image.open('background1.png')

# Création de l'objet PhotoImage
photo_image = ImageTk.PhotoImage(image)

# Ajout de l'image en arrière-plan de la Frame
frame.create_image(0, 0, anchor=NW, image=photo_image)

# Création des boutons
button1 = Button(frame, text="Bouton 1")
button2 = Button(frame, text="Bouton 2")

# Affichage des boutons
button1.pack()
button2.pack()

# Affichage de la Frame
frame.pack()

root.mainloop()
