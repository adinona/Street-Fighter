#adapted this code from the tutorial link below
#http://xorobabel.blogspot.com/2012/10/pythonpygame-2d-animation-jrpg-style.html


import pygame
import time

class Serge(pygame.sprite.Sprite):
    def __init__(self, position):
        self.lastPunch = pygame.time.get_ticks()
        self.lastKick = pygame.time.get_ticks()
        self.lastBlast = pygame.time.get_ticks()
        self.cooldown = 200
        self.sheet = pygame.image.load('/Users/Aditya/Desktop/CMU 16-17 /112/tp/Ken.png').convert_alpha()
        self.sheet.set_clip(pygame.Rect(0, 110, 120, 110))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-self.rect.width*.6,-self.rect.height*.45)
        self.health = 100
        self.rect.topleft = position #intializes top of rectangle
        self.frame = 0
        self.blastBar = 1
        #al the animations images
        self.kick_states = {  1: (240, 2420, 120, 110), 2:(360, 2420, 120, 110),
                                3: (240, 110, 120, 110)}#,7: (240, 110, 120, 110)}

        self.right_states =  {1: (0, 110, 120, 110), 2: (120, 110, 120, 110),
                                        3:(240, 110, 120, 110) }

        self.punch_states = { 1: (120, 2200, 120, 110), 2: (240, 2200, 120, 110),
                                    3: (240, 110, 120, 110)  }

        self.blast_states = { 1: (0, 3300, 120, 110),2: (120, 3300, 120, 110),
                                    3:(240, 110, 120, 110)}
        self.flag = True

        #gets what part of the animation
    def get_frame(self, frame_set):
        self.frame+= 1

        if self.frame > (len(frame_set)):
            self.frame = 1

        return frame_set[self.frame]

        #uses the dictionary of images and sends it to
        #get_frame to get exact image
    def clip(self, clipped_rect):

        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))

        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    def update(self, direction):
        #does different animations and changes positions based on key
        if direction == 'left':
            self.clip(self.right_states)
            self.rect.x -= 5
        if direction == 'right':
            self.clip(self.right_states)
            self.rect.x += 5
        if direction == 'up':
        #so player cant continously attack
            now = pygame.time.get_ticks()
            if now - self.lastKick >= self.cooldown:
                self.lastKick = now
                self.clip(self.kick_states)
                self.rect.x -= 0
        if direction == 'down':
            now = pygame.time.get_ticks()
            if now - self.lastPunch >= self.cooldown:
                self.lastPunch = now
                self.clip(self.punch_states)
                self.rect.y += 0
        if direction == 'blast':
            now = pygame.time.get_ticks()
            if now - self.lastBlast >= self.cooldown:
                self.lastBlast = now
                self.clip(self.blast_states)

        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image = pygame.transform.scale(self.image, (300, 300))



    def handle_event(self, event):
        if event.type == pygame.QUIT:
            game_over = True
            #sees what key has been pressed
        if event.type == pygame.KEYDOWN:
            if (pygame.key.get_pressed()[pygame.K_LEFT]) != 0:
                self.update('left')
            if (pygame.key.get_pressed()[pygame.K_RIGHT]) != 0:
                self.update('right')
            if (pygame.key.get_pressed()[pygame.K_UP]) != 0:
                self.update('up')
            if (pygame.key.get_pressed()[pygame.K_DOWN]) != 0 :
                self.update('down')
            if (pygame.key.get_pressed()[47]) != 0 :
                self.update('blast')

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                self.update('stand_left')
            if event.key == pygame.K_RIGHT:
                self.update('stand_right')
            if event.key == pygame.K_UP:
                self.update('stand_up')
            if event.key == pygame.K_DOWN:
                self.update('stand_down')
            if event.key == pygame.K_DOWN:
                self.update('stand_blast')
