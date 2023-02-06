from tkinter import *
from PIL import ImageFont,Image, ImageTk,ImageDraw,ImageFile
import sqlite3,shutil,time,socket,pyglet, os,tkinter.font,socket,threading,re,marshal,csv,time
from tkinter import ttk
from socket import gethostbyname
from math import *
from random import *
from playsound import playsound
ImageFile.LOAD_TRUNCATED_IMAGES = True

def play_music():
	playsound("music.mp3")

if os.path.exists("assets/perso_fin"):
	perso_fin_dossier = os.listdir("assets/perso_fin")
	for i in perso_fin_dossier:
		if os.path.exists("assets/perso_fin/"+str(i)):
			os.remove("assets/perso_fin/"+str(i))
	os.rmdir("assets/perso_fin")
	os.makedirs("assets/perso_fin")
else:
	os.makedirs("assets/perso_fin")

if os.path.exists("assets/perso_fini"):
	perso_fini_dossier = os.listdir("assets/perso_fini")
	for i in perso_fini_dossier:
		if os.path.exists("assets/perso_fini/"+str(i)):
			os.remove("assets/perso_fini/"+str(i))
	os.rmdir("assets/perso_fini")
	os.makedirs("assets/perso_fini")
else:
	os.makedirs("assets/perso_fini")

user_connection = None

jeu = Tk()
jeu.geometry("1200x700")
jeu.title("Ki c moi?")
jeu.iconbitmap("assets/logo.ico")
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
		b=b.resize((1200,700))
		b.save("assets/background_jeu/"+str(self.nom)+"1.png")

	def background(self):
		self.resize_background()
		self.img=PhotoImage(file = "assets/background_jeu/"+str(self.nom)+"1.png",master=self.fenetre)
		background = Label(jeu,image=self.img)

		background.place(x=-2,y=-2,in_=self.fenetre)
		self.affiche = True
		return self.img
pers = StringVar()


class Image_perso():
	def __init__(self,nom,fenetre,choix,serv):
		self.nom = nom
		self.image = Image.open("assets/perso_fin/"+str(self.nom)+".png")
		self.image = self.image.resize((75,75))
		self.image.save("assets/perso_fini/"+str(nom)+".png")
		self.img = ImageTk.PhotoImage(file="assets/perso_fini/"+str(nom)+".png")
		self.bouton = Button(fenetre,image=self.img,command=self.clic,bg="#c14698",bd=0,activebackground="#852563")
		self.labelimg = Label(fenetre,image=self.img,bg="#c14698")
		self.choix = choix
		self.fenetre = fenetre
		self.serveur = serv
	def bouton_image(self):
		return self.bouton
	def label_image(self):
		return self.labelimg
	def clic(self):
		global liste_prenom_sexe
		if self.serveur !=None:
			self.serveur.envoyer_packet(self.nom,None)
		jeu_ecran(self.choix)
	def clic2(self):
		timage = Image.open("assets/background_jeu/arriere.png")
		timage = timage.resize((75,75))
		timage.save("assets/perso_fin/"+str(self.nom)+".png")
		self.img = ImageTk.PhotoImage(file="assets/perso_fini/"+str(self.nom)+".png")
	def label_image(self):
		return self.labelimg


table_choisi = StringVar()
attriut_choisi = StringVar()

class Personnages():
	def __init__(self,liste_personnages,fenetre,choix,serveur):
		global liste_prenom_sexe,bdd,curseur
		bdd = sqlite3.connect("bdd/perso.db", check_same_thread=False)
		curseur = bdd.cursor()
		self.liste_prenom_sexe = liste_prenom_sexe
		self.liste_personnages = liste_personnages
		self.frame = Frame(fenetre,bg="#c14698")
		self.liste_image = []
		self.f2 = Frame(fenetre,bg="#c14698")
		self.choix = choix
		self.pers = ""
		self.oui_non = StringVar()
		self.oui_non.set("Réponse : ")
		self.nom_entry = StringVar()
		self.serveur = None
		self.nombre_perso_txt=StringVar()
		self.nombre_personnage = StringVar()
		self.nombre_personnage.set(str(40))

	def afficher_en_bouton(self):
		id_perso = 0
		self.frame.pack_forget()
		self.frame = Frame(jeu,bg="#c14698")
		self.frame.pack(padx=90,pady=90)
		for ligne in range(5):
			for colone in range(8):
				if type(self.liste_personnages[id_perso]) != type(str()):
					if len(self.liste_prenom_sexe[self.liste_personnages[id_perso]][1]) >=8:
						self.taille = 7
					else:
						self.taille = 10
				self.f2=Frame(self.frame,bg="#c14698")
				self.liste_image.append(Image_perso(self.liste_personnages[id_perso],self.f2,self.choix,self.serveur))
				id_perso+=1
				self.liste_image[id_perso-1].bouton_image().pack()
				if type(self.liste_personnages[id_perso-1]) != type(str()):
					sexe = curseur.execute("SELECT type FROM Persos JOIN Genre ON Persos.idGenre = Genre.idGenre WHERE prenom = '"+str(self.liste_prenom_sexe[self.liste_personnages[id_perso-1]][1])+"'").fetchall()
					self.label = Label(self.f2,text=str(self.liste_prenom_sexe[self.liste_personnages[id_perso-1]][1])+" ("+str(sexe[0][0][0])+")",font=("Aqum two", self.taille),bg="#c14698")
				else:
					self.label = Label(self.f2,text=str(self.liste_personnages[id_perso-1])+" (H)",font=("Aqum two", 10),bg="#c14698")
				self.label.pack()
				self.f2.grid(row=ligne,column=colone,padx=3)

	def afficher_label(self):
		id_perso = 0
		self.frame.pack_forget()
		self.frame = Frame(jeu,bg="#c14698")
		self.frame.pack(side=LEFT,padx=10,pady=10)
		self.liste_image = []
		for ligne in range(5):
			for colone in range(8):
				if type(self.liste_personnages[id_perso]) != type(str()):
					if len(self.liste_prenom_sexe[self.liste_personnages[id_perso]][1]) >=8:
						self.taille = 7
						print(self.liste_prenom_sexe[self.liste_personnages[id_perso]][1],len(self.liste_prenom_sexe[self.liste_personnages[id_perso]][1]),self.taille)
					else:
						self.taille = 10
				self.f2=Frame(self.frame,bg="#c14698")
				self.liste_image.append(Image_perso(self.liste_personnages[id_perso],self.f2,self.choix,self.serveur))
				id_perso+=1
				self.liste_image[id_perso-1].label_image().pack()
				if type(self.liste_personnages[id_perso-1]) != type(str()):
					sexe = curseur.execute("SELECT type FROM Persos JOIN Genre ON Persos.idGenre = Genre.idGenre WHERE prenom = '"+str(self.liste_prenom_sexe[self.liste_personnages[id_perso-1]][1])+"'").fetchall()
					self.label = Label(self.f2,text=str(self.liste_prenom_sexe[self.liste_personnages[id_perso-1]][1])+" ("+str(sexe[0][0][0])+")",font=("Aqum two", self.taille),bg="#c14698")
				else:
					self.label = Label(self.f2,text=str(self.liste_personnages[id_perso-1])+" (H)",font=("Aqum two", 10),bg="#c14698")
				self.label.pack()
				self.f2.grid(row=ligne,column=colone,padx=3)
		self.combobox_table = ttk.Combobox(jeu,textvariable=table_choisi,values=("Background","Bouche","Cheuveux","Cosmetique","Genre","Nez","Visage","Yeux"),state = 'readonly',postcommand=lambda: self.combobox_attribut.configure(values=attriut_table()),font=("Aqum two", 8))
		self.combobox_attribut = ttk.Combobox(jeu,textvariable=attriut_choisi,values=attriut_table(),state="readonly",font=("Aqum two", 8))
		self.combobox_attribut.place(x=770,y=170)
		self.combobox_table.place(x=770,y=130)
		self.bouton_choix = Button(jeu,text="Rechercher",command=self.chercher,font=("Aqum two", 8))
		self.bouton_choix.place(x=770,y=250)
		self.label_oui=Label(jeu,textvariable=self.oui_non,font=("Aqum two", 8))
		self.label_oui.place(x=770,y=210)
		self.entry_nom = Entry(jeu,textvariable=self.nom_entry,font=("Aqum two", 8))
		self.entry_nom.place(x=770,y=290)
		self.rechercher_nom=Button(jeu,text="Rechercher par nom",command=self.chercher,font=("Aqum two", 8))
		self.rechercher_nom.place(x=770,y=330)
		self.nombre_perso_txt.set("Nombre de perso du joueur : "+self.nombre_personnage.get())
		self.nombre_perso = Label(jeu,textvariable=self.nombre_perso_txt,font=("Aqum two", 8))
		self.nombre_perso.place(x=745,y=370)

	def chercher(self):
		global liste_prenom_sexe
		gagne = False
		caract = curseur.execute("SELECT * FROM Persos WHERE prenom ='"+str(pers.get().title())+"'").fetchall()
		dico_attribut_perso_choisi = {"idCheuveux":caract[0][1],"idVisage" : caract[0][2],"idYeux" : caract[0][3],"idNez" : caract[0][4],"idBouche" : caract[0][5],"idCosmetique" : caract[0][6],"idBackground" : caract[0][7],"idGenre":caract[0][8],"prenom" :caract[0][9].title()}
		try:
			table = table_choisi.get()
			idt = attriut_choisi.get()
			if self.nom_entry.get()!="":
				table="prenom"
				idt = self.nom_entry.get().title()
				if dico_attribut_perso_choisi[str(table)].title() == idt:
					a = "UPDATE Persos SET choisi = 0 WHERE "+str(table)+" !='"+str(idt.title())+"'"
					print(a)
					curseur.execute(a)
					curseur.execute("UPDATE Persos SET choisi =1 WHERE "+str(table)+" =='"+str(idt.title())+"'")
					b = "SELECT prenom FROM Persos WHERE choisi = 1"
					self.b = curseur.execute(b).fetchall()
					print(self.b)
					self.change()
				else:
					a = "UPDATE Persos SET choisi = 0 WHERE "+str(table)+" =='"+str(idt.title())+"'"
					curseur.execute(a)
					print(a)
					b = "SELECT prenom FROM Persos WHERE choisi = 1"
					self.b = curseur.execute(b).fetchall()
					self.change()
					print(self.b)
			else:
				caractere = curseur.execute("SELECT id"+str(table)+" FROM "+str(table)+" WHERE type ='"+str(idt)+"'").fetchall()[0][0]
				if dico_attribut_perso_choisi["id"+str(table)] == caractere:
					self.oui_non.set("Réponse : Oui")
					a = "UPDATE Persos SET choisi = 0 WHERE id"+str(table)+" !="+str(caractere)
					curseur.execute(a)
					curseur.execute("UPDATE Persos SET choisi =1 WHERE prenom =='"+str(dico_attribut_perso_choisi["prenom"])+"'")
					b = "SELECT prenom FROM Persos WHERE choisi = 1"
					self.b = curseur.execute(b).fetchall()
					self.change()
				else:
					self.oui_non.set("Réponse : Non")
					a = "UPDATE Persos SET choisi = 0 WHERE id"+str(table)+" =="+str(caractere)
					curseur.execute(a)
					b = "SELECT prenom FROM Persos WHERE choisi = 1"
					self.b = curseur.execute(b).fetchall()
					self.change()
			if self.serveur !=None:
				self.serveur.envoyer_packet(None,str(len(self.b)))
			print(len(self.b),self.nom_entry.get(),dico_attribut_perso_choisi["prenom"])
			if len(self.b) == 1 and self.nom_entry.get()==dico_attribut_perso_choisi["prenom"]:
				for widget in jeu.winfo_children():
					widget.pack_forget()
					widget.place_forget()
				choix.background()
				txt="Vous avez gagné c'était "+pers.get()
				Label(jeu,text=txt,font=("Aqum two", 25),bg="#c14698").pack(side=LEFT,padx=80)
				if self.serveur !=None:
					tchat.afficher()
				gagne = True
			self.nom_entry.set("")
		finally:
			if self.serveur !=None:
				self.label_oui.configure(textvariable=self.oui_non)
				self.combobox_table.place_forget()
				self.combobox_attribut.place_forget()
				self.bouton_choix.place_forget()
				self.entry_nom.place_forget()
				self.rechercher_nom.place_forget()
				if gagne == False:
					self.serveur.envoyer_packet(None,"a")
				else:
					self.serveur.envoyer_packet(None,"g")
	def change(self):
		perso_list = []
		for i in self.b:
			perso_list.append(i[0].title())
		for i in range(40):
			if type(self.liste_personnages[i])==type(int()):
				if liste_prenom_sexe[self.liste_personnages[i]][1] not in perso_list:
					self.liste_image[i].clic2()
			else:
				if self.liste_personnages[i].title() not in perso_list:
					self.liste_image[i].clic2()
		jeu_ecran(self.choix)

def attriut_table():
	global curseur
	try:
		att = curseur.execute("SELECT type FROM "+str(table_choisi.get())).fetchall()
		a = []
		for i in att:
			a.append(i[0])
		return a
	except:
		return None

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
		global serv_or_join,perso
		serv_or_join = "serv"
		print("strar")
		print(perso.liste_image)
		perso.serveur = self
		self.pseudo = user_connection.pseudo.get()
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = (gethostbyname(str(extract_ip())), 6969)
		self.sock.bind(self.server_address)
		self.sock.listen(1)
		self.connection, self.client_address = self.sock.accept()
	def recevoir_packet(self):
		global perso
		try:
		    while True:
		        data = self.connection.recv(8096)
		        print(data.decode("utf-8"))
		        if data.decode("utf-8")[0] == "t":
		        	tchat.tchat.configure(state='normal')
		        	tchat.tchat.insert(END,data.decode("utf-8")[1:])
		        	tchat.liste_message.append(data.decode("utf-8")[1:])
		        	tchat.tchat.configure(state='disabled')
		        elif data.decode("utf-8")[0] == "c":
		        	pers.set(data.decode("utf-8")[1:])
		        elif data.decode("utf-8")[0]=="a":
		        	perso.afficher_label()
		        elif data.decode("utf-8")[0]=="g":
		        	time.sleep(1)
		        	for widget in jeu.winfo_children():
		        		widget.pack_forget()
		        		widget.place_forget()
		        	choix.background()
		        	txt="Vous avez perdu c'était "+pers.get()
		        	Label(jeu,text=txt,font=("Aqum two", 25),bg="#c14698").pack(side=LEFT,padx=80)
		        	tchat.afficher()
		        else:
		        	perso.nombre_personnage.set(data.decode("utf-8"))
		        break
		except:
		    None
	def envoyer_packet(self,perso_name,requete):
		try:
			if perso_name != None:
				self.perso_name=perso_name
			if tchat.message.get()!="":
				message = "t"+self.pseudo+" : "+tchat.message.get()+str("\n")
				self.connection.sendall(message.encode("utf-8"))
			if type(perso_name) ==type(int()):
				packet = "c"+liste_prenom_sexe[perso_name][1]
				self.connection.sendall(packet.encode("utf-8"))
			elif type(perso_name) == type(str()):
				packet = "c"+perso_name
				self.connection.sendall(packet.encode("utf-8"))
			if requete !=None:
				packet=requete
				self.connection.sendall(packet.encode("utf-8"))
		finally:
			None
	def connect(self):
		global perso
		user_connection.ip = self.client_address
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
			for widget in jeu.winfo_children():
				widget.pack_forget()
				widget.place_forget()
			self.ip = extract_ip()
			img=attente.background()
			frame_ip_jouer = Canvas(jeu,width=1200,height=700)
			frame_ip_jouer.create_image(600,350,image=img)
			self.b = frame_ip_jouer
			self.b.create_text(985,200,text="Joueur en attente...",font=("Aqum two", 17))
			self.b.create_text(850,250,text="Joueur : ...",font=("Aqum two",15),anchor="nw")
			self.b.create_text(850,310,text="IP : ...",font=("Aqum two",15),anchor="nw")
			self.b.create_text(227,417,text="En attente",font=("Aqum two",17))
			self.pseudo_enter = Entry(jeu,textvariable=self.pseudo,font=("Aqum two",13),width=14)
			self.pseudo_enter.place(x=600,y=79) 
			self.confirmer = Button(jeu,command=self.confirm,text="✓")
			self.confirmer.place(x=770,y=80) 
		else:
			self.b.pack_forget()
			ip = extract_ip()
			img=attente.background()
			frame_ip_jouer = Canvas(jeu,width=1200,height=700)
			frame_ip_jouer.create_image(600,350,image=img)
			frame_ip_jouer.create_text(225,90,text="Votre IP : "+str(ip),font=("Aqum two", 17)) 
			self.b = frame_ip_jouer
			self.b.create_text(985,200,text="Joueur connecté ! ",font=("Aqum two", 17))
			self.b.create_text(850,250,text="Joueur : "+str(self.pseudo),font=("Aqum two",15),anchor="nw")
			self.b.create_text(850,310,text="IP : "+str(self.ip[0]),font=("Aqum two",15),anchor="nw")
			Button(jeu,image=self.bouton,command=self.jouer).place(x=60,y=370) 
			self.pseudo_enter.place(x=600,y=79)  
		self.b.pack()
		Button(jeu,text="retour",image=bouton4,command=ecran_principal).place(x=900,y=600)
	def jouer(self):
		self.b.pack_forget()
		choix.background()
		perso.afficher_en_bouton()
	def confirm(self):
		self.confirmer.place_forget()
		self.b.create_text(225,90,text="Votre IP : "+str(self.ip),font=("Aqum two", 17)) 
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
		self.liste_message = []
	def afficher(self):
		self.frame = Frame()
		self.tchat = Text(self.frame,width=30,bg="#31202c",fg="#ffffff",state='disabled')
		self.frame.pack(side=RIGHT,fill=Y,expand=False)
		self.tchat.pack(fill=Y,expand=True)
		self.entry = Entry(self.frame,bg="#b6418c",textvariable=self.message)
		self.entry.pack(side=LEFT,fill=BOTH,expand=True)
		self.bouton=Button(self.frame,text="Envoyer",bg="#852563",activebackground="#c14698",command=self.envoyer)
		self.bouton.pack(side=LEFT,fill=BOTH,expand=True)
		self.tchat.configure(state='normal')
		for i in self.liste_message:
			self.tchat.insert(END,i)
		self.tchat.configure(state='disabled')
	def envoyer(self):
		if self.message.get() !="":
			tchat.tchat.configure(state='normal')
			self.tchat.insert(END,"Moi : "+self.message.get()+str("\n"))
			tchat.tchat.configure(state='disable')
			self.liste_message.append("Moi : "+self.message.get()+str("\n"))
			self.serveur.envoyer_packet(None,None)
		self.message.set("")

bouton=PhotoImage(file=r"assets/background_jeu/bouton_jouer.png")
bouton1=PhotoImage(file=r"assets/background_jeu/bouton_jouer1.png")
bouton2=PhotoImage(file=r"assets/background_jeu/bouton_jouer2.png")
bouton3=PhotoImage(file=r"assets/background_jeu/bouton_remerciement.png")
bouton4=PhotoImage(file=r"assets/background_jeu/bouton_retour.png")
bouton5=PhotoImage(file=r"assets/background_jeu/bouton_comment.png")
bouton6=PhotoImage(file=r"assets/background_jeu/bouton_suivant.png")
bouton7=PhotoImage(file=r"assets/background_jeu/bouton_precedant.png")

def make_perso(liste_perso,serveur):
	global perso
	print(serveur)
	perso =Personnages(liste_perso,jeu,choix,serveur)
	perso.serveur = serveur
	print(perso.serveur)
	return perso

class Join():
	def __init__(self,pseudo,ip):
		for widget in jeu.winfo_children():
			widget.pack_forget()
		self.pseudo = pseudo
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = (ip, 6969)
		self.sock.connect(self.server_address)
		self.sock.sendall(pseudo.encode("utf-8"))
		data = self.sock.recv(8096)
		data = marshal.loads(data)
		Gen_perso_par_liste(data)
		liste_perso = []
		for i in range(40):
			liste_perso.append(data[i*9])
		self.perso = make_perso(liste_perso,self)
		choix.background()
		self.perso.afficher_en_bouton()
	def recevoir_packet(self):
		global perso
		while True:
			data = self.sock.recv(8096)
			print(data.decode("utf-8"))
			if data.decode("utf-8")[0] == "t":
				tchat.tchat.configure(state="normal")
				tchat.tchat.insert(END,data.decode("utf-8")[1:])
				tchat.liste_message.append(data.decode("utf-8")[1:])
				tchat.tchat.configure(state="disabled")
			elif data.decode("utf-8")[0] == "c":
				pers.set(data.decode("utf-8")[1:])
			elif data.decode("utf-8")[0]=="a":
				perso.afficher_label()
			elif data.decode("utf-8")[0]=="g":
				for widget in jeu.winfo_children():
					widget.pack_forget()
					widget.place_forget()
				choix.background()
				txt="Vous avez perdu c'était "+pers.get()	
				Label(jeu,text=txt,font=("Aqum two", 25),bg="#c14698").pack(side=LEFT,padx=80)
				tchat.afficher()
			else:
				perso.nombre_personnage.set(data.decode("utf-8"))

	def envoyer_packet(self,perso,requete):
		if tchat.message.get()!="":
			message = "t"+self.pseudo+" : "+tchat.message.get()+str("\n")
			self.sock.sendall(message.encode("utf-8"))
		if type(perso) ==type(int()):
			packet = "c"+liste_prenom_sexe[perso][1]
			self.sock.sendall(packet.encode("utf-8"))
		elif type(perso) == type(str()):
			packet = "c"+perso
			self.sock.sendall(packet.encode("utf-8"))
		if requete!=None:
			packet=requete
			self.sock.sendall(packet.encode("utf-8"))




def ecran_principal():
	global user_connection
	
	for widget in jeu.winfo_children():
		widget.pack_forget()
		widget.place_forget()
	remerciement.background()
	principal.background()
	user_connection = None
	f = Frame(jeu) 
	f.pack(side=BOTTOM,pady=5) 
	Button(f,text="Jouer",font=("Aqum two",17),image=bouton,command=ecran_multi).pack(side=LEFT) 
	Button(f,text="Jouer",font=("Aqum two",17),image=bouton1,command=ecran_join).pack(side = LEFT)
	Button(f,text="Jouer en solo",font=("Aqum two",17),image=bouton2,command=jeu_solo).pack(side=LEFT) 
	Button(jeu,text="remerciement",image=bouton3,command=remerciement_gens).pack(side=LEFT,anchor=NW,padx=10,pady=10)
	Button(jeu,text="tuto",image=bouton5,command=tuto1).pack(side=RIGHT,anchor=NE,padx=10,pady=10)

def remerciement_gens():
	for widget in jeu.winfo_children():
		widget.pack_forget()
		widget.place_forget()
	remerciement.background()
	Button(jeu,text="retour",image=bouton4,command=ecran_principal).pack(side=LEFT, anchor=SW,padx=10,pady=10)

def tuto1():
	for widget in jeu.winfo_children():
		widget.pack_forget()
		widget.place_forget()
	tuto1_b.background()
	Button(jeu,text="suivant",image=bouton6,command=tuto2).pack(side=LEFT,anchor=SW,padx=130,pady=100)
	Button(jeu,text="retour",image=bouton4,command=ecran_principal).pack(side=RIGHT,anchor=SW,padx=10,pady=10)

def tuto2():
	for widget in jeu.winfo_children():
		widget.pack_forget()
		widget.place_forget()
	tuto2_b.background()
	Button(jeu,text="precedant",image=bouton7,command=easter_egg).pack(side=LEFT,anchor=SW,padx=10,pady=10)
	Button(jeu,text="retour",image=bouton4,command=ecran_principal).pack(side=RIGHT,anchor=SE,padx=10,pady=10)

def easter_egg():
	for widget in jeu.winfo_children():
		widget.pack_forget()
		widget.place_forget()
	easter_egg_b.background()
	Button(jeu,text="retour",image=bouton4,command=ecran_principal).pack(side=RIGHT,anchor=SW,padx=10,pady=10)


ip_image=PhotoImage(file="assets/background_jeu/ip_d.png") 
pseudo_image=PhotoImage(file="assets/background_jeu/pseudo_d.png") 
image_rejoindre=PhotoImage(file="assets/background_jeu/bouton_jouer1.png") 

def ecran_jeu(choix,perso):
	choix.background()
	perso.afficher_en_bouton()

def ecran_join():
	def client():
		global perso,serv
		if ip.get() != "" and pseudo.get() != "":
			curseur.execute("""DELETE FROM Persos WHERE prenom != "Daniel" AND prenom != "Frank" AND prenom != "Yavan" AND prenom != "Remi" AND prenom != "Valentin" """)

			serv = Join(pseudo.get(),ip.get())
			tchat.serveur = serv
			perso.serveur = serv
			while True:
				serv.recevoir_packet()
	for widget in jeu.winfo_children():
		widget.pack_forget()
	thread3 = threading.Thread(target=client)
	choix.background()
	ip = StringVar()
	ip_frame = Frame(jeu) 
	ip_frame.pack(pady=60) 
	ip_label = Label(ip_frame,image=ip_image) 
	ip_label.pack() 
	Entry(ip_frame,textvariable=ip,font=("Aqum two", 11),width=26).place(x=55,y=38) 
	pseudo = StringVar()
	pseudo_frame = Frame(jeu) 
	pseudo_frame.pack(pady=60) 
	pseudo_label=Label(pseudo_frame,image= pseudo_image) 
	pseudo_label.pack() 
	Entry(pseudo_frame,textvariable=pseudo,width=21,font=("Aqum two", 11)).place(x=105,y=38) 
	Button(jeu,command=thread3.start,image=image_rejoindre).pack(pady=60) 
	Button(jeu,text="retour",image=bouton4,command=ecran_principal).pack(side=RIGHT,anchor=SW,padx=10,pady=10)

def ecran_multi():
	global user_connection
	user_connection = User_connect(None)
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

def jeu_solo():
	global liste_prenom_sexe
	for widget in jeu.winfo_children():
		widget.pack_forget()
		widget.place_forget()
	liste_perso = perso.liste_personnages[0:]
	shuffle(liste_perso)
	if type(liste_perso[0]) == type(str()):
		pers.set(liste_perso[0])
	else:
		pers.set(liste_prenom_sexe[liste_perso[0]][1])
	print(pers.get())
	choix.background()
	perso.afficher_label()

def setup_server():
	global tchat,perso,serveur
	serveur = Serveur()
	tchat.serveur = serveur
	print("Oui")
	perso.serveur = serveur
	serveur.connect()
	while True:
		serveur.recevoir_packet()

def join_server():
	global tchat
	serv = Join(None)

bdd = sqlite3.connect("bdd/perso.db", check_same_thread=False)
curseur = bdd.cursor()
curseur.execute("""DELETE FROM Persos WHERE prenom != "Daniel" AND prenom != "Frank" AND prenom != "Yavan" AND prenom != "Remi" AND prenom != "Valentin" """)

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
		self.requete = ("""INSERT INTO Persos VALUES """)
		
		for perso in range(1,41):
			self.generer_attribut_personnage(perso)
	def generer_attribut_personnage(self,nb_perso):
		global liste_prenom_sexe
		self.dico_attribut = {"Cheuveux" : None,"Visage":None,"Yeux":None,"Nez":None,"Bouche":None,"Cosmetique":None,"Background":None,"Genre":None}
		liste_append_bdd = []
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
						liste_append_bdd.append(l_attribut_simple[indice][1])
				except:
					None
		if type(self.liste_perso[nb_perso-1]) != type(str()):
			liste_append_bdd.append(liste_prenom_sexe[self.liste_perso[nb_perso-1]][1])
			curseur.execute(self.requete+"("+"1,"+str(liste_append_bdd[0])+","+str(liste_append_bdd[1])+","+str(liste_append_bdd[2])+","+str(liste_append_bdd[3])+","+str(liste_append_bdd[4])+","+str(liste_append_bdd[5])+","+str(liste_append_bdd[6])+","+str(liste_append_bdd[7])+',"'+str(liste_append_bdd[8])+'")')
		bdd.commit()
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
		if type(self.liste_perso[nb_perso-1]) != type(str()):
			compile_image_perso(self.liste_perso[nb_perso-1],[self.dico_attribut["Cheuveux"][1],self.dico_attribut["Visage"][1],self.dico_attribut["Yeux"][1],self.dico_attribut["Nez"][1],self.dico_attribut["Bouche"][1],self.dico_attribut["Cosmetique"][1],self.dico_attribut["Background"][1]])
	def envoyer_liste(self):
		self.liste_attribut_total = marshal.dumps(self.liste_attribut_total)
		return self.liste_attribut_total
liste_personnages = [] 

class Gen_perso_par_liste():
	def __init__(self,liste):
		global liste_prenom_sexe
		self.requete = ("""INSERT INTO Persos VALUES """)
		self.liste_attribut = ["Cheuveux","Visage","Yeux","Nez","Bouche","Cosmetique","Background","Genre","prenom"]
		self.relation = {"Bouche":[(1,3),(2,2),(3,1),(4,4),(5,2),(6,4),(7,2),(8,2),(9,1)],"Yeux":[(1,1),(2,2),(3,4),(4,2),(5,3),(6,3),(7,3),(8,5),(9,3),(10,3),(11,2),(12,5),(13,4),(14,2),(15,3),(16,3),(17,4),(18,5),(19,3),(20,2),(21,4),(22,5),(23,3)],"Visage":[(1,1),(2,2)],"Nez":[(1,1),(2,2),(3,2),(4,2),(5,2),(6,1),(7,1)],"Cosmetique":[(1,1),(2,2)],"Cheuveux":[(1,1),(2,3),(3,5),(4,2),(5,4),(6,2),(7,3),(8,1)],"Background":[(1,1),(2,1),(3,2),(4,2),(5,2),(6,3),(7,3),(8,3)],"Genre":[(1,1),(2,2)]}
		liste_noms_reel = ["Remi","Daniel","Frank","Valentin","Yavan"]
		for perso in range(40):
			liste_append_bdd = []
			if type(liste[9*perso]) != type(str()):
				self.dico_attribut = {"Cheuveux" : None,"Visage":None,"Yeux":None,"Nez":None,"Bouche":None,"Cosmetique":None,"Background":None,"Genre":None}
				compile_image_perso(liste[9*perso],[liste[9*perso+1],liste[9*perso+2],liste[9*perso+3],liste[9*perso+4],liste[9*perso+5],liste[9*perso+6],liste[9*perso+7],liste[9*perso+8]])
				liste_attribut_simple = [liste[9*perso+1],liste[9*perso+2],liste[9*perso+3],liste[9*perso+4],liste[9*perso+5],liste[9*perso+6],liste[9*perso+7],liste[9*perso+8],liste[9*perso]]
				somme=0
				for i in self.liste_attribut:
					if somme !=8:
						print(liste_attribut_simple[somme])
						self.dico_attribut[i]=self.relation[i][liste_attribut_simple[somme]-1][1]
						somme+=1
					else:
						self.dico_attribut[i]=liste_prenom_sexe[liste_attribut_simple[somme]][1]
				for i in self.dico_attribut.keys():
					liste_append_bdd.append(self.dico_attribut[i])
				curseur.execute(self.requete+"("+"1,"+str(liste_append_bdd[0])+","+str(liste_append_bdd[1])+","+str(liste_append_bdd[2])+","+str(liste_append_bdd[3])+","+str(liste_append_bdd[4])+","+str(liste_append_bdd[5])+","+str(liste_append_bdd[6])+","+str(liste_append_bdd[7])+',"'+str(liste_append_bdd[8])+'")')
			else:
				liste_noms_reel.remove(liste[9*perso])
		for i in liste_noms_reel:
			i = i.replace(".png","")
			curseur.execute('UPDATE Persos SET choisi = 0 WHERE prenom = "'+str(i)+'"')
		bdd.commit()
fichier_nom = open("bdd/liste_des_prenoms.csv")
cr = csv.reader( fichier_nom,delimiter=";")

with fichier_nom as f:
    reader = csv.reader(f)
    list_prenom = list(reader)
liste_prenom_sexe = [] 
for c in list_prenom:
	a = ''
	for i in c:
		a+=i
	a = a.split(";")
	a = a[1:4]
	a.pop(1)
	liste_prenom_sexe.append(a)

liste_prenom_sexe1= liste_prenom_sexe[0:]

liste_random = []
perso_reels = os.listdir("assets/perso_reel/")
perso_reels_liste = []
for perso_reel in perso_reels:
	shutil.copy2("assets/perso_reel/"+str(perso_reel),"assets/perso_fin")
	shutil.copy2("assets/perso_reel/"+str(perso_reel),"assets/perso_fini")
	perso_reels_liste.append(perso_reel)

def generer_nom(liste_nom,liste_total,liste_noms_reel):
	if len(liste_total)==40:
		for i in liste_noms_reel:
			i = i.replace(".png","")
			curseur.execute('UPDATE Persos SET choisi = 0 WHERE prenom = "'+str(i)+'"')
			bdd.commit()
		return liste_total
	else:
		rand = randint(0,40)
		if (rand == 20 or rand == 21) and len(liste_noms_reel) !=0:
			shuffle(liste_noms_reel)
			perso_choisi = liste_noms_reel[0]
			liste_noms_reel.pop(0)
			perso_choisi = perso_choisi.replace(".png","")
			liste_total.append(perso_choisi.title())
			curseur.execute('UPDATE Persos SET choisi = 1 WHERE prenom = "'+str(perso_choisi)+'"')
			return generer_nom(liste_nom,liste_total,liste_noms_reel)
		else:
			nom = randint(1,len(liste_nom)-1)
			liste_total.append(nom)
			liste_nom.pop(nom)
			return generer_nom(liste_nom,liste_total,liste_noms_reel)


liste_personnages = generer_nom(liste_prenom_sexe1,[],perso_reels_liste)
perso_creer = Gen_perso(liste_personnages)

choix = Background("background",jeu)
perso = Personnages(liste_personnages,jeu,choix,None)
attente = Background("IP",jeu)
user_connection = User_connect(None)
principal = Background("background3",jeu)
remerciement = Background("remerciement",jeu)
tuto1_b = Background("tuto1",jeu)
tuto2_b = Background("tuto2",jeu)
easter_egg_b = Background("easter",jeu)


def ecran(choix,perso):
	attente = Background("IP",jeu)
	threadmusic.start()
	ecran_principal()
	#ecran_jeu(choix,perso)
	#jeu_solo(choix)

threadmusic = threading.Thread(target=play_music)
thread1 = threading.Thread(target=setup_server)
ecran(choix,perso)
jeu.mainloop()