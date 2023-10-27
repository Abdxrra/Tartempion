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
from modules.indicateurs import Indicateur
from modules.difficulte import Difficulte
from modules.musique import Musique
from modules.questions import Questions

DIFFICULTE = [
    Difficulte("SUPER FACILE", 10, 60),
    Difficulte("FACILE", 15, 60),
    Difficulte("MOYEN", 21, 60),
    Difficulte("DIFFICILE", 30, 60),
    Difficulte("TRÈS DIFFICILE", 30, 1)
]

MUSIQUES = [
    Musique("Basique", 'audios/musiques/550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav'),
    Musique("Kahoot", 'audios/musiques/kahoot.wav'),
    Musique("Mario", 'audios/musiques/mario.wav')
]

IMAGES = Images()
QUESTIONS = Questions()

difficulte_choisie = DIFFICULTE[2]
musique_choisie = MUSIQUES[0]

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

TAILLE_BUFFER = 65536

# Définir les styles de police pour différents éléments
police_title: tuple = (gui.DEFAULT_FONT, 40, 'italic')
police_etiquettes: tuple = (gui.DEFAULT_FONT, 20, 'normal')
police_temps: tuple = (gui.DEFAULT_FONT, 50, 'normal')
police_question: tuple = (gui.DEFAULT_FONT, 30, 'normal')
police_reponses: tuple = (gui.DEFAULT_FONT, 20, 'normal')
police_ou: tuple = (gui.DEFAULT_FONT, 20, 'italic')


# def hash_fichier(chemin_fichier) -> str:
    
#     sha256 = hashlib.sha256()

#     with open(chemin_fichier, 'rb') as f:
#         while True:
#             donnee = f.read(BUF_SIZE)
#             if not donnee:
#                 break
            
#             sha256.update(donnee)

#     return sha256.hexdigest()

# def calculate_sha256_checksum(file_path):
#     sha256_hash = hashlib.sha256()
#     with open(file_path, 'rb') as file:
#         while True:
#             data = file.read(65536)  # Read in 64 KB blocks
#             if not data:
#                 break
#             sha256_hash.update(data)
#     return sha256_hash.hexdigest()

def afficher_menu() -> None:
    """Afficher le menu"""

    difficulte_selection = gui.Combo(
        DIFFICULTE, DIFFICULTE[2], font=police_reponses, enable_events=True,  readonly=True, key=COMBO_DIFFICULTE)

    musique_selection = gui.Combo(MUSIQUES, musique_choisie, font=police_reponses,
                                  enable_events=True,  readonly=True, key=COMBO_MUSIQUE)

    commencer = gui.Button("COMMENCER", key=BOUTON_COMMENCER, font=police_reponses,
                           button_color=('white', gui.theme_background_color()), border_width=0)
    quitter = gui.Button("QUITTER", key=BOUTON_QUITTER, font=police_reponses,
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


def splasher_equipe(temps_ms: int) -> None:
    """Afficher le logo de l'équipe"""

    gui.Window(TITRE, [[gui.Image(data=IMAGES.equipe_base64(), subsample=2)]],
               no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)


def splasher_titre(delai: int, pardessus: bool) -> None:
    """Afficher le logo du jeu"""

    gui.Window(TITRE, [[gui.Image(data=IMAGES.titre_base64())]], no_titlebar=True,
               keep_on_top=pardessus).read(timeout=delai, close=True)


def fenetre_de_jeu() -> gui.Window:
    """Afficher l'interface du jeu"""

    title = [gui.Text(TITRE, key='TITLE', font=police_title)]

    temps = [[gui.Text('Temps restant', font=police_etiquettes, size=70, justification='center')], [
        gui.Text(str(difficulte_choisie.temps), key=TEMPS, font=police_temps)]]

    boutons_reponse = [gui.Column([[gui.Button(key=BOUTON_GAUCHE, font=police_reponses, button_color=('white', gui.theme_background_color()),
                                               border_width=0, disabled=True, visible=True),
                                    gui.Text(' ou ', key=OU, font=police_ou,
                                             text_color=gui.theme_background_color()),
                                    gui.Button(key=BOUTON_DROIT, font=police_reponses, button_color=('white', gui.theme_background_color()),
                                               border_width=0, disabled=True, visible=True)]], element_justification='center')]

    question = [gui.Text(' ', key=QUESTION, font=police_question)]

    action = [gui.Button(image_data=IMAGES.bouton_jouer_base64(), key=BOUTON_ACTION,
              border_width=0, button_color=(gui.theme_background_color(), gui.theme_background_color()), pad=(0, 10)),
              gui.Image(data=IMAGES.bouton_inactif_base64(), key=IMAGE_BOUTON_INACTIF, visible=False, pad=(0, 10))]

    indicateurs = [*[gui.Image(data=IMAGES.indicateur_vide_base64(), key=f'{INDICATEUR}-{i}', pad=(
        4, 10)) for i in range(difficulte_choisie.nombre_questions)]]

    fenetre = gui.Window(TITRE, [temps, boutons_reponse, question, action, indicateurs], keep_on_top=True, element_padding=(0, 0),
                         element_justification='center', resizable=False, finalize=True)

    return fenetre


def effacer_question(fenetre: gui.Window) -> None:
    """Effacer la question affichée dans la fenêtre"""

    fenetre[QUESTION].update('')
    fenetre[BOUTON_GAUCHE].update('', disabled=True, visible=True)
    fenetre[OU].update(text_color=gui.theme_background_color())
    fenetre[BOUTON_DROIT].update('', disabled=True, visible=True)


def melanger_reponses(reponses: list) -> list:
    """fonction pour mélanger les réponses"""

    reponses = list(reponses)
    random.shuffle(reponses)

    return reponses[::-1]


def splasher_echec(temps_ms: int = 3000) -> None:
    """afficher un écran d'échec"""

    gui.Window(TITRE, [[gui.Image(data=IMAGES.echec_base64())]], transparent_color=gui.theme_background_color(),
               no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)


def splasher_succes(temps_ms: int = 3000) -> None:
    """afficher quand le joueur gagne"""

    gui.Window(TITRE, [[gui.Image(data=IMAGES.succes_base64())]], transparent_color="maroon2",
               no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)


def afficher(fenetre: gui.Window, question: tuple) -> None:
    """afficher la question"""

    fenetre[QUESTION].update(question[0])
    reponses = melanger_reponses((question[1], question[2]))
    fenetre[BOUTON_GAUCHE].update(reponses[0], disabled=False, visible=True)
    fenetre[OU].update(text_color='white')
    fenetre[BOUTON_DROIT].update(reponses[1], disabled=False, visible=True)


def programme_principal() -> None:
    """Fonction principale du programme"""
    
    def nouvelle_partie() -> None:
        fenetre[BOUTON_ACTION].update(disabled=False, visible=True)
        fenetre[IMAGE_BOUTON_INACTIF].update(visible=False)
        temps_restant = difficulte_choisie.temps
        fenetre[TEMPS].update(str(temps_restant))
        fenetre.un_hide()
        questions = QUESTIONS.choisir_questions(difficulte_choisie.nombre_questions)
        prochaine_question = 0

    def fin_partie(est_un_echec: bool) -> None:
        decompte_actif = False
        fenetre.hide()
        effacer_question(fenetre)
        for i in range(difficulte_choisie.nombre_questions):
            fenetre[f'{INDICATEUR}-{i}'].update(data=IMAGES.indicateur_vide_base64())
            
            if not est_un_echec:
                questions[i][1] = Indicateur.VIDE

        musique_questions_controles.stop()
        
        if est_un_echec:
            SON_FIN_PARTIE.play()
            splasher_echec()
        else:
            SON_VICTOIRE.play()
            splasher_succes()

    def commencer() -> None:

        fenetre[BOUTON_ACTION].update(disabled=True, visible=False)
        fenetre[IMAGE_BOUTON_INACTIF].update(visible=True)
        afficher(fenetre, questions[prochaine_question][0])

    # indique qu'il sagit des variables globales
    global difficulte_choisie
    global musique_choisie

    # Changer le thème principal
    gui.theme('Black')

    # Afficher un écran de démarrage pour l'équipe
    splasher_equipe(1500)

    # Afficher un écran de démarrage pour le titre
    splasher_titre(2000, True)

    fenetre_menu = afficher_menu()
    menu_boucle = True

    while menu_boucle:
        event, values = fenetre_menu.read(timeout=10)

        match event:
            case 'BOUTON_COMMENCER':
                menu_boucle = False
                fenetre_menu.close()
                del fenetre_menu

            case 'BOUTON_QUITTER' | gui.WIN_CLOSED:
                return

            case 'COMBO_DIFFICULTE':
                difficulte_choisie = values[COMBO_DIFFICULTE]

            case 'COMBO_MUSIQUE':
                musique_choisie = values[COMBO_MUSIQUE]

    # la musique qui sera joué en fond
    musique_questions = sa.WaveObject.from_wave_file(musique_choisie.chemin_fichier)

    fenetre = fenetre_de_jeu()
    temps_restant = difficulte_choisie.temps
    prochaine_question = 0
    decompte_actif = False

    quitter = False
    # Tant qu'on ne quitte pas le jeu, fait cela
    while not quitter:
        event, valeurs = fenetre.read(timeout=10)

        # Si le décompte est actif, on diminue le temps restant et on met à jour le UI
        if decompte_actif:
            
            dernier_temps = temps_actuel
            temps_actuel = round(time.time())

            if dernier_temps != temps_actuel:
                temps_restant -= 1
                print(temps_restant)
                fenetre[TEMPS].update(str(temps_restant))

                # Si le temps est écoulé, affiche l'écran d'échec
                if temps_restant == 0:
                    
                    # arrete la partie
                    fin_partie(True)
                    
                    # On réaffiche le jeu de début
                    nouvelle_partie()

        # Si on clique sur le bouton pour commencer le jeu, on affiche les questions
        if event == BOUTON_ACTION:
            
            # set le temps
            temps_actuel = round(time.time())
            decompte_actif = True

            # Choisir 21 questions aléatoirement
            questions = QUESTIONS.choisir_questions(difficulte_choisie.nombre_questions)

            # commencer la partie
            commencer()

            # controleur de la musique qui joue
            musique_questions_controles = musique_questions.play()

        # Si on clique sur une des deux réponses (gauche ou droite)
        elif event == BOUTON_GAUCHE or event == BOUTON_DROIT:

            # Si le joueur a choisi la bonne réponse
            if (event == BOUTON_GAUCHE and fenetre[BOUTON_GAUCHE].get_text() != questions[prochaine_question][0][1]) or \
               (event == BOUTON_DROIT and fenetre[BOUTON_DROIT].get_text() != questions[prochaine_question][0][1]):
                
                fenetre[f'{INDICATEUR}-{prochaine_question}'].update(data=IMAGES.indicateur_vert_base64())
                questions[prochaine_question][1] = Indicateur.VERT
                prochaine_question += 1
                
                if prochaine_question < difficulte_choisie.nombre_questions:
                    afficher(fenetre, questions[prochaine_question][0])

                # quand le joueur gagne
                elif difficulte_choisie.nombre_questions <= prochaine_question:
                    fin_partie(False)
                    
                    prochaine_question = 0

                    # On réaffiche le jeu de début
                    nouvelle_partie()

            # Sinon, le joueur a choisi la mauvaise réponse
            else:
                decompte_actif = False
                effacer_question(fenetre)
                for i in range(prochaine_question):
                    fenetre[f'{INDICATEUR}-{i}'].update(
                        data=IMAGES.indicateur_jaune_base64())
                    questions[i][1] = Indicateur.JAUNE
                fenetre[f'{INDICATEUR}-{prochaine_question}'].update(
                    data=IMAGES.indicateur_rouge_base64())
                questions[prochaine_question][1] = Indicateur.ROUGE
                prochaine_question = 0
                fenetre[BOUTON_ACTION].update(disabled=False, visible=True)
                fenetre[IMAGE_BOUTON_INACTIF].update(visible=False)
                SON_ERREUR.play()
                musique_questions_controles.stop()

        # Si on ferme le jeu
        elif event == gui.WIN_CLOSED:
            decompte_actif = False
            quitter = True

    fenetre.close()
    del fenetre


programme_principal()