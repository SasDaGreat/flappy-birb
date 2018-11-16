"""
The source code of Flappy Birb, a meme game made in Python using the pygame module,
for my memeing friends in the German server.
Thank you for being one of my best Discord servers,
and sorry for the long hiatus, Python took all my time D:

This game was coded in a month, starting from the 25th of July.
Some parts were rushed and not thought-out, and I used my own conventions in some places,
so apologies if my code is messier than your everyday spaghetti from a trashcan D:

To change difficulty settings and other things, just change the attributes
inside of the classes. 9 times out of ten, that'll throw errors, but it's worth a try C:

(C) SasDaGreat, 2018 BC - 2018 AD
Any infringement will result in stale German memes being delivered
to the doorstep of the offender, beware.
"""

import pygame
from random import randint,choice
import configparser
pygame.init()
pygame.mixer.init()


BLACK = (0,0,0)
WHITE = (255,255,255)
DISPLAY = WIDTH,HEIGHT = 800,600
ENGLISHLANG = 1
GERMANLANG = 0
DISPLAY_MIDDLE = WIDTH//2,HEIGHT//2


class Image:
    def __init__(self,imageName):
        self.image = pygame.image.load("images\\{}.png".format(imageName))
        self.rect = self.image.get_rect()
        self.ORIGINALIMAGE = self.image

    def move(self,speed):
        self.rect = self.rect.move(speed)
        screen.blit(self.image,self.rect)

class Button(Image):
    # Increase in image size for onHover is 12.5% or by multiplying 1.125 to dimensions. 8/9 for the opposite.

    def __init__(self,imageName,onHoverImage=None,emoticonImage=None):
        super().__init__(imageName)

        if onHoverImage:
            self.onHoverImage = onHoverImage
            self.onHoldImage = pygame.transform.scale(self.onHoverImage,(self.rect.width,self.rect.height))
        else:
            self.onHoverImage = pygame.transform.scale(self.ORIGINALIMAGE,(int(self.rect.width*1.125),int(self.rect.height*1.125)))
            self.onHoldImage = self.ORIGINALIMAGE

        self.emoticonImage = emoticonImage
        if self.emoticonImage: self.emoticonRect = self.emoticonImage.get_rect()
        self.holding = False
        self.activeEmoticon = False

    def checkForMouse(self,action):
        global buttonEventsList
        mousePos = pygame.mouse.get_pos()

        if mousePos[0] >= self.rect.left and mousePos[0] <= self.rect.right and mousePos[1] >= self.rect.top and mousePos[1] <= self.rect.bottom:
            for event in buttonEventsList:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:      # onHold
                    self.holding = True
                    break
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:      # onClick
                    self.holding = False
                    action()
                elif self.holding:
                    break
            else:                                                                   # onHover (if no events break the for loop, then it's hovering)
                self.image = self.onHoverImage

            if self.emoticonImage:
                emoticon.image = self.emoticonImage
                self.activeEmoticon = True

            if self.holding: self.image = self.onHoldImage
        else:
            self.activeEmoticon = False
            self.image = self.ORIGINALIMAGE
            emoticon.image = pygame.Surface(EMOTICON_DIM)
            emoticon.image.fill(WHITE)                                              # clear emoticon
            for event in buttonEventsList:
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.holding = False


class NewFont:
    def __init__(self,fontName,fontSize):
        self.font = pygame.font.SysFont(fontName,fontSize)

    def setText(self,fontTextEng,fontTextGer="Work in progress - please contribute"):
        if language == ENGLISHLANG:
            self.image = self.font.render(fontTextEng,True,BLACK)
        elif language == GERMANLANG:
            self.image = self.font.render(fontTextGer,True,BLACK)

        self.rect = self.image.get_rect()


class Birb(pygame.sprite.Sprite):
    def __init__(self,normalImage,hitImage):
        super().__init__()
        self.normalImage = pygame.image.load("images\\{}.png".format(normalImage))
        self.hitImage    = pygame.image.load("images\\{}.png".format(hitImage))
        self.rect = self.normalImage.get_rect()
        self.image = self.normalImage
        self.ySpeed = 0

        allSprites.add(self)


class Flappy(Birb):
    MAX_YSPEED = 5

    def reset(self):
        self.image = self.normalImage
        self.ySpeed = 0
        self.rect.center = WIDTH//4,HEIGHT//2

    def hop(self):
        self.ySpeed = -4
        pygame.mixer.Channel(4).play(soundBirbFlap)                                 # get these channel ids right

    def hit(self):
        self.image = self.hitImage
        pygame.mixer.Channel(0).play(soundBirbHit)


class Arrem(Birb):
    isHit = True                                                                    # has Arrem been hit by an obstacle/is inactive?
    startY = HEIGHT
    deathNoteEng = "An Austrian has memed."
    deathNoteGer = "Arrem has dich gemement"

    def activate(self,startY):
        self.startY = startY

        self.rect.right = 0
        self.rect.centery = self.startY
        self.xSpeed = 2                                                             # chance xSpeed to change movement speed of arrameme
        self.ySpeed = 0

        self.isHit = False
        obstacleList.add(self)
        allSprites.add(self)

    def hop(self):
        self.ySpeed = -2
        pygame.mixer.Channel(2).play(soundArremFlap)

    def hit(self,hitByObstacle=True):                                                # check arrem collision with obstacle class, not group, in gameloop
        if hitByObstacle:
            pygame.mixer.Channel(3).play(soundArremHit)
            self.image = self.hitImage
        self.isHit = True
        self.ySpeed = 0
        self.xSpeed = obstacle.xSpeed

        obstacleList.remove(self)

    def deactivate(self):
        self.image = self.normalImage
        self.xSpeed = 0
        self.kill()


class Obstacle(pygame.sprite.Sprite):                                               # try either keeping one class instance for ALL obstacles (reuse)
    xSpeed = -2
    MAX_SPEED = -5
    passed = True

    deathMessageEng = "i'm blue da ba dee da ba DIE"
    deathMessageGer = "oh nein 1 blaues dingo"
    germemeDeathEng = "Flap's Bizarre Adventure - Math is Unsolveable"
    germemeDeathGer = "flappy kanns neine mathe"

    def __init__(self):
        super().__init__()
        self.GERMEME_IMAGE = pillarMath

        self.rect = self.GERMEME_IMAGE.get_rect()
        self.rect.topright = (0,0)
        self.ORIGINAL_IMAGE = pygame.Surface((self.rect.width,self.rect.height))
        self.ORIGINAL_IMAGE.fill((0,0,255))
        self.image = self.ORIGINAL_IMAGE

        self.WIDTH = self.rect.width
        self.ySpeed = 0                                                             # if self.ySpeed: checkForYMovement (if self.ySpeed != 0)
        self.minY,self.maxY = 0,0

        self.deathNoteEng = self.deathMessageEng
        self.deathNoteGer = self.deathMessageGer

    def create(self):
        if powerup.powerActive != powerup.germeme.powerActiveID:                    # if germeme is not active
            self.rect.topleft = (WIDTH,randint(0,HEIGHT-self.rect.height))

            if self.rect.top < HEIGHT//3:
                self.rect.height = randint(30,100)
            else:
                self.rect.height = randint(30,150)

            self.ORIGINAL_IMAGE.fill((0,0,255))
            self.image = self.ORIGINAL_IMAGE

            self.deathNoteEng = self.deathMessageEng
            self.deathNoteGer = self.deathMessageGer
        else:
            possibleStartChoices = ((WIDTH,randint(0,HEIGHT//4)), (WIDTH,randint(3*HEIGHT//4,HEIGHT)))
            self.rect.topleft = choice(possibleStartChoices)                        # obstacle will start in the borders
            self.rect.height = randint(30,100)

            self.image = self.GERMEME_IMAGE
            self.deathNoteEng = self.germemeDeathEng
            self.deathNoteGer = self.germemeDeathGer


        self.passed = False
        if randint(1,30) == 1 and arrem.isHit:                                      # 1 in 30 chance
            arrem.activate(self.rect.centery)

        if randint(1,10) == 5:                                                      # 1 in 10 chance
            self.ySpeed = 1
            self.minY = self.rect.y - 50
            self.maxY = self.rect.bottom + 50
        else:
            self.ySpeed = 0

        # not in allSprites because it has a different drawing technique
        obstacleList.add(self)
        actualObstacles.add(self)
        # when one obstacle goes offscreen, it is brought back immediately to front of screen

    def checkPass(self):
        if not self.passed and flappy.rect.centerx >= self.rect.centerx:
            pygame.mixer.Channel(5).play(soundBirbPass)
            self.passed = True
            score.add()

            if randint(1,10) == 1 and not powerup.currentlyOnScreen and powerup.powerActive is None:
                powerup.create()

class Score:
    def __init__(self,pointsImage):
        self.points = 0

        self.text = NewFont("comicsansms",30)
        self.text.setText("{}".format(self.points),"{}es".format(self.points))
        self.text.rect.right = WIDTH - 30
        self.text.rect.top = 20

        self.image = pointsImage
        self.rect = self.image.get_rect()
        self.rect.center = self.text.rect.x-30, 40

    def add(self):
        if powerup.powerActive == powerup.germeme.powerActiveID: self.points += 2
        else: self.points += 1
        self.text.setText("{}".format(self.points), "{}es".format(self.points))
        self.text.rect.right = WIDTH - 30
        self.text.rect.top = 20
        self.rect.center = self.text.rect.x - 30,40

        if self.points % 10 == 0:
            if obstacle.xSpeed > obstacle.MAX_SPEED:
                obstacle.xSpeed -= 1


class Powerup(pygame.sprite.Sprite):
    currentlyOnScreen = None
    powerupsList = []
    powerActive = None
    ACTIVE_LIMIT = 7000

    class PowerupType:                                                              # make instances in init
        def __init__(self,powerActiveID,imageName):
            self.powerActiveID = powerActiveID                                      # unique powerActive ID
            self.image = pygame.image.load(f"images\\{imageName}.png")
            Powerup.powerupsList.append(self)


    def __init__(self,germemeImageName,vitaminsImageName):
        super().__init__()

        self.germeme = self.PowerupType(1,germemeImageName)
        self.vitamins = self.PowerupType(2,vitaminsImageName)

        self.image = None
        self.rect = None

        self.xSpeed = 0
        self.collectedAtTicks = 0

    def create(self):
        # call this when score.add(), if not self.currentlyOnScreen and not self.powerActive
        self.currentlyOnScreen = choice(self.powerupsList)
        self.image = self.currentlyOnScreen.image
        self.rect = self.image.get_rect()

        self.rect.topleft = (WIDTH,randint(HEIGHT//4,3*HEIGHT//4))
        self.xSpeed = obstacle.xSpeed

        allSprites.add(self)
        powerups.add(self)

    def deactivate(self):
        self.currentlyOnScreen = None
        self.powerActive = None
        self.xSpeed = 0
        self.collectedAtTicks = 0
        self.kill()

    def checkDie(self):
        if self.rect.right <= 0:
            self.currentlyOnScreen = None
            self.kill()
            self.xSpeed = 0

    def collected(self):                                                            # doKill should be set to 1
        pygame.mixer.Channel(5).play(soundBirbPass)

        self.powerActive = self.currentlyOnScreen.powerActiveID
        if self.powerActive == self.germeme.powerActiveID:
            pygame.mixer.Channel(0).play(musicGermeme)                              # same channel as birdDeath

        self.currentlyOnScreen = None
        self.xSpeed = 0
        self.collectedAtTicks = pygame.time.get_ticks()                             # when was powerup collected (for disabling purposes)

    def checkPowerExpire(self):
        # if time passed since collected is ACTIVE_LIMIT seconds and collectedAtTicks != 0
        if self.powerActive and pygame.time.get_ticks()-self.collectedAtTicks >= self.ACTIVE_LIMIT and self.collectedAtTicks:
            self.powerActive = None
            self.collectedAtTicks = 0


infoTextEng = """Hiya there! Welcome to my meme of a game - Flappy Birb, a definitely original game! :D

Jokes aside, this is a Flappy Bird clone written in Python using the pygame module.
Source code should be available.

You control the player - a 'flappy' birb (an Eevee, since that was Flappy's avatar iirc).
Hop up with the up/SPACE key, stop upwards momentum with the down key, and... that's it.
There are powerups, but that's basically the entire game.

Objective? Other than dying repeatedly and looking like a fool, nothing much.
Try beating your previous highscore!

This was just made by me as a side project for a month or so, since I had gone on
yet another hiatus from German to devote all my time to learning programming
(+ my internet was being a total meme for half a year and still counting).
Even then, thanks for being there, people of the Meme serve- I mean Maths se-
I mean German Learning server!

<3
SasDaGreat"""
firstTimeEngText = """Seems like it's your first time playing garba-
I mean this game! Worry not, it's pretty simple!

Control the birb with the up/SPACE and down keys.
To exit at any point in the game, press Escape.

Your goal is to... uh... hit the obstacles at all costs!
Hitting obstacles grants you points! (duh)
Hit the random Austrian memer for more points, too!

One of the powerups makes you stronk,
the other makes you trip on germeme acid.
Find out which is which! :D


Press any key (other than Escape) to continue!
Escape to back out into the main menu, but don't do that pls D:"""

config = configparser.ConfigParser()
config.read("settings.ini")
language = int(config["DEFAULT"]["lang"])
highscore = config["DEFAULT"]["highscore"]
firstTime = bool(int(config["DEFAULT"]["firstTime"]))                               # 7u7

screen = pygame.display.set_mode(DISPLAY)
pygame.display.set_caption("Floppy Birb")
gameIcon        = pygame.image.load("images\\gameIcon.png")
pygame.display.set_icon(gameIcon)
screen.fill(WHITE)

clock = pygame.time.Clock()
buttonEventsList = []
allSprites      = pygame.sprite.Group()                                             # for drawing sprites onto screen
obstacleList    = pygame.sprite.Group()                                             # for blue obstacles
actualObstacles = pygame.sprite.Group()                                             # for all obstacles including Arrem
powerups        = pygame.sprite.Group()                                             # for checking powerup collision

startHover      = pygame.image.load("images\\startHover.png")
exitHover       = pygame.image.load("images\\exitHover.png")
infoHover       = pygame.image.load("images\\infoHover.png")
startEmoticon   = pygame.image.load("images\\yespls.png")
exitEmoticon    = pygame.image.load("images\\nopls.png")
infoEmoticon    = pygame.image.load("images\\infopls.png")
EMOTICON_DIM    = (startEmoticon.get_width(),startEmoticon.get_height())

startButton     = Button("startNormal",startHover,startEmoticon)
exitButton      = Button("exitNormal",exitHover,exitEmoticon)
infoButton      = Button("infoNormal",infoHover,infoEmoticon)
langButton      = Button("langNormal")                                              # will be resized for onHover

arrem           = Arrem("handsomeboi","angeryboi")
flappy          = Flappy("flappyNormal","flappyHit")

title           = Image("title")
emoticon        = Image("yespls")                                                   # initialized as yespls
bgGermeme       = Image("germemeBackground")
infoBackground  = Image("infoBg")

powerup         = Powerup("germemeBonus","eeveetaminsBonus")

pillarMath      = pygame.image.load("images\\mathLasagna.png")
pointsImage     = pygame.image.load("images\\star.png")

musicIntro      = pygame.mixer.Sound("sounds\\intro.wav")
musicGermeme    = pygame.mixer.Sound("sounds\\germeme.wav")
soundBirbHit    = pygame.mixer.Sound("sounds\\obstacleHit.wav")
soundBirbPass   = pygame.mixer.Sound("sounds\\obstaclePass.wav")
soundBirbFlap   = pygame.mixer.Sound("sounds\\flap.wav")
soundGravity    = pygame.mixer.Sound("sounds\\gravitySwitch.wav")
soundArremHit   = pygame.mixer.Sound("sounds\\arremHit.wav")
soundArremFlap  = pygame.mixer.Sound("sounds\\handsomeSound.wav")


def gameExit():
    pygame.quit()
    raise SystemExit																# exit() doesn't seem to work with executables...

def updateScreen(backgroundImage=None,rectList=()):
    if backgroundImage: screen.blit(backgroundImage,(0,0))
    if rectList: pygame.display.update(rectList)
    else: pygame.display.flip()

def drawImages(imagesToMove,speed,stillImages=(),backgroundImage=None):
    if backgroundImage: screen.blit(backgroundImage.image,backgroundImage.rect)
    else: screen.fill(WHITE)

    blitImages(stillImages)
    for image in imagesToMove: image.move(speed)
    updateScreen()

def blitImages(imageList):
    for image in imageList:
        screen.blit(image.image,image.rect)

def writeToFile(element,value):
    config["DEFAULT"][element] = f"{value}"
    with open("settings.ini","w") as configfile:
        config.write(configfile)

def menuFontsInitialise():
    global highscore,highscoreFont,langFont
    highscoreFont = NewFont("Calibri", 22)

    if highscore == "None":
        highscoreFont.setText("No highscore achieved... yet.", "I habes neine Highskoren :C")
    else:
        try:
            highscore = int(highscore)

            if highscore < 0 or highscore > 100000:
                highscoreFont.setText("Achievement unlocked: You are a cheater","has du gecheatest? :denken:")
            else:
                highscoreFont.setText("Highscore: {} points. Can you beat that?".format(highscore),"i habes {} punkte lal".format(highscore))
        except ValueError:
            highscoreFont.setText("Stop messing around in me files pls")
            highscore = "None"

            writeToFile("highscore",highscore)

    highscoreFont.rect.center = (WIDTH // 2,30)
    langFont = NewFont("comicsansms",20)
    langFont.setText("Englisch","German")
    langFont.rect.centery = langButton.rect.centery
    langFont.rect.x = langButton.rect.right+20


def gameIntro():
    title.rect.center = (WIDTH//2,0-title.rect.width)
    ySpeed = 0
    POSITIVEGRAVITY = 2                                                             # image goes down
    NEGATIVEGRAVITY = -3                                                            # image goes up
    gravityAcceleration = POSITIVEGRAVITY

    startTime = pygame.time.get_ticks()
    pygame.mixer.Channel(0).play(musicIntro)
    while 1:
        for event in pygame.event.get():
            if event.type  == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                while title.rect.y < HEIGHT: drawImages((title,),(0,3))
                gameExit()


        if pygame.time.get_ticks()-startTime >= 100:                                # 0.1 second updates
            ySpeed += gravityAcceleration
            startTime = pygame.time.get_ticks()                                     # reset the timer

        if gravityAcceleration == POSITIVEGRAVITY and title.rect.centery >= DISPLAY_MIDDLE[1]:
            gravityAcceleration = NEGATIVEGRAVITY                                   # reverse gravity
            ySpeed -= 4                                                             # prevent speed from being too much
        elif gravityAcceleration == NEGATIVEGRAVITY and title.rect.centery <= HEIGHT//3: break

        drawImages((title,),(0,ySpeed))
        clock.tick(300)


    ySpeed = -5
    startButton.rect.y = infoButton.rect.y = HEIGHT
    exitButton.rect.centery = startButton.rect.bottom + 60

    startButton.rect.centerx = WIDTH//3
    infoButton.rect.centerx = 2*WIDTH//3
    exitButton.rect.centerx = DISPLAY_MIDDLE[0]

    while startButton.rect.centery > 370:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                while title.rect.y < HEIGHT:
                    drawImages((startButton,infoButton,exitButton,title),(0,3))
                gameExit()

        drawImages((startButton,exitButton,infoButton),(0,ySpeed),(title,))
        clock.tick(300)

    langButton.rect.center = (75,530)
    updateScreen()

    gameMenu()


def gameMenu():
    global language,buttonEventsList

    title.rect.center       =   (WIDTH//2,HEIGHT//3)
    startButton.rect.center =   (WIDTH//3,370)
    infoButton.rect.center  = (2*WIDTH//3,370)
    exitButton.rect.center  =   (WIDTH//2,startButton.rect.bottom + 60)
    langButton.rect.center  =         (75,530)
    emoticon.rect.center    =   (WIDTH//2,370)
    menuFontsInitialise()

    buttonsList = [startButton,exitButton,infoButton,langButton]
    actionsList = [gameStart,  exitPress, infoMenu,  langSwitch]

    while 1:
        buttonEventsList = pygame.event.get()
        for index in range(len(buttonsList)):
            buttonsList[index].checkForMouse(actionsList[index])
            if buttonsList[index].activeEmoticon: break

        drawImages((),None,(startButton,infoButton,exitButton,langButton,title,highscoreFont,langFont,emoticon))
        clock.tick(60)

    
def infoMenu():
    infoTextEngList = infoTextEng.split("\n")
    infoFontsList = [NewFont("comicsansms",19)] * len(infoTextEngList)
    infoTextSurface = pygame.Surface(DISPLAY)
    infoTextSurface.fill(WHITE)
    infoTextSurface.set_colorkey(WHITE)

    fontLastBottomY = 10
    FONT_SPACE = 2                                                                  # 5px spaces between fonts

    for index in range(len(infoTextEngList)):
        infoFontsList[index].setText(infoTextEngList[index])

        infoFontsList[index].rect.centerx, infoFontsList[index].rect.y = DISPLAY_MIDDLE[0], fontLastBottomY + FONT_SPACE
        fontLastBottomY = infoFontsList[index].rect.bottom

        infoTextSurface.blit(infoFontsList[index].image,infoFontsList[index].rect)

    infoTextRect = infoTextSurface.get_rect()
    infoTextRect.bottom = 0

    goBackFont = NewFont("Calibri",20)
    goBackFont.setText("Press Escape to go back!","komm rauses mith Eskape c:")

    hopped = False
    ySpeed = 0
    gravityAcceleration = 5
    startTicks = pygame.time.get_ticks()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                while infoTextRect.y < HEIGHT:
                    screen.blit(infoBackground.image,infoBackground.rect)
                    infoTextRect = infoTextRect.move((0,3))
                    screen.blit(infoTextSurface,infoTextRect)
                    pygame.display.flip()
                gameExit()

        screen.blit(infoBackground.image,infoBackground.rect)
        infoTextRect = infoTextRect.move((0,ySpeed))
        screen.blit(infoTextSurface,infoTextRect)
        pygame.display.flip()                                                       # can't use functions because infoTextSurface isn't Image class

        if pygame.time.get_ticks()-startTicks >= 100:
            ySpeed += gravityAcceleration
            startTicks = pygame.time.get_ticks()

        if not hopped:
            if infoTextRect.bottom >= HEIGHT-10:
                ySpeed = -ySpeed+5
                hopped = True
        elif infoTextRect.bottom >= HEIGHT:
            screen.blit(infoBackground.image,infoBackground.rect)
            infoTextRect.topleft = (0,0)
            goBackFont.rect.topleft = (550,550)

            screen.blit(infoTextSurface,infoTextRect)
            screen.blit(goBackFont.image,goBackFont.rect)
            pygame.display.flip()

            break

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                while infoTextRect.y < HEIGHT:
                    screen.blit(infoBackground.image,infoBackground.rect)
                    infoTextRect = infoTextRect.move((0,3))
                    screen.blit(infoTextSurface,infoTextRect)
                    pygame.display.flip()
                gameExit()

            elif event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE):
                return


def exitPress():
    while title.rect.y < HEIGHT:
        drawImages((startButton,infoButton,exitButton,title),(0,3))
    gameExit()

def langSwitch():
    global language
    language = int(not language)
    writeToFile("lang",language)

    menuFontsInitialise()


def firstTimeScreen():
    global firstTime
    ftEngTextList = firstTimeEngText.split("\n")
    ftFont = NewFont("Calibri",25)

    fontLastBottomY = 20
    FONT_SPACE = 6

    for line in ftEngTextList:
        ftFont.setText(line)

        ftFont.rect.centerx, ftFont.rect.y = DISPLAY_MIDDLE[0], fontLastBottomY+FONT_SPACE
        fontLastBottomY = ftFont.rect.bottom

        screen.blit(ftFont.image,ftFont.rect)

    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gameMenu()
                else:
                    firstTime = 0
                    writeToFile("firsttime",firstTime)
                    return


def gameStart():
    global firstTime
    screen.fill(WHITE)
    pygame.display.flip()

    if firstTime: firstTimeScreen()

    timerFont = NewFont("Arial",200)

    for number in range(3,0,-1):
        timerFont.setText("{}".format(number),"{}sies".format(randint(1,100)))
        timerFont.rect.center = DISPLAY_MIDDLE
        drawImages((),None,(timerFont,))
        pygame.time.delay(1000)

    gameLoop()


def gameLoop():
    global score,obstacle
    obstacleHit = False

    flappy.reset()
    arrem.deactivate()
    obstacle = Obstacle()
    score = Score(pointsImage)
    finishFont = NewFont("Calibri",40)

    smallGermeme  = pygame.transform.scale(powerup.germeme.image,(30,30))
    smallVitamins = pygame.transform.scale(powerup.vitamins.image,(30,30))
    smallPowerupRect = smallGermeme.get_rect()
    smallPowerupRect.right   = score.rect.left - 20
    smallPowerupRect.centery = score.rect.centery

    GRAVITY_CHANGE_INTERVAL = 75
    NORMAL_GRAVITY = 1
    gravityAcceleration = NORMAL_GRAVITY

    startTicks = pygame.time.get_ticks()
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finishFont.setText("Game exited :C","Spiel raus'd >:")
                gameOver(finishFont)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    if powerup.powerActive != powerup.germeme.powerActiveID:
                        flappy.hop()
                    else:
                        gravityAcceleration *= -1
                        pygame.mixer.Channel(4).play(soundGravity)
                elif event.key == pygame.K_DOWN:
                    if flappy.ySpeed < 0: flappy.ySpeed = 0
                elif event.key == pygame.K_ESCAPE:
                    finishFont.setText("Game exited :C","Spiel raus'd >:")
                    gameOver(finishFont)

        powerup.checkPowerExpire()

        if obstacle.rect.right <= 0:
            obstacle.kill()
            obstacle.create()

        obstacle.checkPass()

        if obstacle.ySpeed:
            if obstacle.rect.y <= obstacle.minY or obstacle.rect.bottom >= obstacle.maxY:
                obstacle.ySpeed *= -1

        if flappy.rect.bottom <= 0:
            if powerup.powerActive != powerup.germeme.powerActiveID:
                finishFont.setText("Ceiling broken, pay for damages","Du hast die Ceiling gememe't")
                gameOver(finishFont)
            else:
                flappy.ySpeed *= -1
        elif flappy.rect.bottom >= HEIGHT:
            if powerup.powerActive != powerup.germeme.powerActiveID:
                finishFont.setText("And the birb goes splat","Oh neins der Boden is gaybroch'd :C")
                gameOver(finishFont)
            else:
                flappy.ySpeed *= -1

        if arrem.rect.centery >= arrem.startY: arrem.hop()

        for object in pygame.sprite.spritecollide(flappy,obstacleList,0):
            if powerup.powerActive != powerup.vitamins.powerActiveID or object == arrem:
                finishFont.setText(object.deathNoteEng,object.deathNoteGer)
                gameOver(finishFont)
            else:                                                                   # if flappy is stronk, die object!
                object.kill()
                pygame.mixer.Channel(3).play(soundArremHit)
                obstacle.image.fill(WHITE)
                score.add()

        if not arrem.isHit:
            if pygame.sprite.spritecollide(arrem,actualObstacles,0):                # if arrem collided with anything
                arrem.hit()
            else:
                if arrem.rect.right >= WIDTH:
                    arrem.hit()

        for collidedPowerup in pygame.sprite.spritecollide(flappy,powerups,1):
            collidedPowerup.collected()


        if pygame.time.get_ticks()-startTicks >= GRAVITY_CHANGE_INTERVAL:
            flappy.ySpeed += gravityAcceleration
            if not arrem.isHit: arrem.ySpeed += NORMAL_GRAVITY
            startTicks = pygame.time.get_ticks()

        flappy.ySpeed = flappy.MAX_YSPEED if flappy.ySpeed >= flappy.MAX_YSPEED else flappy.ySpeed
        flappy.ySpeed = -flappy.MAX_YSPEED if flappy.ySpeed <= -flappy.MAX_YSPEED else flappy.ySpeed


        if powerup.currentlyOnScreen:
            powerup.checkDie()
            powerup.rect = powerup.rect.move((powerup.xSpeed,0))

        flappy.rect = flappy.rect.move((0,flappy.ySpeed))
        obstacle.rect = obstacle.rect.move((obstacle.xSpeed,obstacle.ySpeed))
        arrem.rect = arrem.rect.move((arrem.xSpeed,arrem.ySpeed))

        if powerup.powerActive == powerup.germeme.powerActiveID:                    # if germeme is active
            screen.blit(bgGermeme.image,bgGermeme.rect)
            screen.blit(smallGermeme,smallPowerupRect)
        else:
            gravityAcceleration = NORMAL_GRAVITY
            screen.fill(WHITE)

            if powerup.powerActive == powerup.vitamins.powerActiveID:               # if eeveetamins is active
                screen.blit(smallVitamins,smallPowerupRect)

        screen.blit(obstacle.image, obstacle.rect, (0, 0, obstacle.rect.width, obstacle.rect.height))
        allSprites.draw(screen)
        blitImages((score,score.text))

        pygame.display.flip()
        clock.tick(300)


def gameOver(finishFont):
    global highscore
    flappy.hit()

    gravityAcceleration = 3
    flappy.ySpeed = -5
    startTicks = pygame.time.get_ticks()
    while flappy.rect.y < HEIGHT:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit()

        if pygame.time.get_ticks()-startTicks >= 100:
            flappy.ySpeed += gravityAcceleration
            startTicks = pygame.time.get_ticks()

        flappy.rect = flappy.rect.move((0,flappy.ySpeed))
        screen.fill(WHITE)
        screen.blit(obstacle.image,obstacle.rect,(0,0,obstacle.rect.width,obstacle.rect.height))
        allSprites.draw(screen)
        pygame.display.flip()

    obstacle.kill()
    arrem.kill()
    powerup.deactivate()
    arrem.hit(False)

    finishFont.rect.center = DISPLAY_MIDDLE

    try:
        if (highscore == "None" and score.points) or score.points > highscore:      # if no highscore and positive score/score > current highscore
            highscore = score.points

            scoreAchievedFont = NewFont("comicsansms",20)
            scoreAchievedFont.setText("Highscore achieved!","o wew dU hast 1s hiskore gereceiveth")
            scoreAchievedFont.rect.centerx = DISPLAY_MIDDLE[0]
            blitImages((scoreAchievedFont,))
            pygame.display.update(scoreAchievedFont.rect)

            writeToFile("highscore",highscore)
    except TypeError:
        highscore = "None"
        writeToFile("highscore",highscore)


    playAgainFont,exitFont = NewFont("Arial",35),NewFont("Arial",35)
    playAgainFont.setText("(Y) Play Again","(Y) Spiel'dve wieder")
    exitFont.setText("(N) Exit to menu","(N) Komm rauses")

    playAgainFont.rect.center = (WIDTH//3,2*HEIGHT//3)
    exitFont.rect.center      = (2*WIDTH//3,2*HEIGHT//3)

    blitImages((finishFont,playAgainFont,exitFont))
    pygame.display.update((finishFont.rect,playAgainFont.rect,exitFont.rect))

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_n:
                    gameMenu()
                elif event.key == pygame.K_y:
                    gameLoop()


gameIntro()
