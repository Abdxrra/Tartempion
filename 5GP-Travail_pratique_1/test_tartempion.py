import unittest
import PySimpleGUI as gui

from indicateurs import Indicateur
from monsieur_tartempion import fenetre_de_jeu, charger_questions, melanger_reponses, fermer_programme, choisir_questions, obtenir_activite_decompte

class TestTartempion(unittest.TestCase):
    
    def setUp(self):
        self.toutes_les_questions = charger_questions("questions.bd")
        self.nombre_de_questions = 3
        self.liste_questions = choisir_questions(self.toutes_les_questions, self.nombre_de_questions)

    def test_creation_fenetre_de_jeu(self):
        fenetre = fenetre_de_jeu()
        self.assertIsInstance(fenetre, gui.Window)
    
    def test_charger_questions_bd(self):
        questions = charger_questions("questions.bd")
        self.assertIsInstance(questions, list)
    
    def test_melanger_reponses(self):
        reponses = ('A', 'B')
        shuffled = melanger_reponses(reponses)
        self.assertIn(shuffled, [('A', 'B'), ('B', 'A')])
        
    def test_fermer_fenetre(self):
        fenetre = fenetre_de_jeu()
        fermer_programme(fenetre)
        self.assertTrue(fenetre.is_closed)

    def test_choisir_nombre_questions(self):
        longueur_liste_question = len(self.liste_questions)
        self.assertEqual(longueur_liste_question, self.nombre_de_questions)

    def test_verifier_indicateur_vide(self):
        for question, indicator in self.liste_questions:
            self.assertEqual(indicator, Indicateur.VIDE)


if __name__ == '__main__':
    unittest.main()