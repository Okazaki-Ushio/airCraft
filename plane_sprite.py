import pygame


class GameSprite(pygame.sprite.Sprite):

    def __init__(self, image_name, speed=2):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
