import pygame
from src.game import Game
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE


def main():
    """Point d'entrée principal du jeu"""
    # Initialisation de Pygame
    pygame.init()
    
    # Création de la fenêtre
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    
    # Horloge pour gérer les FPS
    clock = pygame.time.Clock()
    
    # Création du jeu
    game = Game(screen)
    
    # Boucle principale
    running = True
    while running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game.handle_event(event)
        
        # Mise à jour du jeu
        dt = clock.tick(FPS) / 1000.0  # Delta time en secondes
        game.update(dt)
        
        # Affichage
        game.render()
        pygame.display.flip()
    
    # Fermeture propre
    pygame.quit()


if __name__ == "__main__":
    main()