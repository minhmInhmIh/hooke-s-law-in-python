import math
import pygame
import random

WIDTH,HEIGHT = 800,800
FPS = 60
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)

GRAVITY = 9.8
ball_vel = [0,0]

coil_width = 100
coil_height = coil_width/4
number_of_coil = 5

Ball_mass = 35

spring_top = HEIGHT - (coil_height*5)
spring_topPos = [WIDTH/2, spring_top]
# spring_constant = float(input)

spring_border = pygame.Rect(WIDTH/2-coil_width/2, spring_top, coil_width, coil_height*9)

targetRadius = 30
targetX = (random.randint(0+targetRadius,800- targetRadius))
targetY = (random.randint(0+targetRadius,675-targetRadius))




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
        self.vel[1] += self.GRAVITY
        self.pos[1] += self.vel[1]

        if self.pos[1] + self.radius > spring_top:
            self.pos[1] = spring_top - self.radius
            self.vel[1] = 0
            self.launched = False
            spring.released = False

ball = Ball(coil_width/4, Ball_mass, RED)
compression_length = coil_height * number_of_coil 

ball_x = WIDTH / 2
ball_y = HEIGHT + coil_height - (coil_height * 5 * 2) - ball.radius

height_needed = ball_y - targetY

print(f"Target center: {(targetX, targetY)}")
print(f"Ball start: {(ball_x, ball_y)}")
print(f"Ball mass: {Ball_mass} kg")
print(f"Spring compression: {compression_length}")
print(f"Height needed: {height_needed}")

correct_move = targetX - ball_x
correct_k = (2 * Ball_mass * GRAVITY * height_needed) / (compression_length ** 2)

player_move = float(input("How far should the spring move? left = -, right = +: "))
player_k = float(input("Calculate spring constant k: "))

move_tolerance = targetRadius
k_tolerance = 1

if abs(player_move - correct_move) > move_tolerance:
    print("Wrong horizontal movement. You lose.")
    exit()

if abs(player_k - correct_k) > k_tolerance:
    print("Wrong spring constant. You lose.")
    exit()

print("Correct! Press SPACE to test your launch.")

spring = Spring(player_k, compression_length)
spring.move = player_move


def draw(window):
    window.fill(BLACK)
    ball.update_ball()
    spring.draw(window)
    ball.draw(window)
    if (
    not spring_border.collidepoint(targetX-targetRadius, targetY)
    and not spring_border.collidepoint(targetX+targetRadius, targetY)
    and not spring_border.collidepoint(targetX, targetY-targetRadius)
    and not spring_border.collidepoint(targetX, targetY+targetRadius)
):
        pygame.draw.circle(window,GREEN, (targetX,targetY), targetRadius, 5)
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
