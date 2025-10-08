import pygame
from src.utils.constants import *


class Platform:
    """Plateforme centrale du jeu"""
    
    def __init__(self):
        self.rect = pygame.Rect(PLATFORM_X, PLATFORM_Y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        self.color = GRAY
    
    def render(self, surface):
        """Dessine la plateforme"""
        # Plateforme principale
        pygame.draw.rect(surface, self.color, self.rect)
        # Bordure
        pygame.draw.rect(surface, WHITE, self.rect, 3)