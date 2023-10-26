import unittest
import PySimpleGUI as gui

from monsieur_tartempion import fenetre_de_jeu, charger_questions

class TestTartempion(unittest.TestCase):

    def test_creation_fenetre_de_jeu(self):
        fenetre = fenetre_de_jeu()
        self.assertIsInstance(fenetre, gui.Window)
    
    def test_charger_questions_bd(self):
        questions = charger_questions("questions.bd")
        self.assertIsInstance(questions, list)

if __name__ == '__main__':
    unittest.main()