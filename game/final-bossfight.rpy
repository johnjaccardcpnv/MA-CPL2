# =============================================
# MINI JEU DUEL KATANA - VERSION FINALE 2026
# =============================================

# FOND
image duel_bg = "images/bg_combat_none.png"

# Ren (joueur)
image ren_stand  = "images/ren_legs.png"
image ren_attack = "mini_game_animations/attack_ren_katana.png"
image ren_parry  = "mini_game_animations/parry_ren_katana.png"

# Hector (ennemi)
image hector_stand  = "mini_game_animations/stand_hector_katana.png"
image hector_attack = "mini_game_animations/attack_hector_katana.png"
image hector_parry  = "mini_game_animations/parry_hector_katana.png"

define duel_zoom = 0.42

# même style que player_small / enemy_1_small
image ren_duel_stand  = At("ren_stand",  Transform(zoom=duel_zoom))
image ren_duel_attack = At("ren_attack", Transform(zoom=duel_zoom))
image ren_duel_parry  = At("ren_parry",  Transform(zoom=duel_zoom))

image hector_duel_stand  = At("hector_stand",  Transform(zoom=duel_zoom))
image hector_duel_attack = At("hector_attack", Transform(zoom=duel_zoom))
image hector_duel_parry  = At("hector_parry",  Transform(zoom=duel_zoom))


# =============================================
define DUEL_FPS = 60.0
define DUEL_DT  = 1.0 / DUEL_FPS

init python:
    import random
    def duel_update(game):
        # même style que update_shooter
        result = game.update(DUEL_DT)
        renpy.restart_interaction()
        if result in ("win", "lose"):
            renpy.hide_screen("katana_duel_minigame")
        return result

    def duel_player_attack(game):
        game.player_attack()

    def duel_player_parry(game):
        game.player_parry()

    def duel_move(game, direction):
        game.move_dir = direction   # -1 = avancer, +1 = reculer, 0 = stop
    class KatanaDuelGame:
        def __init__(self):
            self.width = renpy.config.screen_width
            self.height = renpy.config.screen_height

            self.min_x = 180
            self.max_x = self.width - 180

            # joueur à gauche, ennemi à droite
            self.player_x = self.min_x + 160
            self.enemy_x  = self.max_x - 160

            self.player_y = self.height * 0.59
            self.enemy_y  = self.height * 0.59

            self.player_hp = 1
            self.enemy_hp  = 20

            self.attack_range = 230.0
            self.player_speed = 13.0
            self.enemy_speed  = 11.0

            self.attack_cd_time = 0.65
            self.parry_cd_time  = 1.1
            self.parry_window   = 0.28
            self.parry_pushback = 135.0
            self.enemy_stun_duration = 1.6

            self.player_attack_cd = 0.0
            self.player_parry_cd  = 0.0
            self.enemy_attack_cd  = 0.0
            self.enemy_parry_cd   = 0.0

            self.player_attack_vis = 0.0
            self.player_parry_vis  = 0.0
            self.enemy_attack_vis  = 0.0
            self.enemy_parry_vis   = 0.0

            self.player_parry_active = 0.0
            self.enemy_parry_active  = 0.0
            self.enemy_stun_time     = 0.0

            self.move_dir = 0
            self.result = None   # "win" ou "lose"

        def distance(self):
            return abs(self.player_x - self.enemy_x)

        def clamp(self):
            self.player_x = max(self.min_x, min(self.player_x, self.max_x))
            self.enemy_x  = max(self.min_x,  min(self.enemy_x,  self.max_x))

        # === actions joueur ===
        def player_attack(self):
            if self.player_attack_cd > 0 or self.result:
                return
            self.player_attack_cd = self.attack_cd_time
            self.player_attack_vis = 0.22

            if self.distance() <= self.attack_range:
                if self.enemy_parry_active > 0:
                    self.player_x -= self.parry_pushback
                    self.enemy_stun_time = self.enemy_stun_duration
                else:
                    self.enemy_hp -= 1
                    if self.enemy_hp <= 0:
                        self.result = "win"

        def player_parry(self):
            if self.player_parry_cd > 0 or self.result:
                return
            self.player_parry_cd = self.parry_cd_time
            self.player_parry_active = self.parry_window
            self.player_parry_vis = 0.22

        # === ennemi ===
        def enemy_attack(self):
            if self.enemy_attack_cd > 0 or self.result:
                return
            self.enemy_attack_cd = self.attack_cd_time
            self.enemy_attack_vis = 0.22

            if self.distance() <= self.attack_range:
                if self.player_parry_active > 0:
                    self.enemy_x += self.parry_pushback
                    self.enemy_stun_time = self.enemy_stun_duration
                else:
                    self.player_hp -= 1
                    if self.player_hp <= 0:
                        self.result = "lose"

        def enemy_ai(self, dt):
            if self.result or self.enemy_stun_time > 0:
                if self.enemy_stun_time > 0:
                    self.enemy_stun_time -= dt
                return

            dist = self.distance()

            if dist > self.attack_range + 30:
                self.enemy_x += self.enemy_speed
            elif dist < self.attack_range * 0.45:
                self.enemy_x -= self.enemy_speed
            elif random.random() < 0.085:
                self.enemy_attack()

            self.clamp()

        def update(self, dt):
            if self.result:
                return self.result

            # cooldowns
            self.player_attack_cd = max(0.0, self.player_attack_cd - dt)
            self.player_parry_cd  = max(0.0, self.player_parry_cd  - dt)
            self.enemy_attack_cd  = max(0.0, self.enemy_attack_cd  - dt)
            self.enemy_parry_cd   = max(0.0, self.enemy_parry_cd   - dt)

            self.player_parry_active = max(0.0, self.player_parry_active - dt)
            self.enemy_parry_active  = max(0.0, self.enemy_parry_active  - dt)

            self.player_attack_vis = max(0.0, self.player_attack_vis - dt)
            self.player_parry_vis  = max(0.0, self.player_parry_vis  - dt)
            self.enemy_attack_vis  = max(0.0, self.enemy_attack_vis - dt)
            self.enemy_parry_vis   = max(0.0, self.enemy_parry_vis   - dt)

            # déplacement joueur
            if self.move_dir != 0:
                self.player_x += self.move_dir * self.player_speed
                self.clamp()

            # IA
            self.enemy_ai(dt)

            return self.result

# =============================================
# FONCTIONS UTILITAIRES
# =============================================

# =============================================
# SCREEN
# =============================================
screen katana_duel_minigame():
    modal True
    zorder 200

    default game = KatanaDuelGame()

    timer DUEL_DT repeat True action Function(duel_update, game)

    # Fond
    add "duel_bg"

    # HUD
    hbox:
        xpos 0.05 ypos 0.04 spacing 100
        text "Hector  [game.enemy_hp]" size 42 color "#ffdddd" outlines [(2,"#000")]
        text "Ren     [game.player_hp]" size 42 color "#ddddff" outlines [(2,"#000")] xalign 1.0

    # Joueur
    $ ren_img = "ren_duel_stand"
    if game.player_attack_vis > 0:
        $ ren_img = "ren_duel_attack"
    elif game.player_parry_active > 0 or game.player_parry_vis > 0:
        $ ren_img = "ren_duel_parry"

    add ren_img:
        xpos game.player_x
        ypos game.player_y
        xanchor 0.5 yanchor 0.78

    # Ennemi
    $ hector_img = "hector_duel_stand"
    if game.enemy_attack_vis > 0:
        $ hector_img = "hector_duel_attack"
    elif game.enemy_parry_active > 0 or game.enemy_parry_vis > 0:
        $ hector_img = "hector_duel_parry"

    add hector_img:
        xpos game.enemy_x
        ypos game.enemy_y
        xanchor 0.5 yanchor 0.78
        xzoom -1

    # Contrôles PC (même style que shooter)
    if not (renpy.android or renpy.ios):
        key "K_LEFT"  action Function(duel_move, game, -1)
        key "K_RIGHT" action Function(duel_move, game,  1)
        key "keyup_K_LEFT"  action Function(duel_move, game, 0)
        key "keyup_K_RIGHT" action Function(duel_move, game, 0)

        key "K_a" action Function(duel_player_attack, game)
        key "K_z" action Function(duel_player_parry, game)
        key "mousedown_1" action Function(duel_player_attack, game)
        key "mousedown_3" action Function(duel_player_parry, game)

    # Mobile inchangé (si tu veux garder)
    if renpy.android or renpy.ios:
        textbutton "← Avancer":
            xpos 40 ypos 720 xsize 180 ysize 110
            text_size 38 action Function(duel_move, game, -1)
        textbutton "Reculer →":
            xpos 260 ypos 720 xsize 180 ysize 110
            text_size 38 action Function(duel_move, game, 1)
        textbutton "STOP":
            xpos 180 ypos 850 xsize 140 ysize 80
            text_size 32 action Function(duel_move, game, 0)

        textbutton "ATTAQUER":
            xpos 880 ypos 680 xsize 220 ysize 130
            background "#ff444488" hover_background "#ff6666cc"
            text_size 42 action Function(duel_player_attack, game)
        textbutton "PARER":
            xpos 1150 ypos 680 xsize 220 ysize 130
            background "#4444ff88" hover_background "#6666ffcc"
            text_size 42 action Function(duel_player_parry, game)

    # Message de fin
    if game.result == "win":
        text "VICTOIRE !" size 90 color "#ff0" outlines [(4,"#000")] xalign 0.5 yalign 0.4
    elif game.result == "lose":
        text "DÉFAITE..." size 90 color "#f00" outlines [(4,"#000")] xalign 0.5 yalign 0.4
