# Déclaration des personnages
define r = Character("Ren", color="#c8ffc8", what_prefix="“", what_suffix="”")
define n = Character("Narrateur")  # narrateur
image r happy = "images/ren_happy.png"
image r ok = "images/ren_happy.png"

# Images (optionnel – à adapter si tu en as)
image bg bedroom = "images/bedroom.jpg"
image bg hallway = "images/hallway.jpg"
image bg bathroom = "images/bathroom.jpg"
image bg street = "images/street.png"
image bg black = Solid("#000")

label start:

    scene bg bedroom:
        zoom 2.5
    play music "music/morning.ogg"

    show r happy at left :
        zoom 2.5

    show r ok at right :
        zoom 2.5

    n "7h43."
    n "Ton réveil n’a pas sonné."
    n "Enfin si."
    n "Mais toi, tu l’as éteint avec la précision d’un ninja endormi."
    n "Ton téléphone vibre."
    n "3 notifications."
    n "Ton estomac gargouille."
    n "Un sentiment étrange t’envahit :"
    n "tu es en retard… quelque part."

    menu:
        "Te lever immédiatement":
            jump scene_1a
        "Rester au lit \"2 minutes\"":
            jump scene_1b
        "Regarder ton téléphone":
            jump scene_1c

# --- SCÈNE 1A ---
label scene_1a:

    n "Tu te lèves d’un bond."
    n "Ton pied rencontre un objet non identifié (probablement un LEGO)."
    n "Tu cries intérieurement."
    n "Direction la salle de bain pour la douche."

    scene bg bathroom:
        zoom 1
    n "Tu te précipites dans la salle de bain."
    n "La journée commence mal… mais au moins tu es debout."

    jump suite_normale

# --- SCÈNE 1B ---
label scene_1b:

    n "Tu décides de rester encore « 2 minutes » en te disant « chill j’ai le temps »."
    n "Tu te redors."

    n "Finalement tu te réveilles à 8h."
    n "Tu te prépares en vitesse."

    scene bg hallway:
        zoom 3
    n "Tu sors de chez toi à 8h50."
    n "Tu croises quelqu’un d’étrange devant chez toi."
    n "Il te lance un regard de SDF mais tu décides de l’ignorer."

    scene bg street:
        zoom 2
    n "Tu continues jusqu’à ta destination (enfin on espère)."

    jump suite_normale

# --- SCÈNE 1C ---
label scene_1c:

    n "Tu ouvres ton téléphone."
    n "Une vidéo."
    n "Puis une autre."
    n "Puis soudain… 8h35."
    n "Ton cerveau : “Ça va passer.”"
    n "La réalité : “Non.”"

    menu:
        "Te lever en panique (risqué)":
            jump scene_2c_b1
        "Assumer le retard":
            jump scene_2c_b2
        "Te doucher (risqué)":
            jump scene_2c_b3

# --- SCÈNE 2C B2 ---
label scene_2c_b2:

    n "Tu décides de ne pas te doucher."
    n "Tu prends un bon croissant des familles pour le trajet."

    scene bg hallway:
        zoom 3
    n "En sortant de chez toi à 8h55, tu croises quelqu’un d’étrange dans le couloir de ton étage."
    n "Il te lance un regard de SDF mais tu décides de l’ignorer."

    scene bg street:
        zoom 2
    n "Tu continues jusqu’à ta destination (enfin on espère)."

    jump suite_normale

# --- SCÈNE 2C B3 (DEAD) ---
label scene_2c_b3:

    scene bg bathroom:
        zoom 1
    n "Tu décides finalement de bouger ton cul et prendre une douche."
    n "Pendant ta douche cramante, tu entends un bruit bizarre."
    n "Cependant tu décides de l’ignorer car ce sont peut-être les voisins et leur sport du matin…"

    n "La porte de la salle de bain s’ouvre."
    n "Un monsieur cagoulé et armé entre."
    n "Dans le choc, tu glisses dans la douche."
    n "Le braqueur court vers ta direction."
    n "Tu essaies de te débattre et de saisir l’arme."
    n "Mais trop tard…"

    scene bg black
    n "Tu es swiss cheese."

    centered "{size=60}{color=#ff0000}DEAD{/color}{/size}"

    return

# --- SCÈNE 2C B1 ---
label scene_2c_b1:

    n "Tu te lèves en panique car tu remarques ton retard (bien joué)."
    n "Tu t’habilles vite avec les premiers trucs que tu vois et files par la porte."

    scene bg hallway:
        zoom 3
    n "Tu sors de chez toi à 8h50."
    n "Tu croises quelqu’un d’étrange devant chez toi."
    n "Il te lance un regard de SDF mais tu décides de l’ignorer."

    scene bg street:
        zoom 2
    n "Tu continues jusqu’à ta destination (enfin on espère)."
    n "### Il pue et il a faim ###"

    jump suite_normale

# --- SUITE COMMUNE (à continuer plus tard) ---
label suite_normale:

    n "La journée ne fait que commencer..."
    n "À toi de décider ce que Ren va vivre ensuite."

    return
