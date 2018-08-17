#adapted this code from the tutorial link below
#http://xorobabel.blogspot.com/2012/10/pythonpygame-2d-animation-jrpg-style.html


import pygame
import time
import random

class BadGuyAI(pygame.sprite.Sprite):
    def __init__(self, position):

        self.lastPunch = pygame.time.get_ticks()
        self.lastKick = pygame.time.get_ticks()
        self.lastBlast = pygame.time.get_ticks()
        self.cooldown = 200
        self.sheet = pygame.image.load('/Users/Aditya/Desktop/CMU 16-17 /112/tp/Ken.png').convert_alpha()
        self.sheet.set_clip(pygame.Rect(0, 110, 120, 110)) #903
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.rotate(self.image,180)
        self.rect = self.image.get_rect()
        self.rect = self.rect.inflate(-self.rect.width*.6,-self.rect.height*.45)
        self.rect.topleft = position
        self.health = 100
        self.frame = 0
        #25
        self.kick_states = {  1: (240, 2420, 120, 110), 2:(360, 2420, 120, 110),
                            3: (240, 110, 120, 110)}#,7: (240, 110, 120, 110)}

        self.right_states =  {1: (0, 110, 120, 110), 2: (120, 110, 120, 110),
                                        3:(240, 110, 120, 110) }

        self.punch_states = { 1: (120, 2200, 120, 110), 2: (240, 2200, 120, 110),
                                    3: (240, 110, 120, 110)  }

        self.blast_states = { 1: (0, 3300, 120, 110),2: (120, 3300, 120, 110),
                                    3:(240, 110, 120, 110)}
        self.count = 0
        self.collision = False
        self.move = -1
        self.blastBar = 0

#23

    #gets what part of the animation
    #http://xorobabel.blogspot.com/2012/10/pythonpygame-2d-animation-jrpg-style.html
    #Method below from link
    def get_frame(self, frame_set):
        self.frame+= 1
        if self.frame > (len(frame_set)):
            self.frame = 1
        return frame_set[self.frame]

    #uses the dictionary of images and sends it to
    #get_frame to get exact image
    #http://xorobabel.blogspot.com/2012/10/pythonpygame-2d-animation-jrpg-style.html
    #Method below from link
    def clip(self, clipped_rect):

        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))

        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect
#AI method
    def whereOpponentIs(self,xPos):

        xPos = xPos + 100
        self.move = random.randint(0, 5)
        #uses random ints to decide move
        if self.count == 0:
            self.count +=1

        # if player is to the left of the AI
        #make 4 special blast
        if ( xPos < self.rect.x) and self.count > 0:
            #moves if AI the the right of player
            if self.move == 1 or self.move == 2:
                self.update('left')

            if self.move == 5:
                self.rect.x += 0

            if self.move == 3:
                self.rect.x -= 2

        # if player is colliding with player and is going to punch
        if self.move == 2 and self.collision ==True:

            self.update('down')
            self.update('down')
            self.update('down')

    # if player is colliding with player and is going to kick

        if self.move == 3 and self.collision ==True:

            self.update('up')
            self.update('up')
            self.update('up')

        if self.move == 4 and self.collision ==True:

            self.rect.x -=5

        # if player is to the right of the AI
        if ( xPos > self.rect.x) and self.count > 0:
            #moves if AI the the left of player

            if self.move == 1 or self.move == 2:
                self.update('right')

            if self.move == 5:
                self.rect.x += 0

            if self.move == 3:
                self.rect.x -=2


    def update(self, direction):
        if direction == 'left':
            self.clip(self.right_states)
            self.rect.x -= 5

        if direction == 'right':
            self.clip(self.right_states)
            self.rect.x += 5

        if direction == 'up':
            now = pygame.time.get_ticks()
            if now - self.lastKick >= self.cooldown:
                self.lastKick = now
                self.clip(self.kick_states)

        if direction == 'down':
            now = pygame.time.get_ticks()
            if now - self.lastPunch >= self.cooldown:
                #so player cant continously attack
                self.lastPunch = now
                self.clip(self.punch_states)
        if direction == 'blast':
            now = pygame.time.get_ticks()
            if now - self.lastBlast >= self.cooldown:
                self.lastBlast = now
                self.clip(self.blast_states)


        #flips image to face opponent
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.rotate(self.image,180)
