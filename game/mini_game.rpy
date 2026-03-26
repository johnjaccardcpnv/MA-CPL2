# fond
image shooter_bg = "images/combat.png"

# joueur
image player = "images/Ren_gun_nobg.png"

define zoomed = 0.28
define hitboxes = (577*zoomed)-40

# ennemis (plusieurs sprites dans un dossier)
image enemy_1 = "images/roberto.png"
image enemy_2 = "images/jackson.png"

image player_small = At("player", Transform(zoom=zoomed))
image enemy_1_small = At("enemy_1", Transform(zoom=zoomed))
image enemy_2_small = At("enemy_2", Transform(zoom=zoomed))

# projectile (facultatif, sinon Solid)
image bullet = Solid("#ff0000")

default minigame_result = None

init python:

    import random
    import math

    class ShooterGame:

        def __init__(self):
            self.mobile_up = False
            self.mobile_down = False  
            self.mobile_left = False
            self.mobile_right = False

            # hitbox / taille logique du joueur
            self.player_w = hitboxes
            self.player_h = hitboxes

            # hitbox / taille logique des ennemis
            self.enemy_w = hitboxes
            self.enemy_h = hitboxes

            # taille des projectiles
            self.bullet_w = 10
            self.bullet_h = 10

            self.width = renpy.config.screen_width
            self.height = renpy.config.screen_height

            # position au centre
            self.player_x = self.width / 2.0
            self.player_y = self.height / 2.0

            # vitesse réglable
            self.player_speed = 6.0

            # mouvement continu : direction actuelle
            self.move_x = 0.0
            self.move_y = 0.0

            self.projectiles = []

            # ennemis = dicts avec position + taille + image
            self.enemies = []

            self.spawn_timer = 0
            self.kills = 0
            self.goal = 10


            # liste d’images ennemies (définies plus bas)
            self.enemy_images = [
            "enemy_1_small",
            "enemy_2_small"
            ]

            # taille des projectiles
            self.bullet_w = 10
            self.bullet_h = 10

            # joystick mobile
            if renpy.android or renpy.ios:
                self.joystick_active = False
                self.joystick_center_x = 150
                self.joystick_center_y = self.height - 150
                self.joystick_distance = 0.0
                self.joystick_angle = 0.0
            else:
                self.joystick_active = True  # Disable sur PC

        def spawn_enemy(self):

            side = random.choice(["top","bottom","left","right"])

            if side == "top":
                x = random.randint(0, self.width)
                y = -self.enemy_h
            elif side == "bottom":
                x = random.randint(0, self.width)
                y = self.height + self.enemy_h
            elif side == "left":
                x = -self.enemy_w
                y = random.randint(0, self.height)
            else:
                x = self.width + self.enemy_w
                y = random.randint(0, self.height)

            img = random.choice(self.enemy_images)

            self.enemies.append({
                "x": float(x),
                "y": float(y),
                "img": img,
            })

        # appelé quand on (dé)appuie sur une touche
        def set_move(self, up, down, left, right):
            mx = 0.0
            my = 0.0        

            if up:
                my -= 1.0
            if down:
                my += 1.0
            if left:
                mx -= 1.0
            if right:
                mx += 1.0       

            length = math.sqrt(mx * mx + my * my)
            if length != 0:
                mx /= length
                my /= length        

            self.move_x = mx
            self.move_y = my        


        def move_player(self):

            self.player_x += self.move_x * self.player_speed
            self.player_y += self.move_y * self.player_speed

            half_w = self.player_w / 2.0
            half_h = self.player_h / 2.0

            self.player_x = max(half_w, min(self.player_x, self.width - half_w))
            self.player_y = max(half_h, min(self.player_y, self.height - half_h))

        def shoot(self, direction):

            speed = 10.0

            vx, vy = 0.0, 0.0
            if direction == "up":
                vy = -speed
            elif direction == "down":
                vy = speed
            elif direction == "left":
                vx = -speed
            elif direction == "right":
                vx = speed

            self.projectiles.append({
                "x": float(self.player_x),
                "y": float(self.player_y),
                "vx": vx,
                "vy": vy,
            })

        def update(self):

            self.spawn_timer += 1
            if self.spawn_timer > 60:
                self.spawn_timer = 0
                self.spawn_enemy()

            # mouvement joueur
            self.move_player()

            # mouvement projectiles
            for p in self.projectiles:
                p["x"] += p["vx"]
                p["y"] += p["vy"]

            # supprimer projectiles hors écran
            self.projectiles = [
                p for p in self.projectiles
                if -50 < p["x"] < self.width + 50 and -50 < p["y"] < self.height + 50
            ]

            # mouvements ennemis
            for e in self.enemies:

                dx = self.player_x - e["x"]
                dy = self.player_y - e["y"]

                dist = math.sqrt(dx*dx + dy*dy)

                if dist == 0:
                    continue

                speed = 3.0

                e["x"] += dx / dist * speed
                e["y"] += dy / dist * speed

            # collision projectile / ennemi (AABB)
            new_enemies = []
            for e in self.enemies:

                ex = e["x"]
                ey = e["y"]

                e_left   = ex - self.enemy_w / 2.0
                e_right  = ex + self.enemy_w / 2.0
                e_top    = ey - self.enemy_h / 2.0
                e_bottom = ey + self.enemy_h / 2.0

                hit = False

                for p in self.projectiles:

                    px = p["x"]
                    py = p["y"]

                    b_left   = px - self.bullet_w / 2.0
                    b_right  = px + self.bullet_w / 2.0
                    b_top    = py - self.bullet_h / 2.0
                    b_bottom = py + self.bullet_h / 2.0

                    if (b_left < e_right and b_right > e_left and
                        b_top < e_bottom and b_bottom > e_top):
                        hit = True
                        self.kills += 1
                        break

                if not hit:
                    new_enemies.append(e)

            self.enemies = new_enemies

            # collision joueur / ennemi (AABB)
            p_left   = self.player_x - self.player_w / 2.0
            p_right  = self.player_x + self.player_w / 2.0
            p_top    = self.player_y - self.player_h / 2.0
            p_bottom = self.player_y + self.player_h / 2.0

            for e in self.enemies:

                ex = e["x"]
                ey = e["y"]

                e_left   = ex - self.enemy_w / 2.0
                e_right  = ex + self.enemy_w / 2.0
                e_top    = ey - self.enemy_h / 2.0
                e_bottom = ey + self.enemy_h / 2.0

                if (p_left < e_right and p_right > e_left and
                    p_top < e_bottom and p_bottom > e_top):
                    return "lose"

            if self.kills >= self.goal:
                return "win"

            return None
        def set_move_touch(self, touch_x, touch_y):
            if not (renpy.android or renpy.ios):
                return
            dx = touch_x - self.joystick_center_x
            dy = touch_y - self.joystick_center_y
            length = math.sqrt(dx*dx + dy*dy)
            if length < 100:
                self.joystick_distance = length / 100.0
                if length > 0:
                    self.joystick_angle = math.atan2(dy, dx)
                    self.move_x = math.cos(self.joystick_angle) * self.joystick_distance
                    self.move_y = math.sin(self.joystick_angle) * self.joystick_distance
                else:
                    self.move_x = self.move_y = 0.0
            self.joystick_active = True

        def clear_joystick(self):
            if renpy.android or renpy.ios:
                self.move_x = 0.0
                self.move_y = 0.0
                self.joystick_active = False
        




screen shooter_minigame():
    modal True
    zorder 200  # ← Priorité max
    default game = ShooterGame()

    timer 0.016 repeat True action Function(update_shooter, game)

    # CLAVIER PC
    if not renpy.android and not renpy.ios and not renpy.emscripten:
        key "K_w" action Function(update_move_state, game, "up", True)
        key "K_s" action Function(update_move_state, game, "down", True)
        key "K_a" action Function(update_move_state, game, "left", True)
        key "K_d" action Function(update_move_state, game, "right", True)
        key "keyup_K_w" action Function(update_move_state, game, "up", False)
        key "keyup_K_s" action Function(update_move_state, game, "down", False)
        key "keyup_K_a" action Function(update_move_state, game, "left", False)
        key "keyup_K_d" action Function(update_move_state, game, "right", False)
        key "K_UP" action Function(shoot_dir, game, "up")
        key "K_DOWN" action Function(shoot_dir, game, "down")
        key "K_LEFT" action Function(shoot_dir, game, "left")
        key "K_RIGHT" action Function(shoot_dir, game, "right")

    # JEU
    add "shooter_bg" xalign 0.5 yalign 0.5
    text "Kills [game.kills]/[game.goal]" xpos 20 ypos 20 size 50 color "#fff" outlines [(3,"#000",0,0)]
    add "player_small" xpos int(game.player_x - game.player_w / 2) ypos int(game.player_y - game.player_h / 2)

    for p in game.projectiles:
        $ px = int(p["x"] - game.bullet_w / 2)
        $ py = int(p["y"] - game.bullet_h / 2)
        add "bullet" xpos px ypos py xsize game.bullet_w ysize game.bullet_h

    for e in game.enemies:
        $ ex = int(e["x"] - game.enemy_w / 2)
        $ ey = int(e["y"] - game.enemy_h / 2)
        add e["img"] xpos ex ypos ey

    # === MOBILE UNIQUEMENT ===
    if renpy.android or renpy.ios:
        # BOUTONS DEPLACEMENT (GAUCHE) - SIMPLIFIE
        textbutton "↑" xpos 0.15 ypos 0.60 background Solid("#44ff4488") hover_background Solid("#66ff66cc") xsize 80 ysize 80 text_size 30 text_color "#fff" text_align (0.5, 0.5) action SetField(game, "mobile_up", True)
        textbutton "↓" xpos 0.15 ypos 0.85 background Solid("#44ff4488") hover_background Solid("#66ff66cc") xsize 80 ysize 80 text_size 30 text_color "#fff" text_align (0.5, 0.5) action SetField(game, "mobile_down", True)
        textbutton "←" xpos 0.07 ypos 0.725 background Solid("#44ff4488") hover_background Solid("#66ff66cc") xsize 80 ysize 80 text_size 30 text_color "#fff" text_align (0.5, 0.5) action SetField(game, "mobile_left", True)
        textbutton "→" xpos 0.23 ypos 0.725 background Solid("#44ff4488") hover_background Solid("#66ff66cc") xsize 80 ysize 80 text_size 30 text_color "#fff" text_align (0.5, 0.5) action SetField(game, "mobile_right", True)
        
        # BOUTONS TIR (DROITE)
        textbutton "↑" action Function(shoot_dir, game, "up") xpos 0.82 ypos 0.60 background Solid("#ff444488") hover_background Solid("#ff6666cc") xsize 80 ysize 80 text_size 30 text_color "#fff"
        textbutton "↓" action Function(shoot_dir, game, "down") xpos 0.82 ypos 0.85 background Solid("#ff444488") hover_background Solid("#ff6666cc") xsize 80 ysize 80 text_size 30 text_color "#fff"
        textbutton "←" action Function(shoot_dir, game, "left") xpos 0.74 ypos 0.725 background Solid("#ff444488") hover_background Solid("#ff6666cc") xsize 80 ysize 80 text_size 30 text_color "#fff"
        textbutton "→" action Function(shoot_dir, game, "right") xpos 0.90 ypos 0.725 background Solid("#ff444488") hover_background Solid("#ff6666cc") xsize 80 ysize 80 text_size 30 text_color "#fff"

init python:
    current_inputs = {"up": False, "down": False, "left": False, "right": False}

    def update_move_state(game, key, is_down):
        if renpy.android or renpy.ios:  # Ignore clavier sur mobile
            return
        if key == "up": current_inputs["up"] = is_down
        elif key == "down": current_inputs["down"] = is_down
        elif key == "left": current_inputs["left"] = is_down
        elif key == "right": current_inputs["right"] = is_down

        game.set_move(current_inputs["up"], current_inputs["down"], current_inputs["left"], current_inputs["right"])

    def handle_touch_move(game, x, y):
        """Appelé par les événements tactiles"""
        if renpy.android or renpy.ios:
            game.set_move_touch(x, y)

    def handle_touch_end(game):
        if renpy.android or renpy.ios:
            game.clear_joystick()

    def shoot_dir(game, direction):
        game.shoot(direction)

    def update_shooter(game):
        global minigame_result
        if renpy.android or renpy.ios:
            game.set_move(game.mobile_up, game.mobile_down, game.mobile_left, game.mobile_right)

        minigame_result = game.update()
        renpy.restart_interaction()

        if minigame_result == "win" or minigame_result == "lose":
            renpy.hide_screen("shooter_minigame")
            return minigame_result
        return None


