import pygame
from pygame.locals import *
import socket
import pickle

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
        pygame.draw.rect(g, self.color, (self.x - camera_x, self.y, self.width, self.height), 0)

    def jump(self):
        self.velocity_y = self.jump_velocity

    def update(self):
        self.velocity_y += self.gravity
        self.y += self.velocity_y

        if self.y >= 500 - self.height:
            self.y = 500 - self.height
            self.velocity_y = 0
        if self.y <= 0:
            self.y = 0
            self.velocity_y = 0

class Obstacle:
    width = 50
    gap = 200  

    def __init__(self, x, gap_y):
        self.x = x
        self.gap_y = gap_y
        self.top_height = self.gap_y
        self.bottom_height = 500 - self.gap_y - self.gap

    def draw(self, g, camera_x):
        pygame.draw.rect(g, (37, 55, 101), (self.x - camera_x, 0, self.width, self.top_height), 0)
        pygame.draw.rect(g, (37, 55, 101), (self.x - camera_x, self.gap_y + self.gap, self.width, self.bottom_height), 0)

class Game:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.player = Player(50, h // 2)
        self.obstacles = []
        self.score = 0
        self.canvas = Canvas(self.width, self.height, "Flappy Bird")
        self.camera_x = 0
        self.last_obstacle_x = 0
        self.server_address = ('172.28.1.81', 12345)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(self.server_address)

    def send_message(self, message):
        try:
            self.client_socket.sendall(message.encode())
            data = self.client_socket.recv(4096)
            return pickle.loads(data)
        except Exception as e:
            print("Error sending/receiving data:", e)
            return None

    def generate_obstacles(self):
        return self.send_message("generate_obstacles")

    def run(self):
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

            self.player.update()
            self.camera_x = self.player.x - self.width // 3

            self.obstacles = self.generate_obstacles()

            self.canvas.draw_background()
            for obstacle in self.obstacles:
                obstacle.draw(self.canvas.get_canvas(), self.camera_x)
            self.player.draw(self.canvas.get_canvas(), self.camera_x)

            self.canvas.update()

        pygame.quit()

class Canvas:
    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(name)

    def update(self):
        pygame.display.update()

    def draw_background(self):
        self.screen.fill((135, 206, 250))

    def get_canvas(self):
        return self.screen

def main():
    pygame.init()
    game = Game(800, 500)
    game.run()

if __name__ == "__main__":
    main()
