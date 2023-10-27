class Difficulte:

    def __init__(self, nom, nombre_questions, temps) -> None:
        self.nom = nom
        self.nombre_questions = nombre_questions
        self.temps = temps
    
    @property
    def nom(self):
        return self._nom
    
    @nom.setter
    def nom(self, nom):
        if len(nom) > 0 and len(nom) < 64:
            self._nom = nom

    @property
    def nombre_questions(self):
        return self._nombre_questions
    
    @nombre_questions.setter
    def nombre_questions(self, nombre):
        if nombre > 0 and nombre < 64:
            self._nombre_questions =nombre

    @property
    def temps(self):
        return self._temps
    
    @temps.setter
    def temps(self, secondes):
        if secondes > 0 and secondes < 100:
            self._temps = secondes

    def __str__(self) -> str:
        return self.nom