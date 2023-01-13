from squlite3 import *

bdd = connect("bdd/perso.db")
curseur = bdd.cursor()

curseur.execute("""CREATE TABLE caracteristique
				(IdCaractere INTEGER PRIMARY KEY,
				Caractere TEXT)
				""")