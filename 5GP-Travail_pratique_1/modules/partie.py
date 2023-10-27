class Partie:

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

    def __init__():
                
        self.difficulte = [
            Difficulte("SUPER FACILE", 10, 60),
            Difficulte("FACILE", 15, 60),
            Difficulte("MOYEN", 21, 60),
            Difficulte("DIFFICILE", 30, 60),
            Difficulte("TRÈS DIFFICILE", 30, 1)
        ]

        self.musiques = [
            Musique("Basique", 'audios/musiques/550764__erokia__msfxp9-187_5-synth-loop-bpm-100.wav'),
            Musique("Kahoot", 'audios/musiques/kahoot.wav'),
            Musique("Mario", 'audios/musiques/mario.wav')
        ]

        self.images = Images()
        self.questions = Questions()

        self.difficulte_choisie = DIFFICULTE[2]
        self.musique_choisie = MUSIQUES[0]

        self.temps_actuel = 0

        self.splasher_equipe()
        self.splasher_titre()

    def splasher_echec(temps_ms: int = 3000) -> None:
        """afficher un écran d'échec"""

        gui.Window(TITRE, [[gui.Image(data=IMAGES.echec_base64())]], transparent_color=gui.theme_background_color(),
                no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)

    def splasher_succes(temps_ms: int = 3000) -> None:
        """afficher quand le joueur gagne"""

        gui.Window(TITRE, [[gui.Image(data=IMAGES.succes_base64())]], transparent_color="maroon2",
                no_titlebar=True, keep_on_top=True).read(timeout=temps_ms, close=True)

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

    def melanger_reponses(reponses: list) -> list:
        """fonction pour mélanger les réponses"""

        reponses = list(reponses)
        random.shuffle(reponses)

        return reponses[::-1]
    
    def afficher(question: tuple) -> None:
        """afficher la question"""

        self.fenetre[QUESTION].update(question[0])
        reponses = melanger_reponses((question[1], question[2]))
        self.fenetre[BOUTON_GAUCHE].update(reponses[0], disabled=False, visible=True)
        self.fenetre[OU].update(text_color='white')
        self.fenetre[BOUTON_DROIT].update(reponses[1], disabled=False, visible=True)

    def effacer_question() -> None:
        """Effacer la question affichée dans la fenêtre"""

        self.fenetre[QUESTION].update('')
        self.fenetre[BOUTON_GAUCHE].update('', disabled=True, visible=True)
        self.fenetre[OU].update(text_color=gui.theme_background_color())
        self.fenetre[BOUTON_DROIT].update('', disabled=True, visible=True)
    
    def nouvelle_partie() -> None:
        """initialise une nouvelle partie"""

        self.fenetre[BOUTON_ACTION].update(disabled=False, visible=True)
        self.fenetre[IMAGE_BOUTON_INACTIF].update(visible=False)
        self.temps_restant = difficulte_choisie.temps
        self.fenetre[TEMPS].update(str(temps_restant))
        self.fenetre.un_hide()
        self.questions = QUESTIONS.choisir_questions(difficulte_choisie.nombre_questions)
        self.prochaine_question = 0

    def fin_partie(est_un_echec: bool) -> None:

        self.decompte_actif = False
        self.fenetre.hide()
        self.effacer_question(fenetre)
        for i in range(difficulte_choisie.nombre_questions):
            fenetre[f'{INDICATEUR}-{i}'].update(data=IMAGES.indicateur_vide_base64())
            
            if not est_un_echec:
                self.questions[i][1] = Indicateur.VIDE

        self.musique_questions_controles.stop()
        
        if est_un_echec:
            SON_FIN_PARTIE.play()
            splasher_echec()
        else:
            SON_VICTOIRE.play()
            splasher_succes()

    def commencer() -> None:
        """commencer la partie"""
        
        self.fenetre = fenetre_de_jeu()

        self.fenetre[BOUTON_ACTION].update(disabled=True, visible=False)
        self.fenetre[IMAGE_BOUTON_INACTIF].update(visible=True)
        self.afficher(questions[prochaine_question][0])
        
        # set le temps
        self.temps_actuel = round(time.time())
        decompte_actif = True

        # Choisir 21 questions aléatoirement
        questions = QUESTIONS.choisir_questions(difficulte_choisie.nombre_questions)

        # controleur de la musique qui joue
        self.musique_questions_controles = musique_questions.play()