from p5 import *
from random import randint
from PIL import Image
from random import randint



def setup():
    size(1200,600)



def draw():
    x = randint(6, 594)
    y = randint(6, 294)
    diametre = 10
    fill(0, 255, 0)
    circle(x, y, diametre)
    image(load_image("Al.png"), 100,100,100,100)
    
run()