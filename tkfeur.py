from tkinter import *
from PIL import ImageFont,Image, ImageTk,ImageDraw
import sqlite3
import time
import socket
import pyglet, os
import tkinter.font
from tkinter import ttk
import socket
from socket import gethostbyname
import threading

jeu = Tk()
jeu.geometry("1200x560")
jeu.resizable(False,False)

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
		self.img=PhotoImage(file = "assets/background_jeu/"+str(self.nom)+"1.png",master=self.fenetre)
		background = Label(jeu,image=self.img)

		background.place(x=0,y=0,in_=self.fenetre)
		self.affiche = True
		return self.img



class Image_perso():
	def __init__(self,nom,fenetre,choix):
		self.nom = nom
		self.image = Image.open("images/"+str(self.nom)+".png")
		self.image = self.image.resize((60,60))
		self.image.save("images/choisi/"+str(self.nom)+".png")
		self.img = ImageTk.PhotoImage(file="images/choisi/"+str(nom)+".png")
		self.bouton = Button(fenetre,image=self.img,command=self.clic)
		self.labelimg = Label(fenetre,image=self.img)
		self.choix = choix
		self.fenetre = fenetre
	def bouton_image(self):
		return self.bouton
	def clic(self):
		thread1.start()
		jeu_ecran(self.choix)
	def label_image(self):
		return self.labelimg


class Personnages():
	def __init__(self,liste_personnages,fenetre,choix):
		self.liste_personnages = liste_personnages
		self.frame = Frame(fenetre)
		self.liste_image = []
		self.f2 = Frame(fenetre)
		self.choix = choix

	def afficher_en_bouton(self):
		id_perso = 0
		self.frame.pack_forget()
		self.frame=Canvas(jeu)
		self.frame.pack(pady=50)
		for ligne in range(5):
			for colone in range(5):
				self.f2=Canvas(self.frame)
				self.liste_image.append(Image_perso(self.liste_personnages[id_perso],self.f2,self.choix))
				id_perso+=1
				self.liste_image[id_perso-1].bouton_image().pack()
				self.label = Label(self.f2,text=self.liste_personnages[id_perso-1]+str(" (F)"),font=("Aqum two", 10))
				self.label.pack()
				self.f2.grid(row=ligne,column=colone,padx=3)

	def afficher_label(self):
		id_perso = 0
		self.frame.pack_forget()
		self.frame = Frame(jeu)
		self.frame.pack(side=LEFT,padx=50,pady=50)
		self.liste_image = []
		for ligne in range(5):
			for colone in range(5):
				self.f2=Canvas(self.frame)
				self.liste_image.append(Image_perso(self.liste_personnages[id_perso],self.f2,self.choix))
				id_perso+=1
				self.liste_image[id_perso-1].label_image().pack()
				self.label = Label(self.f2,text=self.liste_personnages[id_perso-1]+str(" (F)"),font=("Aqum two", 10))
				self.label.pack()
				self.f2.grid(row=ligne,column=colone,padx=3)




def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP



class Serveur():
	def __init__(self):
		self.pseudo = "Mon Pseudo"
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = (gethostbyname(str(extract_ip())), 6969)
		print("c'est good")
		self.sock.bind(self.server_address)
		self.sock.listen(1)
		print('Waiting for a connection')
		print(self.sock)
		self.connection, self.client_address = self.sock.accept()
	def recevoir_packet(self):
		try:
		    while True:
		        data = self.connection.recv(8096)
		        tchat.tchat.configure(state='normal')
		        tchat.tchat.insert(END,data.decode("utf-8"))
		        tchat.tchat.configure(state='disabled')
		        break
		finally:
		    None
	def envoyer_packet(self):
		try:
			message = self.pseudo+" : "+tchat.message.get()+str("\n")
			self.connection.sendall(message.encode("utf-8"))
		finally:
			None



class User_connect():
	def __init__(self,b):
		self.b=b
		self.ip = "13.569.456.11"
		self.pseudo = "Yavan"
	def afficher(self):
		if self.ip == None:
			self.b.create_text(985,200,text="Joueur en attente...",font=("Aqum two", 17))
			self.b.create_text(850,250,text="Joueur : ...",font=("Aqum two",15),anchor="nw")
			self.b.create_text(850,310,text="IP : ...",font=("Aqum two",15),anchor="nw")
			Label(jeu,text="En attente",font=("Aqum two",17)).place(x=169,y=438)
		else:
			self.b.create_text(985,200,text="Joueur connecté ! ",font=("Aqum two", 17))
			self.b.create_text(850,250,text="Joueur : "+str(self.pseudo),font=("Aqum two",15),anchor="nw")
			self.b.create_text(850,310,text="IP : "+str(self.ip),font=("Aqum two",15),anchor="nw")

class Tchat():
	def __init__(self,jeu):
		self.frame = Frame(jeu)
		self.tchat = Text(self.frame)
		self.lastmess = None
		self.message = StringVar()
		self.pseudo = "Feur"
		self.serveur = None
	def afficher(self):
		self.frame = Frame()
		self.tchat = Text(self.frame,width=30,bg="#31202c",fg="#ffffff",state='disabled')
		self.frame.pack(side=RIGHT,fill=Y,expand=False)
		self.tchat.pack(fill=Y,expand=True)
		self.entry = Entry(self.frame,bg="#b6418c",textvariable=self.message)
		self.entry.pack(side=LEFT,fill=BOTH,expand=True)
		self.bouton=Button(self.frame,text="Envoyer",bg="#852563",activebackground="#c14698",command=self.envoyer)
		self.bouton.pack(side=LEFT,fill=BOTH,expand=True)
	def envoyer(self):
		print(self.serveur)
		tchat.tchat.configure(state='normal')
		self.tchat.insert(END,"Moi : "+self.message.get()+str("\n"))
		tchat.tchat.configure(state='disable')
		self.serveur.envoyer_packet()
		self.message.set("")



def ecran_jeu(choix,perso):
	choix.background()
	perso.afficher_en_bouton()

def ecran_multi(jeu):
	ip = extract_ip()
	img=attente.background()
	frame_ip_jouer = Canvas(jeu,width=1200,height=560)
	frame_ip_jouer.create_image(600,280,image=img)
	frame_ip_jouer.create_text(225,100,text="Votre IP : "+str(ip),font=("Aqum two", 17))
	user_connection.b = frame_ip_jouer
	user_connection.afficher()
	frame_ip_jouer.pack(fill=BOTH,expand=True)

tchat=Tchat(jeu)

def jeu_ecran(choix):
	choix.background()
	perso.afficher_label()
	tchat.afficher()	


def setup_server():
	global tchat
	serveur = Serveur()
	print(serveur)
	
	tchat.serveur = serveur
	print(tchat.serveur)
	while True:
		serveur.recevoir_packet()

bdd = sqlite3.connect("bdd/animalcrossing.db")
curseur = bdd.cursor()
req = "SELECT perso_name FROM perso WHERE perso_id ="+str()
liste_personnages = [] 
for perso_id in range(1,26): 
	req = "SELECT perso_name FROM perso WHERE perso_id ="+str(perso_id) 
	r = curseur.execute(req) 
	liste_personnages.append(r.fetchall()[0][0]) 
 

choix = Background("background",jeu)
perso = Personnages(liste_personnages,jeu,choix)
attente = Background("IP",jeu)
user_connection = User_connect(None)


def ecran(choix,perso):
	attente = Background("IP",jeu)


	#ecran_jeu(choix,perso)
	ecran_multi(jeu)


thread1 = threading.Thread(target=setup_server)
ecran(choix,perso)
jeu.mainloop()