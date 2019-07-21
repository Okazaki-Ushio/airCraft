import random
from plane_sprite import *

CREATE_ENEMY = pygame.USEREVENT
FIRE = pygame.USEREVENT + 1


class PlaneGame(object):
    SCREEN_HEIGHT = 700
    SCREEN_WIDTH = 480

    def __init__(self):
        self.screen = pygame.display.set_mode((PlaneGame.SCREEN_WIDTH, PlaneGame.SCREEN_HEIGHT))
        self.__create_sprites__()
        pygame.time.set_timer(CREATE_ENEMY, 1000)
        pygame.time.set_timer(FIRE, 500)
        self.clock = pygame.time.Clock()
        self.time = 60

    def start_game(self):
        while True:
            self.clock.tick(self.time)
            self.__event_handler()
            self.__check_collide()
            self.__update()
            pygame.display.update()

    def __check_collide(self):
        pygame.sprite.groupcollide(self.enemy_group, self.bullet_group, True, True)
        # TODO
        over_list = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(over_list) > 0:
            self.__game_over__()

    def __update(self):
        self.back_group.update()
        self.back_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.bullet_group.update()
        self.bullet_group.draw(self.screen)

    def __create_sprites__(self):
        self.back = Background()
        self.back1 = Background()
        self.back1.rect.y = -PlaneGame.SCREEN_HEIGHT
        self.back_group = pygame.sprite.Group(self.back, self.back1)
        self.enemy_group = pygame.sprite.Group()
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        self.bullet_group = pygame.sprite.Group()

    def __event_handler(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over__()
            elif event.type == CREATE_ENEMY:
                self.enemy = Enemy()
                self.enemy_group.add(self.enemy)
            elif event.type == FIRE:
                for i in (0, 1, 2):
                    self.bullet = Bullet()
                    self.bullet.rect.centerx = self.hero.rect.centerx
                    self.bullet.rect.y = self.hero.rect.y - i * 15
                    self.bullet_group.add(self.bullet)
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.hero.speed = 5
        elif key_pressed[pygame.K_LEFT]:
            self.hero.speed = -5
        else:
            self.hero.speed = 0

    @staticmethod
    def __game_over__():
        print("game over")
        pygame.quit()
        exit()


class Background(GameSprite):

    def __init__(self):
        super().__init__("./images/background.png")

    def update(self):
        super().update()
        if self.rect.y > PlaneGame.SCREEN_HEIGHT:
            self.rect.y = -PlaneGame.SCREEN_HEIGHT


class Enemy(GameSprite):
    state = 0

    def __init__(self):
        super().__init__("./images/enemy1.png")
        self.speed = random.randint(1, 3)
        self.rect.x = random.randint(0, PlaneGame.SCREEN_WIDTH - 57)
        self.rect.y = 0

    def update(self):
        if self.state == 0:
            super().update()
            if self.rect.y > PlaneGame.SCREEN_HEIGHT:
                self.kill()
        elif self.state in (1, 2, 3, 4):
            super().__init__("./images/enemy1_down%d.png" % self.state, 0)
            super().update()
        else:
            self.kill()
            super().update()


class Hero(GameSprite):

    def __init__(self):
        super().__init__("./images/me1.png")
        self.rect.bottom = PlaneGame.SCREEN_HEIGHT - 50
        self.rect.centerx = PlaneGame.SCREEN_WIDTH / 2
        self.speed = 0
        self.clock = pygame.time.Clock()

    def update(self):
        self.rect.x += self.speed
        if self.rect.x <= 0:
            self.rect.x = 0
        elif self.rect.x >= PlaneGame.SCREEN_WIDTH - 102:
            self.rect.x = PlaneGame.SCREEN_WIDTH - 102


class Bullet(GameSprite):

    def __init__(self):
        super().__init__("./images/bullet1.png", -7)

    def update(self):
        super().update()
        if self.rect.y <= 0:
            self.kill()


if __name__ == '__main__':
    play_game = PlaneGame()
    play_game.start_game()
