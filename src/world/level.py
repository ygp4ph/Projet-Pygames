import pygame


class Level:
    """Classe pour gérer les niveaux/maps du jeu"""
    
    def __init__(self):
        """Initialise le niveau"""
        # Pour l'instant c'est vide, on ajoutera Tiled plus tard
        pass
    
    def load_map(self, map_file):
        """Charge une map depuis un fichier Tiled"""
        # À implémenter plus tard avec pytmx
        pass
    
    def update(self, dt):
        """Met à jour le niveau"""
        pass
    
    def render(self, surface):
        """Affiche le niveau"""
        pass