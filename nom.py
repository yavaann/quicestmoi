import csv
from random import randint

fichier = open("bdd/liste_des_prenoms.csv")
cr = csv.reader( fichier,delimiter=";")

with fichier as f:
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


def generer_nom(liste_nom,liste_total):
	if len(liste_total)==40:
		return liste_total
	else:
		nom = randint(1,len(liste_nom)-1)
		liste_total.append(nom)
		liste_nom.pop(nom)
		return generer_nom(liste_nom,liste_total)



for i in range(50):
	a = generer_nom(liste,[])
	print(a)
liste_perso_nom = generer_nom(liste,[])
print(liste_perso_nom)

