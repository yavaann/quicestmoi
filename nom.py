import csv
from random import randint
import os
from random import shuffle

fichier_nom = open("bdd/liste_des_prenoms.csv")
cr = csv.reader( fichier_nom,delimiter=";")

with fichier_nom as f:
    reader = csv.reader(f)
    list_prenom = list(reader)
liste = [] 
for c in list_prenom:
	a = ''
	for i in c:
		a+=i
	a = a.split(";")
	a = a[1:4]
	a.pop(1)
	liste.append(a)


liste_perso_nom = []
liste_random = []
perso_reels = os.listdir("assets/perso_reel/")
perso_reels_liste = []
for perso_reel in perso_reels:
	perso_reels_liste.append(perso_reel)

def generer_nom(liste_nom,liste_total,liste_noms_reel):
	if len(liste_total)==40:
		return liste_total
	else:
		rand = randint(0,40)
		if (rand == 20 or rand == 21) and len(liste_noms_reel) !=0:
			shuffle(liste_nom)
			perso_choisi = liste_noms_reel[0]
			liste_noms_reel.pop(0)
			perso_choisi = perso_choisi.replace(".png","")
			liste_total.append(perso_choisi)
			return generer_nom(liste_nom,liste_total,liste_noms_reel)
		else:
			nom = randint(1,len(liste_nom)-1)
			liste_total.append(nom)
			liste_nom.pop(nom)
			return generer_nom(liste_nom,liste_total,liste_noms_reel)


liste_perso_nom = generer_nom(liste,[],perso_reels_liste)
print(liste_perso_nom)

for i in range(10):
	print(generer_nom(liste,[],perso_reels_liste))