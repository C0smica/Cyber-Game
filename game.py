import pygame
from pygame.locals import *
import socket

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
        self.canvas = Canvas(self.width, self.height, "Sky Jumper")
        self.camera_x = 0
        self.last_obstacle_x = 0
        self.server_address = ("172.28.1.81", 36695)  

    def send_message(self, message):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(self.server_address)
            client_socket.sendall(message.encode())
            data = client_socket.recv(1024)
            return data.decode()

    def generate_obstacles(self):
        reply = self.send_message("generate_obstacles")
        print("Received obstacle data:", reply)
        data = reply.split(':')
        if len(data) == 2:
            gap_y, x = map(int, data)
            self.obstacles.append(Obstacle(x, gap_y))
        else:
            print("Invalid data received:", reply)

    def check_collision(self):
        reply = self.send_message("check_collision")
        return reply == "collision"

    def update_score(self):
        self.send_message("update_score")

    def restart(self):
        self.player.x = self.player.startx
        self.player.y = self.player.starty
        self.obstacles.clear()
        self.score = 0
        self.last_obstacle_x = 0

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
                    if event.key == K_r:
                        self.restart()

            self.player.update()
            self.camera_x = self.player.x - self.width // 3

            for obstacle in self.obstacles:
                if obstacle.collide(self.player):
                    self.restart()
                    break

            self.canvas.draw_background()
            for obstacle in self.obstacles:
                obstacle.draw(self.canvas.get_canvas(), self.camera_x)
            self.player.draw(self.canvas.get_canvas(), self.camera_x)

            self.canvas.draw_text("Score: " + str(self.score), 20, 10, 10)

            self.canvas.update()

            # Check if player passed an obstacle
            for obstacle in self.obstacles:
                if obstacle.x + obstacle.width < self.player.x and obstacle.x + obstacle.width > self.player.x - 2:
                    self.score += 1
                    self.generate_obstacles()  # Request new obstacles from the server

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

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (255, 255, 255))
        self.screen.blit(render, (x, y))

    def get_canvas(self):
        return self.screen

def main():
    pygame.init()
    game = Game(800, 500)
    game.run()

if __name__ == "__main__":
    main()
