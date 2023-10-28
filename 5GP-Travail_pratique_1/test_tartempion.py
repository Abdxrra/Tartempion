import unittest
import PySimpleGUI as gui
import simpleaudio as sa

from modules.indicateurs import Indicateur
from monsieur_tartempion import Jeu
from modules.questions import Questions
from modules.difficulte import Difficulte
from modules.partie import Partie
from modules.musique import Musique

class TestTartempion(unittest.TestCase):
    
    def setUp(self):

        difficultes = [
            Difficulte("SUPER FACILE", 10, 60),
            Difficulte("FACILE", 15, 60),
            Difficulte("MOYEN", 21, 60),
            Difficulte("DIFFICILE", 30, 60),
            Difficulte("TRÈS DIFFICILE", 30, 45)
        ]

        musiques = [
            Musique("Basique", 'audios/musiques/550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav'),
            Musique("Kahoot", 'audios/musiques/kahoot.wav'),
            Musique("Mario", 'audios/musiques/mario.wav')
        ]
        self.jeu = Jeu(difficultes, musiques)
        self.partie = Partie(difficultes[0], musiques[0], self.jeu.images)
        self.question = Questions()
        self.nombre_de_questions = 3
        self.liste_questions = self.question.choisir_questions(self.nombre_de_questions)
        self.music_file = 'audios/musiques/550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav'
    
    def test_creation_fenetre_de_jeu(self):
        fenetre = self.partie.fenetre
        self.assertIsInstance(fenetre, gui.Window)

    def test_jeu_se_cree(self):
        jeu = self.jeu
        self.assertIsNotNone(jeu)
    
    def test_choisir_la_difficulte(self):
        chosen_difficulty = Difficulte("FACILE", 15, 60)
        self.partie = Partie(chosen_difficulty, self.jeu.musiques[0], self.jeu.images)
        self.assertEqual(self.partie.difficulte_choisie, chosen_difficulty)
    
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
        reponses = [(question[0][1], question[0][2]) for question in self.partie.questions]
        shuffled = self.partie._melanger_reponses()
        self.assertNotIn(reponses, shuffled)

    def test_initialiser_la_musique(self):
        try:
            music_wave = sa.WaveObject.from_wave_file(self.jeu.musique_choisie.chemin_fichier)
            play_obj = music_wave.play()
            self.assertIsInstance(play_obj, sa.PlayObject)
        except Exception as e:
            self.fail(f"La musique n'est pas initialisé : {str(e)}")

    def test_choisir_nombre_questions(self):
        longueur_liste_question = len(self.liste_questions)
        self.assertEqual(longueur_liste_question, self.nombre_de_questions)

    def test_verifier_indicateur_vide(self):
        for question, indicator in self.liste_questions:
            self.assertEqual(indicator, Indicateur.VIDE)

    def test_quitter_jeu(self):
        self.jeu.quitter = True
        self.jeu.demarrer_boucle_jeu()
        self.assertTrue(self.jeu.quitter)


if __name__ == '__main__':
    unittest.main()