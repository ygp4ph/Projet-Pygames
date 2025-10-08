import pygame
from .entities import Player, Enemy
from .utils import draw_text, draw_health_bar

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Cyberpunk Battle 2077")
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Couleurs cyberpunk
        self.BLACK = (10, 10, 15)
        self.CYAN = (0, 255, 255)
        self.MAGENTA = (255, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.PURPLE = (138, 43, 226)
        self.WHITE = (255, 255, 255)
        self.GRAY = (50, 50, 60)
        
        self.setup_game()
    
    def setup_game(self):
        # Création du joueur
        self.player = Player("NetRunner", 100, 25, 5, 100, 250, self.CYAN)
        
        # Création des ennemis
        self.enemies = [
            Enemy("Corpo-Garde", 80, 20, 8, 500, 150, self.MAGENTA),
            Enemy("Hacker-Bot", 60, 30, 3, 500, 350, self.PURPLE)
        ]
        
        # État du jeu
        self.player_turn = True
        self.selected_target = 0
        self.message = "Ton tour ! Choisis une action"
        self.message_timer = 0
        self.game_over = False
        self.victory = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN and not self.game_over:
                if self.player_turn:
                    if event.key == pygame.K_1:  # Attaque normale
                        self.player_attack()
                    elif event.key == pygame.K_2:  # Compétence spéciale
                        self.player_special_attack()
                    elif event.key == pygame.K_3:  # Changer cible
                        self.change_target()
        
        return True
    
    def player_attack(self):
        if self.enemies[self.selected_target].is_alive():
            damage = self.player.attack(self.enemies[self.selected_target])
            self.message = f"Tu attaques {self.enemies[self.selected_target].name} ! -{damage} HP"
            self.message_timer = 120
            self.player_turn = False
    
    def player_special_attack(self):
        if self.enemies[self.selected_target].is_alive():
            damage = self.player.special_attack(self.enemies[self.selected_target])
            self.message = f"Compétence spéciale sur {self.enemies[self.selected_target].name} ! -{damage} HP"
            self.message_timer = 120
            self.player_turn = False
    
    def change_target(self):
        self.selected_target = (self.selected_target + 1) % len(self.enemies)
        while not self.enemies[self.selected_target].is_alive():
            self.selected_target = (self.selected_target + 1) % len(self.enemies)
        self.message = f"Cible: {self.enemies[self.selected_target].name}"
        self.message_timer = 60
    
    def enemy_turn(self):
        for enemy in self.enemies:
            if enemy.is_alive():
                damage = enemy.attack(self.player)
                self.message = f"{enemy.name} t'attaque ! -{damage} HP"
                self.message_timer = 120
                
                if not self.player.is_alive():
                    return
        
        self.player_turn = True
        self.message = "Ton tour ! Choisis une action"
    
    def update(self):
        if self.message_timer > 0:
            self.message_timer -= 1
        
        # Vérifier la victoire
        alive_enemies = [e for e in self.enemies if e.is_alive()]
        if len(alive_enemies) == 0 and not self.game_over:
            self.message = "VICTOIRE ! Tu as gagné !"
            self.victory = True
            self.game_over = True
        
        # Vérifier la défaite
        if not self.player.is_alive() and not self.game_over:
            self.message = "GAME OVER ! Tu es mort..."
            self.game_over = True
        
        # Tour des ennemis
        if not self.player_turn and not self.game_over and self.message_timer == 0:
            self.enemy_turn()
    
    def draw_background(self):
        self.screen.fill(self.BLACK)
        
        # Grille cyberpunk
        for i in range(0, self.WIDTH, 40):
            pygame.draw.line(self.screen, (30, 30, 40), (i, 0), (i, self.HEIGHT), 1)
        for i in range(0, self.HEIGHT, 40):
            pygame.draw.line(self.screen, (30, 30, 40), (0, i), (self.WIDTH, i), 1)
    
    def draw_ui(self):
        # Menu d'actions
        if not self.game_over:
            pygame.draw.rect(self.screen, self.GRAY, (50, 430, 700, 150))
            pygame.draw.rect(self.screen, self.CYAN, (50, 430, 700, 150), 3)
            
            actions = ["1: ATTAQUE", "2: COMPETENCE (x1.5)", "3: CHANGER CIBLE"]
            for i, action in enumerate(actions):
                draw_text(self.screen, action, 70 + i * 230, 480, self.YELLOW, 32)
        
        # Message
        draw_text(self.screen, self.message, self.WIDTH // 2, 50, self.YELLOW, 28, center=True)
    
    def draw(self):
        self.draw_background()
        
        # Personnages
        self.player.draw(self.screen)
        for enemy in self.enemies:
            if enemy.is_alive():
                enemy.draw(self.screen)
        
        # Indicateur de cible
        if not self.game_over and self.enemies[self.selected_target].is_alive():
            pygame.draw.rect(self.screen, self.YELLOW, 
                           (self.enemies[self.selected_target].x - 5, 
                            self.enemies[self.selected_target].y - 5, 90, 90), 3)
        
        self.draw_ui()
        pygame.display.flip()
    
    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)
            running = self.handle_events()
            self.update()
            self.draw()
        
        pygame.quit()