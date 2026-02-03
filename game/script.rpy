# Vous pouvez placer le script de votre jeu dans ce fichier.

# Déclarez sous cette ligne les images, avec l'instruction 'image'
# ex: image eileen heureuse = "eileen_heureuse.png"

# Déclarez les personnages utilisés dans le jeu.
define j = Character('Judah', color="#c8ffc8")


# Le jeu commence ici
label start:

    scene bg classroom
    play music "music/theme.ogg"

    show j happy

    j "Coucou les copains et les copines c'est joudah."

    menu:
        "Je vous baise":
            j "Yaaay !"
        "Je vous aime":
            j "Oh… <3"

    return