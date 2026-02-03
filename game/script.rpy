# Déclaration des images
image bg japanStreet = "images/japanStreet.png"
image j happy = "images/judah_happy.png"

# Déclaration des personnages
define j = Character("Judah", color="#c8ffc8")

# Le jeu commence ici
label start:

    scene bg japanStreet:
        zoom 1.5

    play music "music/theme.ogg"

    show j happy at center:
        zoom 0.5

    j "Coucou les copains et les copines, c'est Judah."

    menu:
        "Je vous aime":
            j "Oh… <3"
        "Vous êtes trop cool":
            j "Yaaay !"

    return