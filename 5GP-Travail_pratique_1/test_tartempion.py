import unittest
import PySimpleGUI as gui
import simpleaudio as sa

from modules.indicateurs import Indicateur
from monsieur_tartempion import fenetre_de_jeu, melanger_reponses, musique_choisie
from modules.questions import Questions
from modules.difficulte import Difficulte

class TestTartempion(unittest.TestCase):
    
    def setUp(self):
        question = Questions()
        self.nombre_de_questions = 3
        self.liste_questions = question.choisir_questions(self.nombre_de_questions)
        self.music_file = 'audios/musiques/550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav'
    
    def test_creation_fenetre_de_jeu(self):
        fenetre = fenetre_de_jeu()
        self.assertIsInstance(fenetre, gui.Window)
    
    def test_charger_questions_bd(self):
        question = Questions()
        questions = question.charger_fichier()
        self.assertIsInstance(questions, list)

    def test_choisir_difficulte(self):
        difficulte = Difficulte("TEST", 10, 60)
        questions = Questions()
        question_list = questions.choisir_questions(difficulte.nombre_questions)
        self.assertEqual(len(question_list), difficulte.nombre_questions)

    def test_melanger_reponses(self):
        reponses = [('A', 'B'), ('C', 'D'), ('E', 'F'), ('G', 'H'), ('I', 'J')]
        shuffled = melanger_reponses(reponses)
        self.assertNotIn(reponses, shuffled)
        
    # def test_fermer_fenetre(self):
    #     fenetre = fenetre_de_jeu()
    #     fermer_programme(fenetre)
    #     self.assertTrue(fenetre.is_closed)

    def test_music_initialization(self):
        try:
            music_wave = sa.WaveObject.from_wave_file(musique_choisie.chemin_fichier)
            play_obj = music_wave.play()
            self.assertIsInstance(play_obj, sa.PlayObject)
            play_obj.wait_done()
        except Exception as e:
            self.fail(f"Failed to initialize and play music: {str(e)}")

    def test_choisir_nombre_questions(self):
        longueur_liste_question = len(self.liste_questions)
        self.assertEqual(longueur_liste_question, self.nombre_de_questions)

    def test_verifier_indicateur_vide(self):
        for question, indicator in self.liste_questions:
            self.assertEqual(indicator, Indicateur.VIDE)


if __name__ == '__main__':
    unittest.main()