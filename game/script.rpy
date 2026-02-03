# Déclaration des images
image bg japanStreet = "images/japanStreet.jpg"
image j happy = "images/judah_happy.png"

# Déclaration des personnages
define j = Character("Judah", color="#c8ffc8")

# Le jeu commence ici
label start:

    scene bg japanStreet
    play music "music/theme.ogg"

    show j happy at center

    j "Coucou les copains et les copines, c'est Judah."

    menu:
        "Je vous aime":
            s "Oh… <3"
        "Vous êtes trop cool":
            s "Yaaay !"

    return