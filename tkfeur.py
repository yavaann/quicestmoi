from tkinter import *
from PIL import ImageFont,Image, ImageTk,ImageDraw
import sqlite3

jeu = Tk()
jeu.geometry("1200x560")
jeu.resizable(False,False)
bdd = sqlite3.connect("bdd/animalcrossing.db")
curseur = bdd.cursor()
req = "SELECT perso_name FROM perso WHERE perso_id ="+str()

class Background():
	"""Cette class permet de creer un background, à partir d'une image il va être redimentionné si besoin
	avec la méthode resize_background mais également être affiché via la méthode background"""
	def __init__(self,nom,fenetre):
		self.nom = nom
		self.fenetre = fenetre

	def resize_background(self):
		b = Image.open("assets/background_jeu/"+str(self.nom)+".png")
		b=b.convert("RGBA")
		b=b.resize((1200,560))
		b.save("assets/background_jeu/"+str(self.nom)+"1.png")

	def background(self):
		self.resize_background()
		img=PhotoImage(file = "assets/background_jeu/"+str(self.nom)+"1.png",master=self.fenetre)
		background = Label(jeu,image=img)
		background.img = img 
		background.place(x=0,y=0)



liste_personnages = []
for perso_id in range(1,26):
	req = "SELECT perso_name FROM perso WHERE perso_id ="+str(perso_id)
	r = curseur.execute(req)
	liste_personnages.append(r.fetchall()[0][0])

class Image_perso():
	def __init__(self,nom,fenetre):
		self.nom = nom
		self.image = Image.open("images/"+str(self.nom)+".png")
		self.image = self.image.resize((60,60))
		self.image.save("images/choisi/"+str(self.nom)+".png")
		self.img = ImageTk.PhotoImage(file="images/choisi/"+str(nom)+".png")
		self.bouton = Button(fenetre,image=self.img,command=None)
	def bouton_image(self):
		return self.bouton


class Personnages():
	def __init__(self,liste_personnages,fenetre):
		self.liste_personnages = liste_personnages
		self.frame = Frame(fenetre)
		self.liste_image = []

	def afficher_en_bouton(self):
		id_perso = 0
		self.frame.pack()
		for ligne in range(5):
			for colone in range(5):
				self.liste_image.append(Image_perso(self.liste_personnages[id_perso],self.frame))
				id_perso+=1
				self.liste_image[id_perso-1].bouton_image().grid(row=ligne, column=colone,pady=10,padx=10)



		


choix = Background("background",jeu)

def Ecran_jeu():
	choix.background()
	perso = Personnages(liste_personnages,jeu) 
	perso.afficher_en_bouton()



Ecran_jeu()


jeu.mainloop()
