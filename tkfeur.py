from tkinter import *
from PIL import ImageFont,Image, ImageTk,ImageDraw,ImageFile
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
import re
import marshal
ImageFile.LOAD_TRUNCATED_IMAGES = True

jeu = Tk()
jeu.geometry("1200x760")
jeu.resizable(False,False)
serv_or_join = None
class Background():
	"""Cette class permet de creer un background, à partir d'une image il va être redimentionné si besoin
	avec la méthode resize_background mais également être affiché via la méthode background"""
	def __init__(self,nom,fenetre):
		self.nom = nom
		self.fenetre = fenetre

	def resize_background(self):
		b = Image.open("assets/background_jeu/"+str(self.nom)+".png")
		b=b.convert("RGBA")
		b=b.resize((1200,760))
		b.save("assets/background_jeu/"+str(self.nom)+"1.png")

	def background(self):
		self.resize_background()
		self.img=PhotoImage(file = "assets/background_jeu/"+str(self.nom)+"1.png",master=self.fenetre)
		background = Label(jeu,image=self.img)

		background.place(x=-2,y=-2,in_=self.fenetre)
		self.affiche = True
		return self.img



class Image_perso():
	def __init__(self,nom,fenetre,choix):
		self.nom = nom
		self.image = Image.open("assets/perso_fin/"+str(self.nom)+".png")
		self.image = self.image.resize((75,75))
		self.image.save("assets/perso_fini/"+str(nom)+".png")
		self.img = ImageTk.PhotoImage(file="assets/perso_fini/"+str(nom)+".png")
		self.bouton = Button(fenetre,image=self.img,command=self.clic,bg="#c14698",bd=0,activebackground="#852563")
		self.labelimg = Label(fenetre,image=self.img,bg="#c14698")
		self.choix = choix
		self.fenetre = fenetre
	def bouton_image(self):
		return self.bouton
	def clic(self):
		jeu_ecran(self.choix)
	def label_image(self):
		return self.labelimg


class Personnages():
	def __init__(self,liste_personnages,fenetre,choix):
		self.liste_personnages = liste_personnages
		self.frame = Frame(fenetre,bg="#c14698")
		self.liste_image = []
		self.f2 = Frame(fenetre,bg="#c14698")
		self.choix = choix

	def afficher_en_bouton(self):
		id_perso = 0
		self.frame.pack_forget()
		self.frame=Frame(jeu,bg="#c14698")
		self.frame.pack(padx=90,pady=90)
		for ligne in range(5):
			for colone in range(8):
				self.f2=Frame(self.frame,bg="#c14698")
				self.liste_image.append(Image_perso(self.liste_personnages[id_perso],self.f2,self.choix))
				id_perso+=1
				self.liste_image[id_perso-1].bouton_image().pack()
				self.label = Label(self.f2,text=str(self.liste_personnages[id_perso-1])+str(" (F)"),font=("Aqum two", 10),bg="#c14698")
				self.label.pack()
				self.f2.grid(row=ligne,column=colone,padx=3)

	def afficher_label(self):
		id_perso = 0
		self.frame.pack_forget()
		self.frame = Frame(jeu,bg="#c14698")
		self.frame.pack(side=LEFT,padx=50,pady=50)
		self.liste_image = []
		for ligne in range(5):
			for colone in range(8):
				self.f2=Frame(self.frame,bg="#c14698")
				self.liste_image.append(Image_perso(self.liste_personnages[id_perso],self.f2,self.choix))
				id_perso+=1
				self.liste_image[id_perso-1].label_image().pack()
				self.label = Label(self.f2,text=str(self.liste_personnages[id_perso-1])+str(" (F)"),font=("Aqum two", 10),bg="#c14698")
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
		global serv_or_join
		serv_or_join = "serv"
		self.pseudo = user_connection.pseudo.get()
		print(self.pseudo)
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
		        if data.decode("utf-8")[0] == "t":
		        	tchat.tchat.configure(state='normal')
		        	tchat.tchat.insert(END,data.decode("utf-8")[1:])
		        	tchat.tchat.configure(state='disabled')
		        break
		except:
		    None
	def envoyer_packet(self):
		try:
			if tchat.message.get()!="":
				message = "t"+self.pseudo+" : "+tchat.message.get()+str("\n")
				self.connection.sendall(message.encode("utf-8"))
		finally:
			None
	def connect(self):
		user_connection.ip = self.client_address
		print(self.client_address)
		data = self.connection.recv(8096)
		user_connection.pseudo = data.decode("utf-8")
		user_connection.afficher()
		self.connection.sendall(perso_creer.envoyer_liste())


class User_connect():
	def __init__(self,b):
		self.b=b
		self.ip = None
		self.bouton = PhotoImage(file=r"assets/background_jeu/bouton_jouer.png")
		self.pseudo = StringVar()
		self.pseudo_enter = None
		self.confirmer = None
	def afficher(self):
		if self.ip == None:
			self.ip = extract_ip()
			img=attente.background()
			frame_ip_jouer = Canvas(jeu,width=1200,height=760)
			frame_ip_jouer.create_image(600,380,image=img)
			self.b = frame_ip_jouer
			self.b.create_text(985,200,text="Joueur en attente...",font=("Aqum two", 17))
			self.b.create_text(850,250,text="Joueur : ...",font=("Aqum two",15),anchor="nw")
			self.b.create_text(850,310,text="IP : ...",font=("Aqum two",15),anchor="nw")
			Label(jeu,text="En attente",font=("Aqum two",17)).place(x=169,y=438)
			self.pseudo_enter = Entry(jeu,textvariable=self.pseudo,font=("Aqum two",13),width=14)
			self.pseudo_enter.place(x=600,y=85)
			self.confirmer = Button(jeu,command=self.confirm,text="✓")
			self.confirmer.place(x=770,y=86)
		else:
			self.b.pack_forget()
			ip = extract_ip()
			img=attente.background()
			frame_ip_jouer = Canvas(jeu,width=1200,height=760)
			frame_ip_jouer.create_image(600,380,image=img)
			frame_ip_jouer.create_text(225,100,text="Votre IP : "+str(ip),font=("Aqum two", 17))
			self.b = frame_ip_jouer
			self.b.create_text(985,200,text="Joueur connecté ! ",font=("Aqum two", 17))
			self.b.create_text(850,250,text="Joueur : "+str(self.pseudo),font=("Aqum two",15),anchor="nw")
			self.b.create_text(850,310,text="IP : "+str(self.ip[0]),font=("Aqum two",15),anchor="nw")
			Button(jeu,image=self.bouton,command=self.jouer).place(x=60,y=409)
			self.pseudo_enter.place(x=600,y=85)
		self.b.pack()
	def jouer(self):
		self.b.pack_forget()
		choix.background()
		perso.afficher_en_bouton()
	def confirm(self):
		self.confirmer.place_forget()
		self.b.create_text(225,100,text="Votre IP : "+str(self.ip),font=("Aqum two", 17))
		self.pseudo_enter.configure(state="disabled")
		thread1.start()
class Tchat():
	def __init__(self,jeu):
		global serv_or_join
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
		if self.message !="":
			tchat.tchat.configure(state='normal')
			self.tchat.insert(END,"Moi : "+self.message.get()+str("\n"))
			tchat.tchat.configure(state='disable')
			self.serveur.envoyer_packet()
		self.message.set("")

bouton=PhotoImage(file=r"assets/background_jeu/bouton_jouer.png")
bouton1=PhotoImage(file=r"assets/background_jeu/bouton_jouer1.png")

def make_perso(liste_perso):
	perso =Personnages(liste_perso,jeu,choix)
	return perso

class Join():
	def __init__(self,pseudo,ip):
		for widget in jeu.winfo_children():
			widget.pack_forget()
		self.pseudo = pseudo
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = (ip, 6969)
		print('Connecting to {} port {}'.format(*self.server_address))
		self.sock.connect(self.server_address)
		self.sock.sendall(pseudo.encode("utf-8"))
		data = self.sock.recv(8096)
		data = marshal.loads(data)
		Gen_perso_par_liste(data)
		liste_perso = []
		for i in range(40):
			liste_perso.append(data[i*9])
		print(liste_perso)
		self.perso = make_perso(liste_perso)
		choix.background()
		self.perso.afficher_en_bouton()
	def recevoir_packet(self):
	    while True:
	    	data = self.sock.recv(8096)
	    	if data.decode("utf-8")[0] == "t":
	    		tchat.tchat.configure(state="normal")
	    		tchat.tchat.insert(END,data.decode("utf-8")[1:])
	    		tchat.tchat.configure(state="disabled")
	def envoyer_packet(self):
		if tchat.message.get()!="":
			message = "t"+self.pseudo+" : "+tchat.message.get()+str("\n")
			self.sock.sendall(message.encode("utf-8"))



def ecran_principal(principal):
	principal.background()
	Button(jeu,text="Jouer",font=("Aqum two",17),image=bouton,command=ecran_multi).pack()
	Button(jeu,text="Jouer",font=("Aqum two",17),image=bouton1,command=ecran_join).pack()



def ecran_jeu(choix,perso):
	choix.background()
	perso.afficher_en_bouton()

def ecran_join():
	def client():
		if ip.get() != "" and pseudo.get() != "":
			serv = Join(pseudo.get(),ip.get())
			tchat.serveur = serv
			while True:
				serv.recevoir_packet()
	for widget in jeu.winfo_children():
		widget.pack_forget()
	thread3 = threading.Thread(target=client)
	choix.background()
	ip = StringVar()
	Entry(jeu,textvariable=ip).pack()
	pseudo = StringVar()
	Entry(jeu,textvariable=pseudo).pack()
	Button(jeu,command=thread3.start).pack()


def ecran_multi():
	for widget in jeu.winfo_children():
		widget.pack_forget()
	user_connection.afficher()

tchat=Tchat(jeu)

def jeu_ecran(choix):
	for widget in jeu.winfo_children():
		widget.pack_forget()
	choix.background()
	perso.afficher_label()
	tchat.afficher()	


def setup_server():
	global tchat
	serveur = Serveur()
	tchat.serveur = serveur
	serveur.connect()
	while True:
		serveur.recevoir_packet()

def join_server():
	global tchat
	serv = Join(None)

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
    background = background.convert("RGBA")
    background = background.resize((427,427))
    cadre = Image.open("assets/cadre.png")
    perso.alpha_composite(background)
    perso.alpha_composite(visage)
    perso.alpha_composite(yeux)
    perso.alpha_composite(bouche)
    perso.alpha_composite(cheveux)
    perso.alpha_composite(cosmetique)
    perso.alpha_composite(nez)
    perso.alpha_composite(cadre)
    perso.save("assets/perso_fin/"+str(perso_name)+".png")
    b = Image.open("assets/perso_fin/"+str(perso_name)+".png")
    b=b.convert("RGBA")
    b=b.resize((512,512))
    b.save("assets/perso_fin/"+str(perso_name)+".png")


class Gen_perso():
	def __init__(self,liste_perso):
		self.relation = {"Bouche":[(1,3),(2,2),(3,1),(4,4),(5,2),(6,4),(7,2),(8,2),(9,1)],"Yeux":[(1,1),(2,2),(3,4),(4,2),(5,3),(6,3),(7,3),(8,5),(9,3),(10,3),(11,2),(12,5),(13,4),(14,2),(15,3),(16,3),(17,4),(18,5),(19,3),(20,2),(21,4),(22,5),(23,3)],"Visage":[(1,1),(2,2)],"Nez":[(1,1),(2,2),(3,2),(4,2),(5,2),(6,1),(7,1)],"Cosmetique":[(1,1),(2,2)],"Cheuveux":[(1,1),(2,3),(3,5),(4,2),(5,4),(6,2),(7,3),(8,1)],"Background":[(1,1),(2,1),(3,2),(4,2),(5,2),(6,3),(7,3),(8,3)],"Genre":[(1,1),(2,2)]}
		self.liste_attribut = []
		self.liste_attribut.append(Nb_attribut_list("cheuveux").liste)
		self.liste_attribut.append(Nb_attribut_list("visage").liste)
		self.liste_attribut.append(Nb_attribut_list("yeux").liste)
		self.liste_attribut.append(Nb_attribut_list("nez").liste)
		self.liste_attribut.append(Nb_attribut_list("bouche").liste)
		self.liste_attribut.append(Nb_attribut_list("cosmetique").liste)
		self.liste_attribut.append(Nb_attribut_list("background").liste)
		self.liste_attribut.append(Nb_attribut_list("genre").liste)
		self.liste_perso = liste_perso
		self.liste_attribut_total = []
		
		for perso in range(1,len(self.liste_perso)+1):
			print(perso)
			self.generer_attribut_personnage(perso)
		print(len(self.liste_attribut_total))
		print(Gen_perso_par_liste(self.liste_attribut_total))
	def generer_attribut_personnage(self,nb_perso):
		self.dico_attribut = {"Cheuveux" : None,"Visage":None,"Yeux":None,"Nez":None,"Bouche":None,"Cosmetique":None,"Background":None,"Genre":None}
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
						self.dico_attribut[l_attribut_simple[0]] = (l_attribut_simple[indice][0],random_attribut_list[0])
				except:
					None
		random_attribute = []
		self.liste_attribut_total.append(self.liste_perso[nb_perso-1])
		self.liste_attribut_total.append(self.dico_attribut["Cheuveux"][1])
		self.liste_attribut_total.append(self.dico_attribut["Visage"][1])
		self.liste_attribut_total.append(self.dico_attribut["Yeux"][1])
		self.liste_attribut_total.append(self.dico_attribut["Nez"][1])
		self.liste_attribut_total.append(self.dico_attribut["Bouche"][1])
		self.liste_attribut_total.append(self.dico_attribut["Cosmetique"][1])
		self.liste_attribut_total.append(self.dico_attribut["Background"][1])
		self.liste_attribut_total.append(self.dico_attribut["Genre"][1])
		compile_image_perso(nb_perso,[self.dico_attribut["Cheuveux"][1],self.dico_attribut["Visage"][1],self.dico_attribut["Yeux"][1],self.dico_attribut["Nez"][1],self.dico_attribut["Bouche"][1],self.dico_attribut["Cosmetique"][1],self.dico_attribut["Background"][1]])
	def envoyer_liste(self):
		self.liste_attribut_total = marshal.dumps(self.liste_attribut_total)
		return self.liste_attribut_total
liste_personnages = [] 

class Gen_perso_par_liste():
	def __init__(self,liste):
		for perso in range(40):
			compile_image_perso(perso+1,[liste[9*perso+1],liste[9*perso+2],liste[9*perso+3],liste[9*perso+4],liste[9*perso+5],liste[9*perso+6],liste[9*perso+7],liste[9*perso+8]])


perso_reels = os.listdir("assets/perso_reel/")
perso_reels_liste = []
for perso_reel in perso_reels:
	perso_reels_liste.append(perso_reel)
for perso in range(1,41):
	rand = randint(0,40)
	if rand == 20:
		shuffle(perso_reels_liste)
		perso_choisi = perso_reels_liste[0]
		perso_reels_liste.pop(0)
		perso_choisi = perso_choisi.replace(".png","")
		liste_personnages.append(perso_choisi)
	else:
		liste_personnages.append(perso)
print(liste_personnages)
perso_creer = Gen_perso(liste_personnages)

choix = Background("background",jeu)
perso = Personnages(liste_personnages,jeu,choix)
attente = Background("IP",jeu)
user_connection = User_connect(None)
principal = Background("background3",jeu)


def ecran(choix,perso,principal):
	attente = Background("IP",jeu)
	ecran_principal(principal)
	#ecran_jeu(choix,perso)

thread1 = threading.Thread(target=setup_server)
ecran(choix,perso,principal)
jeu.mainloop()