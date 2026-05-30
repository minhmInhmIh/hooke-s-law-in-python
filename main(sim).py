import math
import pygame
import random

WIDTH,HEIGHT = 800,800
FPS = 60

player_k = float(input("Enter spring constant k: "))

WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)

GRAVITY = 9.8
AIR_DENSITY = 1.225
DRAG_COEFICIENT = 0.47
ball_vel = [0,0]

coil_width = 100
coil_height = coil_width/4
number_of_coil = 5

Ball_mass = 100

spring_top = HEIGHT - (coil_height*5)

PIXEL_PER_METER = 100




class Spring:
    def __init__(self, constant, compression):
        self.constant = constant
        self.compression = compression
        self.force = constant*compression
        self.launchVel = math.sqrt((constant*compression**2)/Ball_mass)
        self.compressed = False
        self.released = False
        self.move = 0
    def draw(self, window):
        if self.compressed:
            for i in range(1,number_of_coil+1):
                self.coil = pygame.Rect(WIDTH/2-coil_width/2 + self.move, HEIGHT-(coil_height*i), coil_width, coil_height)
                pygame.draw.rect(window, WHITE, self.coil)
        else:
            for i in range(1,6):
                self.coil = pygame.Rect(WIDTH/2-coil_width/2 + self.move, HEIGHT+coil_height-(coil_height*i*2), coil_width, coil_height)
                pygame.draw.rect(window, WHITE, self.coil)

class Ball:
    GRAVITY = 9.8
    def __init__(self,radius,mass,color):
        self.radius = radius
        self.mass = mass
        self.color = color
        self.pos = None
        self.vel = [0,0]


        self.launched = False

    def update_ball(self):
        if not spring.released:
            if spring.compressed:
                self.pos = [WIDTH/2 + spring.move,HEIGHT-(coil_height*5) - self.radius]
            else:
                self.pos = [WIDTH/2 + spring.move ,HEIGHT+coil_height-(coil_height*5*2)-self.radius]
    def draw(self,window):
        pygame.draw.circle(window, self.color, (self.pos[0],self.pos[1]),self.radius)
    def launch(self, vel):
        if not self.launched:
            self.vel[1] = -vel
            self.launched = True
    def fall(self):
        radius_m = self.radius / PIXEL_PER_METER
        area = math.pi*radius_m**2

        dragForce = 0.5 * AIR_DENSITY * self.vel[1]**2 * DRAG_COEFICIENT * area
        dragAcc = dragForce/ self.mass

        if self.vel[1] < 0:
            self.vel[1] += dragAcc
        elif self.vel[1] > 0:
            self.vel[1] -= dragAcc
        
        self.vel[1] += self.GRAVITY
        self.pos[1] += self.vel[1]

        if self.pos[1] + self.radius > spring_top:
            self.pos[1] = spring_top - self.radius
            self.vel[1] = 0
            self.launched = False
            spring.released = False
        print(f"{-self.vel[1]} m/s")

ball = Ball(coil_width/4, Ball_mass, RED)
compression_length = coil_height * number_of_coil 



spring = Spring(player_k, compression_length)


def draw(window):
    window.fill(BLACK)
    ball.update_ball()
    spring.draw(window)
    ball.draw(window)
    pygame.display.flip()

def main(window):
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    spring.compressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    spring.compressed = False
                    spring.released = True
                # if event.key == pygame.K_DOWN:
                #     spring.compressed = True
                # if event.key == pygame.K_SPACE:
                #     spring.compressed = False
                #     spring.released = True
        draw(window)
        if spring.released:
            if spring.force > ball.mass*9.8:
                ball.launch(spring.launchVel)
                ball.fall()

    pygame.quit()
if __name__ == "__main__":
    main(WINDOW)
