import pygame, math, pygame.mixer, random
from pygame.locals import *

# Initializes with players position, with default speed 200
class missile:
    def __init__(self, posX, posY):
        self.posX = posX + 11
        self.posY = posY - 40
        self.speed = 750
        self.delay = 2000
        self.image = missileImg
        # self.distance is used to see how long the missile has traveled. Missiles with distance over N will be deleted
        self.distance = 0

# Initializes with enemies position
class enemy:
    def __init__(self, enemyPosX, enemyPosY):
        self.posX = enemyPosX
        self.posY = enemyPosY
        # Used to track downward movement. So it wouldn't descent forever
        self.distanceY = 0
        self.speed = 100
        self.hp = 100
        self.image = enemyObj


# Goes through missileList and uses every missiles variables to draw them
def drawMissiles(missileList):
        for lazor in missileList:
            DISPLAY.blit(lazor.image, (lazor.posX, lazor.posY))
            
# Goes through enemyList and uses every enemies position to draw them
def drawEnemies(enemyList):
    for baddies in enemyList:
        baddies.image.get_rect(center=(baddies.posX, baddies.posY))
        DISPLAY.blit(baddies.image, (baddies.posX, baddies.posY))
        pygame.draw.line(DISPLAY, RED, (baddies.posX, baddies.posY - 5), (baddies.posX + 50, baddies.posY - 5), 5)
        pygame.draw.line(DISPLAY, GREEN, (baddies.posX, baddies.posY - 5), (baddies.posX + baddies.hp / 2, baddies.posY - 5), 5)
        

def drawText(textList):
    for messages in textList:
        fontObj = pygame.font.Font(messages[5], messages[1])
        textObj = fontObj.render(messages[0], True, messages[2], messages[6])
        DISPLAY.blit(textObj, (messages[3], messages[4]))

def say(message, size , color, x, y, font = "freesansbold.ttf"):
        fontObj = pygame.font.Font(font, size)
        textObj = fontObj.render(message, True, color)
        DISPLAY.blit(textObj, (x, y))    

# Required to make pyGame work     
pygame.init()
pygame.mixer.init()

# Setting colour constants
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PINK = (255, 0, 255)
GREY = (128, 128, 128)
DARK_GREEN = (0, 128, 0)
GREEN = (0, 255, 0)
DARK_RED = (128, 0, 0)
DARK_BLUE = (0, 0, 128)
DARK_YELLOW = (128, 128, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)
SILVER = (192, 192, 192)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)
YELLOW = (255, 255,  0)

# Trying to remove magic number
FPS = 30
windowWidth = 640
windowHeigth = 480
borderPadding = 40

# Lists are used to keep track of items in them. Lists are passed into the drawing methods
missileList = []
enemyList = []
textList = []

# Creates the canvas to draw and blit images onto
DISPLAY = pygame.display.set_mode((windowWidth, windowHeigth), 0, 32)

bgObj = pygame.image.load('bg.png').convert()
enemyObj = pygame.image.load("orange_alien.png").convert_alpha()
enemyObj = pygame.transform.scale(enemyObj, (50, 50))
missileImg = pygame.image.load("awesomeDeathMissile.png").convert_alpha()
spaceshipObj = pygame.image.load("spaceShip.png").convert_alpha()
spaceshipObj = pygame.transform.scale(spaceshipObj, (30, 75))
spaceshipLeft = pygame.image.load("left.png").convert_alpha()
spaceshipLeft = pygame.transform.scale(spaceshipLeft, (30, 75))
spaceshipRight = pygame.image.load("right.png").convert_alpha()
spaceshipRight = pygame.transform.scale(spaceshipRight, (30, 75))

#pewSound = pygame.mixer.Sound("pew.wav")
dieSound = pygame.mixer.Sound('alienDeath1.wav')
shootSound = pygame.mixer.Sound('shootSound.wav')

fpsClock = pygame.time.Clock()

# Set the titles
pygame.display.set_caption('Space Invaders')

# CHANGE THESE FOR MORE FUN
spawnTimeStart = 15 # Seconds until mobs start spawning
spawnDelay = 3 # Seconds between spawn
shipSpeed = 10
shootDelay = 50
mobSpeed = 2
mobsInRow = 6
mobsColumns = 3
distanceBetweenMobsX = 90
distanceBetweenMobsY = 55


assert distanceBetweenMobsX * mobsInRow < windowWidth, "Too many mobs"

# Predefining
spaceship = spaceshipObj
shipX = windowWidth/2.0
oldShipX = shipX
shipY = 415
alienDeltaX = mobSpeed
alienDeltaY = 0
score = 0
shootTimer = shootDelay
timeFloat = 0
timeInt = 0
timeSpawn = 0
shipDeltaX = 0
scoreMsg = "SCORE: %s" % score
canShoot = True
isWinner = False
lose = False
lMove = False
rMove = False
Move = False

# Used to create enemies, change the middle number to increase the amount
for x in range(1, mobsInRow + 1, 1):
    for y in range (1, mobsColumns + 1, 1):
        enemyList.append(enemy(x * distanceBetweenMobsX, y * distanceBetweenMobsY))

###########################################################################
while True:

# Upkeep
    gameOn = not (isWinner or lose)
    if not enemyList:
        isWinner = True
        
    if shootTimer >= shootDelay:
        canShoot = True
    else:
        canShoot = False

    oldShipX = shipX
    if lMove or rMove:
        shipX += shipDeltaX
        if shipX + 30 > 640 or shipX < 1:
            shipX = oldShipX
    
    shootTimer += 1000.0 / FPS
    timeFloat += 1.0 / FPS
    if gameOn:
        timeInt = int(timeFloat)

    if timeFloat - timeSpawn > spawnDelay and not isWinner and spawnTimeStart <= timeFloat:
        enemyList.append(enemy(random.randint(150, 350), random.randint(50, 300)))
        timeSpawn = timeFloat
        
# Input
    # Iterates through all events in game, such as mouse movement, key presses, etc.
    for event in pygame.event.get():
        # Quits the game
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # Checks for key presses
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                lMove = False
                spaceship = spaceshipObj
            elif event.key == K_RIGHT:
                rMove = False
                spaceship = spaceshipObj
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == K_LEFT:    
                shipDeltaX = - shipSpeed
                lMove = True
                spaceship = spaceshipLeft
            elif event.key == K_RIGHT:
                shipDeltaX = shipSpeed
                rMove = True
                spaceship = spaceshipRight
            if event.key == K_SPACE and canShoot and not lose:
                shootSound.play()
                shootTimer = 0
                newMissile = missile(shipX, shipY)
                missileList.append(newMissile)
            if event.key == K_a:
                enemyList.append(enemy(random.randint(150, 350), random.randint(50, 300)))
        # Checks for key releases



# Logic
    for lazor in missileList:
        # Removes missiles with distance over 700 pixels
        if lazor.distance > 700:
             missileList.remove(lazor)
        # Moves the lazor according to it's speed. 
        delta = 1.0/FPS * lazor.speed
        # Updates lazor's travelled distance
        lazor.distance += delta
        lazor.posY -= delta

    for baddies in enemyList:
        for lazor in missileList:
            # Checks distance between every enemy and every missile.
            if lazor.posX >= baddies.posX and lazor.posX <= baddies.posX + 50 and lazor.posY >= baddies.posY and lazor.posY <= baddies.posY + 50:
                missileList.remove(lazor)
                baddies.hp += - 20
                if baddies.hp <= 0:
                    dieSound.play()
                    enemyList.remove(baddies)
                    if timeInt > 100:
                        score += 10
                    else:
                        score += 100 - timeInt

    # Handles enemies movement. So they don't go out of bounds and move down instead
        if baddies.posX > windowWidth - 50:
            alienDeltaX = - mobSpeed
            alienDeltaY = mobSpeed
        if baddies.posX < 10:
            alienDeltaX = mobSpeed
            alienDeltaY = mobSpeed

    for baddies in enemyList:
        # Makes enemies stop moving down if they moved 15 pixels already
        if baddies.posY > 400:
            lose = True
            enemyList.remove(baddies)
            shipTopMove = 0
        if baddies.distanceY > 15:
            alienDeltaY = 0
            baddies.distanceY = 0 
        # Updates enemies' position
        baddies.posX += alienDeltaX
        baddies.posY += alienDeltaY
        # Updates enemies' distance traveled in Y axis
        baddies.distanceY += alienDeltaY
# Graphics
    DISPLAY.fill(BLACK)
    DISPLAY.blit(bgObj, (0,0))
    drawMissiles(missileList)
    DISPLAY.blit(spaceship, (shipX, shipY))
    drawEnemies(enemyList)
    drawText(textList)
    say("SCORE: %s" % score, 30, WHITE, 440, 5)
    say("TIME: %s" % timeInt, 30, WHITE, 5, 5)
    if lose:
        say("YOU LOSE", 80, RED, 150, 200)
    if isWinner:
        say("YOU WIN", 80, GREEN, 150, 200)
        
    pygame.display.update()

# Other
    # Waits 1 / FPS  second
    fpsClock.tick(FPS)
