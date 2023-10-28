"""
Monsieur Tartempion - Édition horrifique
420-5GP-BB, automne 2023, Collège Bois-de-Boulogne
Travail pratique 1

Ressources sous licences:
  522243__dzedenz__result-10.wav
  par DZeDeNZ, 2020-07-15
  Licence: https://creativecommons.org/publicdomain/zero/1.0/

  409282__wertstahl__syserr1v1-in_thy_face_short.wav
  par wertstahl, 2017-11-06
  Licence: https://creativecommons.org/licenses/by-nc/4.0/

  173859__jivatma07__j1game_over_mono.wav
  par jivatma07, 2013-01-11
  Licence: https://creativecommons.org/publicdomain/zero/1.0/

  550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav
  par Erokia, 2020-12-26
  Licence: https://creativecommons.org/licenses/by-nc/4.0/
"""

import random
import simpleaudio as sa
import time
import sqlite3 as squirrel
import PySimpleGUI as gui

from modules.images import Images
from modules.difficulte import Difficulte
from modules.musique import Musique
from modules.partie import Partie

TITRE = 'Monsieur Tartempion'
TEMPS = 'TEMPS'
OU = 'OU'

BOUTON_GAUCHE = 'BOUTON_GAUCHE'
BOUTON_DROIT = 'BOUTON_DROIT'
BOUTON_COMMENCER = 'BOUTON_COMMENCER'
BOUTON_QUITTER = 'BOUTON_QUITTER'
COMBO_DIFFICULTE = 'COMBO_DIFFICULTE'
COMBO_MUSIQUE = 'COMBO_MUSIQUE'

QUESTION = 'QUESTION'
INDICATEUR = 'INDICATEUR'
BOUTON_ACTION = 'BOUTON_ACTION'
IMAGE_BOUTON_INACTIF = 'IMAGE_BOUTON_INACTIF'


class Jeu:

    def __init__(self, difficultes: list, musiques: list) -> None:

        self.difficultes = difficultes
        self.musiques = musiques        
        self.images = Images()

        self.quitter = False
        self.difficulte_choisie = self.difficultes[2]
        self.musique_choisie = self.musiques[0]


    def _afficher_fenetre_menu(self):
        """Afficher l'interface du menu"""
        
        police_reponses: tuple = (gui.DEFAULT_FONT, 20, 'normal')

        difficulte_selection = gui.Combo(
            self.difficultes, self.difficulte_choisie, font=police_reponses, enable_events=True, readonly=True, key=COMBO_DIFFICULTE)

        musique_selection = gui.Combo(self.musiques, self.musique_choisie, font=police_reponses,
            enable_events=True, readonly=True, key=COMBO_MUSIQUE)

        commencer = gui.Button("COMMENCER", key=BOUTON_COMMENCER, font=police_reponses,
            button_color=('white', gui.theme_background_color()), border_width=0)
        
        quitter = gui.Button("QUITTER", key=BOUTON_QUITTER, font=police_reponses,
            button_color=('white', gui.theme_background_color()), border_width=0)

        agencement_fenetre = [
            [
                [gui.Text("DIFFICULTÉ", font=police_reponses, pad=(10, 0)),
                    difficulte_selection, gui.VPush()],
                [gui.Text("MUSIQUE", font=police_reponses, pad=(10, 0)),
                    musique_selection, gui.VPush()],
                [commencer, gui.VPush()],
                [quitter, gui.VPush()]
            ]
        ]

        fenetre = gui.Window(TITRE, agencement_fenetre, keep_on_top=True, element_padding=(0, 0),
            element_justification='center', resizable=False, finalize=True, size=(500, 280))

        return fenetre


    def _splasher_equipe(self, temps_ms: int) -> None:
        """Afficher le logo de l'équipe"""

        gui.Window(TITRE, [[gui.Image(data=self.images.equipe_base64(), subsample=2)]],
                no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)


    def _splasher_titre(self, delai: int, pardessus: bool) -> None:
        """Afficher le logo du jeu"""

        gui.Window(TITRE, [[gui.Image(data=self.images.titre_base64())]], no_titlebar=True,
                keep_on_top=pardessus).read(timeout=delai, close=True)


    def _menu(self) -> tuple:
        """Affiche le menu et assigne la difficulte et la musique"""

        fenetre = self._afficher_fenetre_menu()
        menu_boucle = True

        while menu_boucle:
            event, values = fenetre.read(timeout=10)

            match event:
                case 'BOUTON_COMMENCER':
                    menu_boucle = False
                    fenetre.close()
                    del fenetre

                case 'BOUTON_QUITTER' | gui.WIN_CLOSED:
                    menu_boucle = False
                    self.quitter = True

                case 'COMBO_DIFFICULTE':
                    self.difficulte_choisie = values[COMBO_DIFFICULTE]

                case 'COMBO_MUSIQUE':
                    self.musique_choisie = values[COMBO_MUSIQUE]

    def demarrer_boucle_jeu(self) -> None:
        """Boucle principal du jeu"""

        # Afficher un écran de démarrage pour le logo de l'équipe
        self._splasher_equipe(1500)

        # Afficher un écran de démarrage pour le titre
        self._splasher_titre(2000, True)

        # boucle principale
        boucle_jeu = True

        while boucle_jeu and not self.quitter:
            
            self._menu()

            if self.quitter:
                break

            partie = Partie(self.difficulte_choisie, self.musique_choisie, self.images)

            partie.commencer()


if __name__ == '__main__':

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

    jeu = Jeu(difficultes, musiques)
    jeu.demarrer_boucle_jeu()