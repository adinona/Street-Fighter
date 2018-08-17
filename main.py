import pygame
import serge
import badGuy
import badGuyAI
import fireball
import time

pygame.init()
width = 640
height = 480
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pause = False

#screen.set_at((50,100), (0,255,0))

def health_bars(badGuy_health, player_health):
    #health bar changes size and color based on current health
    if player_health > 75:
        player_health_color = (102,204,0)
    elif player_health > 50:
        player_health_color = (255,255,0)
    else:
        player_health_color = (255,0,0)

    if badGuy_health > 75:
        enemy_health_color = (102,204,0)
    elif badGuy_health > 50:
        enemy_health_color = (255,255,0)
    else:
        enemy_health_color = (255,0,0)

    pygame.draw.rect(screen, player_health_color, (535, 60, player_health, 25))
    pygame.draw.rect(screen, enemy_health_color, (85, 60, badGuy_health, 25))

def blastBar(badGuy_health, player_health,blastBarP1,blastBarP2):
    #draws blastBars
        pygame.draw.rect(screen, (0,0,0), (535, 85, blastBarP2, 25))
        pygame.draw.rect(screen, (0,0,0), (85, 85, blastBarP1, 25))

def button(message,x,y,w,h,activeColor,inColor,action= None,font=None,flag=None):
    #takes a font incase message on button to big
    if font == None:
        font = introFont = pygame.font.SysFont("monospace", 40)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
        #uses mouse position to highlight the button
    if ((x+w) > mouse[0] > x) and ((y+h) > mouse[1] > y):
        pygame.draw.rect(screen,activeColor,(x,y,w,h))
        if click[0] == 1 and action != None:
            #each action leads to a different screen
            if action == 'play':
                mainGameAI()
            elif action == 'quit':
                pygame.quit()
                exit(0)
            elif action == 'menu':
                gameIntro()
            elif action == 'twoPlayer':
                mainGame()
            elif action == 'help':
                instruction()
            elif action == 'unpause':
                unPause()

    else:
        pygame.draw.rect(screen,inColor,(x,y,w,h))
    label = font.render(message, 1, (255,255,255))
    screen.blit(label, (x,y))

def gameIntro():
    #menu screen
    backgroundIntro = pygame.image.load('/Users/Aditya/Desktop/CMU 16-17 /112/tp/intro.png')
    backgroundIntro = pygame.transform.scale(backgroundIntro, (width, height))
    introFont = pygame.font.SysFont("monospace", 40)
    intro = True
    while intro:
        for event in pygame.event.get():
            # check if the event is the X button
            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
        screen.fill(0)
        introLabel = introFont.render("Street Fighter", 100, (255,255,255))
        screen.blit(introLabel, (150,50))
        screen.blit(backgroundIntro,(0,0))
        #different modes to play
        button('AI',250,280,200,40,(102,255,102),(102,204,0),'play')
        button('2-Player',250,330,200,40,(102,255,102),(102,204,0),'twoPlayer',
                        pygame.font.SysFont("monospace", 35))
        button('Instructions',250,380,200,40,(102,255,102),(102,204,0),'help',
                        pygame.font.SysFont("monospace", 28))
        button('Quit',250,430,200,40,(204,0,102),(255,0,0),'quit')


        pygame.display.update()

def endScreen(winner,loser,flag):
    #takes in winner and loser to display who won the game
    victory = pygame.image.load('/Users/Aditya/Desktop/CMU 16-17 /112/tp/victory.png')

    victory = pygame.transform.scale(victory, (200, 200))
    end = True
    winnerFont = pygame.font.SysFont("monospace", 50)
    loserFont = pygame.font.SysFont("monospace", 17)


    while end:
        for event in pygame.event.get():
            # check if the event is the X button
            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
        screen.fill(0)
        winnerLabel = winnerFont.render("%s Has Won" %winner, 300,  (255,255,255))
        loserLabel = loserFont.render("%s Better Luck Next Time" %loser, 100, (255,255,255))
        screen.blit(victory,(220,100))
        screen.blit(winnerLabel, (100,50))
        screen.blit(loserLabel, (200,300))

        #different actions that can be performed on this screen
        button('Play Again?',50,350,150,40,(102,255,102),(102,204,0),flag,
                                pygame.font.SysFont("monospace", 20))

        button('Menu',250,350,150,40,(0,128,255),(0,76,153),'menu')

        button('Quit',450,350,150,40,(204,0,102),(255,0,0),'quit')

        pygame.display.update()

def mainGameAI():
    global pause #global allows me to swith between pause and unpause state
    #sets up the players
    player = serge.Serge((100, 200))
    player2 = badGuyAI.BadGuyAI((300, 200))
    #initializes health
    player_health = player.health
    player2_health = player2.health
    myfont = pygame.font.SysFont("monospace", 20)
    label1 = myfont.render("Player 1", 1, (0,0,0))
    label2 = myfont.render("Player 2", 1, (0,0,0))
    mugShot = pygame.image.load('/Users/Aditya/Desktop/CMU 16-17 /112/tp/mug.png')
    background = pygame.image.load("/Users/Aditya/Desktop/CMU 16-17 /112/tp/Bckgrnd0.png")
    background = pygame.transform.scale(background, (width, height))
    direction = ''
    game_over = False
    cooldown = 300
    lastMoveP1 = pygame.time.get_ticks()
    lastMoveP2 = pygame.time.get_ticks()
    flag = 'play' #for play again button at end of game
    countp1 = 0
    countp2 = 0
    blastBarP1 = player.blastBar
    blastBarP2 = player2.blastBar

    while game_over == False:


        for event in pygame.event.get():
            # check if the event is the X button
            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)
                #checks what keys are being held down
            if event.type == pygame.KEYDOWN:
                if event.key == 275:
                    direction = 'left'
                elif event.key== 276:
                    direction = 'right'
                elif event.key== 274:
                    direction = 'up'
                elif event.key== 273:
                    direction = 'down'
                elif event.key == 97:
                    direction = 'a'
                elif event.key == 100:
                    direction = 'd'
                elif event.key == 119:
                    direction = 'w'
                elif event.key == 115:
                    direction = 's'
                elif event.key == 27:
                    pause = True
                    paused()
                elif event.key == 115:
                    direction = 'Notblast'
                elif event.key == 47:
                    direction = 'Notp2blast'

                #checks what keys are not being held down
            if event.type == pygame.KEYUP:
                if event.key == 275:
                    direction = 'aleft'
                elif event.key== 276:
                    direction = 'aright'
                elif event.key== 274:
                    direction = 'aup'
                elif event.key== 273:
                    direction = 'adown'
                elif event.key == 97:
                    direction = 'aa'
                elif event.key == 100:
                    direction = 'ad'
                elif event.key == 119:
                    direction = 'aw'
                elif event.key == 115:
                    direction = 'as'
                elif event.key == 115:
                    direction = 'Notblast'
                elif event.key == 47:
                    direction = 'Notp2blast'
        #intializes fireballs position

        if countp1 == 0:
            blastPos = [player.rect.x+150,player.rect.y+180]
        if countp2 == 0:
            blastPosP2 = [player2.rect.x+150,player2.rect.y+180]

        player.handle_event(event)
        screen.fill(0)
        screen.blit(background,(0,0))
        screen.blit(player.image, player.rect)
        screen.blit(player2.image, player2.rect)
        screen.blit(mugShot,(50,50))
        screen.blit(mugShot,(500,50))
        screen.blit(label1, (50,30))
        screen.blit(label2, (500,30))
        health_bars(player_health,player2_health)
        blastBar(player_health, player2_health,blastBarP1,blastBarP2)
        player2.whereOpponentIs(player.rect.x) #AI for player2\
        #adds to blast bar based on health of ooponent and time
        if blastBarP1 <= 100:
            blastBarP1+= .5

        if blastBarP2 <= 100:
            blastBarP2+=.5

        if player_health == 75:
            if blastBarP2 + 10 > 100:
                blastBarP2 = 100
            else:
                blastBarP2 += 10

        if player_health == 50:
            if blastBarP2 + 20 > 100:
                blastBarP2 = 100
            else:
                blastBarP2 += 20

        if player2_health == 75:
            if blastBarP1 + 10 > 100:
                blastBarP1 = 100
            else:
                blastBarP1 += 10

        if player2_health == 50:
            if blastBarP1 + 20 > 100:
                blastBarP1 = 100
            else:
                blastBarP1 += 20
        #checks for player1's blasts and its collision
        if direction == 'blast':
            if blastBarP1 > 100:
                countp1 += 1
                specialAttack = fireball.Fireball(blastPos)
                screen.blit(specialAttack.blast,blastPos)
                if countp1 ==1:
                    time.sleep(1)
                blastPos[0] += 10
                if specialAttack.blastRect.x == player2.rect.x + 100:
                    if player2_health == 0:
                        player2_health -= 0
                    player2_health -= 20
                    blastBarP1 = 0
                    del specialAttack
                    if player2_health ==0:
                        endScreen('Player 1','Player 2',flag)

        if direction == 'p2blast':
            countp2 += 1
            specialAttack = fireball.Fireball(blastPosP2)
            screen.blit(specialAttack.blast,blastPosP2)
            if count ==1:
                time.sleep(1)
            blastPos[0] -= 10
            if specialAttack.blastRect.x == player1.rect.x + 100:
                if player2_health == 0:
                    player2_health -= 0
                player2_health -= 20
                del specialAttack
                if player2_health ==0:
                    endScreen('Player 1','Player 2',flag)

        #checks for player1's puch and kick collisions
        if pygame.sprite.collide_rect(player, player2):
            player2.collision = True
            now1 = pygame.time.get_ticks()

            if ((direction == 'up' or direction == 'down')):
                if (now1 - lastMoveP1) >= cooldown:
                    lastMoveP1 = now1
                    if player2_health == 0:
                        player2_health -= 0
                    player2_health -= 5
            if player2_health ==0:
                endScreen('Player 1','Player 2',flag)

        #checks for player2's puch and kick collisions

        if pygame.sprite.collide_rect(player2, player):
            player2.collision = True
            player2.whereOpponentIs(player.rect.x)
            now2 = pygame.time.get_ticks()
            if (direction == 'w' or direction == 's' or
             (player2.move == 2 and player.rect.x < player2.rect.x) or
                (player2.move == 3 and player.rect.x < player2.rect.x)):
                if (now2 - lastMoveP2) >= cooldown:
                    lastMoveP2 = now2
                    if player_health == 0:
                        player_health -= 0
                    player_health -= 5
            if player_health ==0:
                endScreen('Player 2','Player 1',flag)
        player2.collision = False

        clock.tick(10)
        pygame.display.flip()

def mainGame():

        global pause#global allows me to swith between pause and unpause state
        #sets up the players
        player = serge.Serge((100, 200))
        player2 = badGuy.BadGuy((300, 200))
        player_health = player.health
        player2_health = player2.health
        myfont = pygame.font.SysFont("monospace", 20)
        label1 = myfont.render("Player 1", 1, (0,0,0))
        label2 = myfont.render("Player 2", 1, (0,0,0))
        mugShot = pygame.image.load('/Users/Aditya/Desktop/CMU 16-17 /112/tp/mug.png')
        background = pygame.image.load("/Users/Aditya/Desktop/CMU 16-17 /112/tp/Bckgrnd0.png")
        background = pygame.transform.scale(background, (width, height))
        direction = ''
        game_over = False
        cooldown = 300
        lastMoveP1 = pygame.time.get_ticks()
        lastMoveP2 = pygame.time.get_ticks()
        times = clock.tick(10)
        flag = 'twoPlayer'
        countp1 = 0
        countp2 = 0
        blastBarP1 = player.blastBar
        blastBarP2 = player2.blastBar


        while game_over == False:


            for event in pygame.event.get():
                # check if the event is the X button
                if event.type==pygame.QUIT:
                    # if it is quit the game
                    pygame.quit()
                    exit(0)
                    #checks for key press
                if event.type == pygame.KEYDOWN:
                    if event.key == 275:
                        direction = 'left'
                    elif event.key== 276:
                        direction = 'right'
                    elif event.key== 274:
                        direction = 'up'
                    elif event.key== 273:
                        direction = 'down'
                    elif event.key == 97:
                        direction = 'a'
                    elif event.key == 100:
                        direction = 'd'
                    elif event.key == 119:
                        direction = 'w'
                    elif event.key == 115:
                        direction = 's'
                    elif event.key == 27:
                        pause = True
                        paused()
                    elif event.key == 47:
                        direction = 'blast'
                    elif event.key == 115:
                        direction = 'p2blast'

                    #checks for keys that arent pressed
                if event.type == pygame.KEYUP:
                    if event.key == 275:
                        direction = 'Notleft'
                    elif event.key== 276:
                        direction = 'Notright'
                    elif event.key== 274:
                        direction = 'Notup'
                    elif event.key== 273:
                        direction = 'Notdown'
                    elif event.key == 97:
                        direction = 'Nota'
                    elif event.key == 100:
                        direction = 'Notd'
                    elif event.key == 119:
                        direction = 'Notw'
                    elif event.key == 115:
                        direction = 'Nots'
                    elif event.key == 47:
                        direction = 'Notblast'
                    elif event.key == 115:
                        direction = 'Notp2blast'

            #intialize fire ball
            if countp1 == 0:
                blastPos = [player.rect.x+150,player.rect.y+180]
            if countp2 == 0:
                blastPosP2 = [player2.rect.x+150,player2.rect.y+180]

            player.handle_event(event)
            player2.handle_event(event)
            screen.fill(0)
            screen.blit(background,(0,0))
            screen.blit(player.image, player.rect)
            screen.blit(player2.image, player2.rect)
            screen.blit(mugShot,(50,50))
            screen.blit(mugShot,(500,50))
            screen.blit(label1, (50,30))
            screen.blit(label2, (500,30))
            health_bars(player_health,player2_health)
            blastBar(player_health, player2_health,blastBarP1,blastBarP2)
        #adds to blast bar based on health of ooponent and time

            if blastBarP1 <= 100:
                blastBarP1+= .5

            if blastBarP2 <= 100:
                blastBarP2+=.5

            if player_health == 75:
                if blastBarP2 + 10 > 100:
                    blastBarP2 = 100
                else:
                    blastBarP2 += 10

            if player_health == 50:
                if blastBarP2 + 20 > 100:
                    blastBarP2 = 100
                else:
                    blastBarP2 += 20

            if player2_health == 75:
                if blastBarP1 + 10 > 100:
                    blastBarP1 = 100
                else:
                    blastBarP1 += 10

            if player2_health == 50:
                if blastBarP1 + 20 > 100:
                    blastBarP1 = 100
                else:
                    blastBarP1 += 20







            #moves fire ball and checks for collision
            if direction == 'blast':
                if blastBarP1 > 100:
                    countp1 += 1
                    specialAttack = fireball.Fireball(blastPos)
                    screen.blit(specialAttack.blast,blastPos)
                    if countp1 ==1:
                        time.sleep(1)
                    blastPos[0] += 10
                    if specialAttack.blastRect.x == player2.rect.x + 100:
                        if player2_health == 0:
                            player2_health -= 0
                        player2_health -= 20
                        blastBarP1 = 0
                        del specialAttack
                        if player2_health ==0:
                            endScreen('Player 1','Player 2',flag)

            if direction == 'p2blast':
                countp2 += 1
                specialAttack = fireball.Fireball(blastPosP2)
                screen.blit(specialAttack.blast,blastPosP2)
                if count ==1:
                    time.sleep(1)
                blastPos[0] -= 10
                if specialAttack.blastRect.x == player1.rect.x + 100:
                    if player2_health == 0:
                        player2_health -= 0
                    player2_health -= 20
                    del specialAttack
                    if player2_health ==0:
                        endScreen('Player 1','Player 2',flag)

                #Checks for puch and kick collisions
            if pygame.sprite.collide_rect(player, player2):
                player2.collision = True
                now1 = pygame.time.get_ticks()

                if ((direction == 'up' or direction == 'down')):
                    if (now1 - lastMoveP1) >= cooldown:
                        lastMoveP1 = now1
                        if player2_health == 0:
                            player2_health -= 0
                        player2_health -= 5
                if player2_health ==0:
                    endScreen('Player 1','Player 2',flag)

            if pygame.sprite.collide_rect(player2, player):
                player2.collision = True
                now2 = pygame.time.get_ticks()
                if (direction == 'w' or direction == 's'):
                    if (now2 - lastMoveP2) >= cooldown:
                        lastMoveP2 = now2
                        if player_health == 0:
                            player_health -= 0
                        player_health -= 5
                if player_health ==0:
                    endScreen('Player 2','Player 1',flag)
            player2.collision = False

            clock.tick(10)
            pygame.display.flip()

def instruction():
        instructions = pygame.image.load('/Users/Aditya/Desktop/CMU 16-17 /112/tp/instructions.png')
        instructions = pygame.transform.scale(instructions, (150, 150))
        bulletPoint = pygame.image.load('/Users/Aditya/Desktop/CMU 16-17 /112/tp/bulletPoint.png')
        bulletPoint = pygame.transform.scale(bulletPoint, (20, 20))
        end = True
        font = pygame.font.SysFont("monospace", 20)



        while end:
            for event in pygame.event.get():
                # check if the event is the X button
                if event.type==pygame.QUIT:
                    # if it is quit the game
                    pygame.quit()
                    exit(0)
            screen.fill((255,255,255))
            #messages
            movingMsgPt1 = "Use the left and Right arrow keys to move p1"
            movingMsgPt2 = "Use the 'a' and 'd' keys to move second p2"
            attackMsgPt1 = "Up key kicks and  Down key punches with p1"
            attackMsgPt2 = "'w' key kicks and 's' key punches with p2"
            specialMove1 = "'?' key will activate special move when bar is full p1"
            specialMove2 = "'q' key will activate special move when bar is full p2"
            pause = "Pressing escape key will pause the game"
            label1 = font.render(movingMsgPt1,300,(0,0,0))
            label2 = font.render(movingMsgPt2, 300, (0,0,0))
            label3 = font.render(attackMsgPt1, 300, (0,0,0))
            label4 = font.render(attackMsgPt2, 300, (0,0,0))
            label5 = font.render(specialMove1, 300, (0,0,0))
            label6 = font.render(specialMove2, 300, (0,0,0))

            label7 = font.render(pause, 300, (0,0,0))
            #puts them on the screen
            screen.blit(instructions,(220,10))
            screen.blit(label1, (35,160))
            screen.blit(bulletPoint,(10,160))
            screen.blit(label2, (35,190))
            screen.blit(bulletPoint,(10,190))
            screen.blit(label3, (35,220))
            screen.blit(bulletPoint,(10,220))
            screen.blit(label4, (35,250))
            screen.blit(bulletPoint,(10,250))
            screen.blit(label5, (35,280))
            screen.blit(bulletPoint,(10,280))
            screen.blit(label6, (35,310))
            screen.blit(bulletPoint,(10,310))
            screen.blit(label7, (35,340))
            screen.blit(bulletPoint,(10,340))


            button('Menu',220,370,150,40,(102,255,102),(102,204,0),'menu',
                                    pygame.font.SysFont("monospace", 20))



            pygame.display.update()

def paused():
    #pauses sceen in-game
    largeText = pygame.font.SysFont("comicsansms",115)
    pauseLabel = largeText.render("Paused" , 100, (255,255,255))
    #instructions = largeText.render("Press Continue to resume or Quit to exit" ,
    #                100, (255,255,255))
    screen.blit(pauseLabel,(160,100))
    #screen.blit(instructions,(220,150))


    while pause:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        #gameDisplay.fill(white)


        button('Continue',50,430,200,40,(102,255,102),(102,204,0),'unpause')
        button('Quit',350,430,200,40,(204,0,102),(255,0,0),'menu')
        pygame.display.update()
        clock.tick(15)

def unPause():
     #unpauses screen
    global pause
    pause = False

gameIntro()
pygame.quit ()
