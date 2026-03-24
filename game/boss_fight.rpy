# Made from Habitacle - https://github.com/Habitacle/battle-engine

# écran pour lancer le jeu
label boss_final:
    "Un Hector sauvage apparait !"
    
    # CORRECT - Sans le $ et sans parentheses
    call boss_combat(player_hp=150)
    
    if result == "win":
        "INCROYABLE! Vous avez vaincu le boss final!"
        jump scene_10
    elif result == "lose":
        "Vous êtes vaincu... GAME OVER."
        jump death_screen
    else:
        "Vous fuyez... mais le boss vous pourchasse!"
        jump death_screen

# VARIABLES À MODIFIER
default potions_hp = 3
default potions_mp = 3
default unlock_baboushka = 0
default baboushka_used = False


default player_config = {
    "name": "REN",
    "max_hp": 150,
    "max_mp": 80,
    "atk": 28,
    "defense": 12,
    "image": "images/ren_gun_nobg.png"
}

default boss_config = {
    "name": "HECTOR", 
    "max_hp": 600,
    "max_mp": 150,
    "atk": 40,
    "defense": 18,
    "image": "images/hector_debout.png"
}

default player_spells = [
    {"name": "Soufflet de Don Gomes", "mp": 0, "power": 150, "image": "images/soufflet.png"},
    {"name": "Baboushka", "mp": 30,"power" : 200, "baboushka": True, "image": "images/baboushka.png"},
    {"name": "Claque du daron", "mp": 15, "power": 100, "image": "images/main.png"},
    {"name": "Poubelle d'Hector", "mp": 15, "heal": 150, "image": "images/poubelle.png"},
    {"name": "Potion HP", "potions": "hp", "image": "images/redbull.png"},
    {"name": "Potion MP", "potions": "mp", "image": "images/mana.png"},
    {"name": "Fuir", "image": "images/exit.png"}
]

default boss_spells = [
    {"name": "Jet de poubelles", "mp": 0, "power": 35},
    {"name": "Patate de forain", "mp": 25, "power": 50}
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

        # =========================
        # BABOUSHKA ATTACK
        # =========================
        if "baboushka" in spell_data:
            if unlock_baboushka == 0:
                add_log("Technique inconnue...")
                return False
            
            if baboushka_used:
                add_log("Baboushka déjà utilisée!")
                return False
            
            if player_stats.get("mp", 0) >= spell_data["mp"]:
                player_stats["mp"] -= spell_data["mp"]

                damage = int(boss_config["max_hp"] * 0.25)
                boss_stats["hp"] -= damage

                baboushka_used = True

                add_log("{} utilise BABOUSHKA !!! [{} dégâts - 25% HP]".format(player_config["name"], damage))
                return True
            else:
                add_log("Pas assez de PM pour Baboushka!")
                return False
        
        if name == "Potion HP" and potions_hp > 0:
            potions_hp -= 1
            heal = min(player_config["max_hp"], 100)
            player_stats["hp"] = min(player_config["max_hp"], get_hp_display(player_stats) + heal)
            add_log("{} utilise {} (x{})! +{} HP".format(player_config["name"], name, potions_hp, heal))
            return True
        elif name == "Potion PM" and potions_mp > 0:
            potions_mp -= 1
            restore = min(player_config["max_mp"], 50)
            player_stats["mp"] = min(player_config["max_mp"], player_stats.get("mp", 0) + restore)
            add_log("{} utilise {} (x{})! +{} PM".format(player_config["name"], name, potions_mp, restore))
            return True
        elif player_stats.get("mp", 0) >= spell_data["mp"]:
            player_stats["mp"] -= spell_data["mp"]
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
                        vbox xalign 0.5 spacing 6:
                            
                            add spell["image"] xsize 100 ysize 100 xalign 0.5

                            text "[spell['name']]" :
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
                    vbox xalign 0.5 spacing 10:
                        fixed:
                            xsize 100 ysize 100
                            add player_spells[4]["image"] xalign 0.5 yalign 0.5
                        text "Potion HP\n(x[potions_hp])" size 18 bold True xalign 0.5 color "#ffffff"
                    action If(potions_hp > 0, Function(player_turn, 3), NullAction())
                
                button:
                    xsize 180 ysize 160
                    background Frame("blank", 10, 10)
                    hover_background "#44ff44aa"
                    vbox xalign 0.5 spacing 10:
                        fixed:
                            xsize 100 ysize 100
                            add player_spells[5]["image"] xalign 0.5 yalign 0.5
                        text "Potion PM\n(x[potions_mp])" size 18 bold True xalign 0.5 color "#ffffff"
                    action If(potions_mp > 0, Function(player_turn, 4), NullAction())
                
                button:
                    xsize 180 ysize 160
                    background Frame("blank", 10, 10)
                    hover_background "#ff4444aa"
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
