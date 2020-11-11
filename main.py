import pygame
import os 
import time
import random
pygame.font.init()



WIDTH = 750
HEIGHT = 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Space Invaders")

# load asset images
# note python constant nameing convention is all CAPS

ENEMY_SHIP_1 = pygame.image.load(os.path.join("assets", "enemy_ship_1.png"))
ENEMY_SHIP_2 = pygame.image.load(os.path.join("assets", "enemy_ship_2.png"))
ENEMY_SHIP_3 = pygame.image.load(os.path.join("assets", "enemy_ship_3.png"))
PLAYER_SHIP = pygame.image.load(os.path.join("assets", "player_ship.png"))

LASER_1 = pygame.image.load(os.path.join("assets", "laser_blue.png"))
LASER_2 = pygame.image.load(os.path.join("assets", "laser_green.png"))
LASER_3 = pygame.image.load(os.path.join("assets", "laser_red.png"))
LASER_PLAYER = pygame.image.load(os.path.join("assets", "laser_yellow.png"))

BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT)) 
# all players will inherit from this class, both enemy and player
# self give access to specific instance
class Ship:
    COOLDOWN = 30 #half fps for fire rate of 2 shots/sec
    def __init__(self, x, y, health= 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
            window.blit(self.ship_img, (self.x, self.y))
            for laser in self.lasers:
                laser.draw(window)
            # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))
    def move_lasers(self, velocity, object):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(object):
                object.health -= 10
                self.lasers.remove(laser)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - self.ship_img.get_width(),self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Player(Ship): # Player inherits from player
    def __init__(self, x, y, health = 100):
        super().__init__(x,y,health)
        self.ship_img = PLAYER_SHIP
        self.laser_img = LASER_PLAYER
        self.mask = pygame.mask.from_surface(self.ship_img)# mask creates pxl perfect hitbox
        self.max_health = health

    def move_lasers(self, velocity, objects):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for object in objects:
                    if laser.collision(object):
                        objects.remove(object)
                        self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health) , 10))

class Enemy(Ship):
    NUMBER_MAP = {
                "one": (ENEMY_SHIP_1, LASER_1),
                "two": (ENEMY_SHIP_2, LASER_2),
                "three": (ENEMY_SHIP_3, LASER_3)
                }

    def __init__(self, x, y,number, health = 100): 
        super().__init__(x,y,health)
        self.ship_img, self.laser_img = self.NUMBER_MAP[number]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity):
        self.y += velocity

class Laser:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self .image = image
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self,height):
        return not self.y <= height and self.y >= 0

    def collision(self, object):
        return collide(object, self)
        
# check if two objects are overriding

def collide(object1, object2):
    offset_x = object2.x - object1.x
    offset_y = object2.y - object1.y
    # returns (x,y) intersection
    return object1.mask.overlap(object2.mask,(offset_x, offset_y)) != None

# main game function
def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)
    player_velocity = 5

    enemies = [] # in python an array(Swift) is a list
    wave_length = 5
    enemy_velocity = 1

    laser_velocity = 4

    # players start game location
    player = Player(350, 630)
    lost = False
    lost_count = 0

    # Note this function will be nested in main function so as to not have to pass on the contants of FPS etc.
    def redraw_window():
        # Note for pygame 0,0 coordnates start at "top left"
        # blit creates a surface for the window or draws one image on another
        WINDOW.blit(BACKGROUND, (0,0))
        # Draw text
        # f string lets you interpolate variable into string
        # the 1 parameter is anti- aliasing, just leave it at 1
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WINDOW.blit(level_label, (10,10))
        WINDOW.blit(lives_label, (WIDTH - lives_label.get_width() - 10, 10))
        

        for enemy in enemies:
            enemy.draw(WINDOW)

        player.draw(WINDOW)

        if lost:
            lost_label = lost_font.render("Game Over", 1, (255,255,255))
                                                      # position:(X,Y)
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    # uses frames to update game
    while run:
        clock.tick(FPS)

        redraw_window()

        if player.health <= 0 or lives <= 0:
            lost = True
            lost_count += 1

        # GameOver Duration atm its 180 frames FPS(60) * 3
        if lost: 
            if lost_count > FPS * 3 :
                run = False
            else:
                continue
        
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["one", "two", "three"]))
                enemies.append(enemy)

        # checks for events at 60hz
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velocity > 0: # left
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH: # right
            player.x += player_velocity
        if keys[pygame.K_s] and player.y - player_velocity + player.get_height() < HEIGHT: # down
            player.y += player_velocity
        if keys[pygame.K_w] and player.y + player_velocity > 0: # up
            player.y -= player_velocity
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]: # NOTE [:] CREATES A COPY OF THE LIST(ARRAY IN SWIFT)
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player)
           
                # gives odds of shooting 25% of the time every second
            if random.randrange(0, 4*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_velocity, enemies)

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    run = True
    while run:
        WINDOW.blit(BACKGROUND, (0,0))
        title_label = title_font.render("Press any key to begin...", 1, (255,255,255))
        WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350)) 

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN: 
                main()

    pygame.quit()
        
        
main_menu()

