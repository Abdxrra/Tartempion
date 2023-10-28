import random
import sqlite3 as squirrel
from .integrite import hash_fichier
from .indicateurs import Indicateur


class Questions:

    def __init__(self) -> None:
        self.__hash_original = "d2ecbcf93b792e64d8642005b88e44e1adee72843c02272df2a5d982e4cf8152"
        self.chemin_fichier_bd = "questions.bd"

        # check si l'integrité du fichier est compromise
        self.integrite_compromise = False
        
        if not self.verifier_integrite():
            self.integrite_compromise = True

        self.banque_questions = self.charger_fichier()

    def charger_fichier(self) -> None:
        """charge les question depuis le fichier BD"""

        # Établir une connexion à la base de données
        connexion = squirrel.connect(self.chemin_fichier_bd)

        with connexion:
            # Exécuter une requête SQL pour obtenir les questions et réponses
            resultat_requete = connexion.execute('SELECT question, reponse_exacte, reponse_erronee FROM QUESTIONS')
            questions = [(enregistrement[0], enregistrement[1], enregistrement[2]) for enregistrement in
                         resultat_requete]

            # Retourner les enregistrements sous forme de liste
            return questions

    def choisir_questions(self, nombre_de_questions: int) -> list:
        """choisi un certain nombre de questions parmi une banque de questions"""

        return [[question, Indicateur.VIDE] for question in
                random.choices(self.banque_questions, k=nombre_de_questions)]

    def verifier_integrite(self) -> bool:
        """Verifie l'integrité du fichier bd"""

        return self.__hash_original == hash_fichier(self.chemin_fichier_bd)
