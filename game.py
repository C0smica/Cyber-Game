import pygame
from pygame.locals import *
import random

class Player:
    width = height = 50
    jump_velocity = -8
    gravity = 0.6

    def __init__(self, startx, starty, color=(134, 188, 56)):
        self.startx = startx
        self.starty = starty
        self.x = startx
        self.y = starty
        self.velocity_y = 0
        self.color = color

    def draw(self, g, camera_x):
        # Draws the player on the screen.
        pygame.draw.rect(g, self.color, (self.x - camera_x, self.y, self.width, self.height), 0)

    def jump(self):
        # Handles player jumping.
        self.velocity_y = self.jump_velocity

    def update(self):
        # Updates player position and applies gravity.
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        # Collision detection with top and bottom boundaries
        if self.y >= 500 - self.height:
            self.y = 500 - self.height
            self.velocity_y = 0
        if self.y <= 0:
            self.y = 0
            self.velocity_y = 0

class Obstacle:
    width = 50
    gap = 200  # Gap between top and bottom obstacles

    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y
        self.top_height = self.gap_y
        self.bottom_height = 500 - self.gap_y - self.gap

    def draw(self, g, camera_x):
        # Draws the obstacle on the screen.
        pygame.draw.rect(g, (37, 55, 101), (self.x - camera_x, 0, self.width, self.top_height), 0)
        pygame.draw.rect(g, (37, 55, 101), (self.x - camera_x, self.gap_y + self.gap, self.width, self.bottom_height), 0)

    def collide(self, player):
        # Checks collision between player and obstacle.
        if (player.x + player.width >= self.x and player.x <= self.x + self.width) and (
                player.y <= self.top_height or player.y + player.height >= self.gap_y + self.gap):
            return True
        return False

class Game:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.player = Player(50, h // 2)
        self.obstacles = []
        self.score = 0  # Initialize score to zero
        self.canvas = Canvas(self.width, self.height, "Sky Jumper") #Cool name
        self.camera_x = 0
        self.last_obstacle_x = 0

    def generate_obstacles(self):
        # Generates new obstacles.
        gap_y = random.randint(100, self.height - Obstacle.gap - 100)
        min_x = max(self.width // 2, self.last_obstacle_x + 150)  # Ensure obstacle appears within visible area
        x = min_x + random.randint(5, 10)  # Smaller distance between obstacles
        self.obstacles.append(Obstacle(x, gap_y))
        self.last_obstacle_x = x

    def restart(self):
        # Resets the game.
        self.player.x = self.player.startx
        self.player.y = self.player.starty
        self.obstacles.clear()
        self.score = 0  # Reset score to zero
        self.last_obstacle_x = 0

    def run(self):
        # Main game loop.
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        run = False
                    if event.key == K_SPACE:
                        self.player.jump()
                    if event.key == K_r:
                        self.restart()

            self.player.update()
            self.camera_x = self.player.x - self.width // 3

            if random.randint(0, 100) < 2:
                self.generate_obstacles()

            for obstacle in self.obstacles:
                if obstacle.collide(self.player):
                    self.restart()
                    break

            for obstacle in self.obstacles:
                if self.player.x > obstacle.x + obstacle.width and self.player.x < obstacle.x + obstacle.width + 2:
        # Increment score if player successfully passed an obstacle
                    self.score += 1


            # Update obstacle positions
            for obstacle in self.obstacles:
                obstacle.x -= 2

            # Remove obstacles that are far enough past the visible area
            self.obstacles = [obstacle for obstacle in self.obstacles if obstacle.x + obstacle.width > -200]

            self.canvas.draw_background()
            for obstacle in self.obstacles:
                obstacle.draw(self.canvas.get_canvas(), self.camera_x)
            self.player.draw(self.canvas.get_canvas(), self.camera_x)

            # Display score on the screen
            self.canvas.draw_text("Score: " + str(self.score), 20, 10, 10)

            self.canvas.update()

        pygame.quit()

class Canvas:
    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(name)

    def update(self):
        # Updates the display.
        pygame.display.update()

    def draw_background(self):
        # Draws the background.
        self.screen.fill((135, 206, 250))

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (255, 255, 255))
        self.screen.blit(render, (x, y))

    def get_canvas(self):
        # Returns the screen.
        return self.screen

def main():
    pygame.init()
    game = Game(800, 500)  # Adjusted height to 500px
    game.run()

if __name__ == "__main__":
    main()
