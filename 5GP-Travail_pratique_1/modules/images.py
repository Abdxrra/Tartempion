import pickle
from modules.integrite import hash_fichier


class Images:

    def __init__(self, chemin_fichier_pickle="../images.pkl") -> None:
        self.integrite = "511f7dc94ed40ce2d033570b5ea3f9b90c2c348151ae1035621fdcc711176393"
        self.chemin_fichier_pickle = chemin_fichier_pickle
        
        if not self.verifier_integrite():
            print("le fichier d'images a été modifié")

        self.charger_fichier()

    def equipe_base64(self) -> bytes:
        return self._equipe_base64

    def echec_base64(self) -> bytes:
        return self._echec_base64

    def succes_base64(self) -> bytes:
        return self._succes_base64

    def bouton_inactif_base64(self) -> bytes:
        return self._bouton_inactif_base64

    def bouton_jouer_base64(self) -> bytes:
        return self._bouton_jouer_base64

    def indicateur_vide_base64(self) -> bytes:
        return self._indicateur_vide_base64

    def indicateur_jaune_base64(self) -> bytes:
        return self._indicateur_jaune_base64

    def indicateur_rouge_base64(self) -> bytes:
        return self._indicateur_rouge_base64

    def indicateur_vert_base64(self) -> bytes:
        return self._indicateur_vert_base64

    def titre_base64(self) -> bytes:
        return self._titre_base64

    def charger_fichier(self) -> None:
        """Charger les images depuis le fichier pickle"""
        with open(self.chemin_fichier_pickle, "rb") as f:
            (self._equipe_base64,
            self._echec_base64,
            self._succes_base64,
            self._bouton_inactif_base64,
            self._bouton_jouer_base64,
            self._indicateur_vide_base64,
            self._indicateur_jaune_base64,
            self._indicateur_rouge_base64,
            self._indicateur_vert_base64,
            self._titre_base64) = pickle.load(f)
    
    def verifier_integrite(self) -> bool:
        """Verifie l'integrité du fichier pickle"""

        return self.integrite == hash_fichier(self.chemin_fichier_pickle)