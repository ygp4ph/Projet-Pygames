import pygame
from src.utils.constants import *


class HUD:
    """Interface utilisateur avec vies et super-pouvoirs"""
    
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 50)
    
    def render(self, surface):
        """Affiche l'interface"""
        self.draw_lives(surface)
        self.draw_health_bar(surface)
        self.draw_stamina_bar(surface)
        self.draw_super_powers(surface)
        self.draw_souls(surface)
        self.draw_controls(surface)
    
    def draw_lives(self, surface):
        """Affiche les vies en haut au centre"""
        lives_text = self.big_font.render(f"VIES: {self.game.player.lives}", True, RED)
        lives_rect = lives_text.get_rect(center=(SCREEN_WIDTH // 2, 30))
        
        # Fond noir semi-transparent
        bg_rect = pygame.Rect(lives_rect.x - 20, lives_rect.y - 5, 
                             lives_rect.width + 40, lives_rect.height + 10)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
        bg_surface.set_alpha(150)
        bg_surface.fill(BLACK)
        surface.blit(bg_surface, bg_rect)
        
        # Texte des vies
        surface.blit(lives_text, lives_rect)
    
    def draw_health_bar(self, surface):
        """Barre de vie"""
        bar_x = 20
        bar_y = 80
        bar_width = 300
        bar_height = 25
        
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
        surface.blit(text, (bar_x + 5, bar_y + 3))
    
    def draw_stamina_bar(self, surface):
        """Barre d'endurance"""
        bar_x = 20
        bar_y = 115
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
    
    def draw_super_powers(self, surface):
        """Affiche les super-pouvoirs disponibles"""
        powers = self.game.player.character_data['powers']
        power_x = 20
        power_y = 150
        
        # Titre
        title = self.small_font.render("SUPER POUVOIRS:", True, WHITE)
        surface.blit(title, (power_x, power_y))
        
        # Afficher chaque pouvoir
        for i, power in enumerate(powers):
            y_pos = power_y + 30 + i * 60
            
            # Couleur selon le pouvoir
            if power == 'vitesse':
                color = YELLOW
                icon = ">>>"
            elif power == 'force':
                color = RED
                icon = "!!!"
            elif power == 'saut':
                color = BLUE
                icon = "^^^"
            
            # Nom du pouvoir
            power_name = self.small_font.render(f"{i+1}. {power.upper()}", True, color)
            surface.blit(power_name, (power_x, y_pos))
            
            # Icône
            icon_text = self.small_font.render(icon, True, color)
            surface.blit(icon_text, (power_x + 180, y_pos))
            
            # État (actif, cooldown, prêt)
            if self.game.player.power_active and self.game.player.current_power == power:
                status = f"{int(self.game.player.power_timer / 1000)}s"
                status_color = GREEN
            elif self.game.player.power_cooldown > 0:
                status = f"CD: {int(self.game.player.power_cooldown / 1000)}s"
                status_color = GRAY
            else:
                status = "PRET"
                status_color = GREEN
            
            status_text = self.small_font.render(status, True, status_color)
            surface.blit(status_text, (power_x, y_pos + 20))
    
    def draw_souls(self, surface):
        """Affiche le score (âmes)"""
        text = self.font.render(f"AMES: {self.game.souls}", True, YELLOW)
        surface.blit(text, (SCREEN_WIDTH - 250, 80))
    
    def draw_controls(self, surface):
        """Affiche les contrôles"""
        controls = [
            "Q/D: Bouger | ESPACE: Sauter | E: Attaquer | SHIFT: Roulade",
            "1/2: Super Pouvoirs | ESC: Pause"
        ]
        
        y_offset = SCREEN_HEIGHT - 60
        for control in controls:
            text = self.small_font.render(control, True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            
            # Fond semi-transparent
            bg_rect = pygame.Rect(text_rect.x - 10, text_rect.y - 3, 
                                 text_rect.width + 20, text_rect.height + 6)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(120)
            bg_surface.fill(BLACK)
            surface.blit(bg_surface, bg_rect)
            
            surface.blit(text, text_rect)
            y_offset += 25