import pygame as pg
import random
from os import path

vec = pg.math.Vector2

TITLE = "idkWhatToPutHereIGuessThis'llDoForNow"
WIDTH = 800
HEIGHT = 450
FPS = 60
#FONT_NAME ="Acknowledge TT (BRK)"
FONT_NAME = "Arial"
HS_FILE = "highscore.txt"
SPRITESHEET = "SheetoSprites.png"

img_dir = path.join(path.dirname(__file__), 'img')

# (x, y, w, h)
PLATFORM_LIST1 = [(-800, HEIGHT + 400),
                #start platform
                (400, HEIGHT - 230),
                # left 2
                (-800, HEIGHT + 150),
                #left 1
                (-470, HEIGHT + 280),
                #middle
                (470, HEIGHT + 280),
                #right 1
                (2500, HEIGHT + 280),
                #right 2
                (2300, HEIGHT + 150)]

GO_LIST = ["This Was Your Fault",
           "You Died",
           "You Are Died",
           "They Don't Seem To Like You",
           "You Have Dead",
           "This Was Not Your Fault"]

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DEEP_BLUE = (0, 2, 43)

PLAYER_ACC = 7.0
PLAYER_FRICTION = -0.7
PLAYER_GRAV = 0.5
PLAYER_JUMP = 18


class Game:
   def __init__(self):
       # creates window
       pg.init()
       pg.mixer.init()
       self.screen = pg.display.set_mode((WIDTH, HEIGHT))
       pg.display.set_caption(TITLE)
       self.clock = pg.time.Clock()
       self.running = True
       self.font_name = pg.font.match_font(FONT_NAME)
       self.load_data()

   def load_data(self):
       #loads game assets from folder
       self.dir = path.dirname(__file__)
       img_dir = path.join(self.dir, 'img')
       self.background = pg.image.load(path.join(img_dir, "Nacht_Himmel.png")).convert()
       self.background_rect = self.background.get_rect()
       self.dir = path.dirname(__file__)
       with open(path.join(self.dir, HS_FILE), 'w') as f:
           try:
               self.highscore = int(f.read())
           except:
               self.highscore = 0
        #load spritesheet image
       self.spritesheet = Spritesheet(path.join(img_dir, SPRITESHEET))

   def new(self):
       # start a new game
       self.score = 0
       self.all_sprites = pg.sprite.Group()
       self.platforms = pg.sprite.Group()
       self.items = pg.sprite.Group()
       self.player = Player(self)
       self.all_sprites.add(self.player)
       for plat in PLATFORM_LIST1:
           # P = Platform(plat[0], plat[1], plat[2], plat[3])
           p = Platform(self,*plat)
           self.all_sprites.add(p)
           self.platforms.add(p)
       self.run()

   def run(self):
       # game loop
       self.playing = True
       while self.playing:
           self.clock.tick(FPS)
           self.events()
           self.update()
           self.draw()

   def update(self):
       self.all_sprites.update()
       # check for platform
       if self.player.vel.y > 0:
           hits = pg.sprite.spritecollide(self.player, self.platforms, False)
           if hits:
               lowest = hits[0]
               for hit in hits:
                   if hit.rect.bottom > lowest.rect.bottom:
                       lowest = hit
               if self.player.pox.x < lowest.rect.right + 5 and self.player.pos.x > lowest.rect.left + 5:
                    if self.player.pos.y < lowest.rect.bottom:
                        #self.player.pos.y = hits[0].rect.top
                        self.player.pos.y = lowest.rect.top + 1
                        self.player.vel.y = 0
                        self.player.jumping = False
       # scrolls the screen to follow player
       if self.player.rect.top <= HEIGHT / 2:
           self.player.pos.y += abs(self.player.vel.y)
           for plat in self.platforms:
               plat.rect.y += abs(self.player.vel.y)
       if self.player.rect.top >= HEIGHT / 2:
           self.player.pos.y -= abs(self.player.vel.y)
           for plat in self.platforms:
               plat.rect.y -= abs(self.player.vel.y)
       if self.player.rect.right <= 400:
           self.player.pos.x += abs(self.player.vel.x)
           for plat in self.platforms:
               plat.rect.x += abs(self.player.vel.x)
       if self.player.rect.right >= 405:
           self.player.pos.x -= abs(self.player.vel.x)
           for plat in self.platforms:
               plat.rect.x -= abs(self.player.vel.x)

       if self.player.rect.bottom > HEIGHT:
           self.playing = False

   def events(self):
       for event in pg.event.get():
           if event.type == pg.QUIT:
               if self.playing:
                   self.playing = False
               self.running = False
           if event.type == pg.KEYDOWN:
               if event.key == pg.K_SPACE:
                   self.player.jump()
           if event.type == pg.KEYUP:
               if event.key == pg.K_SPACE:
                   self.player.jump_cut()

   def draw(self):
       self.screen.fill(BLACK)
       self.screen.blit(self.background, self.background_rect)
       self.all_sprites.draw(self.screen)
       self.screen.blit(self.player.image, self.player.rect)
       self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 15)
       pg.display.flip()

   def show_start_screen(self):
       # start screen
       #("text", size, color, x, y)
       self.screen.fill(DEEP_BLUE)
       self.screen.fill(BLACK)
       self.draw_text("TELEPORT", 40, WHITE, WIDTH / 2, HEIGHT / 4)
       self.draw_text("CHOOSE CHARACTER TO START", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
       self.draw_text("HIGH SCORE: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
       pg.display.flip()
       self.wait_for_key()

   def show_go_screen(self):
       # game over screen
       if not self.running:
           return
       self.screen.fill(DEEP_BLUE)
       self.draw_text(random.choice(GO_LIST))
       self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
       self.draw_text("CHOOSE CHARACTER TO START AGAIN", 22., WHITE, WIDTH / 2, HEIGHT * 3 / 4)
       if self.score > self.highscore:
           self.highscore = self.score
           with open(path.join(self.dir, HS_FILE), 'w') as f:
               f.write(str(self.score))
       pg.display.flip()
       self.wait_for_key()

   def wait_for_key(self):
       #keeps start and g.o. screen on screen until corresponding key is pressed
       waiting = True
       while waiting:
           self.clock.tick(FPS)
           for event in pg.event.get():
               if event.type == pg.QUIT:
                   waiting = False
                   self.running = False
               if event.type == pg.KEYDOWN:
                   if event.key == pg.K_z:
                       waiting = False
                   if event.key == pg.K_x:
                       waiting = False
                   if event.key == pg.K_c:
                       waiting = False
                   if event.key == pg.K_v:
                       waiting = False
                   if event.key == pg.K_SPACE:
                       waiting = False

   def draw_text(self, text, size, color, x, y):
       font = pg.font.Font(self.font_name, size)
       text_surface =font.render(text, True, color)
       text_rect = text_surface.get_rect()
       text_rect.midtop = (x, y)
       self.screen.blit(text_surface, text_rect)

class Spritesheet:
    #loads and parses spritesheets
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        #image = pg.transform.scale(image, (width * 2, height * 2))
        return image

class Player(pg.sprite.Sprite):
   def __init__(self, game):
       pg.sprite.Sprite.__init__(self)
       self.game = game
       self.run = False
       self.jumping = False
       self.current_frame = 0
       self.last_update = 0
       self.load_images()
       #loads player sprite (x, y, width, height)
       self.image = self.standing_frame[0]
       #self.player_img = pg.image.load(path.join(img_dir, "Survivor.png")).convert()
       #self.image = pg.transform.scale(self.player_img, (0, 0))
       #self.image = self.player_img
       self.image.set_colorkey(BLACK)
       self.rect = self.image.get_rect()
       self.rect.center = (WIDTH / 2, HEIGHT / 2)
       self.pos = vec(WIDTH / 2, HEIGHT / 2)
       self.vel = vec(0, 0)
       self.acc = vec(0, 0)

   def load_images(self):
       self.standing_frame = [self.game.spritesheet.get_image(0, 0, 28, 22)]
       self.run_frames_l = [self.game.spritesheet.get_image(0, 26, 28, 20),
                             self.game.spritesheet.get_image(0, 50, 28, 20),
                             self.game.spritesheet.get_image(0, 72, 28, 22),
                             self.game.spritesheet.get_image(0, 96, 28, 22),
                             self.game.spritesheet.get_image(0, 122, 28, 20),
                             self.game.spritesheet.get_image(0, 146, 28, 20),
                             self.game.spritesheet.get_image(0, 168, 28, 22),
                             self.game.spritesheet.get_image(0, 192, 28, 22)]
       self.run_frames_r = []
       for frame in self.run_frames_l:
           self.run_frames_r.append(pg.transform.flip(frame, True, False))
       self.jump_frame = self.game.spritesheet.get_image(0, 216, 28, 22)

   def jump_cut(self):
       if self.jumping:
           if self.vel.y < -3:
               self.vel.y = -3


   def jump(self):
       # will jump only on platform
       self.rect.x += 2
       hits = pg.sprite.spritecollide(self, self.game.platforms, False)
       self.rect.x -= 2
       if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -PLAYER_JUMP

   def update(self):
       self.animate()
       self.acc = vec(0, PLAYER_GRAV)
       keys = pg.key.get_pressed()
       if keys[pg.K_LEFT]:
           self.acc.x = -PLAYER_ACC
       if keys[pg.K_RIGHT]:
           self.acc.x = PLAYER_ACC

       # player friction
       self.acc.x += self.vel.x * PLAYER_FRICTION

       self.vel += self.acc
       if abs(self.vel.x) < 0.3:
           self.vel.x = 0
       self.pos += self.vel + 0.5 * self.acc

       if self.pos.x > WIDTH:
           self.pos.x = 0
       if self.pos.x < 0:
           self.pos.x = WIDTH

       self.rect.midbottom = self.pos

   def animate(self):
       now = pg.time.get_ticks()
       if self.vel.x != 0:
           self.run = True
       else:
           self.run = False
       #walk animation
       if self.run:
           if now - self.last_update > 250:
               self.last_update = now
               self.current_frame = (self.current_frame + 1) % len(self.run_frames_l)
               bottom = self.rect.bottom
               if self.vel.x > 0:
                   self.image = self.run_frames_r[self.current_frame]
               else:
                   self.image = self.run_frames_l[self.current_frame]
               self.rect = self.image.get_rect()
               self.rect.bottom = bottom

class Platform(pg.sprite.Sprite):
   def __init__(self, game, x, y):
       self.groups = game.all_sprites, game.platforms
       pg.sprite.Sprite.__init__(self)
       self.game = game
       images = [#platform xml co-ords
                ]
       self.image = random.choice(images)
       self.image.set_colorkey(BLACK)
       self.rect = self.image.get_rect()
       self.rect.x = x
       self.rect.y = y

class Item(pg.sprite.Sprite):
   def __init__(self, game, plat):
       self.groups = game.all_sprites, game.items
       pg.sprite.Sprite.__init__(self, self.groups)
       self.game = game
       self.plat = plat
       self.type = random.choice([#Standard Items
                                  'Thick Dew', 'Thornquill', 'Shock Bracelet',
                                  'Illicit Acquisitions', 'Bronze Monocle',
                                  #Priority Items
                                  'Antique Dollar Bill', 'Potent Brew', 'Eclipse Dagger',
                                  'Civilian Taser', 'Box o Wonders',
                                  #Fragile Items
                                  "Family Ruby", "Broken Watch",
                                  "Purple Amulet", "Regenerophage Sample",
                                  #Military Items
                                  "Portable AI Mines", "Defective Tesla Gun",
                                  "Targeting System Scope", "Wrist Mounted Micro Cannon",
                                  "Portable AT Mine Layer"])
       self.image.set_colorkey(BLACK)
       self.rect = self.image.get_rect()
       self.rect.centerx = self.plat.rect.centerx
       self.rect.bottom = self.plat.rect.top - 5

   def update(self):
       self.rect.bottom = self.plat.rect.top - 5

class Muk(pg.sprite.Sprite):
   def __init__(self):
       pg.sprite.Sprite.__init__(self)
       self.image = pg.Surface((30, 40))
       self.image.fill(GREEN)
       self.rect = self.image.get_rect()
       self.rect.x = random.randrange(WIDTH + self.rect.width)
       self.rect.y = random.randrange(-100, -40)
       self.speedy = 3

   def update(self):
       self.rect.x += self.speedy


g = Game()
g.show_start_screen()
while g.running:
   g.new()
   g.show_go_screen

pg.quit()
