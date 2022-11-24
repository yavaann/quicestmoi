import pyxel

class App:
    def __init__(self):
        pyxel.init(600, 600)
        self.x = 0
        pyxel.load("images/Al.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        self.x = (self.x + 1) % pyxel.width

    def draw(self):
        pyxel.image(0).load(10,10,"images/Al.png")

App()
