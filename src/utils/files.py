import os

def append_file(chemin_complet, contenu):
    """Ajoute du contenu à un fichier spécifié par son chemin complet."""
    # Vérifie si le répertoire existe, sinon le crée
    os.makedirs(os.path.dirname(chemin_complet), exist_ok=True)
    
    with open(chemin_complet, 'a', encoding='utf-8') as fichier: # créer si n'existe pas
        fichier.write(contenu + '\n')  # Ajoute le contenu suivi d'un saut de ligne