import pygame

class Fireball(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.blast = pygame.image.load('/Users/Aditya/Desktop/CMU 16-17 /112/tp/fireballs.png')
        #intializes rect for fireball image
        self.blastRect = self.blast.get_rect()
        self.blastRect.topleft = position

        self.flag = False

#moves fireball
    def move(self,direction):
        print(self.blastRect.x)
        self.blastRect.x += direction
