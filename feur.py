from p5 import *
from random import randint
from PIL import Image
import sqlite3
bdd = sqlite3.connect("bdd/animalcrossing.db")
curseur = bdd.cursor()
req = "SELECT perso_name FROM perso WHERE perso_id ="+str()


image_perso_liste = []
x=50
y=-50
compteur_id_perso = 1


class image_personnage():
    def __init__(self,x,y,perso_id):
        self.x = x
        self.y = y
        req = "SELECT perso_name FROM perso WHERE perso_id ="+str(perso_id)
        r = curseur.execute(req)
        self.nom_perso = r.fetchall()[0][0]

    def afficher(self):
        image(load_image("images/"+self.nom_perso+".png"),self.x,self.y,50,50)
        text_align(align_x="CENTER")
        fill(0,0,0)
        text(str(self.nom_perso),self.x+25,self.y+50)

for i in range(1,6):
    y+=100
    x=50
    for j in range(1,6):
        compteur_id_perso+=1
        image_perso_liste.append(image_personnage(x,y,compteur_id_perso))
        x +=100




def setup():
    size(1200,560)
    font = create_font("police/Aqum2.otf",34)
    text_font(font, 15)
def draw():
    for image_perso in image_perso_liste:
        image_perso.afficher()
    
run()