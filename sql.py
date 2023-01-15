import sqlite3
con = sqlite3.connect("sql.db")
cur = con.cursor()

("CREATE TABLE Yeux(idYeux INTEGER PRIMARY KEY,couleur TEXT)")
("""
    INSERT INTO Yeux VALUES
        (1,'Rouge'),
        (2,'Vert'),
        (3,'Jaune'),
        (4,'Gris'),
        (5,'Bleu')
""")

("CREATE TABLE Nez(idNez INTEGER PRIMARY KEY,taille TEXT)")
("""
    INSERT INTO Nez VALUES
        (1,'Gros'),
        (2,'Fin')
       
""")


("CREATE TABLE Cheuveux(idCheuveux INTEGER PRIMARY KEY,couleur TEXT)")
("""
    INSERT INTO Cheuveux VALUES
        (1,'Marron'),
        (2,'Vert'),
        (3,'Jaune'),
        (4,'Chauve'),
        (5,'Bleu')
""")


("CREATE TABLE Visage(idVisage INTEGER PRIMARY KEY,couleur TEXT)")
("""
    INSERT INTO Visage VALUES
        (1,'Blanc'),
        (2,'Noir')
""")


("CREATE TABLE Bouche(idBouche INTEGER PRIMARY KEY,caracteristique TEXT)")
("""
    INSERT INTO Bouche VALUES
        (1,'Ouvert'),
        (2,'Ferme'),
        (3,'Pilosite')
""")



("CREATE TABLE Genre(idGenre INTEGER PRIMARY KEY,Genre TEXT)")
("""
    INSERT INTO Genres VALUES
        (1,'Homme'),
        (2,'Femme')
""")


("CREATE TABLE Cosmetique(idCosmetique INTEGER PRIMARY KEY,caracteristique TEXT)")
("""
    INSERT INTO Cosmetique VALUES
        (1,'Rougissement'),
        (2,'TacheDeRousseur')
        
""")


("CREATE TABLE Background(idBackground INTEGER PRIMARY KEY,type TEXT)")


("CREATE TABLE Prenoms(idPrenom INTEGER PRIMARY KEY,prenom TEXT)")



