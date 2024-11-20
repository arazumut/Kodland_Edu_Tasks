import pgzrun
import random
from pgzero.rect import Rect

# Ekran ve Oyun Ayarları
WIDTH = 625
HEIGHT = 370
TITLE = "Uzaylı Koşusu"
FPS = 30

game_state = "menu"
music_on = True

# Arka Plan ve Sprite Görselleri
background_image = "background1"
menu_background_image = "background1"

# Müzik ve Ses
def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        music.play("music")
    else:
        music.stop()

# Karakter Hareket ve Özellik Sınıfı
class Character:
    def __init__(self, image, position):
        self.actor = Actor(image, position)
        self.default_image = image
        self.animations = {
            "run": ["hero2", "hero3"],
            "jump": "hero4",
            "idle": ["hero1", "hero1,5", "hero1,5,2", "hero1,5,3", "hero1,5,4"]
        }
        self.is_jumping = False
        self.jump_speed = 0
        self.gravity = 0.8
        self.animation_index = 0
        self.animation_timer = 0

    def draw(self):
        self.actor.draw()

    def update(self, dt, keys):
        # Yön tuşlarına basıldığında hareket et
        if keys["left"]:
            self.actor.x = max(20, self.actor.x - 5)
            if not self.is_jumping:
                self._animate("run", dt)
        elif keys["right"]:
            self.actor.x = min(WIDTH - 20, self.actor.x + 5)
            if not self.is_jumping:
                self._animate("run", dt)
        elif not self.is_jumping:
            self._animate("idle", dt)

        # Space tuşuna basıldığında zıpla
        if keys["jump"] and not self.is_jumping and self.actor.y >= 240:
            self.is_jumping = True
            self.jump_speed = -12
            self.actor.image = self.animations["jump"]

        # Aşağı ok tuşuna basıldığında hero4 animasyonunu göster
        if keys["down"]:
            self.actor.image = "hero4"

        if self.is_jumping:
            self.actor.y += self.jump_speed
            self.jump_speed += self.gravity
            if self.actor.y >= 240:
                self.actor.y = 240
                self.is_jumping = False

    def _animate(self, animation_type, dt):
        if animation_type in self.animations:
            self.animation_timer += dt
            if self.animation_timer > 0.1:
                self.animation_timer = 0
                animation_frames = self.animations[animation_type]
                if isinstance(animation_frames, list):
                    self.animation_index = (self.animation_index + 1) % len(animation_frames)
                    self.actor.image = animation_frames[self.animation_index]
                else:
                    self.actor.image = animation_frames

# Düşmanlar
class Enemy:
    def __init__(self, image, position, speed):
        self.actor = Actor(image, position)
        self.speed = speed

    def draw(self):
        self.actor.draw()

    def update(self):
        self.actor.x -= self.speed
        if self.actor.x < -20:
            self.actor.x = WIDTH + random.randint(20, 100)

# Oyun Durumu
uzayli = Character("hero1", (50, 240))
kutu = Enemy("enemy2", (550, 265), 5)
ari = Enemy("enemy1", (850, 175), 5)
puan = 0
oyun_sonu = False

# Oyun Fonksiyonları
def start_game():
    global game_state, puan, oyun_sonu
    game_state = "playing"
    puan = 0
    oyun_sonu = False
    uzayli.actor.pos = (50, 240)
    kutu.actor.pos = (550, 265)
    ari.actor.pos = (850, 175)

def quit_game():
    exit()

# Menü Butonları
buttons = [
    {"text": "Start", "x": 250, "y": 180, "width": 100, "height": 50, "action": start_game},
    {"text": "Music", "x": 250, "y": 240, "width": 100, "height": 50, "action": toggle_music},
    {"text": "Exit", "x": 250, "y": 300, "width": 100, "height": 50, "action": quit_game}
]

def draw_buttons():
    for button in buttons:
        screen.draw.filled_rect(Rect((button["x"], button["y"], button["width"], button["height"])), "red")
        screen.draw.text(button["text"], center=(button["x"] + button["width"] // 2, button["y"] + button["height"] // 2), color="white")

def on_mouse_down(pos):
    if game_state == "menu":
        for button in buttons:
            rect = Rect((button["x"], button["y"], button["width"], button["height"]))
            if rect.collidepoint(pos):
                button["action"]()

def draw():
    screen.clear()
    if game_state == "menu":
        screen.blit(menu_background_image, (0, 0))
        screen.draw.text("The Platformer", center=(WIDTH // 2, 100), fontsize=50, color="white")
        draw_buttons()
    elif game_state == "playing":
        screen.blit(background_image, (0, 0))
        uzayli.draw()
        kutu.draw()
        ari.draw()
        screen.draw.text(f"Point: {puan}", (10, 10), fontsize=24, color="white")
        if oyun_sonu:
            screen.draw.text("Game Over! Press Enter", center=(WIDTH // 2, HEIGHT // 2), fontsize=36, color="red")

def update(dt):
    global oyun_sonu, puan

    if game_state != "playing":
        return

    if oyun_sonu:
        if keyboard.RETURN:
            start_game()
        return

    keys = {
        "left": keyboard.left or keyboard.a,
        "right": keyboard.right or keyboard.d,
        "jump": keyboard.space,
        "down": keyboard.down  # Aşağı ok tuşu
    }
    uzayli.update(dt, keys)

    kutu.update()
    ari.update()

    # Puan arttırma: Düşmanlar ekranın sol tarafından geçtiğinde
    if kutu.actor.x < -20:
        puan += 1
        kutu.actor.x = WIDTH + random.randint(20, 100)  # Yeniden başlat
    if ari.actor.x < -20:
        puan += 1
        ari.actor.x = WIDTH + random.randint(20, 100)  # Yeniden başlat

    # Çarpışma kontrolü
    if uzayli.actor.colliderect(kutu.actor) or uzayli.actor.colliderect(ari.actor):
        oyun_sonu = True

# Başlangıçta müzik çal
music.play("music")

pgzrun.go()
