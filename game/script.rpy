# =========================================================
# DÉCLARATIONS
# =========================================================

define r = Character("Ren", color="#c8ffc8", what_prefix="“", what_suffix="”")
define n = Character("Narrateur")

# Sprites
image r happy = "images/ren_happy.png"
image r tel = "images/ren_tel.png"
image r savon = "images/ren_savon.png"

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

transform ren_left:
    xalign 0.0
    yalign 1.0
    zoom 2.5


# =========================================================
# START
# =========================================================

label start:

    scene bg black
    with fade

    $ renpy.movie_cutscene("videos/introduction_long.webm")

    play music "musics/mii.mp3" fadein 1.0

    scene bg bedroom
    show r happy at ren_left

    n "7h43."
    n "Ton réveil n’a pas sonné."
    n "Enfin si."
    n "Mais tu l’as éteint avec la précision d’un ninja endormi."
    n "Ton téléphone vibre."
    n "3 notifications."
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
    show r savon at ren_left

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
    show r happy at ren_left

    n "8h50."
    n "Personne étrange devant chez toi."
    n "Regard de SDF."
    n "Tu ignores."

    jump arrive_travail_blessure


# =========================================================
# SCÈNE 1C — TÉLÉPHONE
# =========================================================

label scene_1c:

    show r tel at ren_left

    n "Une vidéo."
    n "Puis une autre."
    n "Puis 8h35."
    n "Ton cerveau : “Ça va passer.”"
    n "La réalité : “Non.”"

    menu:
        "Te lever en panique (risqué)":
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
    show r savon at ren_left

    n "Tu prends une douche."
    n "Bruit étrange."
    n "Tu ignores."

    n "La porte s’ouvre."
    n "Un homme cagoulé et armé entre."
    n "Tu glisses."
    n "Trop tard."

    scene bg black
    centered "{size=60}{color=#ff0000}DEAD{/color}{/size}"

    return


# =========================================================
# B2 — ASSUMER RETARD
# =========================================================

label scene_b2:

    n "Pas de douche."
    n "Croissant stratégique."

    scene bg hallway
    show r happy at ren_left

    n "8h55."
    n "Personne étrange dans le couloir."
    n "Tu ignores."

    jump arrive_travail_normal


# =========================================================
# B1 — PANIQUE
# =========================================================

label scene_b1:

    n "Tu t’habilles avec n’importe quoi."
    n "Tu files dehors."

    scene bg reception
    show r happy at ren_left

    n "Tu arrives au travail."
    n "La réceptionniste fronce les sourcils."
    n "« On n’emploie pas des SDFs ici. »"

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
    show r happy at ren_left

    n "Tu arrives à la réception."
    n "Une réceptionniste te fait un clin d’œil."

    jump bureau_normal


# =========================================================
# ARRIVÉE AVEC BLESSURE
# =========================================================

label arrive_travail_blessure:

    scene bg reception
    show r happy at ren_left

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
    show r happy at ren_left

    n "Tâches monotones."
    n "Vue par la fenêtre."

    # Fond noir pour que rien ne cache la vidéo
    scene black
    with fade

    # --- Lecture de la vidéo plein écran ---
    $ renpy.movie_cutscene("videos/patron_tombe.webm")  
    # Ren’Py attend la fin de la vidéo automatiquement
    
    scene bg office
    show r happy at ren_left

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
    show r happy at ren_left

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
    show r happy at ren_left

    n "Tu marches vers les toilettes."

    scene bg toilet
    show r happy at ren_left

    n "Tu entends des cris."
    n "La porte s’ouvre violemment."
    n "Un homme parle au téléphone."

    menu:
        "Sortir (risqué)":
            jump mort_vaporise
            scene bg hallway_toilet
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

    centered "{size=60}{color=#ff0000}DEAD{/color}{/size}"

    return


label survie_toilette:

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
    show r happy at ren_left

    n "Tu vas te rafraîchir."

    scene bg toilet
    show r happy at ren_left

    n "Petit nettoyage express."

    jump bureau_normal