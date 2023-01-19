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
from math import *
from random import *

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
		self.image = Image.open("assets/perso_fin/"+str(self.nom)+".png")
		self.image = self.image.resize((63,63))
		self.image.save("images/choisi/"+str(nom)+".png")
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
			for colone in range(8):
				self.f2=Canvas(self.frame)
				self.liste_image.append(Image_perso(self.liste_personnages[id_perso],self.f2,self.choix))
				id_perso+=1
				self.liste_image[id_perso-1].bouton_image().pack()
				self.label = Label(self.f2,text=str(self.liste_personnages[id_perso-1])+str(" (F)"),font=("Aqum two", 10))
				self.label.pack()
				self.f2.grid(row=ligne,column=colone,padx=3)

	def afficher_label(self):
		id_perso = 0
		self.frame.pack_forget()
		self.frame = Frame(jeu)
		self.frame.pack(side=LEFT,padx=50,pady=50)
		self.liste_image = []
		for ligne in range(5):
			for colone in range(8):
				self.f2=Canvas(self.frame)
				self.liste_image.append(Image_perso(self.liste_personnages[id_perso],self.f2,self.choix))
				id_perso+=1
				self.liste_image[id_perso-1].label_image().pack()
				self.label = Label(self.f2,text=str(self.liste_personnages[id_perso-1])+str(" (F)"),font=("Aqum two", 10))
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

bdd = sqlite3.connect("bdd/perso.db")
curseur = bdd.cursor()


class Nb_attribut_list():
	def __init__(self,nom):
		self.requete = "SELECT * FROM "+str(nom.title())
		self.liste_tuple = curseur.execute(self.requete).fetchall()
		self.liste = []
		self.nom = nom
		numl = [i+1 for i in range(40)]
		nb = 0
		shuffle(numl)
		for i in range(len(self.liste_tuple)):
			liste = []
			liste.append(self.liste_tuple[i][1])
			liste.append(self.liste_tuple[i][0])
			if len(self.liste)==0:
				liste.append(self.tri(numl[0:ceil(40/len(self.liste_tuple))]))
				nb+=ceil(40/len(self.liste_tuple))
			else:
				liste.append(self.tri(numl[nb:nb+floor(40/len(self.liste_tuple))]))
				nb +=floor(40/len(self.liste_tuple))
			self.liste.append(liste)
		self.liste.insert(0,nom.title())


	def fusion(self,L1,L2):
		if L1 ==[]:
			return L2
		if L2 == []:
			return L1
		if L1[0]<L2[0]:
			return [L1[0]]+ self.fusion(L1[1:],L2)
		else:
			return [L2[0]] + self.fusion(L1, L2[1:])
	
	def tri(self,liste):
		nb = len(liste)
		if nb<=1:
			return liste
		L1 = liste[0:nb//2]
		L2 = liste[nb//2:nb]
		return self.fusion(self.tri(L1),self.tri(L2))

def compile_image_perso(perso_name,list_arg):
    perso = Image.open("assets/perso_vierge.png")
    perso = perso.convert("RGBA")
    cheveux = Image.open("assets/cheveux/cheveux"+str(list_arg[0])+".png")
    visage = Image.open("assets/visage/visage"+str(list_arg[1])+".png")
    yeux = Image.open("assets/yeux/yeux"+str(list_arg[2])+".png")
    nez = Image.open("assets/nez/nez"+str(list_arg[3])+".png")
    bouche = Image.open("assets/bouche/bouche"+str(list_arg[4])+".png")
    cosmetique = Image.open("assets/cosmetique/cosmetique"+str(list_arg[5])+".png")
    background = Image.open("assets/background/background"+str(list_arg[6])+".png")
    perso.alpha_composite(background)
    perso.alpha_composite(visage)
    perso.alpha_composite(yeux)
    perso.alpha_composite(bouche)
    perso.alpha_composite(cheveux)
    perso.alpha_composite(cosmetique)
    perso.alpha_composite(nez)
    perso.save("assets/perso_fin/"+str(perso_name)+".png")
    b = Image.open("assets/perso_fin/"+str(perso_name)+".png")
    b=b.convert("RGBA")
    b=b.resize((512,512))
    b.save("assets/perso_fin/"+str(perso_name)+".png")


class Gen_perso():
	def __init__(self):
		self.relation = {"Bouche":[(1,3),(2,2),(3,1),(4,1)],"Yeux":[(1,1),(2,2),(3,4),(4,2),(5,3),(6,2)],"Visage":[(1,1),(2,2)],"Nez":[(1,1),(2,2),(3,2)],"Cosmetique":[(1,1),(2,2)],"Cheuveux":[(1,1),(2,3),(3,5),(4,2),(5,4)],"Background":[(1,1)],"Genre":[(1,1),(2,2)]}
		self.liste_attribut = []
		self.liste_attribut.append(Nb_attribut_list("cheuveux").liste)
		self.liste_attribut.append(Nb_attribut_list("visage").liste)
		self.liste_attribut.append(Nb_attribut_list("yeux").liste)
		self.liste_attribut.append(Nb_attribut_list("nez").liste)
		self.liste_attribut.append(Nb_attribut_list("bouche").liste)
		self.liste_attribut.append(Nb_attribut_list("cosmetique").liste)
		self.liste_attribut.append(Nb_attribut_list("background").liste)
		self.liste_attribut.append(Nb_attribut_list("genre").liste)
		self.liste_perso = []
		for perso in range(1,41):
			self.generer_attribut_personnage(perso)
	def generer_attribut_personnage(self,nb_perso):
		self.dico_attribut = {"Cheuveux" : None,"Visage":None,"Yeux":None,"Nez":None,"Bouche":None,"Cosmetique":None,"Background":None,"Genre":None,}
		for l_attribut_simple in self.liste_attribut:
			for indice in range(1,len(l_attribut_simple)):
				random_attribut_list = []
				try:
					if nb_perso == l_attribut_simple[indice][2][0]:
						for num_att in self.relation[l_attribut_simple[0]]:
							if num_att[1] == l_attribut_simple[indice][1]:
								random_attribut_list.append(num_att[0])
								shuffle(random_attribut_list)
						l_attribut_simple[indice][2].pop(0)
						print(l_attribut_simple[indice][0],random_attribut_list[0])
						self.dico_attribut[l_attribut_simple[0]] = (l_attribut_simple[indice][0],random_attribut_list[0])
				except:
					None
		random_attribute = []
		compile_image_perso(nb_perso,[self.dico_attribut["Cheuveux"][1],self.dico_attribut["Visage"][1],self.dico_attribut["Yeux"][1],self.dico_attribut["Nez"][1],self.dico_attribut["Bouche"][1],self.dico_attribut["Cosmetique"][1],self.dico_attribut["Background"][1]])

liste_personnages = [] 

perso_creer = Gen_perso()
print("oui")
print(perso_creer.liste_perso)

for perso_id in range(1,41): 
	liste_personnages.append(perso_id) 
 

choix = Background("background",jeu)
perso = Personnages(liste_personnages,jeu,choix)
attente = Background("IP",jeu)
user_connection = User_connect(None)


def ecran(choix,perso):
	attente = Background("IP",jeu)


	ecran_jeu(choix,perso)
	#ecran_multi(jeu)


thread1 = threading.Thread(target=setup_server)
ecran(choix,perso)
jeu.mainloop()