import random
import time

import PySimpleGUI as gui
import simpleaudio as sa

from .musique import Musique
from .difficulte import Difficulte
from .questions import Questions
from .images import Images
from .indicateurs import Indicateur

SON_VICTOIRE = sa.WaveObject.from_wave_file('audios/effet sonores/522243__dzedenz__result-10.wav')
SON_ERREUR = sa.WaveObject.from_wave_file('audios/effet sonores/409282__wertstahl__syserr1v1-in_thy_face_short.wav')
SON_FIN_PARTIE = sa.WaveObject.from_wave_file('audios/effet sonores/173859__jivatma07__j1game_over_mono.wav')

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

# Définir les styles de police pour différents éléments
police_title: tuple = (gui.DEFAULT_FONT, 40, 'italic')
police_etiquettes: tuple = (gui.DEFAULT_FONT, 20, 'normal')
police_temps: tuple = (gui.DEFAULT_FONT, 50, 'normal')
police_question: tuple = (gui.DEFAULT_FONT, 30, 'normal')
police_reponses: tuple = (gui.DEFAULT_FONT, 20, 'normal')
police_ou: tuple = (gui.DEFAULT_FONT, 20, 'italic')

class Partie:
    def __init__(self, difficulte_choisie: Difficulte, musique_choisie: Musique, images: Images):

        self.difficulte_choisie = difficulte_choisie
        self.musique_choisie = sa.WaveObject.from_wave_file(musique_choisie.chemin_fichier)
        self.musique_questions_controles = None

        self.images = images
        self.questions = Questions().choisir_questions(self.difficulte_choisie.nombre_questions)
        self.reponses = self.__melanger_reponses()

        self.decompte_actif = False

        self.temps_restant = self.difficulte_choisie.temps

        self.prochaine_question = 0
        self.position_meilleure_tentative = 0

        self.fenetre = self.__fenetre_de_jeu()

    def __fenetre_de_jeu(self) -> gui.Window:
        """Afficher l'interface du jeu"""

        temps = [[gui.Text('Temps restant', font=police_etiquettes, size=70, justification='center')], [
            gui.Text(str(self.difficulte_choisie.temps), key=TEMPS, font=police_temps)]]

        boutons_reponse = [gui.Column(
            [[gui.Button(key=BOUTON_GAUCHE, font=police_reponses, button_color=('white', gui.theme_background_color()),
                         border_width=0, disabled=True, visible=True),
              gui.Text(' ou ', key=OU, font=police_ou,
                       text_color=gui.theme_background_color()),
              gui.Button(key=BOUTON_DROIT, font=police_reponses, button_color=('white', gui.theme_background_color()),
                         border_width=0, disabled=True, visible=True)]], element_justification='center')]

        question = [gui.Text(' ', key=QUESTION, font=police_question)]

        action = [gui.Button(image_data=self.images.bouton_jouer_base64(), key=BOUTON_ACTION,
                             border_width=0, button_color=(gui.theme_background_color(), gui.theme_background_color()),
                             pad=(0, 10)),
                  gui.Image(data=self.images.bouton_inactif_base64(), key=IMAGE_BOUTON_INACTIF, visible=False, pad=(0, 10))]

        indicateurs = [*[gui.Image(data=self.images.indicateur_vide_base64(), key=f'{INDICATEUR}-{i}', pad=(
            4, 10)) for i in range(self.difficulte_choisie.nombre_questions)]]

        fenetre = gui.Window(TITRE, [temps, boutons_reponse, question, action, indicateurs], keep_on_top=True,
                             element_padding=(0, 0),
                             element_justification='center', resizable=False, finalize=True)

        return fenetre

    def __melanger_reponses(self) -> list:
        """fonction pour mélanger les réponses"""

        reponses = [(question[0][1], question[0][2]) for question in self.questions]

        for position_couple_reponses in range(len(reponses)):
            reponses[position_couple_reponses] = (
                reponses[position_couple_reponses][0], reponses[position_couple_reponses][1]) if bool(
                random.getrandbits(1)) else (
                reponses[position_couple_reponses][1], reponses[position_couple_reponses][0])
        return reponses

    def __splasher_echec(self, temps_ms: int = 3000) -> None:
        """afficher un écran d'échec"""

        gui.Window(TITRE, [[gui.Image(data=self.images.echec_base64())]], transparent_color=gui.theme_background_color(),
                   no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)

    def __splasher_succes(self, temps_ms: int = 3000) -> None:
        """afficher quand le joueur gagne"""

        gui.Window(TITRE, [[gui.Image(data=self.images.succes_base64())]], transparent_color="maroon2",
                   no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)

    def __afficher_question(self, question: tuple, reponses: tuple) -> None:
        """afficher la question"""
        fenetre = self.fenetre

        fenetre[QUESTION].update(question[0])
        fenetre[BOUTON_GAUCHE].update(reponses[0], disabled=False, visible=True)
        fenetre[OU].update(text_color='white')
        fenetre[BOUTON_DROIT].update(reponses[1], disabled=False, visible=True)

    def __effacer_question(self) -> None:
        """Effacer la question affichée dans la fenêtre"""

        self.fenetre[QUESTION].update('')
        self.fenetre[BOUTON_GAUCHE].update('', disabled=True, visible=True)
        self.fenetre[OU].update(text_color=gui.theme_background_color())
        self.fenetre[BOUTON_DROIT].update('', disabled=True, visible=True)

    def __fin_partie(self, est_un_echec: bool) -> None:

        self.decompte_actif = False
        self.fenetre.hide()
        self.__effacer_question()
        for i in range(self.difficulte_choisie.nombre_questions):
            self.fenetre[f'{INDICATEUR}-{i}'].update(data=self.images.indicateur_vide_base64())

            if not est_un_echec:
                self.questions[i][1] = Indicateur.VIDE

        self.musique_questions_controles.stop()

        if est_un_echec:
            SON_FIN_PARTIE.play()
            self.__splasher_echec()
        else:
            SON_VICTOIRE.play()
            self.__splasher_succes()

        self.fenetre.close()

    def __reprendre_partie(self):
        self.fenetre[BOUTON_ACTION].update(disabled=True, visible=False)
        self.fenetre[IMAGE_BOUTON_INACTIF].update(visible=True)
        self.__afficher_question(self.questions[self.prochaine_question][0], self.reponses[self.prochaine_question])

        # set le temps
        self.temps_actuel = round(time.time())
        self.decompte_actif = True

        # controleur de la musique qui joue
        self.musique_questions_controles = self.musique_choisie.play()

    def commencer(self) -> None:
        """commencer la partie"""
        fenetre = self.fenetre

        quitter = False
        # Tant qu'on ne quitte pas le jeu, fait cela
        while not quitter:
            evenement, valeurs = fenetre.read(timeout=10)

            # Si le décompte est actif, on diminue le temps restant et on met à jour le UI
            if self.decompte_actif:

                dernier_temps = self.temps_actuel
                self.temps_actuel = round(time.time())

                if dernier_temps != self.temps_actuel:
                    self.temps_restant -= 1
                    print(self.temps_restant)
                    fenetre[TEMPS].update(str(self.temps_restant))

                    # Si le temps est écoulé, affiche l'écran d'échec
                    if self.temps_restant == 0:
                        # arrete la partie
                        self.__fin_partie(True)


            # Si on clique sur le bouton pour commencer le jeu, on affiche les questions
            if evenement == BOUTON_ACTION:

                # set le temps
                self.temps_actuel = round(time.time())
                self.decompte_actif = True

                # demarrer ou reprendre la partie
                self.__reprendre_partie()

            # Si on clique sur une des deux réponses (gauche ou droite)
            elif evenement == BOUTON_GAUCHE or evenement == BOUTON_DROIT:

                # Si le joueur a choisi la bonne réponse
                if (evenement == BOUTON_GAUCHE and fenetre[BOUTON_GAUCHE].get_text() != self.questions[self.prochaine_question][0][
                    1]) or \
                        (evenement == BOUTON_DROIT and fenetre[BOUTON_DROIT].get_text() != self.questions[
                            self.prochaine_question][0][
                            1]):

                    fenetre[f'{INDICATEUR}-{self.prochaine_question}'].update(data=self.images.indicateur_vert_base64())
                    self.questions[self.prochaine_question][1] = Indicateur.VERT
                    self.prochaine_question += 1

                    if self.prochaine_question < self.difficulte_choisie.nombre_questions:
                        self.__afficher_question(self.questions[self.prochaine_question][0], self.reponses[
                            self.prochaine_question])

                    # quand le joueur gagne
                    elif self.difficulte_choisie.nombre_questions <= self.prochaine_question:
                        self.__fin_partie(False)

                # Sinon, le joueur a choisi la mauvaise réponse
                else:
                    self.decompte_actif = False
                    self.__effacer_question()

                    for i in range(self.prochaine_question):
                        fenetre[f'{INDICATEUR}-{i}'].update(
                            data=self.images.indicateur_jaune_base64())
                        self.questions[i][1] = Indicateur.JAUNE

                    if self.prochaine_question > self.position_meilleure_tentative or self.position_meilleure_tentative == 0:
                        self.position_meilleure_tentative = self.prochaine_question
                        fenetre[f'{INDICATEUR}-{self.position_meilleure_tentative}'].update(
                            data=self.images.indicateur_rouge_base64())
                        self.questions[self.position_meilleure_tentative][1] = Indicateur.ROUGE

                    fenetre[BOUTON_ACTION].update(disabled=False, visible=True)
                    fenetre[IMAGE_BOUTON_INACTIF].update(visible=False)

                    self.prochaine_question = 0

                    self.musique_questions_controles.stop()
                    SON_ERREUR.play()

            # Si on ferme le jeu
            elif evenement == gui.WIN_CLOSED:
                self.decompte_actif = False
                quitter = True

        fenetre.close()
