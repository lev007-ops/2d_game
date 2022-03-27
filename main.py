# Pygame шаблон - скелет для нового проекта Pygame
import sys
from time import sleep
import pygame
import os

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

WIDTH = 600  # ширина игрового окна
HEIGHT = 600  # высота игрового окна
FPS = 30  # частота кадров в секунду

# Цвета (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

background_image = pygame.image.load(os.path.join(img_folder,
                                                  'background.png')).convert()


class Sprite(pygame.sprite.Sprite):
    speed = 4
    def __init__(self, x_size=100, y_size=100, x=200, y=200, image=None,
                 color=BLACK):
        """Инициализация объекта

        Args:
            x_size (int, optional): размер по x. Defaults to 100.
            y_size (int, optional): размер по y. Defaults to 100.
            x (int, optional): позиция x. Defaults to 500.
            y (int, optional): позиция y. Defaults to 500.
            image (str, optional): картинка для спрайта. Defaults to None.
            color (str, optional): цвет. Defaults to BLACK.
        """
        pygame.sprite.Sprite.__init__(self)
        if image is None:
            self.image = pygame.Surface((x_size, y_size))
            self.image.fill(color)
        else:
            img = pygame.transform.scale(pygame.image.load(
                os.path.join(img_folder, image)
            ), (x_size, y_size))
            self.image = img

        self.rect = self.image.get_rect()
        self.rect.size = (x_size, y_size)
        self.rect.x = x
        self.rect.y = y


class Player(Sprite):
    speed = 4

    coins = 0

    def __is_collide(self):
        return (pygame.sprite.spritecollide(self, walls, False) or
                self.rect.x == -4 or self.rect.y == -4 or
                self.rect.x == WIDTH - 80 or self.rect.y == HEIGHT - 80)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.__is_collide():
                self.rect.x += self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.__is_collide():
                self.rect.x -= self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            if self.__is_collide():
                self.rect.y += self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            if self.__is_collide():
                self.rect.y -= self.speed

        if pygame.sprite.spritecollide(self, coins, True):
            self.coins += 1
            print(f'Монеток собрано - {self.coins}')
        print(self.rect.x, self.rect.y)


class Enemy(Sprite):
    def update(self) -> None:
        if self.rect.colliderect(player):
            sleep(1)
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)


player = Player(image='player.png', x=20)
wall = Sprite(x_size=10, y_size=500, y=100)
wall2 = Sprite(x_size=10, y_size=500, y=0, x=340)
wall2 = Sprite(x_size=10, y_size=500, y=0, x=340)
wall3 = Sprite(x_size=100, y_size=10, y=400, x=500)
wall4 = Sprite(x_size=100, y_size=10, y=250, x=340)
coin = Sprite(50, 50, 250, 300, 'coin.png')
coin2 = Sprite(50, 50, 310, 530, 'coin.png')
finis_coin = Sprite(50, 50, 390, 170, 'coin.png')
bomb = Enemy(20, 70)
walls = pygame.sprite.Group()
coins = pygame.sprite.Group()
coins.add(coin, coin2, finis_coin)
walls.add(wall, wall2, wall3, wall4)
all_sprites.add(wall, player, wall2, coin, wall3, wall4, coin2,
                finis_coin, bomb)

# Цикл игры
running = True
finish = False
while running:
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False
    # Обновление

    # Визуализация (сборка)

    # Ренлеринг всех отрисованных объектов (После него объекты не добавлять)
    screen.blit(background_image, [0, 0])
    if not finish:
        player.update()
        all_sprites.draw(screen)

        if player.coins == 3:
            finish = True
            background_image = pygame.transform.scale(pygame.image.load(os.path.join(img_folder,
                                                                                     'winner.jpg')).convert(), [WIDTH, HEIGHT])

        bomb.update()

    pygame.display.flip()
