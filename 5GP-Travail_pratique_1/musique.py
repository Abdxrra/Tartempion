class Musique:

    def __init__(self, nom, chemin_fichier) -> None:
        self.nom = nom
        self.chemin_fichier = chemin_fichier
        
    def __str__(self) -> str:
        return self.nom