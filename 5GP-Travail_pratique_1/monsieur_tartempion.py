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
import pickle

from images import *
from indicateurs import Indicateur
from difficulte import Difficulte
from musique import Musique

DIFFICULTE = [
    Difficulte("SUPER FACILE", 10, 60),
    Difficulte("FACILE", 15, 60),
    Difficulte("MOYEN", 21, 60),
    Difficulte("DIFFICILE", 30, 60),
    Difficulte("TRÈS DIFFICILE", 30, 45)
]

MUSIQUES = [
    Musique("Basique", '550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav'),
    Musique("Kahoot", 'kahoot.wav'),
    Musique("Mario", 'mario.wav')
]

TITRE = "Monsieur Tartempion"
difficulte_choisie = DIFFICULTE[2]
musique_choisie = MUSIQUES[0]


#musique_actuelle

police_title = (gui.DEFAULT_FONT, 40, 'italic')
police_etiquettes = (gui.DEFAULT_FONT, 20, 'normal')
police_temps = (gui.DEFAULT_FONT, 50, 'normal')
police_question = (gui.DEFAULT_FONT, 30, 'normal')
police_reponses = (gui.DEFAULT_FONT, 20, 'normal')
police_ou = (gui.DEFAULT_FONT, 20, 'italic')

# fonctionnalité à ajouter
def afficher_menu() -> None:
    """Afficher le menu"""

    difficulte_selection = gui.Combo(DIFFICULTE, DIFFICULTE[2], font=police_reponses, enable_events=True,  readonly=True, key='COMBO_DIFFICULTE')

    musique_selection = gui.Combo(MUSIQUES, musique_choisie, font=police_reponses,  enable_events=True,  readonly=True, key='COMBO_MUSIQUE')

    commencer = gui.Button("COMMENCER", key='BOUTON-COMMENCER', font=police_reponses, button_color=('white', gui.theme_background_color()), border_width=0)
    quitter = gui.Button("QUITTER", key='BOUTON-QUITTER', font=police_reponses, button_color=('white', gui.theme_background_color()), border_width=0)
    
    design = [
            [
                [gui.Text("DIFFICULTÉ", font=police_reponses, pad=(10, 0)), difficulte_selection, gui.VPush()],
                [gui.Text("MUSIQUE", font=police_reponses, pad=(10, 0)), musique_selection, gui.VPush()],
                [commencer, gui.VPush()],
                [quitter, gui.VPush()]
            ]
    ]

    fenetre = gui.Window(TITRE, design, keep_on_top=True, element_padding=(0, 0),
                        element_justification='center', resizable=False, finalize=True, size=(500, 280))

    return fenetre


def splasher_equipe(temps_ms: int) -> None:
    """Afficher le logo de l'équipe"""

    gui.Window(TITRE, [[gui.Image(data=equipe_base64(), subsample=2)]], no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)


def splacher_titre(delai: int, pardessus: bool) -> None:
    """Afficher le logo du jeu"""

    gui.Window(TITRE, [[gui.Image(data=titre_base64())]], no_titlebar=True, keep_on_top=pardessus).read(timeout=delai, close=True)


def afficher_jeu() -> gui.Window:
    """Afficher l'interface du jeu"""

    title = [gui.Text(TITRE, key='TITLE', font=police_title)]

    temps = [[gui.Text('Temps restant', font=police_etiquettes, size=70, justification='center')], [gui.Text(str(difficulte_choisie.temps), key='TEMPS', font=police_temps)]]

    boutons_reponse = [gui.Column([[gui.Button(key='BOUTON-GAUCHE', font=police_reponses, button_color=('white', gui.theme_background_color()),
                   border_width=0, disabled=True, visible=True),
        gui.Text(' ou ', key='OU', font=police_ou, text_color=gui.theme_background_color()),
        gui.Button(key='BOUTON-DROIT', font=police_reponses, button_color=('white', gui.theme_background_color()),
                   border_width=0, disabled=True, visible=True)]], element_justification='center')]

    question = [gui.Text(' ', key='QUESTION', font=police_question)]

    action = [gui.Button(image_data=bouton_jouer_base64(), key='BOUTON-ACTION', border_width=0, button_color=(gui.theme_background_color(), gui.theme_background_color()), pad=(0, 10)),
              gui.Image(data=bouton_inactif_base64(), key='IMAGE-BOUTON-INACTIF', visible=False, pad=(0, 10))]

    indicateurs = [*[gui.Image(data=indicateur_vide_base64(), key=f'INDICATEUR-{i}', pad=(4, 10)) for i in range(difficulte_choisie.nombre_questions)]]

    fenetre = gui.Window(TITRE, [temps, boutons_reponse, question, action, indicateurs], keep_on_top=True, element_padding=(0, 0),
                        element_justification='center', resizable=False, finalize=True)

    return fenetre


def effacer_question_affichee(fenetre: gui.Window) -> None:
    """efface la question et désactive les boutons """

    fenetre['BOUTON-GAUCHE'].update('', disabled=True, visible=True)
    fenetre['QUESTION'].update("")
    fenetre['OU'].update(text_color=gui.theme_background_color())
    fenetre['BOUTON-DROIT'].update('', disabled=True, visible=True)


def charger_questions(fichier_db: str) -> list:
    """charge les question depuis le fichier BD"""

    connexion = squirrel.connect(fichier_db)

    with connexion:
        resultat_requete = connexion.execute('SELECT question, reponse_exacte, reponse_erronee FROM QUESTIONS')
    
    questions = [(enregistrement[0], enregistrement[1], enregistrement[2]) for enregistrement in resultat_requete]
    
    connexion.close()

    return questions


def choisir_questions(banque: list, nombre: int) -> list:
    """choisi une question random depuis la liste des questions"""

    return [[question, Indicateur.VIDE] for question in random.choices(banque, k=nombre)]


def melanger_reponses(reponses: tuple) -> tuple:
    """mélange le choix des réponses"""

    return (reponses[0], reponses[1]) if bool(random.getrandbits(1)) else (reponses[1], reponses[0])


def splasher_echec(temps_ms: int) -> None:
    """afficher quand le joueur perd"""

    gui.Window(TITRE, [[gui.Image(data=echec_base64())]], transparent_color=gui.theme_background_color(),
               no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)


def splasher_succes() -> None:
    """afficher quand le joueur gagne"""

    gui.Window(TITRE, [[gui.Image(data=succes_base64())]], transparent_color="maroon2",
               no_titlebar=True, keep_on_top=True).read(timeout=3000, close=True)


def afficher(fenetre: gui.Window, question: tuple) -> None:
    """afficher la question"""

    fenetre['QUESTION'].update(question[0])
    reponses = melanger_reponses((question[1], question[2]))
    fenetre['BOUTON-GAUCHE'].update(reponses[0], disabled=False, visible=True)
    fenetre['OU'].update(text_color='white')
    fenetre['BOUTON-DROIT'].update(reponses[1], disabled=False, visible=True)


def effacer_question(fenetre: gui.Window) -> None:
    """enlever la question de l'écran"""
    
    fenetre['QUESTION'].update('')
    fenetre['BOUTON-GAUCHE'].update('', disabled=True, visible=True)
    fenetre['OU'].update(text_color=gui.theme_background_color())
    fenetre['BOUTON-DROIT'].update('', disabled=True, visible=True)


def programme_principal() -> None:
    """Despote suprême de toutes les fonctions."""
    global difficulte_choisie
    global musique_choisie

    gui.theme('Black')

    son_victoire = sa.WaveObject.from_wave_file('522243__dzedenz__result-10.wav')
    son_erreur = sa.WaveObject.from_wave_file('409282__wertstahl__syserr1v1-in_thy_face_short.wav')
    son_fin_partie = sa.WaveObject.from_wave_file('173859__jivatma07__j1game_over_mono.wav')

    #splasher_equipe(1500)
    #splacher_titre(2000, True)

    toutes_les_questions = charger_questions("questions.bd")
    questions = choisir_questions(toutes_les_questions, 21)

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
    musique_questions = sa.WaveObject.from_wave_file(musique_choisie.chemin_fichier)

    fenetre = afficher_jeu()
    temps_restant = difficulte_choisie.temps
    prochaine_question = 0
    decompte_actif = False

    quitter = False
    while not quitter:
        event = fenetre.read(timeout=10)[0]
        if decompte_actif:
            dernier_temps = temps_actuel
            temps_actuel = round(time.time())
            if dernier_temps != temps_actuel:
                temps_restant -= 1
                fenetre['TEMPS'].update(str(temps_restant))
                if temps_restant == 0:
                    decompte_actif = False
                    fenetre.hide()
                    effacer_question(fenetre)
                    for i in range(difficulte_choisie.nombre_questions):
                        fenetre[f'INDICATEUR-{i}'].update(data=indicateur_vide_base64())
                    son_fin_partie.play()
                    musique_questions_controles.stop()
                    splasher_echec(3000)
 
                    fenetre['BOUTON-ACTION'].update(disabled=False, visible=True)
                    fenetre['IMAGE-BOUTON-INACTIF'].update(visible=False)
                    temps_restant = difficulte_choisie.temps
                    fenetre['TEMPS'].update(str(temps_restant))
                    fenetre.un_hide()
                    questions = choisir_questions(toutes_les_questions, difficulte_choisie.nombre_questions)
                    prochaine_question = 0
                    continue

        if event == 'BOUTON-ACTION':
            fenetre['BOUTON-ACTION'].update(disabled=True, visible=False)
            fenetre['IMAGE-BOUTON-INACTIF'].update(visible=True)
            temps_actuel = round(time.time())
            decompte_actif = True
            afficher(fenetre, questions[prochaine_question][0])
            musique_questions_controles = musique_questions.play()
        elif event == 'BOUTON-GAUCHE' or event == 'BOUTON-DROIT':
            if (event == 'BOUTON-GAUCHE' and fenetre['BOUTON-GAUCHE'].get_text() != questions[prochaine_question][0][1]) or \
               (event == 'BOUTON-DROIT' and fenetre['BOUTON-DROIT'].get_text() != questions[prochaine_question][0][1]):
                # le joueur a choisi la mauvaise réponse
                fenetre[f'INDICATEUR-{prochaine_question}'].update(data=indicateur_vert_base64())
                questions[prochaine_question][1] = Indicateur.VERT
                prochaine_question += 1
                if prochaine_question < difficulte_choisie.nombre_questions:
                    afficher(fenetre, questions[prochaine_question][0])

                # quand le joueur gagne
                elif difficulte_choisie.nombre_questions <= prochaine_question:
                    decompte_actif = False
                    fenetre.hide()
                    effacer_question_affichee(fenetre)
                    print("test ben")
                    for i in range(difficulte_choisie.nombre_questions):
                        fenetre[f'INDICATEUR-{i}'].update(data=indicateur_vide_base64())
                        questions[i][1] = Indicateur.VIDE
                    musique_questions_controles.stop()
                    son_victoire.play()
                    splasher_succes()
                    fenetre['BOUTON-ACTION'].update(disabled=False, visible=True)
                    fenetre['IMAGE-BOUTON-INACTIF'].update(visible=False)
                    temps_restant = difficulte_choisie.temps
                    fenetre['TEMPS'].update(str(temps_restant))
                    fenetre.un_hide()
                    questions = choisir_questions(toutes_les_questions, difficulte_choisie.nombre_questions)
                    prochaine_question = 0
                    continue
            else:
                # le joueur a choisi la bonne réponse
                decompte_actif = False
                effacer_question(fenetre)
                for i in range(prochaine_question):
                    fenetre[f'INDICATEUR-{i}'].update(data=indicateur_jaune_base64())
                    questions[i][1] = Indicateur.JAUNE
                fenetre[f'INDICATEUR-{prochaine_question}'].update(data=indicateur_rouge_base64())
                questions[prochaine_question][1] = Indicateur.ROUGE
                prochaine_question = 0
                fenetre['BOUTON-ACTION'].update(disabled=False, visible=True)
                fenetre['IMAGE-BOUTON-INACTIF'].update(visible=False)
                son_erreur.play()
                musique_questions_controles.stop()
        elif event == gui.WIN_CLOSED:
            decompte_actif = False
            quitter = True

    fenetre.close()
    del fenetre


programme_principal()