import pygame
from src.utils.constants import *


class HUD:
    """Interface utilisateur affichant les informations du joueur"""
    
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
    def render(self, surface):
        """Affiche l'interface"""
        self.draw_health_bar(surface)
        self.draw_stamina_bar(surface)
        self.draw_souls(surface)
        self.draw_controls(surface)
    
    def draw_health_bar(self, surface):
        """Dessine la barre de vie du joueur"""
        bar_x = 20
        bar_y = 20
        bar_width = 300
        bar_height = 30
        
        # Fond
        pygame.draw.rect(surface, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # Barre de vie
        health_ratio = self.game.player.health / self.game.player.max_health
        current_width = int(bar_width * health_ratio)
        pygame.draw.rect(surface, RED, (bar_x, bar_y, current_width, bar_height))
        
        # Bordure
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Texte
        text = self.small_font.render(
            f"VIE: {int(self.game.player.health)}/{self.game.player.max_health}", 
            True, WHITE
        )
        surface.blit(text, (bar_x + 5, bar_y + 5))
    
    def draw_stamina_bar(self, surface):
        """Dessine la barre d'endurance du joueur"""
        bar_x = 20
        bar_y = 60
        bar_width = 300
        bar_height = 20
        
        # Fond
        pygame.draw.rect(surface, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
        
        # Barre d'endurance
        stamina_ratio = self.game.player.stamina / self.game.player.max_stamina
        current_width = int(bar_width * stamina_ratio)
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, current_width, bar_height))
        
        # Bordure
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Texte
        text = self.small_font.render(
            f"ENDURANCE: {int(self.game.player.stamina)}", 
            True, WHITE
        )
        surface.blit(text, (bar_x + 5, bar_y + 1))
    
    def draw_souls(self, surface):
        """Affiche le nombre d'âmes (score)"""
        text = self.font.render(f"ÂMES: {self.game.souls}", True, WHITE)
        surface.blit(text, (SCREEN_WIDTH - 250, 20))
    
    def draw_controls(self, surface):
        """Affiche les contrôles en bas de l'écran"""
        controls = [
            "Q/D: Déplacer | ESPACE: Sauter | E: Attaquer",
            "SHIFT: Roulade | F5: Sauvegarder | F9: Charger | ESC: Pause"
        ]
        
        y_offset = SCREEN_HEIGHT - 60
        for control in controls:
            text = self.small_font.render(control, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            surface.blit(text, text_rect)
            y_offset += 25