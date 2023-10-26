import unittest
import PySimpleGUI as gui

from indicateurs import Indicateur
from monsieur_tartempion import fenetre_de_jeu, charger_questions, obtenir_activite_decompte, fermer_programme

class TestTartempion(unittest.TestCase):
    
    def test_creation_fenetre_de_jeu(self):
        fenetre = fenetre_de_jeu()
        self.assertIsInstance(fenetre, gui.Window)
    
    def test_charger_questions_bd(self):
        questions = charger_questions("questions.bd")
        self.assertIsInstance(questions, list)
        
    def test_decompte_inactif(self):
        decompte_actif = obtenir_activite_decompte()
        self.assertFalse(decompte_actif)
        
    def test_fermer_fenetre(self):
        fenetre = fenetre_de_jeu()
        fermer_programme(fenetre)
        self.assertNotIsInstance(fenetre, gui.Window)


if __name__ == '__main__':
    unittest.main()