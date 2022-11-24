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
draw_perso = 0
i=0

class image_personnage():
    def __init__(self,x,y,perso_id):
        self.x = x+275
        self.y = y
        self.compteur=0
        self.choisi = False
        self.affiche = False
        req = "SELECT perso_name FROM perso WHERE perso_id ="+str(perso_id)
        r = curseur.execute(req)
        self.nom_perso = r.fetchall()[0][0]

    def afficher(self):
        image(load_image("images/"+self.nom_perso+".png"),self.x,self.y,50,50)
        text_align(align_x="CENTER")
        fill(0,0,0)
        if self.x != 610 and self.y !=25:
            text(str(self.nom_perso),self.x+25,self.y+50)
        if self.choisi == True and self.x ==610 and self.y==25:
            text(str(self.nom_perso),self.x+25,self.y+75)
            text("Personnage choisi",self.x+25,self.y+50)

    def clic(self):
        global draw_perso
        if mouse_x>=self.x and mouse_x <= self.x+50:# and mouse_y>=self.y and mouse_y+50 <= self.y+50:
            if mouse_y>=self.y and mouse_y <= self.y+50:
                if mouse_is_pressed and mouse_button == "LEFT" :
                    if self.compteur == 0:
                        self.choisi = True
                        self.compteur +=1
                        clear()
        return 1




for i in range(1,6):
    y+=100
    x=50
    for j in range(1,6):
        compteur_id_perso+=1
        image_perso_liste.append(image_personnage(x,y,compteur_id_perso))
        x +=100

compteur_id_perso = 0


def setup():
    size(1200,560)
    font = create_font("police/Aqum2.otf",34)
    text_font(font, 15)
    title("Qui c'est moi ?")
i = 0

def draw():
    global draw_perso,i,compteur_id_perso
    if draw_perso ==0 and image_perso_liste[i].affiche == False:
        image_perso_liste[i].afficher()
        image_perso_liste[i].affiche = True
        compteur_id_perso +=1
        if compteur_id_perso >=25:
            draw_perso =1
            compteur_id_perso = 0
    if draw_perso == 1:
        for image_perso in image_perso_liste:
            draw_perso = image_perso.clic()
            if image_perso.choisi == True:
                draw_perso =2
                for image_perso in image_perso_liste:
                    image_perso.affiche = False
                    i = 0
                break
    if draw_perso == 2 and image_perso_liste[i].affiche == False:
        image_perso_liste[i].x -=275
        image_perso_liste[i].afficher()
        image_perso_liste[i].affiche = True
        if image_perso_liste[i].choisi == True:
            rect(550,0,5,650)
            image_perso_liste[i].x = 610
            image_perso_liste[i].y =25
            image_perso_liste[i].affiche = False
            image_perso_liste[i].afficher()
            image_perso_liste[i].affiche = True

    noStroke()
    i+=1
    if i ==25:
        i=0


    
run()

#test