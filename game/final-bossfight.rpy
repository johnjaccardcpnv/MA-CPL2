# --- IMAGES DE BASE ---
image duel_bg = "images/combat.png"

image player_samurai = "images/ren_tel.png"
image enemy_samurai  = "images/hector_debout.png"

define duel_zoom = 0.4
define duel_hitbox_w = 400 * duel_zoom
define duel_hitbox_h = 600 * duel_zoom

image player_samurai_small = At("player_samurai", Transform(zoom=duel_zoom))
image enemy_samurai_small  = At("enemy_samurai",  Transform(zoom=duel_zoom))

init python:

    import math
    import random

    class KatanaDuelGame:

        def __init__(self):
            self.width = renpy.config.screen_width
            self.height = renpy.config.screen_height

            # Positions horizontales logiques (1D)
            # Ennemi à gauche, joueur à droite
            self.min_x = 200
            self.max_x = self.width - 200

            self.player_x = self.max_x - 100
            self.enemy_x  = self.min_x + 100

            # Y (fixe, même hauteur pour les deux)
            self.player_y = self.height * 0.6
            self.enemy_y  = self.height * 0.6

            # Stats
            self.player_hp = 1
            self.enemy_hp  = 20

            # Portée de katana (distance max pour toucher)
            self.attack_range = 220.0

            # Vitesse avance / recule
            self.player_speed = 12.0
            self.enemy_speed  = 10.0

            # Cooldowns (en secondes, convertis en frames 60 fps)
            self.attack_cd_time = 0.7
            self.parry_cd_time  = 1.0

            self.player_attack_cd = 0.0
            self.player_parry_cd  = 0.0
            self.enemy_attack_cd  = 0.0
            self.enemy_parry_cd   = 0.0

            self.player_attack_vis = 0.0
            self.player_parry_vis  = 0.0
            self.enemy_attack_vis  = 0.0
            self.enemy_parry_vis   = 0.0

            # Durée de la parade (fenêtre active)
            self.parry_window = 0.25
            self.player_parry_active = 0.0
            self.enemy_parry_active  = 0.0

            # Stun
            self.enemy_stun_time = 0.0  # ennemi étourdi
            self.enemy_stun_duration = 1.5

            # Recul quand on pare
            self.parry_pushback = 120.0

            # Entrées joueur
            self.move_dir = 0  # -1 recule, +1 avance, 0 rien

            # Pour mobile : flags simples
            self.mobile_forward = False
            self.mobile_backward = False

            # État de fin
            self.result = None  # "win" ou "lose" ou None

        # --- OUTILS D’ESPACE ---
        def distance(self):
            return abs(self.player_x - self.enemy_x)

        def clamp_positions(self):
            self.player_x = max(self.min_x, min(self.player_x, self.max_x))
            self.enemy_x  = max(self.min_x, min(self.enemy_x, self.max_x))

        # --- ENTRÉES JOUEUR ---
        def set_move_dir(self, forward, backward):
            # forward = vers l’ennemi (gauche), backward = s’éloigner (droite)
            d = 0
            if forward and not backward:
                d = -1
            elif backward and not forward:
                d = 1
            self.move_dir = d

        def player_attack(self):
            if self.player_attack_cd > 0 or self.result:
                return
            self.player_attack_cd = self.attack_cd_time
            self.player_attack_vis = 0.2  # 0.2s rouge

            if self.distance() <= self.attack_range:
                if self.enemy_parry_active > 0:
                    self.player_x += self.parry_pushback
                    self.enemy_stun_time = self.enemy_stun_duration
                    self.enemy_parry_vis = 0.2  # vert ennemi qui pare
                else:
                    self.enemy_hp -= 1
                    if self.enemy_hp <= 0:
                        self.result = "win"

        def player_parry(self):
            if self.player_parry_cd > 0 or self.result:
                return
            self.player_parry_cd = self.parry_cd_time
            self.player_parry_active = self.parry_window
            self.player_parry_vis = 0.2  # 0.2s vert

        def enemy_attack(self):
            if self.enemy_attack_cd > 0 or self.result:
                return
            self.enemy_attack_cd = self.attack_cd_time
            self.enemy_attack_vis = 0.2  # ennemi rouge

            if self.distance() <= self.attack_range:
                if self.player_parry_active > 0:
                    if self.enemy_x < self.player_x:
                        self.enemy_x -= self.parry_pushback
                    else:
                        self.enemy_x += self.parry_pushback
                    self.enemy_stun_time = self.enemy_stun_duration
                    self.player_parry_vis = 0.2
                    self.clamp_positions()
                else:
                    self.player_hp -= 1
                    if self.player_hp <= 0:
                        self.result = "lose"

        # --- IA ENNEMI ---
        def enemy_ai(self, dt):
            if self.result:
                return

            # Stun ?
            if self.enemy_stun_time > 0:
                self.enemy_stun_time -= dt
                return

            dist = self.distance()

            # Choix : s’approcher si trop loin pour attaquer
            if dist > self.attack_range * 0.9:
                # L’ennemi se déplace vers le joueur (droite)
                if self.enemy_x < self.player_x:
                    self.enemy_x += self.enemy_speed
                else:
                    self.enemy_x -= self.enemy_speed
                self.clamp_positions()
            else:
                # A portée : essayer d’attaquer
                if self.enemy_attack_cd <= 0:
                    self.enemy_attack()
                # La "parade" de l'ennemi est en réaction aux attaques du joueur,
                # gérée dans enemy_maybe_parry().


        def enemy_maybe_parry(self, is_player_attack):
            if not is_player_attack or self.enemy_parry_cd > 0:
                return
            chance = 0.1 if self.enemy_hp > 10 else 0.25
            if random.random() < chance:
                self.enemy_parry_cd = self.parry_cd_time
                self.enemy_parry_active = self.parry_window
                self.enemy_parry_vis = 0.2
        
        # --- MISE À JOUR GLOBALE ---
        def update(self, dt):
            if self.result:
                return self.result

            # Mise à jour cooldowns et fenêtres de parade
            self.player_attack_cd = max(0.0, self.player_attack_cd - dt)
            self.player_parry_cd  = max(0.0, self.player_parry_cd  - dt)
            self.enemy_attack_cd  = max(0.0, self.enemy_attack_cd  - dt)
            self.enemy_parry_cd   = max(0.0, self.enemy_parry_cd   - dt)

            self.player_parry_active = max(0.0, self.player_parry_active - dt)
            self.enemy_parry_active  = max(0.0, self.enemy_parry_active  - dt)

            # Timers visuels
            self.player_attack_vis = max(0.0, self.player_attack_vis - dt)
            self.player_parry_vis  = max(0.0, self.player_parry_vis  - dt)
            self.enemy_attack_vis  = max(0.0, self.enemy_attack_vis - dt)
            self.enemy_parry_vis   = max(0.0, self.enemy_parry_vis   - dt)

            # Déplacement joueur (avance = vers la gauche)
            if self.move_dir != 0:
                self.player_x += self.move_dir * self.player_speed
                self.clamp_positions()

            # IA ennemi
            self.enemy_ai(dt)

            return self.result

        # Pour mobile : wrappers simples
        def set_mobile_move(self, forward, backward):
            self.mobile_forward  = forward
            self.mobile_backward = backward
            self.set_move_dir(forward, backward)




transform attack_tint:
    matrixcolor TintMatrix("#ff5555")

transform parry_tint:
    matrixcolor TintMatrix("#55ff55")
# --- FONCTIONS UTILITAIRES POUR LE SCREEN ---

init python:
    DUEL_FPS = 60.0
    DUEL_DT  = 1.0 / DUEL_FPS

    def duel_update(game):
        # Sur mobile, ré-applique les entrées tactiles
        if renpy.android or renpy.ios:
            game.set_move_dir(game.mobile_forward, game.mobile_backward)

        result = game.update(DUEL_DT)
        renpy.restart_interaction()
        if result in ("win", "lose"):
            renpy.hide_screen("katana_duel_minigame")
            return result
        return None

    # Gestion clavier (PC)
    duel_inputs = {"forward": False, "backward": False}

    def duel_move_key(game, key, is_down):
        if renpy.android or renpy.ios:
            return
        if key == "forward":
            duel_inputs["forward"] = is_down
        elif key == "backward":
            duel_inputs["backward"] = is_down
        game.set_move_dir(duel_inputs["forward"], duel_inputs["backward"])

    def duel_player_attack(game):
        # Lancer l’attaque du joueur et décider si l’ennemi pare
        was_cd = (game.player_attack_cd > 0)
        game.player_attack()
        # Si l’attaque vient juste d’être utilisée, on peut lancer la logique de parade ennemie
        if not was_cd:
            game.enemy_maybe_parry(is_player_attack=True)

    def duel_player_parry(game):
        game.player_parry()

# --- SCREEN REN'PY ---

screen katana_duel_minigame():
    modal True
    zorder 200
    default game = KatanaDuelGame()

    timer DUEL_DT repeat True action Function(duel_update, game)

    # Choix du transform pour le joueur
    $ player_tr = None
    if game.player_attack_vis > 0:
        $ player_tr = attack_tint
    elif game.player_parry_vis > 0:
        $ player_tr = parry_tint

    # Choix du transform pour l’ennemi
    $ enemy_tr = None
    if game.enemy_attack_vis > 0:
        $ enemy_tr = attack_tint
    elif game.enemy_parry_vis > 0:
        $ enemy_tr = parry_tint

    # Ennemi à gauche
    if enemy_tr is None:
        add "enemy_samurai_small" xpos int(game.enemy_x - duel_hitbox_w/2) ypos int(game.enemy_y - duel_hitbox_h/2)
    else:
        add "enemy_samurai_small" at enemy_tr xpos int(game.enemy_x - duel_hitbox_w/2) ypos int(game.enemy_y - duel_hitbox_h/2)

    # Joueur à droite
    if player_tr is None:
        add "player_samurai_small" xpos int(game.player_x - duel_hitbox_w/2) ypos int(game.player_y - duel_hitbox_h/2)
    else:
        add "player_samurai_small" at player_tr xpos int(game.player_x - duel_hitbox_w/2) ypos int(game.player_y - duel_hitbox_h/2)

    text "AtkCD: [round(game.player_attack_cd, 2)]  ParryCD: [round(game.player_parry_cd, 2)]" xpos 0.3 ypos 0.15 size 25 color "#fff"

    # CLAVIER + SOURIS PC
    if not renpy.android and not renpy.ios and not renpy.emscripten:
        # Avancer / reculer (comme avant)
        key "K_a" action Function(duel_move_key, game, "forward", True)
        key "K_LEFT" action Function(duel_move_key, game, "forward", True)
        key "keyup_K_a" action Function(duel_move_key, game, "forward", False)
        key "keyup_K_LEFT" action Function(duel_move_key, game, "forward", False)

        key "K_d" action Function(duel_move_key, game, "backward", True)
        key "K_RIGHT" action Function(duel_move_key, game, "backward", True)
        key "keyup_K_d" action Function(duel_move_key, game, "backward", False)
        key "keyup_K_RIGHT" action Function(duel_move_key, game, "backward", False)

        # Attaque / parade au clavier (optionnel)
        key "K_j" action Function(duel_player_attack, game)
        key "K_k" action Function(duel_player_parry, game)

        # Souris :
        # clic gauche = attaquer
        key "mousedown_1" action Function(duel_player_attack, game)
        # clic droit = parer
        key "mousedown_3" action Function(duel_player_parry, game)
    # FOND
    add "duel_bg" xalign 0.5 yalign 0.5

    # HUD simple
    hbox:
        xpos 0.05
        ypos 0.05
        spacing 40
        text "PV Ennemi: [game.enemy_hp]" size 40 color "#fff"
        text "PV Joueur: [game.player_hp]" size 40 color "#fff"

    # Affichage des sprites (2D latéral)
    # Ennemi à gauche
    add "enemy_samurai_small" xpos int(game.enemy_x - duel_hitbox_w/2) ypos int(game.enemy_y - duel_hitbox_h/2)
    # Joueur à droite
    add "player_samurai_small" xpos int(game.player_x - duel_hitbox_w/2) ypos int(game.player_y - duel_hitbox_h/2)

    # Optionnel: Debug distance / cooldown
    # text "Dist: [int(game.distance())]" xpos 0.45 ypos 0.05 size 30 color "#fff"

    # --- CONTROLES MOBILE SIMPLES ---
    if renpy.android or renpy.ios:
        # Déplacements (gauche / droite logiques)
        textbutton "Avancer":
            xpos 0.05
            ypos 0.75
            xsize 160
            ysize 90
            background Solid("#44ff4488")
            hover_background Solid("#66ff66cc")
            action [SetField(game, "mobile_forward", True), SetField(game, "mobile_backward", False), Function(game.set_mobile_move, True, False)]

        textbutton "Reculer":
            xpos 0.25
            ypos 0.75
            xsize 160
            ysize 90
            background Solid("#44ff4488")
            hover_background Solid("#66ff66cc")
            action [SetField(game, "mobile_forward", False), SetField(game, "mobile_backward", True), Function(game.set_mobile_move, False, True)]

        textbutton "Stop":
            xpos 0.15
            ypos 0.87
            xsize 150
            ysize 80
            background Solid("#44ff4488")
            hover_background Solid("#66ff66cc")
            action [SetField(game, "mobile_forward", False), SetField(game, "mobile_backward", False), Function(game.set_mobile_move, False, False)]

        # Attaque / Parade
        textbutton "Frapper":
            xpos 0.70
            ypos 0.75
            xsize 160
            ysize 90
            background Solid("#ff444488")
            hover_background Solid("#ff6666cc")
            action Function(duel_player_attack, game)

        textbutton "Parer":
            xpos 0.85
            ypos 0.75
            xsize 160
            ysize 90
            background Solid("#4444ff88")
            hover_background Solid("#6666ffcc")
            action Function(duel_player_parry, game)
