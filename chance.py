import sqlite3
from math import *
from random import *

bdd = sqlite3.connect("bdd/perso.db")
curseur = bdd.cursor()


class Nb_attribut_list():
	def __init__(self,nom):
		self.requete = "SELECT * FROM "+str(nom.title())
		self.liste_tuple = curseur.execute(self.requete).fetchall()
		self.liste = []
		numl = [i+1 for i in range(25)]
		nb = 0
		shuffle(numl)
		for i in range(len(self.liste_tuple)):
			liste = []
			liste.append(self.liste_tuple[i][1])
			if len(self.liste)==0:
				liste.append(self.tri(numl[0:ceil(25/len(self.liste_tuple))]))
				nb+=ceil(25/len(self.liste_tuple))
			else:
				liste.append(self.tri(numl[nb:nb+floor(25/len(self.liste_tuple))]))
				nb +=floor(25/len(self.liste_tuple))
			self.liste.append(liste)
		print(self.liste)
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



nez = Nb_attribut_list("nez")
bouche = Nb_attribut_list("bouche")
genre = Nb_attribut_list("genre")
cheveux = Nb_attribut_list("cheuveux")
cosmetique = Nb_attribut_list("cosmetique")
visage = Nb_attribut_list("visage")
yeux = Nb_attribut_list("yeux")
background = Nb_attribut_list("background")