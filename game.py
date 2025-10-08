import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Constantes
LARGEUR = 800
HAUTEUR = 600
FPS = 60

# Couleurs cyberpunk
NOIR = (10, 10, 15)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
JAUNE = (255, 255, 0)
VIOLET = (138, 43, 226)
BLANC = (255, 255, 255)
GRIS = (50, 50, 60)

# Fenêtre
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Cyber Battles 2077")
horloge = pygame.time.Clock()

# Classe Personnage
class Personnage:
    def __init__(self, nom, hp_max, attaque, defense, x, y, couleur):
        self.nom = nom
        self.hp_max = hp_max
        self.hp = hp_max
        self.attaque = attaque
        self.defense = defense
        self.x = x
        self.y = y
        self.couleur = couleur
        self.est_joueur = False
        
    def attaquer(self, cible):
        degats = max(1, self.attaque - cible.defense + random.randint(-5, 5))
        cible.hp -= degats
        if cible.hp < 0:
            cible.hp = 0
        return degats
    
    def competence_speciale(self, cible):
        degats = int(self.attaque * 1.5) - cible.defense
        cible.hp -= degats
        if cible.hp < 0:
            cible.hp = 0
        return degats
    
    def est_vivant(self):
        return self.hp > 0
    
    def dessiner(self, ecran):
        # Carré pour représenter le perso (tu pourras mettre une image plus tard)
        pygame.draw.rect(ecran, self.couleur, (self.x, self.y, 80, 80), 0)
        pygame.draw.rect(ecran, CYAN, (self.x, self.y, 80, 80), 2)
        
        # Nom
        font = pygame.font.Font(None, 24)
        texte_nom = font.render(self.nom, True, BLANC)
        ecran.blit(texte_nom, (self.x, self.y - 25))
        
        # Barre de vie
        largeur_barre = 80
        hauteur_barre = 10
        ratio_hp = self.hp / self.hp_max
        pygame.draw.rect(ecran, GRIS, (self.x, self.y + 85, largeur_barre, hauteur_barre))
        pygame.draw.rect(ecran, MAGENTA, (self.x, self.y + 85, largeur_barre * ratio_hp, hauteur_barre))
        
        # HP
        texte_hp = font.render(f"{self.hp}/{self.hp_max}", True, BLANC)
        ecran.blit(texte_hp, (self.x, self.y + 100))

# Création des personnages
joueur = Personnage("NetRunner", 100, 25, 5, 100, 200, CYAN)
joueur.est_joueur = True

ennemis = [
    Personnage("Corpo-Garde", 80, 20, 8, 600, 150, MAGENTA),
    Personnage("Hacker-Bot", 60, 30, 3, 600, 300, VIOLET)
]

# Variables de jeu
tour_joueur = True
cible_selectionnee = 0
message = "Ton tour ! Choisis une action"
message_timer = 0

# Fonction pour afficher le menu d'actions
def afficher_menu(ecran):
    font = pygame.font.Font(None, 32)
    y_pos = 450
    
    pygame.draw.rect(ecran, GRIS, (50, 430, 700, 150))
    pygame.draw.rect(ecran, CYAN, (50, 430, 700, 150), 3)
    
    actions = ["1: ATTAQUE", "2: COMPETENCE (x1.5)", "3: CHANGER CIBLE"]
    for i, action in enumerate(actions):
        texte = font.render(action, True, JAUNE)
        ecran.blit(texte, (70 + i * 230, y_pos))

# Fonction pour afficher les messages
def afficher_message(ecran, msg):
    font = pygame.font.Font(None, 28)
    texte = font.render(msg, True, JAUNE)
    rect = texte.get_rect(center=(LARGEUR // 2, 50))
    pygame.draw.rect(ecran, NOIR, (rect.x - 10, rect.y - 5, rect.width + 20, rect.height + 10))
    pygame.draw.rect(ecran, CYAN, (rect.x - 10, rect.y - 5, rect.width + 20, rect.height + 10), 2)
    ecran.blit(texte, rect)

# Fonction pour le tour de l'ennemi
def tour_ennemi():
    global message, message_timer, tour_joueur
    
    for ennemi in ennemis:
        if ennemi.est_vivant():
            pygame.time.wait(500)
            degats = ennemi.attaquer(joueur)
            message = f"{ennemi.nom} t'attaque ! -{degats} HP"
            message_timer = 120
            
            if not joueur.est_vivant():
                return
    
    tour_joueur = True
    message = "Ton tour ! Choisis une action"

# Boucle de jeu principale
en_jeu = True
jeu_fini = False

while en_jeu:
    horloge.tick(FPS)
    
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            en_jeu = False
        
        if event.type == pygame.KEYDOWN and not jeu_fini:
            if tour_joueur:
                if event.key == pygame.K_1:  # Attaque
                    if ennemis[cible_selectionnee].est_vivant():
                        degats = joueur.attaquer(ennemis[cible_selectionnee])
                        message = f"Tu attaques {ennemis[cible_selectionnee].nom} ! -{degats} HP"
                        message_timer = 120
                        tour_joueur = False
                
                elif event.key == pygame.K_2:  # Compétence
                    if ennemis[cible_selectionnee].est_vivant():
                        degats = joueur.competence_speciale(ennemis[cible_selectionnee])
                        message = f"Compétence spéciale sur {ennemis[cible_selectionnee].nom} ! -{degats} HP"
                        message_timer = 120
                        tour_joueur = False
                
                elif event.key == pygame.K_3:  # Changer de cible
                    cible_selectionnee = (cible_selectionnee + 1) % len(ennemis)
                    while not ennemis[cible_selectionnee].est_vivant():
                        cible_selectionnee = (cible_selectionnee + 1) % len(ennemis)
                    message = f"Cible: {ennemis[cible_selectionnee].nom}"
                    message_timer = 60
    
    # Mise à jour
    if message_timer > 0:
        message_timer -= 1
    
    # Vérifier si tous les ennemis sont morts
    ennemis_vivants = [e for e in ennemis if e.est_vivant()]
    if len(ennemis_vivants) == 0 and not jeu_fini:
        message = "VICTOIRE ! Tu as gagné !"
        jeu_fini = True
    
    # Vérifier si le joueur est mort
    if not joueur.est_vivant() and not jeu_fini:
        message = "GAME OVER ! Tu es mort..."
        jeu_fini = True
    
    # Tour de l'ennemi
    if not tour_joueur and not jeu_fini and message_timer == 0:
        tour_ennemi()
    
    # Affichage
    ecran.fill(NOIR)
    
    # Grille cyberpunk en fond
    for i in range(0, LARGEUR, 40):
        pygame.draw.line(ecran, (30, 30, 40), (i, 0), (i, HAUTEUR), 1)
    for i in range(0, HAUTEUR, 40):
        pygame.draw.line(ecran, (30, 30, 40), (0, i), (LARGEUR, i), 1)
    
    # Dessiner les personnages
    joueur.dessiner(ecran)
    for ennemi in ennemis:
        if ennemi.est_vivant():
            ennemi.dessiner(ecran)
    
    # Indicateur de cible
    if not jeu_fini and ennemis[cible_selectionnee].est_vivant():
        pygame.draw.rect(ecran, JAUNE, 
                        (ennemis[cible_selectionnee].x - 5, 
                         ennemis[cible_selectionnee].y - 5, 90, 90), 3)
    
    # Afficher le menu et les messages
    if not jeu_fini:
        afficher_menu(ecran)
    afficher_message(ecran, message)
    
    pygame.display.flip()

pygame.quit()
sys.exit()