from tkinter import *
import random
import time

class Jeu:
    def __init__(self):
        self.tk=Tk()
        self.tk.title("M. Filiforme court vers la sortie")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=500, height=500, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.hauteur_canevas = 500
        self.largeur_canevas = 500
        self.ap = PhotoImage(file="arriere-plan.gif")
        large = self.ap.width()
        haut = self.ap.height()
        for x in range(0, 5):
            for y in range(0, 5):
                self.canvas.create_image(x*large, y * haut, image=self.ap, anchor='nw')
        self.lutins = []
        self.enfonction = True
        
    def boucle_principale(self):
        while 1:
            if self.enfonction == True:
                for lutin in self.lutins:
                    lutin.deplacer()
                self.tk.update_idletasks()
                self.tk.update()
                time.sleep(0.01)
class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

def dans_x(co1, co2):
    if(co1.x1 > co2.x1 and co1.x1 < co2.x2) \
            or(co1.x2 > co2.x1 and co1.x2 < co2.x2) \
            or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
            or(co2.x2 > co1.x1 and co2.x2 < co1.x1):
        return True
    else:
        return False

def dans_y(co1, co2):
    if(co1.y1 > co2.y1 and co1.y1 < co2.y2) \
            or(co1.y2 > co2.y1 and co1.y2 < co2.y2) \
            or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
            or(co2.y2 > co1.y1 and co2.y2 < co1.y1):
        return True
    else:
        return False
def collision_gauche(co1, co2):
    if dans_y(co1, co2):
        if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
            return True
        return False
    
def collision_droite(co1, co2):
    if dans_y(co1, co2):
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            return True
        return False
    

def collision_haut(co1, co2):
    if dans_x(co1, co2):
        if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
            return True
        return False

def collision_bas(y, co1, co2):
    if dans_x(co1, co2):
        y_calc = co1.y2 + y
        if y_calc >= co2.y1 and y_calc <= co2.y2:
            return True
        return False
        
class Lutin:
    def __init__(self, jeu):
        self.jeu = jeu
        self.finjeu = False
        self.coordonees = None
    def deplacer(self):
        pass
    def coords(self):
        return self.coordonnees
    
class LutinPlateForme(Lutin):
    def __init__(self, jeu, image_photo, x, y, largeur, hauteur):
        Lutin.__init__(self, jeu)
        self.image_photo = image_photo
        self.image = jeu.canvas.create_image(x, y,\
                image=self.image_photo, anchor='nw')
        self.coordonnees = Coords(x, y, x + largeur, y + hauteur)
        
class LutinPersonnage(Lutin):
    def __init__(self, jeu):
        Lutin.__init__(self, jeu)
        self.images_gauche = [
            PhotoImage(file="fil-G1.gif"),
            PhotoImage(file="fil-G2.gif"),
            PhotoImage(file="fil-G3.gif"),
        ]
        self.images_droite = [
            PhotoImage(file="fil-D1.gif"),
            PhotoImage(file="fil-D2.gif"),
            PhotoImage(file="fil-D3.gif"),
        ]
        self.image = jeu.canvas.create_image(200, 470, \
                image=self.images_gauche[0], anchor='nw')
        self.x = -2
        self.y = 0
        self.image_courante = 0
        self.ajout_image_courante = 1
        self.compte_sauts = 0
        self.derniere_heure = time.time()
        self.coordonees = Coords()
        jeu.canvas.bind_all('<KeyPress-Left>', self.tourner_a_gauche)
        jeu.canvas.bind_all('<KeyPress-Right>', self.tourner_a_droite)
        jeu.canvas.bind_all('<space>', self.sauter)

    def tourner_a_gauche(self, evt):
        if self.y == 0:
            self.x = -2

    def tourner_a_droite(self, evt):
        if self.y == 0:
            self.x = 2
            
    def sauter(self, evt):
        if self.y == 0:
            self.y = -4
            self.compte_sauts = 0
            
    def animer(self):
        if self.x != 0 and self.y == 0:
            if time.time() - self.derniere_heure > 0.1:
                self.derniere_heure = time.time()
                self.image_courante += self.ajout_image_courante
                if self.image_courante >= 2:
                    self.ajout_image_courante = -1
                if self.image_courante <= 0:
                    self.ajout_image_courante = 1
        if self.x < 0:
            if self.y != 0:
                self.jeu.canvas.itemconfig(self.image, \
                    image=self.images_gauche[2])
            else:
                self.jeu.canvas.itemconfig(self.image, \
                    image=self.images_gauche[self.image_courante])
        elif self.x > 0:
            if self.y != 0:
                self.jeu.canvas.itemconfig(self.image, \
                    image=self.images_droite[2])
            else:
                self.jeu.canvas.itemconfig(self.image, \
                    image=self.images_droite[self.image_courante])
                
    def coords(self):
        xy = self.jeu.canvas.coords(self.image)
        self.coordonees.x1 = xy[0]
        self.coordonees.y1 = xy[1] 
        self.coordonees.x2 = xy[0] + 27
        self.coordonees.y2 = xy[1] + 30
        return self.coordonees

    def deplacer(self):
        self.animer()
        if self.y < 0:
            self.compte_sauts += 1
            if self.compte_sauts > 20:
                self.y = 4
        if self.y > 0:
            self.compte_sauts -= 1
        co = self.coords()
        gauche = True
        droite = True
        haut = True
        bas = True
        tombe = True
        if self.y > 0 and co.y2 >= self.jeu.hauteur_canevas:
            self.y = 0
            bas = False
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            haut = False
        if self.x > 0 and co.x2 >= self.jeu.largeur_canevas:
            self.x = 0
            droite = False
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0
            gauche = False
        for lutin in self.jeu.lutins:
            if lutin == self:
                continue
            co_lutin = lutin.coords()
            if haut and self.y < 0 and collision_haut(co, co_lutin):
                self.y = -self.y
                haut = False
            if bas and self.y > 0 and collision_bas(self.y, co, co_lutin):
                self.y = co_lutin.y1 - co.y2
                if self.y < 0:
                    self.y = 0
                bas = False
                haut = False
            if bas and tombe and self.y == 0 \
               and co.y2 < self.jeu.hauteur_canevas \
               and collision_bas(1, co, co_lutin):
                tombe = False
            if gauche and self.x < 0 \
                and collision_gauche(co, co_lutin):
                self.x = 0
                gauche = False
                if lutin.finjeu:
                    self.jeu.enfonction = False
            if droite and self.x > 0 \
                and collision_droite(co, co_lutin):
                self.x = 0
                droite = False
                if lutin.finjeu:
                    self.jeu.enfonction = False

        if tombe and bas and self.y == 0 \
           and co.y2 < self.jeu.hauteur_canevas:
            self.y = 4
        self.jeu.canvas.move(self.image, self.x, self.y)
            
class LutinPorte(Lutin):
    def __init__(self, jeu, image_photo, x, y, largeur, hauteur):
        Lutin.__init__(self, jeu)
        self.image_photo = image_photo
        self.image = jeu.canvas.create_image(x, y,\
                image=self.image_photo, anchor='nw')
        self.coordonnees = Coords(x, y, x + (largeur / 2), y + hauteur)
        self.finjeu = True

jeu = Jeu()
plateforme1 = LutinPlateForme(jeu, PhotoImage(file="plate-forme1.gif"), \
                              0, 480, 100, 10)
plateforme2 = LutinPlateForme(jeu, PhotoImage(file="plate-forme1.gif"), \
                              150, 440, 100, 10)
plateforme3 = LutinPlateForme(jeu, PhotoImage(file="plate-forme1.gif"), \
                              300, 400, 100, 10)
plateforme4 = LutinPlateForme(jeu, PhotoImage(file="plate-forme1.gif"), \
                              300, 160, 100, 10)
plateforme5 = LutinPlateForme(jeu, PhotoImage(file="plate-forme2.gif"), \
                              175, 350, 66, 10)
plateforme6 = LutinPlateForme(jeu, PhotoImage(file="plate-forme2.gif"), \
                              50, 300, 66, 10)
plateforme7 = LutinPlateForme(jeu, PhotoImage(file="plate-forme2.gif"), \
                              170, 120, 66, 10)
plateforme8 = LutinPlateForme(jeu, PhotoImage(file="plate-forme2.gif"), \
                              45, 60, 66, 10)
plateforme9 = LutinPlateForme(jeu, PhotoImage(file="plate-forme3.gif"), \
                              170, 250, 32, 10)
plateforme10 = LutinPlateForme(jeu, PhotoImage(file="plate-forme3.gif"), \
                              230, 200, 32, 10)

jeu.lutins.append(plateforme1)
jeu.lutins.append(plateforme2)
jeu.lutins.append(plateforme3)
jeu.lutins.append(plateforme4)
jeu.lutins.append(plateforme5)
jeu.lutins.append(plateforme6)
jeu.lutins.append(plateforme7)
jeu.lutins.append(plateforme8)
jeu.lutins.append(plateforme9)
jeu.lutins.append(plateforme10)
porte = LutinPorte(jeu, PhotoImage(file="porte1.gif"), 45, 30, 40, 35)
jeu.lutins.append(porte)
personnage = LutinPersonnage(jeu)
jeu.lutins.append(personnage)
jeu.boucle_principale()
