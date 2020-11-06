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
class Ship:
    def __init__(self, x, y, health= 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.laser = []
        self.cool_down_counter = 0

    def draw(self, window):
            window.blit(self.ship_img, (self.x, self.y))
            # pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 50, 50))
    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship): # Player inherits from player
    def __init__(self, x, y, health = 100):
        super().__init__(x,y,health)
        self.ship_img = PLAYER_SHIP
        self.laser_img = LASER_PLAYER
        self.mask = pygame.mask.from_surface(self.ship_img)# mask creates pxl perfect hitbox
        self.max_health = health




        

# main game function
def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    level = 1
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    player_velocity = 5

    player = Player(300, 650)

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
        
        player.draw(WINDOW)

        pygame.display.update()

    # uses frames to update game
    while run:
        clock.tick(FPS)
        redraw_window()

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


        
main()

