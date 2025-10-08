import pygame
from src.entities.player import Player
from src.entities.enemy import Enemy
from src.ui.hud import HUD
from src.utils.constants import *
from src.utils.save_manager import SaveManager


class Game:
    """Classe principale qui gère toute la logique du jeu"""
    
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        
        # État du jeu
        self.running = True
        self.paused = False
        self.game_state = "menu"  # "menu", "playing", "game_over", "pause_menu", "confirm_quit"
        self.souls = 0  # Score du joueur
        
        # Boutons pour les menus
        self.selected_button = 0
        self.pause_button_count = 3  # Reprendre, Sauvegarder, Quitter
        
        # Gestionnaire de sauvegarde
        self.save_manager = SaveManager()
        
        # Initialiser le jeu
        self.init_game()
    
    def init_game(self):
        """Initialise ou réinitialise le jeu"""
        # Création du joueur
        self.player = Player(100, 400)
        
        # Liste des ennemis
        self.enemies = [
            Enemy(400, 400),
            Enemy(700, 400)
        ]
        
        # Interface utilisateur
        self.hud = HUD(self)
        
        # Groupes de sprites
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        for enemy in self.enemies:
            self.all_sprites.add(enemy)
        
        # Réinitialiser les âmes si nouveau jeu depuis le menu
        if self.game_state == "menu":
            self.souls = 0
    
    def handle_event(self, event):
        """Gère les événements clavier et souris"""
        if event.type == pygame.KEYDOWN:
            # Navigation dans les menus
            if self.game_state == "menu":
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    self.selected_button = (self.selected_button - 1) % 2
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_button = (self.selected_button + 1) % 2
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.handle_menu_selection()
            
            elif self.game_state == "pause_menu":
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    self.selected_button = (self.selected_button - 1) % self.pause_button_count
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_button = (self.selected_button + 1) % self.pause_button_count
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.handle_pause_menu_selection()
                elif event.key == pygame.K_ESCAPE:
                    self.game_state = "playing"
                    self.selected_button = 0
            
            elif self.game_state == "confirm_quit":
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    self.selected_button = (self.selected_button - 1) % 3
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_button = (self.selected_button + 1) % 3
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.handle_quit_confirmation()
                elif event.key == pygame.K_ESCAPE:
                    self.game_state = "pause_menu"
                    self.selected_button = 0
            
            elif self.game_state == "game_over":
                if event.key == pygame.K_UP or event.key == pygame.K_z:
                    self.selected_button = (self.selected_button - 1) % 2
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.selected_button = (self.selected_button + 1) % 2
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.handle_menu_selection()
            
            # En jeu
            elif self.game_state == "playing":
                if event.key == pygame.K_ESCAPE:
                    self.game_state = "pause_menu"
                    self.selected_button = 0
                elif event.key == pygame.K_F5:
                    self.save_game()
                elif event.key == pygame.K_F9:
                    self.load_game()
    
    def handle_menu_selection(self):
        """Gère la sélection dans les menus"""
        if self.game_state == "menu":
            if self.selected_button == 0:  # Nouvelle partie
                self.game_state = "playing"
                self.init_game()
            elif self.selected_button == 1:  # Charger partie
                if self.load_game():
                    self.game_state = "playing"
        
        elif self.game_state == "game_over":
            if self.selected_button == 0:  # Rejouer
                self.game_state = "playing"
                self.init_game()
            elif self.selected_button == 1:  # Menu principal
                self.game_state = "menu"
                self.selected_button = 0
    
    def handle_pause_menu_selection(self):
        """Gère la sélection dans le menu pause"""
        if self.selected_button == 0:  # Reprendre
            self.game_state = "playing"
            self.selected_button = 0
        elif self.selected_button == 1:  # Sauvegarder
            self.save_game()
        elif self.selected_button == 2:  # Quitter
            self.game_state = "confirm_quit"
            self.selected_button = 0
    
    def handle_quit_confirmation(self):
        """Gère la confirmation de sortie"""
        if self.selected_button == 0:  # Sauvegarder et quitter
            self.save_game()
            self.game_state = "menu"
            self.selected_button = 0
        elif self.selected_button == 1:  # Quitter sans sauvegarder
            self.game_state = "menu"
            self.selected_button = 0
        elif self.selected_button == 2:  # Annuler
            self.game_state = "pause_menu"
            self.selected_button = 0
    
    def update(self, dt):
        """Met à jour la logique du jeu"""
        if self.game_state != "playing":
            return
        
        # Mise à jour du joueur
        self.player.update(dt, self.enemies)
        
        # Vérifier si le joueur est mort
        if not self.player.is_alive():
            self.game_state = "game_over"
            self.selected_button = 0
            return
        
        # Mise à jour des ennemis
        for enemy in self.enemies[:]:
            enemy.update(dt, self.player)
            
            # Si l'ennemi est mort, on le retire et on gagne des âmes
            if enemy.health <= 0:
                self.souls += ENEMY_KILL_SOULS
                self.enemies.remove(enemy)
                self.all_sprites.remove(enemy)
    
    def render(self):
        """Affiche tous les éléments du jeu"""
        if self.game_state == "menu":
            self.render_menu()
        elif self.game_state == "playing":
            self.render_game()
        elif self.game_state == "pause_menu":
            self.render_game()  # Afficher le jeu en arrière-plan
            self.render_pause_menu()
        elif self.game_state == "confirm_quit":
            self.render_game()  # Afficher le jeu en arrière-plan
            self.render_quit_confirmation()
        elif self.game_state == "game_over":
            self.render_game_over()
    
    def render_menu(self):
        """Affiche le menu principal"""
        self.screen.fill(BLACK)
        
        # Titre
        title_font = pygame.font.Font(None, 100)
        title = title_font.render("DARK SOULS 2D", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Boutons
        button_font = pygame.font.Font(None, 50)
        buttons_text = ["Nouvelle Partie", "Charger Partie"]
        
        for i, text in enumerate(buttons_text):
            color = WHITE if i == self.selected_button else GRAY
            button = button_font.render(text, True, color)
            button_rect = button.get_rect(center=(SCREEN_WIDTH // 2, 350 + i * 80))
            self.screen.blit(button, button_rect)
        
        # Instructions
        info_font = pygame.font.Font(None, 30)
        info = info_font.render("Utilisez Z/S et ENTREE pour selectionner", True, GRAY)
        info_rect = info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(info, info_rect)
    
    def render_game(self):
        """Affiche le jeu en cours"""
        # Fond
        self.screen.fill(DARK_GRAY)
        
        # Sol temporaire
        pygame.draw.rect(self.screen, GRAY, (0, 500, SCREEN_WIDTH, 220))
        
        # Affichage de tous les sprites
        self.all_sprites.draw(self.screen)
        
        # Affichage des barres de vie des ennemis
        for enemy in self.enemies:
            enemy.draw_health_bar(self.screen)
        
        # Affichage de l'interface
        self.hud.render(self.screen)
    
    def render_pause_menu(self):
        """Affiche le menu pause par-dessus le jeu"""
        # Overlay sombre
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Titre Pause
        title_font = pygame.font.Font(None, 100)
        title = title_font.render("PAUSE", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)
        
        # Boutons
        button_font = pygame.font.Font(None, 50)
        buttons_text = ["Reprendre", "Sauvegarder", "Quitter"]
        
        for i, text in enumerate(buttons_text):
            color = WHITE if i == self.selected_button else GRAY
            button = button_font.render(text, True, color)
            button_rect = button.get_rect(center=(SCREEN_WIDTH // 2, 320 + i * 80))
            self.screen.blit(button, button_rect)
        
        # Instructions
        info_font = pygame.font.Font(None, 30)
        info = info_font.render("Z/S pour naviguer | ENTREE pour valider | ESC pour reprendre", True, GRAY)
        info_rect = info.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.screen.blit(info, info_rect)
    
    def render_quit_confirmation(self):
        """Affiche la confirmation de sortie"""
        # Overlay encore plus sombre
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        # Question
        title_font = pygame.font.Font(None, 60)
        title = title_font.render("Voulez-vous sauvegarder ?", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        # Boutons
        button_font = pygame.font.Font(None, 50)
        buttons_text = ["Sauvegarder et quitter", "Quitter sans sauvegarder", "Annuler"]
        
        for i, text in enumerate(buttons_text):
            color = WHITE if i == self.selected_button else GRAY
            button = button_font.render(text, True, color)
            button_rect = button.get_rect(center=(SCREEN_WIDTH // 2, 340 + i * 80))
            self.screen.blit(button, button_rect)
    
    def render_game_over(self):
        """Affiche l'écran de Game Over"""
        self.screen.fill(BLACK)
        
        # Titre Game Over
        title_font = pygame.font.Font(None, 120)
        title = title_font.render("YOU DIED", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(title, title_rect)
        
        # Score final
        score_font = pygame.font.Font(None, 50)
        score = score_font.render(f"Ames collectees : {self.souls}", True, WHITE)
        score_rect = score.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(score, score_rect)
        
        # Boutons
        button_font = pygame.font.Font(None, 50)
        buttons_text = ["Rejouer", "Menu Principal"]
        
        for i, text in enumerate(buttons_text):
            color = WHITE if i == self.selected_button else GRAY
            button = button_font.render(text, True, color)
            button_rect = button.get_rect(center=(SCREEN_WIDTH // 2, 420 + i * 80))
            self.screen.blit(button, button_rect)
    
    def save_game(self):
        """Sauvegarde la partie"""
        data = {
            'player_x': self.player.rect.x,
            'player_y': self.player.rect.y,
            'player_health': self.player.health,
            'player_stamina': self.player.stamina,
            'souls': self.souls,
            'enemies': [
                {'x': enemy.rect.x, 'y': enemy.rect.y, 'health': enemy.health}
                for enemy in self.enemies
            ]
        }
        self.save_manager.save(data)
        print("Partie sauvegardée !")
    
    def load_game(self):
        """Charge une partie sauvegardée"""
        data = self.save_manager.load()
        if data:
            # Restaurer le joueur
            self.player.rect.x = data['player_x']
            self.player.rect.y = data['player_y']
            self.player.health = data['player_health']
            self.player.stamina = data['player_stamina']
            self.souls = data['souls']
            
            # Restaurer les ennemis
            self.enemies.clear()
            self.all_sprites.empty()
            self.all_sprites.add(self.player)
            
            for enemy_data in data['enemies']:
                enemy = Enemy(enemy_data['x'], enemy_data['y'])
                enemy.health = enemy_data['health']
                self.enemies.append(enemy)
                self.all_sprites.add(enemy)
            
            print("Partie chargée !")
            return True
        else:
            print("Aucune sauvegarde trouvée.")
            return False