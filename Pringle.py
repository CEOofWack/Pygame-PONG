#Welcome to PONG Pygame! Made by Bisher A with help of
#Real Python's Pygame tutorial and Tech with Tim's PONG tutorial for collision
#and calculations
#as well as Vincent from our class. Thank you!

#Import the pygame module
import pygame

#Initialize pygame
pygame.init()

#Import pygame.locals for access to key coordinates
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
#Width and height of the screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

#Variables for points
points1 = 0
points2 = 0

#Initialize initial ball position
ball_position = (500 , 300)
player1_position = (50 , 270)
player2_position = (920 , 270)

BLACK = (0, 0, 0)

#Initialize font
font1 = pygame.font.Font(None, 50)
score1 = font1.render(f"{points1}", True, BLACK)
score2 = font1.render(f"{points2}", True ,BLACK)

#The surface drawn on the screen is now an attribute of 'player'
#Initializes players' paddles within the class 'player'
class player(pygame.sprite.Sprite):
    def __init__(self, position, up_key, down_key):
        super(player, self).__init__()
        self.surf = pygame.Surface((20, 120))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(topleft=position)
        self.up_key = up_key
        self.down_key = down_key
    def update(self, keys1):
        if keys1[self.up_key]:
            self.rect.move_ip(0, -5)
        if keys1[self.down_key]:
            self.rect.move_ip(0, 5)
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
#Initializes ball and ball attributes within the class 'ball'
class ball(pygame.sprite.Sprite):
    max_speed = 2
    def __init__(self, position , x, y, radius):
        super(ball, self).__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.x_speed = self.max_speed
        self.y_speed = 0
        self.radius = 15
        self.diameter = self.radius * 2
        self.surf = pygame.Surface((self.diameter, self.diameter))
        self.surf.fill((0, 0, 0))
        pygame.draw.circle(self.surf, (0, 0, 0), (self.radius, self.radius), self.radius)
        self.rect = self.surf.get_rect(center = (500,300))

    #Initialize movement speed
    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.rect.center = (self.x, self.y)

    #Handles ball colision relative to ball with paddles as well as walls
    def handle_collision(self, ball, player1, player2):
        if ball.y + ball.radius >= SCREEN_HEIGHT:
            ball.y_speed *= -1
        elif ball.y - ball.radius <= 0:
            ball.y_speed *= -1
        if ball.x_speed < 0:
            if player1.rect.top <= ball.y <= player1.rect.bottom:
                if ball.x - ball.radius <= player1.rect.right:
                    self.x_speed *= -1
                    middle_y = player1.rect.y - player1.rect.height/2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (player1.rect.height / 2) / ball.max_speed
                    y_speed = difference_in_y / reduction_factor
                    ball.y_speed = -1 * y_speed
        else:
            if ball.y >= player2.rect.y and ball.y <= player2.rect.y + player2.rect.height:
                if ball.x + ball.radius >= player2.rect.x:
                    ball.x_speed *= -1
                    middle_y = player2.rect.y - player2.rect.height / 2
                    difference_in_y = middle_y - ball.y
                    reduction_factor = (player1.rect.height / 2) / ball.max_speed
                    y_speed = difference_in_y / reduction_factor
                    ball.y_speed = -1 *y_speed





#Start up a screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
x = SCREEN_WIDTH / 2
y = SCREEN_HEIGHT / 2

#Set screen caption
pygame.display.set_caption('CS GO')

#Set input keys for players
player1 = player((50, 270), pygame.K_w, pygame.K_s)
player2 = player((920, 270), K_UP, K_DOWN )

#Ball position
ball = ball((500,300) ,500, 300,15)

#Variable to keep the main loop running
running = True

#Main loop
while running:
    clock = pygame.time.Clock()
    clock.tick(120)
    # or loop through the event queue
    for event in pygame.event.get():
        #Check for KEYDOWN event
        if event.type == KEYDOWN:
            #If the Esc key is pressed, then exit the main loop
            if event.key == K_ESCAPE:
                running = False
        #Check for QUIT event. If QUIT, then set running to false.
        elif event.type == QUIT:
            running = False
    #Get the pressed keys and store them in their respective variables
    keys1 = pygame.key.get_pressed()
    keys2 = pygame.key.get_pressed()
    #Update the keys based on input
    player1.update(keys1)
    player2.update(keys2)

    #Screen white colour
    screen.fill((255, 255, 255))
    #Draw first player
    screen.blit(player1.surf, player1.rect)
    #Draw second player
    screen.blit(player2.surf, player2.rect)
    #Draw ball
    screen.blit(ball.surf, ball.rect)

    #Move and handle ball colision
    ball.move()
    ball.handle_collision(ball, player1, player2)

    #Return ball to initial posistion when scored and add to points2
    if ball.x < 0:
        points2 += 1
        ball.x = 500
        ball.y = 300
        player1.rect.x = 50
        player2.rect.y = 270
        player2.rect.x = 920
        player1.rect.y = 270
        ball.move()

    #Return ball to initial posistion when scored and add to points1
    elif ball.x > 1000:
        points1 += 1
        ball.x = 500
        ball.y = 300
        player1.rect.x = 50
        player2.rect.y = 270
        player2.rect.x = 920
        player1.rect.y = 270
        ball.move()

    #Render fonts for score and draw score
    score1 = font1.render(f"{points1}", True, (0, 0, 0))
    score2 = font1.render(f"{points2}", True, (0, 0, 0))
    screen.blit(score1, (70, 0))
    screen.blit(score2, (SCREEN_WIDTH - 100, 0))





    #Updates the display
    pygame.display.flip()

#Quits game when ended
pygame.quit()
