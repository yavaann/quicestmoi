import sqlite3
from math import *
from random import *

from random import randint
from PIL import ImageFont,Image, ImageTk,ImageDraw
import sqlite3

bdd = sqlite3.connect("bdd/perso.db")
curseur = bdd.cursor()


class Nb_attribut_list():
	def __init__(self,nom):
		self.requete = "SELECT * FROM "+str(nom.title())
		self.liste_tuple = curseur.execute(self.requete).fetchall()
		self.liste = []
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
						self.dico_attribut[l_attribut_simple[0]] = (l_attribut_simple[indice][0],random_attribut_list[0])
				except:
					None
		random_attribute = []
		compile_image_perso(nb_perso,[self.dico_attribut["Cheuveux"][1],self.dico_attribut["Visage"][1],self.dico_attribut["Yeux"][1],self.dico_attribut["Nez"][1],self.dico_attribut["Bouche"][1],self.dico_attribut["Cosmetique"][1],self.dico_attribut["Background"][1]])


perso = Gen_perso()
