from p5 import *
from random import randint
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
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

def compile_image(liste_image):
    background_image = Image.open("background_image.png")
    background_image = background_image.convert("RGBA")
    imagelist = []
    font = ImageFont.truetype("police/Aqum2.otf", 15)
    for i in range(25):
        imagelist.append(Image.open("images/"+str(liste_image[i].nom_perso)+str(".png")))

        imagelist[i] = imagelist[i].convert("RGBA")
        imagelist[i] = imagelist[i].resize((50,50))
    y=0
    compteur_id_perso=0
    contour = Image.open("images/contour.png")
    for i in range(1,6):
        y+=100
        if i == 1:
            y = 0
        x=100
        for j in range(1,6):
            background_image.alpha_composite(imagelist[compteur_id_perso],dest=(x,y))
            background_image.alpha_composite(contour,dest=(x-5,y-5))
            compteur_id_perso+=1
            x +=100
    background_image2 = ImageDraw.Draw(background_image)
    y=-50
    compteur_id_perso=0
    for i in range(1,6):
        y+=100
        x=125
        for j in range(1,6):
            background_image2.text((x,y),liste_image[compteur_id_perso].nom_perso,(255,255,255),font=font,anchor="ma")
            compteur_id_perso+=1
            x +=100
    background_image.save("yes.png")

def compile_image_perso(perso_name,list_arg):
    perso = Image.open("images/perso_vierge.png")
    perso = perso.convert("RGBA")
    if len(liste_image) == 0:
        cheveux = randint(1,10)
        visage = randint(1,10)
        yeux = randint(1,10)
        nez = randint(1,10)
        bouche = randint(1,10)
        cosmetique = randint(1,10)
        moustache = randint(1,10)
        barbe = randint(1,10)
        background = randint(1,10)
    else:
        cheveux = Image.open("assets/cheveux/"+str(list_arg[0]))
        visage = Image.open("assets/visage/"+str(list_arg[1]))
        yeux = Image.open("assets/yeux/"+str(list_arg[2]))
        nez = Image.open("assets/nez/"+str(list_arg[3]))
        bouche = Image.open("assets/bouche/"+str(list_arg[4]))
        cosmetique = Image.open("assets/cosmetique/"+str(list_arg[5]))
        moustache = Image.open("assets/moustache/"+str(list_arg[6]))
        barbe = Image.open("assets/barbe/"+str(list_arg[7]))
        background = Image.open("assets/background/"+str(list_arg[8]))









class image_personnage():
    def __init__(self,x,y,perso_id):
        self.x = x+275
        self.y = y
        self.compteur=0
        self.choisi = False
        self.affiche = False
        self.souris_dessus = False
        self.switch = False
        self.temp = False

        req = "SELECT perso_name FROM perso WHERE perso_id ="+str(perso_id)
        r = curseur.execute(req)
        self.nom_perso = r.fetchall()[0][0]

    def afficher(self):
        try:
            if self.choisi == True:
                image(load_image("images/"+self.nom_perso+".png"),self.x,self.y,50,50)
        except:
            None
        text_align(align_x="CENTER")
        fill(0,0,0)
        #if self.x != 610 and self.y !=25:
            #text(str(self.nom_perso),self.x+25,self.y+50)
        if self.choisi == True and self.x ==610 and self.y==25:
            fill(255,255,255)
            text(str(self.nom_perso),self.x+25,self.y+75)
            text("Personnage choisi",self.x+25,self.y+50)

    def clic(self):
        global draw_perso
        if mouse_x>=self.x and mouse_x <= self.x+50 and mouse_y>=self.y and mouse_y <= self.y+50:
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
compile_image(image_perso_liste)

def setup():
    size(1200,560)
    font = create_font("police/Aqum2.otf",34)
    text_font(font, 15)
    title("Qui c'est moi ?")
i = 0
souris_dessus = False

def draw():
    global draw_perso,i,compteur_id_perso
    if draw_perso ==0 and image_perso_liste[i].affiche == False:
        draw_perso =1
        background(0,0,0)
        image(load_image("yes.png"),225,50)
    if draw_perso == 1:
        for image_perso in image_perso_liste:
            i +=1
            if image_perso.souris_dessus == True and i==24:
                souris_dessus == True
            else:
                souris_dessus == False
        for image_perso in image_perso_liste:
            draw_perso = image_perso.clic()
            if image_perso.choisi == True:
                draw_perso =2
                for image_perso in image_perso_liste:
                    image_perso.affiche = False
                    i = 0
                    background(0,0,0)
                break
    if draw_perso == 2 and image_perso_liste[i].affiche == False:
        for i in range(25):
            image_perso_liste[i].x -=275
            image_perso_liste[i].affiche = True
            if image_perso_liste[i].choisi == True:
                fill(30,30,30)
                rect(550,0,5,650)
                for ligne in range(120,650,40):
                    rect(550,ligne,650,3)
                image_perso_liste[i].x = 610
                image_perso_liste[i].y =25
                image_perso_liste[i].affiche = False
                image_perso_liste[i].afficher()
                image_perso_liste[i].affiche = True
                image(load_image("yes.png"),-50,50)

    noStroke()


    
run()

#x = 50 y = 100, or x = 325 y = 50