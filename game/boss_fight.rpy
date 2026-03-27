# Made from Habitacle - https://github.com/Habitacle/battle-engine

# écran pour lancer le jeu
label boss_final:
    "Un Hector sauvage apparait !"
    
    # CORRECT - Sans le $ et sans parentheses
    call boss_combat(player_hp=150) from _call_boss_combat
    
    if result == "win":
        "INCROYABLE! Vous avez vaincu Hector !"
        jump scene_10
    elif result == "lose":
        "Vous êtes vaincu..."
        jump death_screen
    else:
        "Vous fuyez... mais Hector vous cavalle après."
        "Vous vous prenez le tapis et tomber par terre."
        "Looser va fallait pas fuir"
        jump death_screen

# VARIABLES À MODIFIER
default potions_hp = 3
default potions_mp = 3
default unlock_baboushka = 0
default baboushka_used = False
default spell_tooltip = ""
default spell_tooltip_x = 0.0
default spell_tooltip_y = 0.0


default player_config = {
    "name": "REN",
    "max_hp": 150,
    "max_mp": 80,
    "atk": 28,
    "defense": 12,
    "image": "images/attack_ren_katana.png"
}

default boss_config = {
    "name": "HECTOR", 
    "max_hp": 1000,
    "max_mp": 150,
    "atk": 35,
    "defense": 18,
    "image": "images/stand_hector_katana.png"
}

default player_spells = [
    {"name": "Soufflet de Don Gomes", "mp": 0, "power": 100,"desc": "Gros soufflet physique.\nDMG:100", "image": "images/soufflet.png"},
    {"name": "Baboushka","mp":0, "power" : 250,"desc": "Son pouvoir vous éblouit mais vous ne pouvez l'utiliser qu'une seule fois.\nDMG:250", "baboushka": True, "image": "images/baboushka.png"},
    {"name": "Claque du daron", "mp": 15, "power": 150,"desc": "Le pouvoir du daron coule dans vos veines.\nDMG:150\nPM:15", "image": "images/main.png"},
    {"name": "Poubelle d'Hector", "mp": 40, "heal": 40,"desc": "Manger ces déchets vous guéri étrangement.\nPV:40\nPM:40", "image": "images/poubelle.png"},
    {"name": "Potion HP", "potions": "hp","desc": "Redbull donne des ailes.\nPV:100", "image": "images/redbull.png"},
    {"name": "Potion MP", "potions": "mp","desc": "Brevage étrange vous redonnant de la magie.\nPM:50", "image": "images/mana.png"},
    {"name": "Fuir","desc": "Seule une sombre merde ferait cela.", "image": "images/exit.png"}
]

default boss_spells = [
    {"name": "Jet de poubelles", "mp": 0, "power": 10},
    {"name": "Patate de forain", "mp": 25, "power": 20}
]

image bg_combat = "images/home_fight.png"
image bar_menu = "images/spellbook.png"
image blank = "images/blank.png"

# =====================================================
init python:
    combat_log = []
    
    def add_log(msg):
        combat_log.append(msg)
        if len(combat_log) > 10:
            combat_log.pop(0)

    player_stats = {}
    boss_stats = {}

    def get_hp_display(stats):
        return max(0, stats.get("hp", 0))

    def check_game_over():
        if get_hp_display(player_stats) <= 0:
            return "lose"
        if get_hp_display(boss_stats) <= 0:
            return "win"
        return None

    def player_turn(spell_index):
        global potions_hp, potions_mp, baboushka_used, unlock_baboushka
        spell_data = player_spells[spell_index]
        name = spell_data["name"]

        # BABOUSHKA ATTACK
        if "baboushka" in spell_data:
            if unlock_baboushka == 0:
                add_log("Technique inconnue...")
                return False
            
            if baboushka_used:
                add_log("Baboushka déjà utilisée!")
                return False
            
            if player_stats.get("mp", 0) >= spell_data["mp"]:
                player_stats["mp"] -= spell_data["mp"]
                damage = spell_data["power"]
                boss_stats["hp"] -= damage
                baboushka_used = True
                add_log("{} utilise BABOUSHKA !!!".format(player_config["name"], damage))
                return True
            else:
                add_log("Pas assez de PM pour Baboushka!")
                return False

        # POTIONS (AVANT le test MP)
        if "potions" in spell_data:
            if name == "Potion HP" and potions_hp > 0:
                potions_hp -= 1
                heal = 100
                player_stats["hp"] = min(player_config["max_hp"], get_hp_display(player_stats) + heal)
                add_log("{} utilise {} (x{})! +{} HP".format(player_config["name"], name, potions_hp, heal))
                return True
            elif name == "Potion MP" and potions_mp > 0:
                potions_mp -= 1
                restore = min(player_config["max_mp"], 50)
                player_stats["mp"] = min(player_config["max_mp"], player_stats.get("mp", 0) + restore)
                add_log("{} utilise {} (x{})! +{} PM".format(player_config["name"], name, potions_mp, restore))
                return True
            else:
                add_log("Plus de potions!")
                return False

        # SORTS NORMAUX (avec MP)
        if player_stats.get("mp", 0) >= spell_data.get("mp", 0):  # .get("mp", 0) au cas où
            player_stats["mp"] -= spell_data.get("mp", 0)
            if "heal" in spell_data:
                heal = min(spell_data["heal"], player_config["max_hp"] - get_hp_display(player_stats))
                player_stats["hp"] += heal
                add_log("{} utilise {}! +{} HP".format(player_config["name"], name, heal))
            elif name != "Fuir":
                damage = max(1, spell_data["power"] + player_config["atk"] - boss_config["defense"]//2)
                boss_stats["hp"] -= damage
                add_log("{} utilise {}! [{} dégâts]".format(player_config["name"], name, damage))
            return True
        else:
            add_log("{}: Pas assez de PM!".format(player_config["name"]))
            return False

    def boss_turn():
        import random
        spell = random.choice(boss_spells)
        boss_stats["mp"] = max(0, boss_stats.get("mp", 0) - spell["mp"])
        damage = max(1, spell["power"] + boss_config["atk"] - player_config["defense"]//2)
        player_stats["hp"] = max(0, get_hp_display(player_stats) - damage)
        add_log("{} utilise {}! [{} dégâts]".format(boss_config["name"], spell["name"], damage))

# =====================================================
screen combat_ui():
    add "bg_combat"
    add player_config["image"] xpos 75 ypos 250 xsize 577
    add boss_config["image"] xpos 1375 ypos 250 xsize 577
    
    frame:
        xpos 50 ypos 50 background "#444444aa"
        vbox spacing 10:
            null height 10
            text "[player_config['name']]" size 36 bold True xalign 0.5 color "#ffffff"
            bar value StaticValue(get_hp_display(player_stats), player_config["max_hp"]) xmaximum 300 ysize 30
            text "HP: [get_hp_display(player_stats)]/[player_config['max_hp']] PM: [player_stats['mp'] or 0]/[player_config['max_mp']]" size 18
            text "Potions: HPx[potions_hp] PMx[potions_mp]" size 16 color "#44ff44"
    
    frame:
        xpos 1450 ypos 50 background "#ff4444aa"
        vbox spacing 10:
            text "[boss_config['name']]" size 36 bold True xalign 0.5 color "#ff4444"
            bar value StaticValue(get_hp_display(boss_stats), boss_config["max_hp"]) xmaximum 300 ysize 30
            text "HP: [get_hp_display(boss_stats)]/[boss_config['max_hp']] PM: [boss_stats['mp'] or 0]/[boss_config['max_mp']]" size 24

    viewport:
        xpos 80 ypos 1000 xsize 1500 ysize 180 mousewheel True scrollbars "vertical"
        vbox:
            for msg in combat_log:
                text "[msg]" size 22 color "#ffffff" xsize 1480

screen player_menu():
    modal True
    use combat_ui()
    
    frame:
        background Frame("bar_menu", 20, 20)
        xpos 450 ypos 550 xsize 900 ysize 450
        
        vbox spacing 15 xalign 0.5 ypos 20:
            text "Menu d'action" size 30 bold True color "#000000" xalign 0.5
            
            hbox spacing 30 xalign 0.5:
                for i in range(4):
                    $ spell = player_spells[i]
                    # Cache Baboushka si pas débloquée OU déjà utilisée
                    if spell.get("baboushka") and (unlock_baboushka == 0 or baboushka_used):
                        continue
                    button:
                        xsize 180 ysize 160
                        background Frame("blank", 10, 10)
                        hover_background "#44ff44aa"
                        hovered [
                            SetVariable("spell_tooltip", spell.get("desc", "")),
                            SetVariable("spell_tooltip_x", 450 +  i * 210 + 90),  # centre du bouton
                            SetVariable("spell_tooltip_y", 550 + 160)              # milieu vertical du bouton
                        ]
                        unhovered SetVariable("spell_tooltip", "")
                        vbox xalign 0.5 spacing 6:
                            add spell["image"] xsize 100 ysize 100 xalign 0.5
                            text "[spell['name']]":
                                size 18
                                bold True
                                xalign 0.5
                                color "#ffffff"
                                text_align 0.5
                        action Function(player_turn, i)
            
            hbox spacing 30 xalign 0.5:
                button:
                    xsize 180 ysize 160
                    background Frame("blank", 10, 10)
                    hover_background "#44ff44aa"
                    hovered [
                    SetVariable("spell_tooltip", player_spells[4].get("desc", "")),
                    SetVariable("spell_tooltip_x", 450 + 0 * 210 + 90),
                    SetVariable("spell_tooltip_y", 550 + 340)   # rangée du bas
                    ]
                    unhovered SetVariable("spell_tooltip", "")
                    tooltip player_spells[4].get("desc", "")
                    vbox xalign 0.5 spacing 10:
                        fixed:
                            xsize 100 ysize 100
                            add player_spells[4]["image"] xalign 0.5 yalign 0.5
                        text "Potion HP\n(x[potions_hp])" size 18 bold True xalign 0.5 color "#ffffff"
                    action If(potions_hp > 0, Function(player_turn, 4), NullAction())
                button:
                    xsize 180 ysize 160
                    background Frame("blank", 10, 10)
                    hover_background "#44ff44aa"
                    tooltip player_spells[5].get("desc", "")
                    hovered [
                    SetVariable("spell_tooltip", player_spells[5].get("desc", "")),
                    SetVariable("spell_tooltip_x", 450 + 1 * 210 + 90),
                    SetVariable("spell_tooltip_y", 550 + 340)
                    ]
                    unhovered SetVariable("spell_tooltip", "")
                    vbox xalign 0.5 spacing 10:
                        fixed:
                            xsize 100 ysize 100
                            add player_spells[5]["image"] xalign 0.5 yalign 0.5
                        text "Potion PM\n(x[potions_mp])" size 18 bold True xalign 0.5 color "#ffffff"
                    action If(potions_mp > 0, Function(player_turn, 5), NullAction())
                button:
                    xsize 180 ysize 160
                    background Frame("blank", 10, 10)
                    hover_background "#ff4444aa"
                    tooltip player_spells[6].get("desc", "")
                    hovered [
                    SetVariable("spell_tooltip", player_spells[6].get("desc", "")),
                    SetVariable("spell_tooltip_x", 450 + 2 * 210 + 90),
                    SetVariable("spell_tooltip_y", 550 + 340)
                    ]
                    unhovered SetVariable("spell_tooltip", "")
                    vbox xalign 0.5 spacing 10:
                        fixed:
                            xsize 100 ysize 100
                            add player_spells[6]["image"] xalign 0.5 yalign 0.5
                        text "Fuir" size 20 bold True xalign 0.5 color "#ff4444"
                    action Return("flee")

screen boss_turn_menu():
    modal True
    use combat_ui()
    timer 0.8 action Return(None)

screen spell_tooltip_box():
    zorder 200
    if spell_tooltip:
        frame:
            xpos spell_tooltip_x
            ypos spell_tooltip_y - 80    # 80 px au‑dessus, ajuste si besoin
            xanchor 0.5
            yanchor 1.0
            background "#000000cc"
            padding (8, 6)
            text spell_tooltip size 18 color "#ffffff" xmaximum 260
# =====================================================
label boss_combat(player_hp=150):
    play music "musics/battle_song.mp3" loop
    $ baboushka_used = False
    $ potions_hp = 3
    $ potions_mp = 3
    $ player_stats = {"hp": player_hp, "mp": player_config["max_mp"]}
    $ boss_stats = {"hp": boss_config["max_hp"], "mp": boss_config["max_mp"]}
    $ combat_log = []
    
    # LOGS DÉBUT COMBAT
    $ duel_msg = "Duel: {} VS {}!".format(player_config["name"], boss_config["name"])
    $ add_log(duel_msg)
    $ start_msg = "{} attaque en premier!".format(player_config["name"])
    $ add_log(start_msg)
    
    scene bg_combat
    show screen combat_ui()
    show screen spell_tooltip_box
    
    label .combat_loop:
        $ result = check_game_over()
        if result == "lose":
            $ game_over_msg = "GAME OVER - {} a été vaincu par {}!".format(player_config["name"], boss_config["name"])
            hide screen combat_ui
            "[game_over_msg]"
            return "lose"
        if result == "win":
            $ victory_msg = "VICTOIRE! {} terrasse {}!".format(player_config["name"], boss_config["name"])
            hide screen combat_ui
            "[victory_msg]"
            return "win"
        
        call screen player_menu
        
        if _return == "flee":
            stop music fadeout 1.0
            $ flee_msg = "{} fuit le combat!".format(player_config["name"])
            hide screen combat_ui
            "[flee_msg]"
            hide bg_combat
            hide combat_ui
            return "flee"
        
        $ result = check_game_over()
        if result == "lose":
            stop music fadeout 1.0
            $ game_over_msg = "GAME OVER - {} a été vaincu par {}!".format(player_config["name"], boss_config["name"])
            hide screen combat_ui
            "[game_over_msg]"
            hide bg_combat
            hide combat_ui
            return "lose"
        if result == "win":
            stop music fadeout 1.0
            $ victory_msg = "VICTOIRE! {} terrasse {}!".format(player_config["name"], boss_config["name"])
            hide screen combat_ui
            "[victory_msg]"
            hide bg_combat
            hide combat_ui
            return "win"
        
        pause 0.3
        with hpunch
        pause 0.6
        
        call screen boss_turn_menu
        $ boss_turn()
        pause 0.4
        with vpunch
        pause 1.0
        
        $ result = check_game_over()
        if result == "lose":
            $ game_over_msg = "GAME OVER - {} a été vaincu par {}!".format(player_config["name"], boss_config["name"])
            hide screen combat_ui
            "[game_over_msg]"
            return "lose"
        if result == "win":
            $ victory_msg = "VICTOIRE! {} terrasse {}!".format(player_config["name"], boss_config["name"])
            hide screen combat_ui
            "[victory_msg]"
            return "win"
        
        jump .combat_loop
