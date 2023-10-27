class Musique:

    def __init__(self, nom, chemin_fichier) -> None:
        self.nom = nom
        self.chemin_fichier = chemin_fichier

    @property
    def nom(self):
        return self._nom
    
    @nom.setter
    def nom(self, nom):
        if len(nom) > 0 and len(nom) < 64:
            self._nom = nom

    @property
    def chemin_fichier(self):
        return self._chemin_fichier
    
    @chemin_fichier.setter
    def chemin_fichier(self, nouveau_chemin_fichier):
        if len(nouveau_chemin_fichier) > 0 and len(nouveau_chemin_fichier) < 1024:
            self._chemin_fichier = nouveau_chemin_fichier

    def __str__(self) -> str:
        return self.nom