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

import random, sys
import simpleaudio as sa
import time
import sqlite3 as squirrel
import PySimpleGUI as gui
import hashlib


from modules.images import Images
from modules.indicateurs import Indicateur
from modules.difficulte import Difficulte
from modules.musique import Musique

DIFFICULTE = [
    Difficulte("SUPER FACILE", 10, 60),
    Difficulte("FACILE", 15, 60),
    Difficulte("MOYEN", 21, 60),
    Difficulte("DIFFICILE", 30, 60),
    Difficulte("TRÈS DIFFICILE", 30, 45)
]

MUSIQUES = [
    Musique("Basique", 'audios/musiques/550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav'),
    Musique("Kahoot", 'audios/musiques/kahoot.wav'),
    Musique("Mario", 'audios/musiques/mario.wav')
]

IMAGES = Images()

TITRE = "Monsieur Tartempion"
difficulte_choisie = DIFFICULTE[2]
musique_choisie = MUSIQUES[0]


# Définir le nombre de questions
NB_QUESTIONS: int = 21

# Définir les styles de police pour différents éléments
police_titre: tuple = (gui.DEFAULT_FONT, 40, 'italic')
police_etiquettes: tuple = (gui.DEFAULT_FONT, 20, 'normal')
police_temps: tuple = (gui.DEFAULT_FONT, 50, 'normal')
police_question: tuple = (gui.DEFAULT_FONT, 30, 'normal')
police_reponses: tuple = (gui.DEFAULT_FONT, 20, 'normal')
police_ou: tuple = (gui.DEFAULT_FONT, 20, 'italic')

decompte_actif = False

decompte_actif = False


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


def splasher_equipe(temps_ms: int) -> None:
    gui.Window('Monsieur Tartempion', [[gui.Image(data=equipe_base64())]],
               no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)


def splasher_titre(delai: int, pardessus: bool) -> None:
    gui.Window('Monsieur Tartempion', [[gui.Image(data=titre_base64())]],
               no_titlebar=True, keep_on_top=pardessus).read(timeout=delai, close=True)

def fenetre_de_jeu() -> gui.Window:
    temps = [[gui.Text('Temps restant', font=police_etiquettes, size=70, justification='center')],
             [gui.Text('60', key='TEMPS', font=police_temps)]]

    boutons_reponse = [gui.Column([[gui.Button(key='BOUTON-GAUCHE', font=police_reponses,
                                    button_color=('white', gui.theme_background_color()),
                                    border_width=0, disabled=True, visible=True),
                                   gui.Text(' ou ', key='OU', font=police_ou, text_color=gui.theme_background_color()),
                                   gui.Button(key='BOUTON-DROIT', font=police_reponses,
                                    button_color=('white', gui.theme_background_color()),
                                    border_width=0, disabled=True, visible=True)]], element_justification='center')]

    question = [gui.Text(' ', key=QUESTION, font=police_question)]

    action = [gui.Button(image_data=bouton_jouer_base64(), key='BOUTON-ACTION',
              border_width=0, button_color=(gui.theme_background_color(), gui.theme_background_color()), pad=(0, 10)),
              gui.Image(data=bouton_inactif_base64(), key='IMAGE-BOUTON-INACTIF', visible=False, pad=(0, 10))]

    indicateurs = [*[gui.Image(data=indicateur_vide_base64(), key=f'INDICATEUR-{i}', pad=(4, 10)) for i in range(NB_QUESTIONS)]]

    # Construire la fenêtre avec tout les éléments
    fenetre = gui.Window('Monsieur Tartempion', [temps, boutons_reponse, question, action, indicateurs], keep_on_top=True,
                        element_padding=(0, 0), element_justification='center', resizable=False, finalize=True)

    return fenetre


def effacer_question_affichee(fenetre: gui.Window) -> None:
    fenetre['BOUTON-GAUCHE'].update('', disabled=True, visible=True)
    fenetre['QUESTION'].update("")
    fenetre['OU'].update(text_color=gui.theme_background_color())
    fenetre['BOUTON-DROIT'].update('', disabled=True, visible=True)


# Définition d'une fonction pour charger les questions à partir d'une base de données
def charger_questions(fichier_db: str) -> list:
    # Établir une connexion à la base de données
    connexion = squirrel.connect(fichier_db)

    # Exécuter une requête SQL pour obtenir les questions et réponses
    with connexion:
        resultat_requete = connexion.execute('SELECT question, reponse_exacte, reponse_erronee FROM QUESTIONS')

    # Retourner les enregistrements sous forme de liste
    return [(enregistrement[0], enregistrement[1], enregistrement[2]) for enregistrement in resultat_requete]

def choisir_questions(banque: list, nombre: int) -> list:
    """choisi un certain nombre de questions parmi une banque de questions"""

    return [[question, Indicateur.VIDE] for question in random.choices(banque, k=nombre)]

# Définition d'une fonction pour mélanger les réponses
def melanger_reponses(reponses: tuple) -> tuple:
    return (reponses[0], reponses[1]) if bool(random.getrandbits(1)) else (reponses[1], reponses[0])


def splasher_echec(temps_ms: int) -> None:
    gui.Window('Monsieur Tartempion', [[gui.Image(data=echec_base64())]],
               transparent_color=gui.theme_background_color(),
               no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)


def splasher_succes() -> None:
    gui.Window('Monsieur Tartempion', [[gui.Image(data=succes_base64())]],
               transparent_color="maroon2",
               no_titlebar=True, keep_on_top=True).read(timeout=3000, close=True)

# Définition d'une fonction pour afficher une question dans la fenêtre
def afficher(fenetre: gui.Window, question: tuple) -> None:
    fenetre['QUESTION'].update(question[0])
    reponses = melanger_reponses((question[1], question[2]))
    fenetre['BOUTON-GAUCHE'].update(reponses[0], disabled=False, visible=True)
    fenetre['OU'].update(text_color='white')
    fenetre['BOUTON-DROIT'].update(reponses[1], disabled=False, visible=True)

# Définition d'une fonction pour effacer la question affichée dans la fenêtre
def effacer_question(fenetre: gui.Window) -> None:
    fenetre['QUESTION'].update('')
    fenetre['BOUTON-GAUCHE'].update('', disabled=True, visible=True)
    fenetre['OU'].update(text_color=gui.theme_background_color())
    fenetre['BOUTON-DROIT'].update('', disabled=True, visible=True)

# Fonction principale du programme
def programme_principal() -> None:
    """Fonction principale du programme"""
    global difficulte_choisie
    global musique_choisie

    # Changer le thème principal
    gui.theme('Black')

    # Charger des fichiers audio pour les effets sonores
    son_victoire = sa.WaveObject.from_wave_file('audios/effet sonores/522243__dzedenz__result-10.wav')
    son_erreur = sa.WaveObject.from_wave_file('audios/effet sonores/409282__wertstahl__syserr1v1-in_thy_face_short.wav')
    son_fin_partie = sa.WaveObject.from_wave_file('audios/effet sonores/173859__jivatma07__j1game_over_mono.wav')

    # Afficher un écran de démarrage pour l'équipe
    splasher_equipe(1500)

    # Afficher un écran de démarrage pour le titre
    splasher_titre(2000, True)

    # Charger toutes les questions depuis la base de données
    toutes_les_questions = charger_questions("questions.bd")

    # Choisir 21 questions aléatoirement
    questions = choisir_questions(toutes_les_questions, 21)

    # Reponses avec un ordre melange
    reponses = melanger_reponses([(question[0][1], question[0][2]) for question in questions])

    fenetre_menu = afficher_menu()
    menu_boucle = True

    while menu_boucle:
        event, values = fenetre_menu.read(timeout=10)
        print(event)
        match event:
            case 'BOUTON-COMMENCER':
                menu_boucle = False
                fenetre_menu.close()
                del fenetre_menu

            case 'BOUTON-QUITTER' | gui.WIN_CLOSED:
                return

            case 'COMBO_DIFFICULTE':
                difficulte_choisie = values['COMBO_DIFFICULTE']

            case 'COMBO_MUSIQUE':
                musique_choisie = values['COMBO_MUSIQUE']

    # met la musique ici pour actualiser
    musique_questions = sa.WaveObject.from_wave_file(
        musique_choisie.chemin_fichier)

    fenetre = fenetre_de_jeu()

    temps_restant = 3
    prochaine_question = 0
    decompte_actif = False
    quitter = False

    # position de la question echouee lors de la meilleure tentative
    position_meilleure_tentative = 0

    def nouvelle_partie() -> None:
        fenetre[BOUTON_ACTION].update(disabled=False, visible=True)
        fenetre[IMAGE_BOUTON_INACTIF].update(visible=False)

        nonlocal temps_restant
        temps_restant = TEMPS_EPREUVE

        fenetre[TEMPS].update(str(temps_restant))
        fenetre.un_hide()

        nonlocal questions
        questions = choisir_questions(toutes_les_questions, NB_QUESTIONS)

        nonlocal reponses
        reponses = melanger_reponses([(question[0][1], question[0][2]) for question in questions])

        nonlocal prochaine_question
        prochaine_question = 0

        nonlocal position_meilleure_tentative
        position_meilleure_tentative = 0

    # Tant qu'on ne quitte pas le jeu, fait cela
    while not quitter:
        event, valeurs = fenetre.read(timeout=10)

        # Si le décompte est actif, on diminue le temps restant et on met à jour le UI
        if decompte_actif:
            dernier_temps = temps_actuel
            temps_actuel = round(time.time())

            if dernier_temps != temps_actuel:
                temps_restant -= 1
                fenetre['TEMPS'].update(str(temps_restant))
                
                # Si le temps est écoulé, affiche l'écran d'échec
                if temps_restant == 0:
                    decompte_actif = False
                    fenetre.hide()
                    effacer_question(fenetre)
                    for i in range(NB_QUESTIONS):
                        fenetre[f'INDICATEUR-{i}'].update(data=indicateur_vide_base64())
                    musique_questions_controles.stop()
                    son_fin_partie.play()

                    splasher_echec(3000)

                    # On réaffiche le jeu de début
                    fenetre['BOUTON-ACTION'].update(disabled=False, visible=True)
                    fenetre['IMAGE-BOUTON-INACTIF'].update(visible=False)
                    temps_restant = 60
                    fenetre['TEMPS'].update(str(temps_restant))
                    fenetre.un_hide()
                    questions = choisir_questions(toutes_les_questions, NB_QUESTIONS)
                    prochaine_question = 0
        
        # Si on clique sur le bouton pour commencer le jeu, on affiche les questions
        if event == BOUTON_ACTION:
            fenetre[BOUTON_ACTION].update(disabled=True, visible=False)
            fenetre[IMAGE_BOUTON_INACTIF].update(visible=True)

            temps_actuel = round(time.time())
            decompte_actif = True

            afficher(fenetre, questions[prochaine_question][0], reponses[prochaine_question])
            musique_questions_controles = musique_questions.play()

        # Si on clique sur une des deux réponses (gauche ou droite)
        elif event == 'BOUTON-GAUCHE' or event == 'BOUTON-DROIT':
            
            # Si le joueur a choisi la bonne réponse
            if (event == 'BOUTON-GAUCHE' and fenetre['BOUTON-GAUCHE'].get_text() != questions[prochaine_question][0][1]) or \
               (event == 'BOUTON-DROIT' and fenetre['BOUTON-DROIT'].get_text() != questions[prochaine_question][0][1]):
                fenetre[f'INDICATEUR-{prochaine_question}'].update(data=indicateur_vert_base64())
                questions[prochaine_question][1] = Indicateur.VERT
                prochaine_question += 1
                if prochaine_question < NB_QUESTIONS:
                    afficher(fenetre, questions[prochaine_question][0])
                elif 21 <= prochaine_question:
                    decompte_actif = False
                    fenetre.hide()
                    effacer_question_affichee(fenetre)
                    for i in range(NB_QUESTIONS):
                        fenetre[f'INDICATEUR-{i}'].update(data=indicateur_vide_base64())
                        questions[i][1] = Indicateur.VIDE

                    musique_questions_controles.stop()
                    son_victoire.play()

                    splasher_succes()
                    fenetre['BOUTON-ACTION'].update(disabled=False, visible=True)
                    fenetre['IMAGE-BOUTON-INACTIF'].update(visible=False)
                    fenetre['TEMPS'].update(str(temps_restant))
                    fenetre.un_hide()
                    questions = choisir_questions(toutes_les_questions, NB_QUESTIONS)
                    prochaine_question = 0
                    
            # Sinon, le joueur a choisi la mauvaise réponse
            else:
                decompte_actif = False
                effacer_question(fenetre)

                for i in range(prochaine_question):
                    fenetre[f'INDICATEUR-{i}'].update(data=indicateur_jaune_base64())
                    questions[i][1] = Indicateur.JAUNE
                fenetre[f'INDICATEUR-{prochaine_question}'].update(data=indicateur_rouge_base64())
                questions[prochaine_question][1] = Indicateur.ROUGE
                prochaine_question = 0
                fenetre[BOUTON_ACTION].update(disabled=False, visible=True)
                fenetre[IMAGE_BOUTON_INACTIF].update(visible=False)

                musique_questions_controles.stop()
        
        # Si on ferme le jeu
        elif event == gui.WIN_CLOSED:
            decompte_actif = False
            quitter = True

    fermer_programme(fenetre)



programme_principal()
