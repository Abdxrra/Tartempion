import random
import simpleaudio as sa
import time
import sqlite3 as squirrel
import PySimpleGUI as gui


from modules.images import Images
from modules.indicateurs import Indicateur
from modules.difficulte import Difficulte
from modules.musique import Musique


class Jeu:
       
    NOM_APP = 'Monsieur Tartempion'

    NOM_FICHIER_SON_VICTOIRE = '522243__dzedenz__result-10.wav'
    NOM_FICHIER_SON_ERREUR = '409282__wertstahl__syserr1v1-in_thy_face_short.wav'
    NOM_FICHIER_SON_FIN_PARTIE = '173859__jivatma07__j1game_over_mono.wav'
    NOM_FICHIER_MUSIQUE_QUESTIONS = '550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav'

    # Clés des elements de l'interface
    TITRE = 'TITRE'
    TEMPS = 'TEMPS'
    BOUTON_GAUCHE = 'BOUTON_GAUCHE'
    OU = 'OU'
    BOUTON_DROIT = 'BOUTON_DROIT'
    QUESTION = 'QUESTION'
    BOUTON_ACTION = 'BOUTON_ACTION'
    IMAGE_BOUTON_INACTIF = 'IMAGE_BOUTON_INACTIF'
    INDICATEUR = 'INDICATEUR'

    # Styles de police pour les éléments d'interface
    police_title: tuple = (gui.DEFAULT_FONT, 40, 'italic')
    police_etiquettes: tuple = (gui.DEFAULT_FONT, 20, 'normal')
    police_temps: tuple = (gui.DEFAULT_FONT, 50, 'normal')
    police_question: tuple = (gui.DEFAULT_FONT, 30, 'normal')
    police_reponses: tuple = (gui.DEFAULT_FONT, 20, 'normal')
    police_ou: tuple = (gui.DEFAULT_FONT, 20, 'italic')


    def __init__():
        Images = Images()
        
        Musiques = [
            Musique("Basique", 'audios/musiques/550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav'),
            Musique("Kahoot", 'audios/musiques/kahoot.wav'),
            Musique("Mario", 'audios/musiques/mario.wav')
        ]

        Difficultes = [
            Difficulte("SUPER FACILE", 10, 60),
            Difficulte("FACILE", 15, 60),
            Difficulte("MOYEN", 21, 60),
            Difficulte("DIFFICILE", 30, 60),
            Difficulte("TRÈS DIFFICILE", 30, 45)
        ]

        self.difficulte_choisie = DIFFICULTE[2]
        self.musique_choisie = MUSIQUES[0]
        self.decompte_actif = False
        self.temps_restant = difficulte_choisie.temps

            
    def afficher_menu() -> None:
        """Afficher le menu"""

        difficulte_selection = gui.Combo(
            DIFFICULTE, DIFFICULTE[2], font=police_reponses, enable_events=True,  readonly=True, key='COMBO_DIFFICULTE')

        musique_selection = gui.Combo(MUSIQUES, musique_choisie, font=police_reponses,
                                    enable_events=True,  readonly=True, key='COMBO_MUSIQUE')

        commencer = gui.Button("COMMENCER", key='BOUTON-COMMENCER', font=police_reponses,
                            button_color=('white', gui.theme_background_color()), border_width=0)
        quitter = gui.Button("QUITTER", key='BOUTON-QUITTER', font=police_reponses,
                            button_color=('white', gui.theme_background_color()), border_width=0)

        design = [
            [
                [gui.Text("DIFFICULTÉ", font=police_reponses, pad=(10, 0)),
                difficulte_selection, gui.VPush()],
                [gui.Text("MUSIQUE", font=police_reponses, pad=(10, 0)),
                musique_selection, gui.VPush()],
                [commencer, gui.VPush()],
                [quitter, gui.VPush()]
            ]
        ]

        fenetre = gui.Window(TITRE, design, keep_on_top=True, element_padding=(0, 0),
                            element_justification='center', resizable=False, finalize=True, size=(500, 280))

        return fenetre
    
    def afficher_jeu() -> None:
        """Afficher l'interface du jeu"""

        title = [gui.Text(TITRE, key='TITLE', font=police_title)]

        temps = [[gui.Text('Temps restant', font=police_etiquettes, size=70, justification='center')], [
            gui.Text(str(difficulte_choisie.temps), key='TEMPS', font=police_temps)]]

        boutons_reponse = [gui.Column([[gui.Button(key='BOUTON-GAUCHE', font=police_reponses, button_color=('white', gui.theme_background_color()),
                                                border_width=0, disabled=True, visible=True),
                                        gui.Text(' ou ', key='OU', font=police_ou,
                                                text_color=gui.theme_background_color()),
                                        gui.Button(key='BOUTON-DROIT', font=police_reponses, button_color=('white', gui.theme_background_color()),
                                                border_width=0, disabled=True, visible=True)]], element_justification='center')]

        question = [gui.Text(' ', key='QUESTION', font=police_question)]

        action = [gui.Button(image_data=IMAGES.bouton_jouer_base64(), key='BOUTON-ACTION',
                border_width=0, button_color=(gui.theme_background_color(), gui.theme_background_color()), pad=(0, 10)),
                gui.Image(data=IMAGES.bouton_inactif_base64(), key='IMAGE-BOUTON-INACTIF', visible=False, pad=(0, 10))]

        indicateurs = [*[gui.Image(data=IMAGES.indicateur_vide_base64(), key=f'INDICATEUR-{i}', pad=(
            4, 10)) for i in range(difficulte_choisie.nombre_questions)]]

        fenetre = gui.Window(TITRE, [temps, boutons_reponse, question, action, indicateurs], keep_on_top=True, element_padding=(0, 0),
                            element_justification='center', resizable=False, finalize=True)

        return fenetre

    def splasher_equipe(temps_ms: int) -> None:
        """Afficher le logo de l'équipe"""

        gui.Window(TITRE, [[gui.Image(data=IMAGES.equipe_base64(), subsample=2)]],
                no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)

    def splasher_titre(delai: int, pardessus: bool) -> None:
        """Afficher le logo du jeu"""

        gui.Window(TITRE, [[gui.Image(data=IMAGES.titre_base64())]], no_titlebar=True,
                keep_on_top=pardessus).read(timeout=delai, close=True)

    def splasher_echec(temps_ms: int = 3000) -> None:
        """afficher un écran d'échec"""

        gui.Window(TITRE, [[gui.Image(data=IMAGES.echec_base64())]], transparent_color=gui.theme_background_color(),
                no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)

    def splasher_succes(temps_ms: int = 3000) -> None:
        """afficher un écran de réussite"""

        gui.Window(TITRE, [[gui.Image(data=IMAGES.succes_base64())]], transparent_color="maroon2",
                no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)

    def nouvelle_partie():
        pass

    def perdu():
        pass

    def gagner():
        pass
    
    def main():
        splasher_equipe()
        
        
if "__name__" == "__main__":
    jeu = Jeu()
    jeu.afficher_menu()