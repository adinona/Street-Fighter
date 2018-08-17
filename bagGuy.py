#adapted this code from the tutorial link below
#http://xorobabel.blogspot.com/2012/10/pythonpygame-2d-animation-jrpg-style.html


import pygame

class BadGuy(pygame.sprite.Sprite):
    def __init__(self, position):
        self.sheet = pygame.image.load('/Users/Aditya/Desktop/CMU 16-17 /112/tp/Ken.png').convert()
        self.sheet.set_clip(pygame.Rect(0, 110, 120, 110)) #903
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect()
        self.health = 100
        self.rect.topleft = position
        self.frame = 0
        #25
        self.kick_states = { 0: (0, 2420, 120, 110), 1: (120, 2420, 120, 110), 2: (240, 2420, 120, 110),
                                3:(360, 2420, 120, 110),4: (480, 2420, 120, 110),
                                5: (600, 2420, 120, 110),6: (720, 2420, 120, 110),7: (240, 110, 120, 110)}
        self.right_states = { 0: (0, 110, 120, 110), 1: (120, 110, 120, 110), 2: (240, 110, 120, 110)}
                                    #3:(260,110,120, 110)}
        #self.up_states = { 0: (0, 228, 120, 110), 1: (52, 228, 120, 110), 2: (156, 228, 120, 110) }
        #self.down_states = { 0: (0, 0, 120, 110), 1: (52, 0, 120, 110), 2: (156, 0, 120, 110) }

    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]

    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect

    def update(self, direction):
        if direction == 'a':
            self.clip(self.right_states)
            self.rect.x -= 5
        if direction == 'd':
            self.clip(self.right_states)
            self.rect.x += 5
        if direction == 'w':
            self.clip(self.kick_states)
            self.rect.x -= 0
        if direction == 's':
            #self.clip(self.down_states)
            self.rect.y += 0

        #if direction == 'stand_left':
        #    self.clip(self.kick_states[0])

        #if direction == 'stand_right':
        #    self.clip(self.right_states[0])
        #if direction == 'stand_left':
        #    self.clip(self.right_states[0])
        #if direction == 'stand_up':
        #    self.clip(self.up_states[0])
        #if direction == 'stand_down':
            #self.clip(self.down_states[0])

        self.image = self.sheet.subsurface(self.sheet.get_clip())

    def is_collided_with(self, sprite):
        print(pygame.sprite.collide_mask(sprite, sprite))
        #print(sprite.rect)
        return pygame.sprite.collide_mask(sprite, sprite)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_A:
                self.update('a')
            if event.key == pygame.K_D:
                self.update('d')
            if event.key == pygame.W:
                self.update('w')
            if event.key == pygame.S:
                self.update('s')

        if event.type == pygame.KEYUP:

            if event.key == pygame.K_LEFT:
                self.update('stand_left')
            if event.key == pygame.K_RIGHT:
                self.update('stand_right')
            if event.key == pygame.K_UP:
                self.update('stand_up')
            if event.key == pygame.K_DOWN:
                self.update('stand_down')
