import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports

# Global Variables for the game
FPS = 32
SCREENWIDTH = 289 
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8 #638.75
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = r'D:\Flappy Bird\Gallary\sprites\bird.png'
BACKGROUND = r'D:\Flappy Bird\Gallary\sprites\background.png'
PIPE= r'D:\Flappy Bird\Gallary\sprites\pipe.png'

def welcomeScreen():
    """
    Shows welcome images on the screen
    """

    playerx = int(SCREENWIDTH/5) #57.8  
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2) #at center of screen
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.0003) 
    basex = 0 
    while True:
        for event in pygame.event.get(): #get event from the queue
            # if user clicks on cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return # at main screen 
            else: 
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery)) 
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))     #draw one image onto another
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))    
                    
                pygame.display.update()
                FPSCLOCK.tick(FPS) #to control the FPS

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe() # a list
    newPipe2 = getRandomPipe() # a list

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -4 #to create the illusion 

    playerVelY = -9 # player fall down and get some acc and min vel =-8
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping


    while True: #game loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0: #player in screen
                    playerVelY = playerFlapAccv #playerFlapAccv = -8
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes) # This function will return true if the player is crashed
        if crashTest:
            return     

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2 # center position of player 
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2 #center of pipe
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"Your score is {score}") 
                GAME_SOUNDS['point'].play()


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY # increase velocity of player 

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight) # min(+no., 0) so that it doesnt get outside the base 
        

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width(): # as it turns -ve
            
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height()  - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe






if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's  modules
    FPSCLOCK = pygame.time.Clock() #create an object to help track time
    pygame.display.set_caption('Flappy Bird')
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load(r'D:\Flappy Bird\Gallary\sprites\0.png').convert_alpha(), #convert alpha is used to adjust the pixels for easy blitting
        pygame.image.load(r'D:\Flappy Bird\Gallary\sprites\1.png').convert_alpha(),
        pygame.image.load(r'D:\Flappy Bird\Gallary\sprites\2.png').convert_alpha(),
        pygame.image.load(r'D:\Flappy Bird\Gallary\sprites\3.png').convert_alpha(),
        pygame.image.load(r'D:\Flappy Bird\Gallary\sprites\4.png').convert_alpha(),
        pygame.image.load(r'D:\Flappy Bird\Gallary\sprites\5.png').convert_alpha(),
        pygame.image.load(r'D:\Flappy Bird\Gallary\sprites\6.png').convert_alpha(),
        pygame.image.load(r'D:\Flappy Bird\Gallary\sprites\7.png').convert_alpha(),
        pygame.image.load(r'D:\Flappy Bird\Gallary\sprites\8.png').convert_alpha(),
        pygame.image.load(r'D:\Flappy Bird\Gallary\sprites\9.png').convert_alpha(),
    )
    
    GAME_SPRITES['message']=pygame.image.load(r'D:\Flappy Bird\Gallary\sprites\message.png').convert_alpha()
    GAME_SPRITES['base'] =pygame.image.load(r'D:\Flappy Bird\Gallary\sprites\base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )
    
    GAME_SOUNDS['die']=pygame.mixer.Sound(r'D:\Flappy Bird\Gallary\audio\die.wav')
    GAME_SOUNDS['hit']=pygame.mixer.Sound(r'D:\Flappy Bird\Gallary\audio\hit.wav')
    GAME_SOUNDS['point']=pygame.mixer.Sound(r'D:\Flappy Bird\Gallary\audio\point.wav')
    GAME_SOUNDS['swoosh']=pygame.mixer.Sound(r'D:\Flappy Bird\Gallary\audio\swoosh.wav')
    GAME_SOUNDS['wing']=pygame.mixer.Sound(r'D:\Flappy Bird\Gallary\audio\wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() # Shows welcome screen to the user until he presses a button
        mainGame() # This is the main game function 
