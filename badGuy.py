


import pygame

class BadGuy(pygame.sprite.Sprite):
    def __init__(self, position):
        self.lastPunch = pygame.time.get_ticks()
        self.lastKick = pygame.time.get_ticks()
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
        self.blastBar = 1
        #25
        self.kick_states = {  1: (240, 2420, 120, 110), 2:(360, 2420, 120, 110),
                        3: (240, 110, 120, 110)}#,7: (240, 110, 120, 110)}

        self.right_states =  {1: (0, 110, 120, 110), 2: (120, 110, 120, 110),
                                3:(240, 110, 120, 110) }

        self.punch_states = { 1: (120, 2200, 120, 110), 2: (240, 2200, 120, 110),
                            3: (240, 110, 120, 110)  }

        self.blast_states = { 1: (0, 3300, 120, 110),2: (120, 3300, 120, 110),
                            3:(240, 110, 120, 110)}
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
        if direction == 'down':
            now = pygame.time.get_ticks()
            if now - self.lastPunch >= self.cooldown:
                self.lastPunch = now
                self.clip(self.punch_states)

        #keeps flipping image so facing player 1
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.image = pygame.transform.flip(self.image, False, True)
        self.image = pygame.transform.rotate(self.image,180)


    def handle_event(self, event):
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            #does even based on key press
            if (pygame.key.get_pressed()[97] != 0):
                self.update('left')
            if (pygame.key.get_pressed()[100] != 0):
                self.update('right')
            if (pygame.key.get_pressed()[119] != 0):
                self.update('up')
            if (pygame.key.get_pressed()[115] != 0):
                self.update('down')


        if event.type == pygame.KEYUP:

            if event.key == 97:
                self.update('stand_left')
            if event.key == 100:
                self.update('stand_right')
            if event.key == 119:
                self.update('stand_up')
            if event.key == 115:
                self.update('stand_down')
