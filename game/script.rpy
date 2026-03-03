# =========================================================
# DÉCLARATIONS
# =========================================================

define r = Character("Ren", color="#2a109c", what_prefix="“", what_suffix="”")
define t = Character("Réceptionniste", color="#fc00e7")
define j = Character("Jackson", color="#f707e3")
define m = Character("Homme aux toilette", color="#b94f08")
define h = Character("Hector", color="#ffffff")
define n = Character("Narrateur")

# Sprites
image r happy = "images/ren_legs.png"
image r tel = "images/ren_tel.png"
image r savon = "images/ren_savon.png"

image t normal = "images/receptionniste.png"

image j normal = "images/jackson.png"

image m normal = "images/toiletteman.png"

image h trash = "images/hector_w_trash.png"
image h normal = "images/hector_debout.png"
image h explose = "images/hector_explosion.png"

# Backgrounds
image bg bedroom = "images/bedroom.jpg"
image bg bathroom = "images/bathroom.jpg"
image bg hallway = "images/hallway.jpg"
image bg street = "images/street.png"
image bg office = "images/office.png"
image bg reception = "images/reception.png"
image bg toilet = "images/toillet.png"
image bg hallway_toilet = "images/toillet_hallway.png"
image bg black = Solid("#000")

image bg death = "images/death.jpg"

transform breathing:
    xalign 0.0
    yalign 1.0
    zoom 2.0
    linear 1.5 zoom 1.02
    linear 1.5 zoom 1.0
    repeat


transform left_unzoomed:
    xalign 0.0
    yalign 1.0
    zoom 2


transform right_zoomed:
    xalign 1.0
    yalign 1.0
    zoom 2.5

transform right_unzoomed:
    xalign 1.0
    yalign 1.0
    zoom 2

transform right_far:
    xalign 1.0
    yalign 0.5
    zoom 1

transform midright:
    xalign 0.7
    yalign 1.0
    zoom 2

label death_screen:
    stop music
    scene bg death
    with fade

    
    $ _rollback = False
    $ quick_menu = False

    play sound "audio/gui/death.mp3"

    pause 3.0


    show screen death_button

    pause


# =========================================================
# START
# =========================================================

label start:

    scene bg black
    with fade

    $ renpy.movie_cutscene("videos/introduction_long.webm")

    play music "musics/mii.mp3" fadein 1.0 volume 0.3

    scene bg bedroom
    with fade
    show r happy at left_unzoomed

    n "7h43."
    n "Ton réveil n’a pas sonné."
    n "Enfin si."
    n "Mais tu l’as éteint avec la précision d’un ninja endormi."
    n "Ton téléphone vibre."
    play sound "audio/object/notification.wav" volume 0.5
    n "3 notifications."
    play sound "audio/character/gargouillement.mp3"
    n "Ton estomac gargouille."
    n "Tu es en retard… quelque part."

    menu:
        "Te lever immédiatement":
            jump scene_1a
        "Rester au lit \"2 minutes\"":
            jump scene_1b
        "Regarder ton téléphone":
            jump scene_1c


# =========================================================
# SCÈNE 1A — MODE URGENCE
# =========================================================

label scene_1a:

    n "Tu te lèves d’un bond."
    n "Ton pied rencontre un LEGO."
    n "Douleur."
    n "Direction la salle de bain."


    scene bg bathroom
    with fade
    show r savon at left_unzoomed
    with moveinleft

    n "Douche rapide."
    n "Tu pars travailler."

    jump arrive_travail_normal


# =========================================================
# SCÈNE 1B — ENCORE 2 MINUTES
# =========================================================

label scene_1b:

    n "Encore « 2 minutes »."
    n "Tu te rendors."
    n "Tu te réveilles à 8h."
    n "Préparation express."

    scene bg street
    show r happy at left_unzoomed

    n "8h50."
    n "Personne étrange devant chez toi."
    show h trash at right_far
    with moveinright 

    n "Regard de SDF."
    n "Tu ignores."

    jump arrive_travail_blessure


# =========================================================
# SCÈNE 1C — TÉLÉPHONE
# =========================================================

label scene_1c:

    show r tel at left_unzoomed

    n "Une vidéo."
    play sound "audio/object/video.mp3" volume 0.3
    n "Puis une autre."
    n "Puis 8h35."
    n "Ton cerveau : “Ça va passer.”"
    n "La réalité : “Non.”"

    menu:
        "Te lever en panique (risqué)":
            n "Tu t’habilles avec n’importe quoi."
            n "Tu files dehors."
            jump scene_b1
        "Assumer le retard":
            jump scene_b2
        "Te doucher (risqué)":
            jump scene_b3


# =========================================================
# B3 — MORT DOUCHE
# =========================================================

label scene_b3:

    scene bg bathroom
    show r savon at left_unzoomed

    n "Tu prends une douche."

    play sound "audio/object/vitre.mp3"

    n "Bruit étrange."
    n "Tu ignores."

    n "La porte s’ouvre."

    play sound "audio/object/porte.mp3"

    show j normal at right_unzoomed
    with moveinright

    n "Un homme cagoulé et armé entre."

    play sound "audio/character/glissade.mp3"

    n "Tu glisses."
    n "Trop tard."
    
    jump death_screen

# =========================================================
# B2 — ASSUMER RETARD
# =========================================================

label scene_b2:

    n "Pas de douche."
    n "Croissant stratégique."

    scene bg hallway
    show r happy at left_unzoomed
    n "8h55."
    show h explose at right_unzoomed
    with moveinright
    n "Personne étrange dans le couloir."
    n "Il te lance regard de SDF"
    menu:
        "le regarder":
            h "T'habites ici ?"
            r "Oui pourquoi ?"
            h "Pour rien, je demandais juste..."
            jump scene_b1
        "Tu l'ignores":
            n "Tu ignores la personne."
            n "Il te regarde bizarrement."
            n "Tu continues ton chemin."
            n "Il te suit."
            n "Tu accélères le pas."
            n "Il accélère aussi."
            n "Tu te retournes."
            n "Il est juste derrière toi."
            n "il te lance une bombe dessus."

            # Fond noir pour que rien ne cache la vidéo
            scene black
            # --- Lecture de la vidéo plein écran ---
            $ renpy.movie_cutscene("videos/explosion.webm")  
            # Ren’Py attend la fin de la vidéo automatiquement

            jump death_screen





# =========================================================
# B1 — PANIQUE
# =========================================================

label scene_b1:

    scene bg reception
    show r happy at left_unzoomed
  
    

    n "Tu arrives au travail."
    show t normal at right_unzoomed
    with moveinright
    n "La réceptionniste fronce les sourcils."
    t "On n’emploie pas des SDFs ici. "

    menu:
        "Aller aux toilettes te soigner":
            jump toilette_apparence
        "Ignorer et aller au bureau":
            jump bureau_normal


# =========================================================
# ARRIVÉE TRAVAIL NORMAL
# =========================================================

label arrive_travail_normal:

    scene bg reception
    show r happy at left_unzoomed
    with moveinleft

    show t normal at right_unzoomed
    with moveinright
    

    n "Tu arrives à la réception."
    n "Une réceptionniste te fait un clin d’œil."

    jump bureau_normal


# =========================================================
# ARRIVÉE AVEC BLESSURE
# =========================================================

label arrive_travail_blessure:

    scene bg reception
    show r happy at left_unzoomed

    n "Tu glisses sur les marches."
    n "Ta cheville se tord."

    menu:
        "Rester au bureau":
            jump bureau_blessure
        "Aller aux toilettes (risqué)":
            jump toilette_risque


# =========================================================
# BUREAU NORMAL
# =========================================================

label bureau_normal:

    scene bg office
    show r happy at left_unzoomed

    n "Tâches monotones."
    n "Vue par la fenêtre."

    # Fond noir pour que rien ne cache la vidéo
    scene black
    with fade

    # --- Lecture de la vidéo plein écran ---
    $ renpy.movie_cutscene("videos/patron_tombe.webm")  
    # Ren’Py attend la fin de la vidéo automatiquement
    
    scene bg office
    show r happy at left_unzoomed

    n "Ton patron tombe avec sa chaise près de la vitre."
    n "Les collègues crient."
    n "Tu souris intérieurement."

    n "Tu quittes le bureau."

    return


# =========================================================
# BUREAU BLESSÉ
# =========================================================

label bureau_blessure:

    scene bg office
    show r happy at left_unzoomed

    n "Tu continues malgré la douleur."
    n "Existentialisme intensifié."

    n "Ton patron tombe encore."
    n "Tu quittes le travail."

    return


# =========================================================
# TOILETTES RISQUE
# =========================================================

label toilette_risque:

    scene bg hallway_toilet
    show r happy at left_unzoomed

    n "Tu marches vers les toilettes."

    scene bg toilet
    show r happy at left_unzoomed
    with moveinleft

    n "Tu entends des cris."
    n "La porte s’ouvre violemment."

    show m normal at right_unzoomed

    n "Un homme parle au téléphone."

    menu:
        "Sortir (risqué)":
            jump mort_vaporise
        "Rester caché":
            jump survie_toilette


label mort_vaporise:

    n "l'homme au téléphone te vaporise."

    # Fond noir pour que rien ne cache la vidéo
    scene black
    with fade

    # --- Lecture de la vidéo plein écran ---
    $ renpy.movie_cutscene("videos/vaporisated_ren.webm")  
    # Ren’Py attend la fin de la vidéo automatiquement

    jump death_screen



label survie_toilette:

    scene bg toilet
    show r happy at left_unzoomed
    show m normal at right_unzoomed

    n "Tu bloques la porte."
    n "Tu écoutes."
    n "Il parle d’argent."
    n "Il part."

    n "Tu quittes discrètement le bureau."

    return


# =========================================================
# TOILETTE APPARENCE
# =========================================================

label toilette_apparence:

    scene bg hallway_toilet
    show r happy at left_unzoomed

    n "Tu vas te rafraîchir."

    scene bg toilet
    show r happy at left_unzoomed

    n "Petit nettoyage express."

    jump bureau_normal