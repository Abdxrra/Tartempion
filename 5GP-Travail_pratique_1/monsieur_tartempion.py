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
# import simpleaudio as sa
import time
import sqlite3 as squirrel
import PySimpleGUI as gui

from images import *
from indicateurs import Indicateur

NOM_FICHIER_SON_VICTOIRE = '522243__dzedenz__result-10.wav'
NOM_FICHIER_SON_ERREUR = '409282__wertstahl__syserr1v1-in_thy_face_short.wav'
NOM_FICHIER_SON_FIN_PARTIE = '173859__jivatma07__j1game_over_mono.wav'
NOM_FICHIER_MUSIQUE_QUESTIONS = '550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav'

NB_QUESTIONS = 21

TEMPS_EPREUVE = 60

TITRE = 'TITRE'
TEMPS = 'TEMPS'
BOUTON_GAUCHE = 'BOUTON_GAUCHE'
OU = 'OU'
BOUTON_DROIT = 'BOUTON_DROIT'
QUESTION = 'QUESTION'
BOUTON_ACTION = 'BOUTON_ACTION'
IMAGE_BOUTON_INACTIF = 'IMAGE_BOUTON_INACTIF'
INDICATEUR = 'INDICATEUR'

police_titre = (gui.DEFAULT_FONT, 40, 'italic')
police_etiquettes = (gui.DEFAULT_FONT, 20, 'normal')
police_temps = (gui.DEFAULT_FONT, 50, 'normal')
police_question = (gui.DEFAULT_FONT, 30, 'normal')
police_reponses = (gui.DEFAULT_FONT, 20, 'normal')
police_ou = (gui.DEFAULT_FONT, 20, 'italic')


def splasher_equipe(temps_ms: int) -> None:
    gui.Window('Monsieur Tartempion', [[gui.Image(data=equipe_base64())]],
               # transparent_color=gui.theme_background_color(),
               no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)


def splacher_titre(delai: int, pardessus: bool) -> None:
    gui.Window('Monsieur Tartempion', [[gui.Image(data=titre_base64())]], no_titlebar=True, keep_on_top=pardessus).read(
        timeout=delai, close=True)


def afficher_jeu() -> gui.Window:
    title = [gui.Text('Monsieur Tartempion', key=TITRE, font=police_titre)]

    temps = [[gui.Text('Temps restant', font=police_etiquettes, size=70, justification='center')],
             [gui.Text(str(TEMPS_EPREUVE), key=TEMPS, font=police_temps)]]

    boutons_reponse = [gui.Column(
        [[gui.Button(key=BOUTON_GAUCHE, font=police_reponses, button_color=('white', gui.theme_background_color()),
                     border_width=0, disabled=True, visible=True),
          gui.Text(' ou ', key=OU, font=police_ou, text_color=gui.theme_background_color()),
          gui.Button(key=BOUTON_DROIT, font=police_reponses, button_color=('white', gui.theme_background_color()),
                     border_width=0, disabled=True, visible=True)]], element_justification='center')]

    question = [gui.Text(' ', key=QUESTION, font=police_question)]

    action = [gui.Button(image_data=bouton_jouer_base64(), key=BOUTON_ACTION, border_width=0,
                         button_color=(gui.theme_background_color(), gui.theme_background_color()), pad=(0, 10)),
              gui.Image(data=bouton_inactif_base64(), key=IMAGE_BOUTON_INACTIF, visible=False, pad=(0, 10))]

    indicateurs = [
        *[gui.Image(data=indicateur_vide_base64(), key=f'{INDICATEUR}-{i}', pad=(4, 10)) for i in range(NB_QUESTIONS)]]

    fenetre = gui.Window('Monsieur Tartempion', [temps, boutons_reponse, question, action, indicateurs],
                         keep_on_top=True, element_padding=(0, 0),
                         element_justification='center', resizable=False, finalize=True)

    return fenetre


def effacer_question_affichee(fenetre: gui.Window) -> None:
    fenetre[BOUTON_GAUCHE].update('', disabled=True, visible=True)
    fenetre[QUESTION].update("")
    fenetre[OU].update(text_color=gui.theme_background_color())
    fenetre[BOUTON_DROIT].update('', disabled=True, visible=True)


def charger_questions(fichier_db: str) -> list:
    connexion = squirrel.connect(fichier_db)

    with connexion:
        resultat_requete = connexion.execute('SELECT question, reponse_exacte, reponse_erronee FROM QUESTIONS')

    return [(enregistrement[0], enregistrement[1], enregistrement[2]) for enregistrement in resultat_requete]


def choisir_questions(banque: list, nombre: int) -> list:
    return [[question, Indicateur.VIDE] for question in random.choices(banque, k=nombre)]


def melanger_reponses(reponses: tuple) -> tuple:
    return (reponses[0], reponses[1]) if bool(random.getrandbits(1)) else (reponses[1], reponses[0])


def splasher_echec(temps_ms: int) -> None:
    gui.Window('Monsieur Tartempion', [[gui.Image(data=echec_base64())]],
               transparent_color=gui.theme_background_color(),
               no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)


def splasher_succes() -> None:
    gui.Window('Monsieur Tartempion', [[gui.Image(data=succes_base64())]], transparent_color="maroon2",
               no_titlebar=True, keep_on_top=True).read(timeout=3000, close=True)


def afficher(fenetre: gui.Window, question: tuple) -> None:
    fenetre[QUESTION].update(question[0])
    reponses = melanger_reponses((question[1], question[2]))
    fenetre[BOUTON_GAUCHE].update(reponses[0], disabled=False, visible=True)
    fenetre[OU].update(text_color='white')
    fenetre[BOUTON_DROIT].update(reponses[1], disabled=False, visible=True)


def effacer_question(fenetre: gui.Window) -> None:
    fenetre[QUESTION].update('')
    fenetre[BOUTON_GAUCHE].update('', disabled=True, visible=True)
    fenetre[OU].update(text_color=gui.theme_background_color())
    fenetre[BOUTON_DROIT].update('', disabled=True, visible=True)


def programme_principal() -> None:
    """Despote suprême de toutes les fonctions."""

    gui.theme('Black')

    # son_victoire = sa.WaveObject.from_wave_file(NOM_FICHIER_SON_VICTOIRE)
    # son_erreur = sa.WaveObject.from_wave_file(NOM_FICHIER_SON_ERREUR)
    # son_fin_partie = sa.WaveObject.from_wave_file(NOM_FICHIER_SON_FIN_PARTIE)
    # musique_questions = sa.WaveObject.from_wave_file(NOM_FICHIER_MUSIQUE_QUESTIONS)

    splasher_equipe(1500)
    splacher_titre(2000, True)

    toutes_les_questions = charger_questions("questions.bd")
    questions = choisir_questions(toutes_les_questions, NB_QUESTIONS)

    fenetre = afficher_jeu()
    temps_restant = TEMPS_EPREUVE
    prochaine_question = 0
    decompte_actif = False

    def nouvelle_partie() -> None:
        fenetre[BOUTON_ACTION].update(disabled=False, visible=True)
        fenetre[IMAGE_BOUTON_INACTIF].update(visible=False)
        temps_restant = TEMPS_EPREUVE
        fenetre[TEMPS].update(str(temps_restant))
        fenetre.un_hide()
        questions = choisir_questions(toutes_les_questions, NB_QUESTIONS)
        prochaine_question = 0

    quitter = False
    while not quitter:
        event, valeurs = fenetre.read(timeout=10)
        if decompte_actif:
            temps_actuel = round(time.time())
            dernier_temps = temps_actuel
            if dernier_temps != temps_actuel:
                temps_restant -= 1
                fenetre[TEMPS].update(str(temps_restant))
                if temps_restant == 0:
                    decompte_actif = False
                    fenetre.hide()
                    effacer_question(fenetre)
                    for i in range(NB_QUESTIONS):
                        fenetre[f'{INDICATEUR}-{i}'].update(data=indicateur_vide_base64())
                    # son_fin_partie.play()
                    # musique_questions_controles.stop()
                    splasher_echec(3000)
                    nouvelle_partie()
                    continue

        if event == BOUTON_ACTION:
            fenetre[BOUTON_ACTION].update(disabled=True, visible=False)
            fenetre[IMAGE_BOUTON_INACTIF].update(visible=True)
            temps_actuel = round(time.time())
            decompte_actif = True
            afficher(fenetre, questions[prochaine_question][0])
            # musique_questions_controles = musique_questions.play()
        elif event == BOUTON_GAUCHE or event == BOUTON_DROIT:
            if (event == BOUTON_GAUCHE and fenetre[BOUTON_GAUCHE].get_text() != questions[prochaine_question][0][1]) or \
                    (event == BOUTON_DROIT and fenetre[BOUTON_DROIT].get_text() != questions[prochaine_question][0][1]):
                # le joueur a choisi la mauvaise réponse
                fenetre[f'{INDICATEUR}-{prochaine_question}'].update(data=indicateur_vert_base64())
                questions[prochaine_question][1] = Indicateur.VERT
                prochaine_question += 1
                if prochaine_question < NB_QUESTIONS:
                    afficher(fenetre, questions[prochaine_question][0])
                elif NB_QUESTIONS <= prochaine_question:
                    decompte_actif = False
                    fenetre.hide()
                    effacer_question_affichee(fenetre)
                    for i in range(NB_QUESTIONS):
                        fenetre[f'{INDICATEUR}-{i}'].update(data=indicateur_vide_base64())
                        questions[i][1] = Indicateur.VIDE
                    # musique_questions_controles.stop()
                    # son_victoire.play()
                    splasher_succes()
                    nouvelle_partie()
                    continue
            else:
                # le joueur a choisi la bonne réponse
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
                # son_erreur.play()
                # musique_questions_controles.stop()
        elif event == gui.WIN_CLOSED:
            decompte_actif = False
            quitter = True

    fenetre.close()
    del fenetre


programme_principal()
