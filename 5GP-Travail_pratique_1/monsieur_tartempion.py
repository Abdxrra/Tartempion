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

from images import *
from indicateurs import Indicateur


# Définir le nombre de questions
NB_QUESTIONS: int = 21
NOM_FICHIER_SON_VICTOIRE = '522243__dzedenz__result-10.wav'
NOM_FICHIER_SON_ERREUR = '409282__wertstahl__syserr1v1-in_thy_face_short.wav'
NOM_FICHIER_SON_FIN_PARTIE = '173859__jivatma07__j1game_over_mono.wav'
NOM_FICHIER_MUSIQUE_QUESTIONS = '550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav'

NB_QUESTIONS = 21

TITRE = 'TITRE'
TEMPS = 'TEMPS'
BOUTON_GAUCHE = 'BOUTON_GAUCHE'
OU = 'OU'
BOUTON_DROIT = 'BOUTON_DROIT'
QUESTION = 'QUESTION'
BOUTON_ACTION = 'BOUTON_ACTION'
IMAGE_BOUTON_INACTIF = 'IMAGE_BOUTON_INACTIF'
INDICATEUR = 'INDICATEUR'

# Définir les styles de police pour différents éléments
police_titre: tuple = (gui.DEFAULT_FONT, 40, 'italic')
police_etiquettes: tuple = (gui.DEFAULT_FONT, 20, 'normal')
police_temps: tuple = (gui.DEFAULT_FONT, 50, 'normal')
police_question: tuple = (gui.DEFAULT_FONT, 30, 'normal')
police_reponses: tuple = (gui.DEFAULT_FONT, 20, 'normal')
police_ou: tuple = (gui.DEFAULT_FONT, 20, 'italic')

# Définir une fonction pour afficher un écran de démarrage pour l'équipe
def splasher_equipe(temps_ms: int) -> None:
    gui.Window('Monsieur Tartempion', [[gui.Image(data=equipe_base64())]],
               no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)

# Définir une fonction pour afficher un écran de démarrage pour le titre
def splasher_titre(delai: int, pardessus: bool) -> None:
    gui.Window('Monsieur Tartempion', [[gui.Image(data=titre_base64())]],
               no_titlebar=True, keep_on_top=pardessus).read(timeout=delai, close=True)

# Définir une fonction pour créer la fenêtre de jeu principale
def fenetre_de_jeu() -> gui.Window:
    title = [gui.Text('Monsieur Tartempion', key=TITRE, font=police_titre)]

    temps = [[gui.Text('Temps restant', font=police_etiquettes, size=70, justification='center')],
             [gui.Text('60', key=TEMPS, font=police_temps)]]

    boutons_reponse = [gui.Column([[gui.Button(key=BOUTON_GAUCHE, font=police_reponses,
                                    button_color=('white', gui.theme_background_color()),
                                    border_width=0, disabled=True, visible=True),
                                   gui.Text(' ou ', key=OU, font=police_ou, text_color=gui.theme_background_color()),
                                   gui.Button(key=BOUTON_DROIT, font=police_reponses,
                                    button_color=('white', gui.theme_background_color()),
                                    border_width=0, disabled=True, visible=True)]], element_justification='center')]

    question = [gui.Text(' ', key=QUESTION, font=police_question)]

    action = [gui.Button(image_data=bouton_jouer_base64(), key=BOUTON_ACTION,
              border_width=0, button_color=(gui.theme_background_color(), gui.theme_background_color()), pad=(0, 10)),
              gui.Image(data=bouton_inactif_base64(), key=IMAGE_BOUTON_INACTIF, visible=False, pad=(0, 10))]

    indicateurs = [*[gui.Image(data=indicateur_vide_base64(), key=f'{INDICATEUR}-{i}', pad=(4, 10)) for i in range(NB_QUESTIONS)]]

    # Construire la fenêtre avec tout les éléments
    fenetre = gui.Window('Monsieur Tartempion', [temps, boutons_reponse, question, action, indicateurs], keep_on_top=True,
                        element_padding=(0, 0), element_justification='center', resizable=False, finalize=True)

    return fenetre

# Définir une fonction pour effacer la question affichée
def effacer_question_affichee(fenetre: gui.Window) -> None:
    fenetre[BOUTON_GAUCHE].update('', disabled=True, visible=True)
    fenetre[QUESTION].update("")
    fenetre[OU].update(text_color=gui.theme_background_color())
    fenetre[BOUTON_DROIT].update('', disabled=True, visible=True)


# Définition d'une fonction pour charger les questions à partir d'une base de données
def charger_questions(fichier_db: str) -> list:
    # Établir une connexion à la base de données
    connexion = squirrel.connect(fichier_db)

    # Exécuter une requête SQL pour obtenir les questions et réponses
    with connexion:
        resultat_requete = connexion.execute('SELECT question, reponse_exacte, reponse_erronee FROM QUESTIONS')

    # Retourner les enregistrements sous forme de liste
    return [(enregistrement[0], enregistrement[1], enregistrement[2]) for enregistrement in resultat_requete]

# Définition d'une fonction pour choisir un certain nombre de questions parmi une banque de questions
def choisir_questions(banque: list, nombre: int) -> list:
    return [[question, Indicateur.VIDE] for question in random.choices(banque, k=nombre)]

# Définition d'une fonction pour mélanger les réponses
def melanger_reponses(reponses: tuple) -> tuple:
    return (reponses[0], reponses[1]) if bool(random.getrandbits(1)) else (reponses[1], reponses[0])

# Définition d'une fonction pour afficher un écran d'échec
def splasher_echec(temps_ms: int) -> None:
    gui.Window('Monsieur Tartempion', [[gui.Image(data=echec_base64())]],
               transparent_color=gui.theme_background_color(),
               no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)

# Définition d'une fonction pour afficher un écran de succès
def splasher_succes() -> None:
    gui.Window('Monsieur Tartempion', [[gui.Image(data=succes_base64())]],
               transparent_color="maroon2",
               no_titlebar=True, keep_on_top=True).read(timeout=3000, close=True)

# Définition d'une fonction pour afficher une question dans la fenêtre
def afficher(fenetre: gui.Window, question: tuple) -> None:
    fenetre[QUESTION].update(question[0])
    reponses = melanger_reponses((question[1], question[2]))
    fenetre[BOUTON_GAUCHE].update(reponses[0], disabled=False, visible=True)
    fenetre[OU].update(text_color='white')
    fenetre[BOUTON_DROIT].update(reponses[1], disabled=False, visible=True)

# Définition d'une fonction pour effacer la question affichée dans la fenêtre
def effacer_question(fenetre: gui.Window) -> None:
    fenetre[QUESTION].update('')
    fenetre[BOUTON_GAUCHE].update('', disabled=True, visible=True)
    fenetre[OU].update(text_color=gui.theme_background_color())
    fenetre[BOUTON_DROIT].update('', disabled=True, visible=True)

# Fonction principale du programme
def programme_principal() -> None:

    # Changer le thème principal
    gui.theme('Black')

    # Charger des fichiers audio pour les effets sonores
    son_victoire = sa.WaveObject.from_wave_file('522243__dzedenz__result-10.wav')
    son_erreur = sa.WaveObject.from_wave_file('409282__wertstahl__syserr1v1-in_thy_face_short.wav')
    son_fin_partie = sa.WaveObject.from_wave_file('173859__jivatma07__j1game_over_mono.wav')
    musique_questions = sa.WaveObject.from_wave_file('550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav')

    # Afficher un écran de démarrage pour l'équipe
    splasher_equipe(1500)

    # Afficher un écran de démarrage pour le titre
    splasher_titre(2000, True)

    # Charger toutes les questions depuis la base de données
    toutes_les_questions = charger_questions("questions.bd")

    # Choisir 21 questions aléatoirement
    questions = choisir_questions(toutes_les_questions, 21)

    # Créer la fenêtre de jeu
    fenetre = fenetre_de_jeu()

    temps_restant = 3
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
                fenetre[TEMPS].update(str(temps_restant))

                # Si le temps est écoulé, affiche l'écran d'échec
                if temps_restant == 0:
                    decompte_actif = False
                    fenetre.hide()
                    effacer_question(fenetre)
                    for i in range(NB_QUESTIONS):
                        fenetre[f'{INDICATEUR}-{i}'].update(data=indicateur_vide_base64())
                    musique_questions_controles.stop()
                    son_fin_partie.play()
                    splasher_echec(3000)

                    # On réaffiche le jeu de début
                    fenetre[BOUTON_ACTION].update(disabled=False, visible=True)
                    fenetre[IMAGE_BOUTON_INACTIF].update(visible=False)
                    temps_restant = 60
                    fenetre[TEMPS].update(str(temps_restant))
                    fenetre.un_hide()
                    questions = choisir_questions(toutes_les_questions, NB_QUESTIONS)
                    prochaine_question = 0

        # Si on clique sur le bouton pour commencer le jeu, on affiche les questions
        if event == BOUTON_ACTION:
            fenetre[BOUTON_ACTION].update(disabled=True, visible=False)
            fenetre[IMAGE_BOUTON_INACTIF].update(visible=True)
            temps_actuel = round(time.time())
            decompte_actif = True
            afficher(fenetre, questions[prochaine_question][0])
            musique_questions_controles = musique_questions.play()

        # Si on clique sur une des deux réponses (gauche ou droite)
        elif event == BOUTON_GAUCHE or event == BOUTON_DROIT:

            # Si le joueur a choisi la bonne réponse
            if (event == BOUTON_GAUCHE and fenetre[BOUTON_GAUCHE].get_text() != questions[prochaine_question][0][1]) or \
               (event == BOUTON_DROIT and fenetre[BOUTON_DROIT].get_text() != questions[prochaine_question][0][1]):
                fenetre[f'{INDICATEUR}-{prochaine_question}'].update(data=indicateur_vert_base64())
                questions[prochaine_question][1] = Indicateur.VERT
                prochaine_question += 1
                if prochaine_question < NB_QUESTIONS:
                    afficher(fenetre, questions[prochaine_question][0])
                elif 21 <= prochaine_question:
                    decompte_actif = False
                    fenetre.hide()
                    effacer_question_affichee(fenetre)
                    for i in range(NB_QUESTIONS):
                        fenetre[f'{INDICATEUR}-{i}'].update(data=indicateur_vide_base64())
                        questions[i][1] = Indicateur.VIDE
                    musique_questions_controles.stop()
                    son_victoire.play()
                    splasher_succes()
                    fenetre[BOUTON_ACTION].update(disabled=False, visible=True)
                    fenetre[IMAGE_BOUTON_INACTIF].update(visible=False)
                    temps_restant = TEMPS_EPREUVE
                    fenetre[TEMPS].update(str(temps_restant))
                    fenetre.un_hide()
                    questions = choisir_questions(toutes_les_questions, NB_QUESTIONS)
                    prochaine_question = 0

            # Sinon, le joueur a choisi la mauvaise réponse
            else:
                decompte_actif = False
                effacer_question(fenetre)
                for i in range(prochaine_question):
                    fenetre[f'{INDICATEUR}-{i}'].update(data=indicateur_jaune_base64())
                    questions[i][1] = Indicateur.JAUNE
                fenetre[f'{INDICATEUR}-{prochaine_question}'].update(data=indicateur_rouge_base64())
                questions[prochaine_question][1] = Indicateur.ROUGE
                prochaine_question = 0
                fenetre[BOUTON_ACTION].update(disabled=False, visible=True)
                fenetre[IMAGE_BOUTON_INACTIF].update(visible=False)
                son_erreur.play()
                musique_questions_controles.stop()

        # Si on ferme le jeu
        elif event == gui.WIN_CLOSED:
            decompte_actif = False
            quitter = True

    fenetre.close()
    del fenetre


programme_principal()
