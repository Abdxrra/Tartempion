import sqllite3 as squirrel
from modules.integrite import hash_fichier


class Questions:
    
    def __init__(self, chemin_fichier_bd="../questions.bd") -> None:
        self.integrite = "511f7dc94ed40ce2d033570b5ea3f9b90c2c348151ae1035621fdcc711176393"
        self.chemin_fichier_bd = chemin_fichier_bd
        
        if self.verifier_integrite():
            print("le fichier de questions a été modifié")

        self.banque_questions = self.charger_fichier()
    
    def charger_fichier(self) -> None:
        """charge les question depuis le fichier BD"""
    
        # Établir une connexion à la base de données
        connexion = squirrel.connect(fichier_db)

        with connexion:
            
            # Exécuter une requête SQL pour obtenir les questions et réponses    
            resultat_requete = connexion.execute('SELECT question, reponse_exacte, reponse_erronee FROM QUESTIONS')
            questions = [(enregistrement[0], enregistrement[1], enregistrement[2]) for enregistrement in resultat_requete]

            #fermer la connection
            connexion.close()

            # Retourner les enregistrements sous forme de liste
            return questions
        
    def choisir_questions(self, nombre_de_questions: int) -> list:
        """choisi un certain nombre de questions parmi une banque de questions"""

        return [[question, Indicateur.VIDE] for question in random.choices(banque, k=nombre_de_questions)]

    def verifier_integrite(self) -> bool:
        """Verifie l'integrité du fichier pickle"""

        return self.integrite == hash_fichier(self.chemin_fichier_pickle)
    