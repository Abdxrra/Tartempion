class Difficulte:

    def __init__(self, nom, nombre_question, temps) -> None:
        self._nom = nom
        self._nombre_questions = nombre_question
        self._temps = temps
    
    @property
    def nom(self):
        return self._nom
    
    @nom.setter
    def nom(self, nom):
        if len(nom) > 0:
            self._nom = nom

    @property
    def nombre_questions(self):
        return self._nombre_questions
    
    @nombre_questions.setter
    def nombre_questions(self, nombre):
        if nombre > 0:
            return self._nombre_questions

    @property
    def temps(self):
        return self._temps
    
    @temps.setter
    def temps(self, secondes):
        if secondes > 0:
            self._temps = secondes

    def __str__(self) -> str:
        return self.nom