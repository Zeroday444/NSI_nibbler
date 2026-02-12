from tkinter import *
from PIL import Image, ImageTk
import random
import os

# Liste pour la création de la carte les lettres correspondent aux murs, les '.' au espaces, et les 'p' aux pommes
tableau = ["fbbbbbbbbbbbbbbbbbe",
           "a..p....p......p..a",
           "a.fbe.a.bbb.a.fbe.a",
           "a.a.a.a.....a.a.a.a",
           "a.cbd.a.a.a.a.cbd.a",
           "a..p..a.a.a.a..p..a",
           "a.fbbbd.a.a.cbbbe.a",
           "a.a..p......p...a.a",
           "a.a.bbbbb.bbbbb.a.a",
           "a..p....p....p....a",
           "a.bbbbb.fbe.bbbbb.a",
           "a...p...a.a.......a",
           "a.fbe.a.cbd.a.fbe.a",
           "a.a.a.a..p..a.a.a.a",
           "a.cbd.a.fbe.a.cbd.a",
           "a.p..pa.a.a.ap.p..a",
           "a.bbbbd.cbd.cbbbb.a",
           "a..p.....p.....p..a",
           "cbbbbbbbbbbbbbbbbbd"]  

# Definis la taille d'une case en pixel
TAILLE_CASE = 32
# vitesse du serpent
speed = 1
# position de la tête du serpent
i, j = 17,8
# direction par défaut du serpent
direction = ""
# Liste qui contient les coordonnées du serpent
l_serpent = [[i,j], [i,j-1], [i,j-2]]
# S'occuppe du score et du temps
score = 0
temps = 0
score_label = None
timer_label = None

def dessiner_carte():
    """
    Docstring for dessiner_carte
    Dessine la carte en fonction de la liste tableau, chaque lettre correspond à une image différente
    """
    # Boucle qui parcourt la liste afin de créer la carte
    for j in range(len(tableau)):
        for i in range(len(tableau[j])):
            if tableau[j][i] == "a":
                canvas.create_image(32*i, j*32, anchor=NW, image=a)
            elif tableau[j][i] == "b":
                canvas.create_image(32*i, j*32, anchor=NW, image=b)
            elif tableau[j][i] == "c":
                canvas.create_image(32*i, j*32, anchor=NW, image=c)
            elif tableau[j][i] == "d":
                canvas.create_image(32*i, j*32, anchor=NW, image=d)
            elif tableau[j][i] == "e":
                canvas.create_image(32*i, j*32, anchor=NW, image=e)
            elif tableau[j][i] == "f":
                canvas.create_image(32*i, j*32, anchor=NW, image=f)
            elif tableau[j][i] == "p":
                tags = f"pomme_{j}_{i}"
                canvas.create_image(32*i, j*32, anchor=NW, image=pomme, tags=tags)
            elif tableau[j][i] == ".":
                pass

def interface():
    """
    Docstring for interface
    Crée l'interface du jeu, charge les images, et initialise les éléments graphiques
    """
    global fenetre, canvas, a, b, c, d, e, f, pomme, tete_base, tetes_images, timer_label, score_label, meilleur_label
    
    # Créela fenêtre principale et les éléments graphiques
    fenetre = Tk()
    fenetre.title("Nibbler")
    canvas = Canvas(
                    fenetre,
                    width=608,
                    height=608,
                    bg="black"
                    )
    canvas.pack(side=LEFT)

    hud_frame = Frame(fenetre, width=150, height=608, bg="grey")
    hud_frame.pack(side=RIGHT, fill=Y)

    score = 0
    temps = 0

    meilleur_score = charger_meilleur_score()
    meilleur_label = Label(hud_frame, text=f"Meilleur score: {meilleur_score}", font=("Arial", 14), bg="grey")
    meilleur_label.pack(pady=20)

    score_label = Label(hud_frame, text=f"Score: {score}", font=("Arial", 14), bg="grey")
    score_label.pack(pady=20)

    timer_label = Label(hud_frame, text=f"Temps: {temps}s", font=("Arial", 14), bg="grey")
    timer_label.pack(pady=20)

    instruction_label = Label(hud_frame, text="Utilisez les flèches pour déplacer le serpent", font=("Arial", 12), bg="grey")
    instruction_label.pack(pady=20)
    
    # Chargement des images
    imagea = Image.open("mur_a.png")
    a = ImageTk.PhotoImage(imagea)
    
    imageb = Image.open("mur_b.png")
    b = ImageTk.PhotoImage(imageb)
    
    imagec = Image.open("mur_c.png")
    c = ImageTk.PhotoImage(imagec)

    imaged = Image.open("mur_d.png")
    d = ImageTk.PhotoImage(imaged)
    
    imagee = Image.open("mur_e.png")
    e = ImageTk.PhotoImage(imagee)
    
    imagef = Image.open("mur_f.png")
    f = ImageTk.PhotoImage(imagef)
    
    imagep = Image.open("pomme.png")
    pomme = ImageTk.PhotoImage(imagep)

    image_tete = Image.open("tete.png")
    tete_base = ImageTk.PhotoImage(image_tete)

    # Liste des images de la tête du serpent pour chaque direction
    tetes_images = {
        "Right": ImageTk.PhotoImage(image_tete.rotate(0)),
        "Left": ImageTk.PhotoImage(image_tete.rotate(360)),
        "Up": ImageTk.PhotoImage(image_tete.rotate(90)),
        "Down": ImageTk.PhotoImage(image_tete.rotate(270)),
    }

    # Lier les touches du clavier à la fonction de déplacement, dessinne la carte, ...
    fenetre.bind("<Key>", deplacer)
    dessiner_carte()
    ajouter_pomme_aleatoire()
    dessiner(j * TAILLE_CASE, i * TAILLE_CASE, "red")
    
    fenetre.after(200, maj) 
    fenetre.after(1000, update_timer)

def update_timer():
    """
    Docstring for update_timer
    Met à jour le timer toutes les secondes et affiche le temps écoulé dans l'interface
    """
    global temps
    temps += 1
    if timer_label:
        timer_label.config(text=f"Temps: {temps}s")
    fenetre.after(1000, update_timer)

def charger_meilleur_score():
    """
    Docstring for charger_meilleur_score
    Charge le meilleur score depuis un fichier texte, si le fichier n'existe pas, il le crée et initialise le score à 0
    """
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")
        return 0
    with open("highscore.txt", "r") as f:
        return int(f.read().strip())

def sauvegarder_meilleur_score(score):
    """
    Docstring for sauvegarder_meilleur_score
    
    :param score: Le score actuel du joueur
    :return: Le meilleur score mis à jour Compare le score actuel avec le meilleur
    """
    meilleur = charger_meilleur_score()
    if score > meilleur:
        with open("highscore.txt", "w") as f:
            f.write(str(score))
        return score
    return meilleur

def ajouter_pomme_aleatoire():
    """
    Docstring for ajouter_pomme_aleatoire
    Ajoute une pomme à une position aléatoire sur la carte, en s'assurant que la case est vide et ne fait pas partie du serpent
    """
    # Cherche les cases vides "."
    cases_vides = []
    for y in range(len(tableau)):
        for x in range(len(tableau[y])):
            if tableau[y][x] == "." and [y, x] not in l_serpent:
                cases_vides.append((y, x))

    if not cases_vides:
        return  # aucune case disponible

    y, x = random.choice(cases_vides)
    tableau[y] = tableau[y][:x] + "p" + tableau[y][x+1:]
    
    # Crée l'image sur le canvas avec un tag unique
    canvas.create_image(x*TAILLE_CASE, y*TAILLE_CASE, anchor=NW, image=pomme, tags=f"pomme_{y}_{x}")

    # Relancer la fonction toutes les 2 ms
    fenetre.after(2000, ajouter_pomme_aleatoire)


def dessiner(x,y,color=None, image=None):
    """
    Docstring for dessiner
    
    :param x: coordonnée x en pixel
    :param y: coordonnée y en pixel
    :param color: couleur de l'objet, si rien par défaut None
    :param image: image à dessiner, si rien par défaut None
    """
    #x = j * TAILLE_CASE
    #y = i * TAILLE_CASE
    if image:
        canvas.create_image(x, y, anchor=NW, image=image, tags="snake")
    else: # si pas d'image, dessinne un rectangle
        canvas.create_rectangle(x,y, 
                            x+TAILLE_CASE,
                            y+TAILLE_CASE, 
                            fill=color, 
                            tags="snake"
                            )

def deplacer(event):
    """
    Docstring for deplacer
    
    :param event: change la direction du serpent en fonction de la touche pressée
    """
    #print(event)
    global direction, fenetre
    if event.keysym == "Right":
        direction = "Right"
    elif event.keysym == "Left":
        direction = "Left"
    elif event.keysym == "Up":
        direction = "Up"
    elif event.keysym == "Down":
        direction = "Down"

def collision(x,y):
    """
    Docstring for collision
    
    :param x: coordonnée x en pixel de la tête du serpent
    :param y: cordonnée y en pixel de la tête du serpent
    :return un tuple (mur, pomme)
    """
    # Gestion du hors carte
    if x<0 or y<0:
        return True, False
    if y >= len(tableau) or x >= len(tableau[0]):
        return True, False
    # Gestion des murs
    pomme_condition = False
    if tableau[y][x] == "p":
        pomme_condition = True
    return tableau[y][x] in ["a","b","c","d","e","f"], pomme_condition

    return False, False

def maj():
    """
    Docstring for maj
    Met à jour la position du serpent, gère les collisions, la croissance du serpent, et redessine le serpent à sa nouvelle position
    """
    global j,i


    canvas.delete("snake")

    j1,i1 = j,i # Position n+1

    # Direction du serpent, on ajoute ou soustrait la vitesse à la position actuelle en fonction de la direction choisie
    if direction == "Right":
        j1 += speed
        #print(tableau[-2])
    elif direction == "Left":
        j1 -= speed
        #print(len(l_serpent))
    elif direction == "Up":
        i1 -= speed
        #print(len(l_serpent))
    elif direction == "Down":
        i1 += speed
        #print(len(l_serpent))
    else:
        fenetre.after(200, maj) 
        return

    # Gestion des collisions, on vérifie si la nouvelle position de la tête du serpent est un mur ou une pomme
    mur, pomme = collision(j1, i1)

    if mur:
        j1, i1 = j, i
    
    # Si un mur GAME OVER -> non implémenté
    #if [i1, j1] in l_serpent[1:-1]:
     #   print("GAME OVER")
      #  return

    # Met à jour les coordonnées du serpent
    ancienne_tete = l_serpent[0].copy()
    for k in range(1, len(l_serpent)):
        ancienne_tete, l_serpent[k] = l_serpent[k], ancienne_tete

    l_serpent[0] = [i1, j1]
    j, i = j1, i1

    # Gestion des pommes
    if pomme:
            l_serpent.append(ancienne_tete)
            global score
            score += 1 # score + 1 si une pomme est mangée
            # Augmentation du score et mise à jour de l'affichage du score et du meilleur score
            if score_label:
                score_label.config(text=f"Score: {score}")
                nouveau_meilleur = sauvegarder_meilleur_score(score)
                meilleur_label.config(text=f"Meilleur score: {nouveau_meilleur}")
            canvas.delete(f"pomme_{i1}_{j1}")
            tableau[i1] = tableau[i1][:j1] + "." + tableau[i1][j1+1:]

    # Redessine le serpent à sa nouvelle position, la tête est dessinée avec une image et le reste du corps en vert
    for ind in range(len(l_serpent)): 
        x = l_serpent[ind][1] * TAILLE_CASE
        y = l_serpent[ind][0] * TAILLE_CASE
        if ind == 0:
            img_tete = tetes_images.get(direction)
            if img_tete:
                dessiner(x, y, image=img_tete)
            else:
                # SI l'image de la tête n'est pas disponible, dessine un rectangle rouge à la place
                dessiner(x, y, color="green")
        else:
            dessiner(x, y, color="red")

    fenetre.after(200, maj)


#global fenetre

interface()
fenetre.mainloop()