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
import re
import marshal


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

pseudo = input("Pseudo : ")


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


class Gen_perso_par_liste():
    def __init__(self,liste):
        for perso in range(40):
            compile_image_perso(perso+1,[liste[9*perso+1],liste[9*perso+2],liste[9*perso+3],liste[9*perso+4],liste[9*perso+5],liste[9*perso+6],liste[9*perso+7],liste[9*perso+8]])


class srv():
    def __init__(self,pseudo):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (extract_ip(), 6969)
        print('Connecting to {} port {}'.format(*self.server_address))
        self.sock.connect(self.server_address)
        self.sock.sendall(pseudo.encode("utf-8"))
        data = self.sock.recv(8096)
        data = marshal.loads(data)
        print(data)
        Gen_perso_par_liste(data)
    def recevoir(self):
        while True:
            try:
                data = self.sock.recv(8096)
                print(data.decode("utf-8"))
            finally:
                None
    def envoyer(self):
        while True:
            while True:
                message = input(">> ")
                if message == "":
                    break
                message = pseudo+" : "+message+"\n"
                self.sock.sendall(message.encode("utf-8"))

serv = srv(pseudo)

t1 = threading.Thread(target=serv.recevoir)
t2 = threading.Thread(target=serv.envoyer)
t1.start()
t2.start()
t1.join()
t2.join()