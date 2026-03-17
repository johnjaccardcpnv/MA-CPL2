# =========================================================
# DÉCLARATIONS
# =========================================================

define f = Character("Francesco (serveur)", color="#008C45", what_prefix="“", what_suffix="”")
define b = Character("Baboushka", color="#8b4513", what_prefix="“", what_suffix="”")
define r = Character("Ren", color="#2a109c", what_prefix="“", what_suffix="”")
define t = Character("Réceptionniste", color="#fc00e7", what_prefix="“", what_suffix="”")
define j = Character("Jackson", color="#f707e3", what_prefix="“", what_suffix="”")
define roberto = Character("Roberto", color="#c4b10c", what_prefix="“", what_suffix="”")
define m = Character("Homme aux toilette", color="#b94f08", what_prefix="“", what_suffix="”")
define h = Character("Hector", color="#ffffff")
define n = Character("Narrateur")
define rh = Character("Jennifer", color="#dd0a0a", what_prefix="“", what_suffix="”")

default qte_time = 3.0
default qte_key = renpy.random.choice(["K_SPACE", "2", "1"])

# Props
image drink = "images/drink.png"
image pizza = "images/pizza.png"

# Sprites
image r happy = "images/ren_legs.png"
image r tel = "images/ren_tel.png"
image r savon = "images/ren_savon.png"
image r gun = "images/ren_gun_nobg.png"

image t normal = "images/receptionniste.png"

image roberto normal = "images/roberto.png"

image j normal = "images/jackson.png"

image m normal = "images/toiletteman.png"

image f normal = "images/francesco.png"

image h trash = "images/hector_w_trash.png"
image h normal = "images/hector_debout.png"
image h explose = "images/hector_explosion.png"

image rh normal = "images/jennifer_pants.png"
image rh choc = "images/jennifer_choc.png"

image b happy = "images/baboushka.png"  

# Backgrounds
image bg bedroom = "images/bedroom.jpg"
image bg bathroom = "images/bathroom.jpg"
image bg hallway = "images/hallway.jpg"
image bg street = "images/street.png"
image bg office = "images/office.png"
image bg reception = "images/reception.png"
image bg toilet = "images/toillet.png"
image bg hallway_toilet = "images/toillet_hallway.png"
image bg bar = "images/bar.png"
image bg restaurant = "images/restaurant.jpg"
image bg outdoor_restaurant = "images/outdoor_restaurant.png"
image bg black = Solid("#000")
image bg gun_fight = "images/bg_combat.png"
image bg gun_fight_end = "images/bg_combat_end.png"
image bg left_street = "images/left_street.jpg"
image bg right_street = "images/right_street.png"
image bg right_far = "images/right_far.png"
image bg street_market = "images/street_market.png"

image bg jennifer_camion = "images/Jennifer-camion_video_bg.png"

 

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


# Écran de mort
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

    

# QTE bar
screen qte_bar():

    bar:
        value qte_time
        range 3.0
        xsize 400
        xpos 0.5
        ypos 0.6
        xanchor 0.5
    
    key qte_key.upper() action Return(True)

    text "Appuie sur [qte_key] !" xpos 0.5 ypos 0.55 xanchor 0.5

    timer 0.05 repeat True action [
        SetVariable("qte_time", qte_time - 0.05),
        Function(renpy.restart_interaction)
    ]

    key "K_SPACE" action Return(True)

    if qte_time <= 0:
        timer 0.01 action Return(False)


# =========================================================
# Le réveil
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
        "test":
            jump scene_6a_d4


# =========================================================
# Mode urgence
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

    jump scene_2a


# =========================================================
# Encore deux minutes 
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

    jump scene_2b


# =========================================================
# Le piège du téléphone 
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
            jump scene_3c_b1
        "Assumer le retard":
            jump scene_2c_b2
        "Te doucher (risqué)":
            jump scene_2c_b3


# =========================================================
# Te doucher (risqué) 
# =========================================================

label scene_2c_b3:

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
# Assumer le retard 
# =========================================================

label scene_2c_b2:

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
            jump scene_3c_b1
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
#  Te lever en panique (risqué) 
# =========================================================

label scene_3c_b1:

    scene bg reception
    show r happy at left_unzoomed
  
    

    n "Tu arrives au travail."
    show t normal at right_unzoomed
    with moveinright
    n "La réceptionniste fronce les sourcils."
    t "On n’emploie pas des SDFs ici. "

    menu:
        "Partir aux toilettes pour soigner ton apparence":
            n "Tu as compris que tu pues, donc tu vas aux toilettes pour te soigner."
            jump scene_4c_c1
        "Aller dans les bureaux":
            n "Tu te dis dans ta tête « Elle exagère celle-là » et tu vas direct au bureau."
            jump scene_4c_c2


# =========================================================
# Suite Mode urgence 
# =========================================================

label scene_2a:

    scene bg reception
    show r happy at left_unzoomed
    with moveinleft

    show t normal at right_unzoomed
    with moveinright
    

    n "Tu arrives à la réception."
    n "Une réceptionniste te fait un clin d’œil."

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

    jump scene_5


# =========================================================
# Encore deux minutes
# =========================================================

label scene_2b:

    scene bg reception
    show r happy at left_unzoomed

    n "Tu glisses sur les marches."
    n "Ta cheville se tord."

    menu:
        "Rester au bureau":
            jump scene_3b_c1
        "Aller aux toilettes (risqué)":
            jump scene_3b_c2


# =========================================================
# Aller au bureau 
# =========================================================

label scene_4c_c2:
    scene bg office
    show r happy at left_unzoomed

    n "Tu es au bureau à ton travail."  
    
    n "Tu complètes différentes tâches monotones, ennuyeuse et admire la vue."
    
    # Fond noir pour que rien ne cache la vidéo
    scene black
    with fade
    # --- Lecture de la vidéo plein écran ---
    $ renpy.movie_cutscene("videos/patron_tombe.webm")  
    # Ren’Py attend la fin de la vidéo automatiquement
    
    scene bg office
    show r happy at left_unzoomed
    
    n "Tu entends les cris de divers collègues et tu souris intérieurement."  
    n "Tu prends la décision de quitter au bureau à la suite du léger accident au travail."

    jump scene_5


# =========================================================
# Rester au bureau 
# =========================================================

label scene_3b_c1:

    scene bg office
    show r happy at left_unzoomed

    n "Tu continues malgré la douleur."
    n "Existentialisme intensifié."

    n "Ton patron tombe encore."
    n "Tu quittes le travail."

    jump scene_5


# =========================================================
# Allez aux toilettes (risqué) 
# =========================================================

label scene_3b_c2:

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
            jump scene_4b_d1
        "Rester caché":
            jump scene_4b_d2


# =========================================================
# Quitter ton cabinet (risqué) 
# =========================================================
label scene_4b_d1:

    n "l'homme au téléphone te vaporise."

    # Fond noir pour que rien ne cache la vidéo
    scene black
    with fade

    # --- Lecture de la vidéo plein écran ---
    $ renpy.movie_cutscene("videos/vaporisated_ren.webm")  
    # Ren’Py attend la fin de la vidéo automatiquement

    jump death_screen


# =========================================================
# Tu restes (parce que t’as peur d’être social) 
# =========================================================
label scene_4b_d2:

    scene bg toilet
    show r happy at left_unzoomed
    show m normal at right_unzoomed

    n "Tu bloques la porte."
    n "Tu écoutes."
    n "Il parle d’argent."
    n "Il part."

    n "Tu quittes discrètement le bureau."

    jump scene_5


# =========================================================
# Partir aux toilettes pour soigner ton apparence 
# =========================================================
label scene_4c_c1:


    scene bg office
    show r happy at left_unzoomed
    n "Tu es au bureau à ton travail."
 
    n "Tu complètes différentes tâches monotones, ennuyeuse et admire la vue."
    
    # Fond noir pour que rien ne cache la vidéo
    scene black
    with fade

    # --- Lecture de la vidéo plein écran ---
    $ renpy.movie_cutscene("videos/patron_tombe.webm")  
    # Ren’Py attend la fin de la vidéo automatiquement
    
    scene bg office
    show r happy at left_unzoomed
 

    n "Tu entends les cris de divers collègues et tu souris intérieurement."
 
    n "Tu prends la décision de quitter le bureau à la suite du léger accident au travail."  


    jump scene_5


# =========================================================
# Midi
# =========================================================
label scene_5:
    
    scene bg office
    show r happy at left_unzoomed
    n "Tu décides d’aller manger quelque part (parce que tu as faim…)."
    menu:
        "Aller à ton bar préféré":
            jump scene_6a_d1
        "Aller dans un restaurant italien":
            jump scene_6b_d2

# =========================================================
# Restaurant
# =========================================================
label scene_6b_d2:

    scene bg restaurant
    show r happy at left_unzoomed
    n "Tu décides (vue que tu as la dalle énorme) d’aller dans un très bon restaurant italien (alors que tu es Japon)."
    n "Ce restaurant a 4 Etoiles Michelin et ils servent des plats exceptionnels."
    n "Alors c’est décidé, tu vas dans ce restaurant car tu es BLINDééééééééééé !"
    n "On t’a apporté la carte des plats mais tu sais déjà quel prendre. Car sur la carte c’est ecrit, Pizza of the season."
    n "Alors tu commandes cette pizza. Et pour la boisson, tu demandes au restaurant, une suprise parmi la selection exclusive que le restaurant possède."
    n "5 min après..."
    n "Tu vois une énorme assiette."
    r "Ohhh j’ai hâte, ça l’air trop bon…"

    show f normal at right_unzoomed

    f "Votre pizza all-in-one exclusive pro-max plus pro limited edition est prête avec votre boisson surprise digne des dieux romains."
    n "Tu te baves par ce mot sublime que le serveur te dit."

    hide f

    n "Et là…"

    show drink at truecenter
    pause 3
    hide drink

    show pizza at truecenter
    pause 3
    hide pizza

    n "Etonnement (en fait tu es bizarre), tu kiffes ce que tu vois et entame ce festin."
    n "1 min après..."

    show f normal at right_unzoomed
    f "Alors Monsieur, tout se passe à merv……"
    n "Le serveur n’a pas le temps de finir sa phrase que tu as tout mangé et apprécie la fin de ta boisson (frérot tu es bizarre)."
    r "C’était délicieux, je veux bien l’addition svp"
    n "Le serveur émerveillé par ce qu’il a vu, part et te ramene l’addition. "

    hide f
    pause 1
    show f normal at right_unzoomed

    n "Et là ……     108230,40 Yen Japonais"
    n "Mais tellement que tu es blindax, tu poses ta petite carte American Express Platium Pro Max Worldwide Obama Certified Edition et bim ça valide le paiement."
    f "Merci beaucoup pour votre visite, bonne fin de journée et à bientôt"

    hide r
    hide f
    show r happy at truecenter
    show bg outdoor_restaurant

    n "Tu quittes ce restaurant avec un ventre rempli et un sourire qui pointe vers le ciel."
    n "Tu décides maintenant de prendre le chemin :"
    menu:
        "Droite":
            jump scene_6b_d3
        "Gauche":
            jump scene_6b_d4



# =========================================================
# Aller à ton bar préféré 
# =========================================================
label scene_6a_d1:
    scene bg office
    show r happy at left_unzoomed
    n "Tu décides d’aller à ton bar préféré. "

    scene bg bar
    show r happy at left_unzoomed
 
    r "J’ai besoin d’une bonne bière après ce que j’ai vu !"
    
    menu:
        "Boire avec modération (c’est un super type ce modération)":
            jump scene_6a_d3
        "Profiter…. (Modération absent) (risqué)":
            jump scene_6a_d4

# =========================================================
# Boire avec modération
# =========================================================
label scene_6a_d3:
    scene bg bar
    show r happy at left_unzoomed
    with moveinleft
    n "Tu passes un bon moment, tu sociabilises avec beaucoup de personnes (l’alcool ça aide…) et du coin de l’œil tu remarques une tête familière."
    n "Tu décides d’aller vers cette personne et surprise c’est ta RH, Jennifer."
    show rh normal at right_unzoomed
    with moveinright

    n "Comme tu as de l’alcool dans le sang, donc tu vas parler avec elle."

    r "J’en suis à un stade où la musique me regarde de travers."
    
    rh "Ok, t’es officiellement trop bourré pour ce bar."

    r "Mais parfaitement sobre pour ton canapé."
    
    rh "(Avec un sourire) J’ai du vin chez moi. Et zéro musique."

    r "C’est la meilleure phrase que j’ai entendu ce soir."

    rh "Viens avant que tu dises une connerie de plus."
    n "Tu discutes avec elle et après 2 chopes de bières (boire avec modération), vous sortez du bar et vous dirigez chez la RH."
    scene bg street
    with fade
    n "Vous marchez et rigolez"
    show r happy at left_unzoomed
    with moveinleft

    r "Il fait bizarrement froid d’un coup."
    show rh normal at right_unzoomed
    with moveinright
    rh "C’est toujours comme ça en sortant d’un bar."

    r "Ouais… ou quand on marche trop vite."

    rh "(Souris) T’es sûr que ça va ?"

    r "Oui."
    r "Enfin… j’ai juste beaucoup ri ce soir."

    rh "Moi aussi."
    rh "Ça fait du bien."
    n "(petit silence, ils continuent de marcher)"

    rh "On est presque arrivés."

    r "Ok." 
    n "Eh oui t’es bientôt chez elle. Mais vous devez traverser la route." 

    n "Vous apercevez deux voitures qui approchent à grande vitesse."

    hide r 
    hide rh
    hide bg street
    # --- Lecture de la vidéo plein écran ---
    $ renpy.movie_cutscene("videos/Jennifer-camion_debut.webm") 
    #video accident part 1
    scene bg jennifer_camion
    with fade
    n "Une des voitures se prend le poteau (le gros nul)."
    n "Le poteau se renvers."

    n "Esquivez vite le poteau !"

    $ qte_time = 3.0
    $ result = renpy.call_screen("qte_bar")

    if result:
        n "Bravo tu as réussi à esquiver le poteau mais, Jennifer n’a pas eu cette même chance"
    else:
        jump death_screen

    # S’il reussi à esquiver :

    n "Bravo tu as réussi à esquiver le poteau mais, Jennifer n’a pas eu cette même chance"

    hide bg jennifer_camion
    # --- Lecture de la vidéo plein écran ---
    $ renpy.movie_cutscene("videos/Jennifer-camion_fin.webm") 

    scene bg street
    with fade
    show r happy at left_unzoomed
    with moveinleft
    n "Jennifer à été slimed par les ops"

    n "Rempli de haine car ils ont ruiné ta date tu cours vers le camion militaire pour t’armer, et te venger sur les responsables de cet accident"

    n "Le conducteur du camion est mort sur impact mais ils a des armes dans le cabinet"

    menu:
        "Prendre le fusil d’assaut":
            jump scene_6a_d5
        "Prendre le lance-roquette":
            jump scene_6a_d6


# =========================================================
# Boire avec modération
# =========================================================
label scene_6a_d4:    
    scene bg bar
    show r happy at left_unzoomed
    with moveinleft
    n "Tu passes un bon moment, tu sociabilises avec beaucoup de personnes (l’alcool ça aide…) et du coin de l’œil tu remarques une tête familière."
    n "Tu décides d’aller vers cette personne et surprise c’est ta RH, Jennifer."
    n "Comme tu as trop d’alcool dans le sang (en même temps tu forces), donc tu vas parler avec elle."
    show rh normal at right_unzoomed
    with moveinright
    r "⍑ᔑᓭℸ ̣ ᒷ ᓭᓭᒷ ᓭᔑ⍊ᒷ ⎓ᔑ∷ᒲᔑ…"
    rh "…hein ?"
    r "⎓╎∷ᒷ ᔑᓭ! ᒲᔑᓭℸ ̣ ᒷ∷ ᒷリᓵ⍑ᔑリℸ ̣ !"
    rh "Tu te fous de ma—"
    r "ᒷ! ᒷ! ᓭ╎ꖎꖌ ℸ ̣ 𝙹⚍ᓵ⍑! "
    n "CLAQUE."
    hide rh
    r "…ᒷ⍊ᔑᓭ╎𝙹リ ꖎᒷ⍊ᒷꖎ 0."
    n "Là tu t’es pris un râteau de l’espace par Jennifer."
    n "Pour oublier cette scène, tu décides de rejoindre une soirée random"

    # Fond noir pour que rien ne cache la vidéo
    scene black
    with fade

    # --- Lecture de la vidéo plein écran ---
    $ renpy.movie_cutscene("videos/Project_X_with_REN.webm") 

        # --- Lecture de la vidéo plein écran ---
    $ renpy.movie_cutscene("videos/sensîbilisation.webm")   

    jump death_screen

# =========================================================
# Prendre le fusil d’assaut 
# =========================================================
label scene_6a_d5:
    scene bg street
    show r happy at left_unzoomed
    n "Tu décides de prendre cette belle SCAR-15 légendaire (référence à CS) et te tourne vers les malfaiteurs." 
    hide r 
    show r gun at left_unzoomed
    n "Tu leur donnes une « bonne leçon » "
    n "Les portières du véhicule claquent. Deux gars descendent, très confiants, très énervés."
    show roberto normal at right_far
    with moveinright
    show j normal at midright
    with moveinright
    roberto "Eh toi."
    roberto "On va te massacrer."
    j "Ouais. Lentement."
    n "Notre perso regarde la SCAR-15 dans ses mains, puis les regarde, puis re-regarde la SCAR-15."
    r "Non non."
    r "Alors ça… vraiment non."
    n "Les deux gars s’arrêtent."
    n "Il lève l’arme. Petit silence."
    j "Attends attends attends—"
    n "TROP TARD."
    hide roberto with dissolve
    hide j with dissolve
    hide r with dissolve
    # Bruit de tirs. Les deux gars disparaissent de l’écran
    show bg gun_fight
    
    play music "musics/gun_theme.mp3" fadein 1.0 volume 0.8
    pause 2.0

    $result = renpy.call_screen("shooter_minigame")


    if result == "win":
        pause 0.1    
        stop music fadeout 1.0
        $ renpy.movie_cutscene("videos/gun_fight.webm")
        play music "musics/mii.mp3" fadein 1.0 volume 0.3
        scene bg gun_fight_end
        show r happy at left_unzoomed
        n "Il regarde là où ils étaient, petit sourire."
        r "Hasta la vista…"
        r "les nulos."
    else:
        jump death_screen


# =========================================================
# Prendre le lance-roquette 
# =========================================================
label scene_6a_d6:
    hide r
    hide rh
    scene bg black
    with fade

    n "Tu décides de prendre ce beau RPG-7 pour montrer à ces malfaiteurs qui est le boss."
    stop music fadeout 1.0
    $ renpy.movie_cutscene("videos/explosion_rocket.webm")
    jump death_screen

# =========================================================
# rue de gauche
# =========================================================
label scene_6b_d4:
    scene bg left_street

    n "Tu décides de prendre le chemin à gauche (parce que tu entends de la bonne musique)."
    n "Tu marches dans cette direction et tu arrives à coté d’une immense house party de malade."
    n "Tu réfléchis est ce que tu t’incrustes dans cette fête mais tu n’as pas apercu le titan colossal qui va tomber sur toi."

    # --- Lecture de la vidéo plein écran ---
    $ renpy.movie_cutscene("videos/promenade_fete.webm")
    # Ren’Py attend la fin de la vidéo automatiquement

    jump death_screen



# =========================================================
# rue de droite
# =========================================================
label scene_6b_d3:
    scene bg right_street
    show r happy at left_unzoomed

    n "Tu décides d’aller à droite et tu tombes sur cette magnifique rue nommé Shinjuwan."
    n "Tu marches un petit moment et tu arrives dans cette street market vraiment sympa"

    hide bg right_street
    scene bg right_far

    n "Tu marches un petit moment et tu arrives dans cette street market vraiment sympa."

    hide r
    hide bg right_far
    scene bg street_market

    n "Et tu te retrouves devant un street market qui vend des fruits issue du Mont Fuji (mais version Temu)."
    n "Tu te fais accoster par la baboushka qui te demande : "

    show r happy at left_unzoomed
    show b happy at right_unzoomed

    b "Comment puis-je vous aider jeune monsieur ? "

    menu:
        "Refuser (mechant)":
            jump scene_6b_d5
        "Acheter un fruit (c’est bien les vitamines)"
            #jump scene_6b_d6
        "Acheter le tout (MrBeast challenge)"
            #jump scene_6b_d7


# =========================================================
# refus à la baboushka
# =========================================================
label scene_6b_d5:
    show r happy at left_unzoomed
    show b happy at right_unzoomed
    scene bg street_market

    n "La vieille baboushka te regarde avec un grand sourire."
    b "Comment puis-je vous aider jeune monsieur ?"
    r "Non merci… vos fruits ont l’air un peu… suspects."
    n "Le sourire disparaît."
    n "La baboushka se penche sous son stand."
    n "Elle sort un énorme couteau de cuisine."
    b "Tu veux goûter… ou partir ?"

    menu:
        "Fuir":
            jump scene_6b_d5_1
        "S'excuser":
            jump scene_6b_d5_2



# =========================================================
# refus à la baboushka fin 1
# =========================================================
#WIP
label scene_6b_d5_1:

    n "Tu tournes les talons et sprintes comme un dératé."
    r "VIE SAUVE !"
    n "Tu cours 10 mètres."
    n "15 mètres."
    n "20 mètres."
    n "Tu souris."
    r "Facile."
    n "Soudain…"
    n "CRASH"
    n "Tu te fais renverser par une camionnette de livraison de fruits."

    jump death_screen



# =========================================================
# refus à la baboushka fin 2
# =========================================================
label scene_6b_d5_2:
    show r happy at left_unzoomed
    show b happy at right_unzoomed
    scene bg street_market

    r "OK OK désolé ! Vos fruits ont l’air incroyables !"
    n "La baboushka te regarde."
    b "Trop tard."
    n "Elle te donne une pomme."
    b "Mange."
    n "Tu prends une bouchée."
    r "Pas mal… "
    n "Tu t’arrêtes."
    n "Tu deviens pâle."
    r "Attendez… c’est quoi ce goût…"
    b "Pesticide soviétique."

    jump death_screen







