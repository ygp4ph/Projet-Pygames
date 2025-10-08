import json
import os
from src.utils.constants import SAVE_FILE


class SaveManager:
    """Gère la sauvegarde et le chargement des parties"""
    
    def __init__(self):
        # Créer le dossier saves s'il n'existe pas
        save_dir = os.path.dirname(SAVE_FILE)
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
    
    def save(self, data):
        """Sauvegarde les données dans un fichier JSON"""
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")
            return False
    
    def load(self):
        """Charge les données depuis le fichier JSON"""
        if not os.path.exists(SAVE_FILE):
            print("Aucun fichier de sauvegarde trouvé.")
            return None
        
        try:
            with open(SAVE_FILE, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f"Erreur lors du chargement : {e}")
            return None
    
    def delete_save(self):
        """Supprime le fichier de sauvegarde"""
        if os.path.exists(SAVE_FILE):
            try:
                os.remove(SAVE_FILE)
                print("Sauvegarde supprimée.")
                return True
            except Exception as e:
                print(f"Erreur lors de la suppression : {e}")
                return False
        return False