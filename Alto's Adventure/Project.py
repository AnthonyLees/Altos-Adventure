#My term project: Alto's Adventure
################################################################################
################################################################################
##############################CITATIONS#########################################
#Rock Image copied and edited from:
#http://gamenomnom.com/after-3/3-altos-adventure
#Player Image copied and edited from from:
#https://noodlecake.com/games/altos-adventure/ 
#Title screen copied and edited from:
#https://noodlecake.com/games/altos-adventure/
#Background image copied and edited from:
#https://www.pinterest.com/pin/549791067000087642/
#Coin image copied and edited from:
#https://sixcolors.com/link/2015/02/altos-adventure-is-anything-but-a-grind/
#Music taken from: https://www.youtube.com/watch?v=jMzgAhC9Ig0
#Eagle image copied and edited from:
#https://www.pinterest.com/pin/45739752450860447/
#Scarf image copied and edited from:
#https://vulcanpost.com/191171/everything-need-know-ace-altos-adventure/
##############################CITATIONS#########################################
################################################################################
################################################################################
import math, copy, random, string, decimal
from cmu_112_graphics import *
from tkinter import *
from PIL import Image, ImageEnhance, ImageFilter
import pygame
#Copied from: CS 15-112 Fall 2019 Homework 3 helper functions
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#Copied from: CS 15-112 Fall 2019 Homework 3 helper functions
def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

#Copied from: http://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
class MyModalApp(ModalApp):
    def appStarted(app):
        app.splashScreenMode = SplashScreenMode()
        app.gameMode = GameMode()
        app.helpMode = HelpMode()
        app.gameOverMode= GameOverMode()
        app.setActiveMode(app.splashScreenMode)
        app.timerDelay = 50

class SplashScreenMode(Mode):
    #Copied from: https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    def readFile(mode, path):
        with open(path, "rt") as f:
            return f.read()

#Copied from: https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    def writeFile(mode, path, contents):
        with open(path, "wt") as f:
            f.write(contents)

    def appStarted(mode):
        mode.music=False
        pygame.mixer.init()
        pygame.mixer.music.load("Soundtrack.mp3")
        backgroundImage=mode.loadImage("Alto's Adventure Title Screen.jpg")
        mode.spriteBackground=mode.scaleImage(backgroundImage, 5/6)
        mode.username=None
        mode.contentToWrite=mode.readFile("Leaderboard.txt")
        pygame.mixer.music.play(-1)
        mode.checkMusic()
    
    def checkMusic(mode):
        if mode.music==False:
            pygame.mixer.music.pause()
            pygame.mixer.music.rewind()
        elif mode.music==True:
            pygame.mixer.music.unpause()

    def checkForWhitespaceUsername(mode, username):
        if username!=None:
            whitespaceCharacterCounter=0
            for char in username:
                if char in string.whitespace:
                    whitespaceCharacterCounter+=1
            if whitespaceCharacterCounter==len(username):
                return True
            else:
                return False

    def keyPressed(mode, event):
        name=mode.getUserInput("What is your username?")
        isNameWhitespace=mode.checkForWhitespaceUsername(name)
        while name==None or isNameWhitespace==True:
            name=mode.getUserInput("You must enter a username to play!")
            isNameWhitespace=mode.checkForWhitespaceUsername(name)
        mode.username=name
        mode.app.setActiveMode(mode.app.gameMode)
        mode.music=True
        mode.checkMusic()

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2,\
            image=ImageTk.PhotoImage(mode.spriteBackground))
        font="Arial 12 bold"
        canvas.create_text(mode.width/2, 290,\
        text="Press any key to begin", font=font, fill="black")

class HelpMode(Mode):
    def appStarted(mode):
        backgroundImage=mode.loadImage("Background2.png")
        mode.backgroundImage=mode.scaleImage(backgroundImage, 7/10)

    def redrawAll(mode, canvas):
        canvas.create_image(mode.width*2/5, mode.height/2,\
        image=ImageTk.PhotoImage(mode.backgroundImage))
        canvas.create_text(mode.width/2, mode.height/20, text="How to Play",\
        font="Georgia 20 bold")
        canvas.create_text(mode.width/20, mode.height/6, text="Welcome to Alto's Adventure! In this game, you play as Alto, a",\
        font="Bahnschrift 16 bold", anchor="w")
        canvas.create_text(mode.width/20, mode.height/6+50, text="skier tasked with skiing down a never-ending hill. Your main",\
        font="Bahnschrift 16 bold", anchor="w")
        canvas.create_text(mode.width/20, mode.height/6+100, text="task is to simply stay alive and get as high as a score as",\
        font="Bahnschrift 16 bold", anchor="w")
        canvas.create_text(mode.width/20, mode.height/6+150, text="possible. Be sure to avoid obstacles such as rocks and",\
        font="Bahnschrift 16 bold", anchor="w")
        canvas.create_text(mode.width/20, mode.height/6+200, text="canyons, while also doing flips and collecting coins in",\
        font="Bahnschrift 16 bold", anchor="w")
        canvas.create_text(mode.width/20, mode.height/6+250, text="order to boost your score. Makes sure Alto lands parallel",\
        font="Bahnschrift 16 bold", anchor="w")
        canvas.create_text(mode.width/20, mode.height/6+300, text="to the slope of the hill, or otherwise he might crash!",\
        font="Bahnschrift 16 bold", anchor="w")
        canvas.create_text(mode.width/20, mode.height/6+350, text="Finally, be wary of eagles, as if they successfully hit",\
        font="Bahnschrift 16 bold", anchor="w")
        canvas.create_text(mode.width/20, mode.height/6+400, text="you then you lose points. Good luck, and have fun!",\
        font="Bahnschrift 16 bold", anchor="w")
        #skier tasked with skiing down
        #a never-ending hill. Your main task is to simply stay alive and get as a high a score as possible.\
        # Be sure to avoid obstacles such as rocks and canyons, while also doing flips and collecting coins
        #  in order to boost your score. However, be wary of eagles, as if they successfully hit you then you 
        # lose points. Good luck, and have fun!"
        

    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.gameMode)

class GameMode(Mode):
    def appStarted(mode):
        mode.app.splashScreenMode.music=True
        mode.app.splashScreenMode.checkMusic()
        backgroundImage=mode.loadImage("Background2.png")
        mode.backgroundImage=mode.scaleImage(backgroundImage, 7/10)
        mode.player=Player(5, mode.height*1/2)
        mode.scrollX=0
        mode.scrollY=0
        mode.scrollMarginX=mode.width/2
        mode.scrollMarginY=mode.height/2-5
        mode.hill1=Hill(mode, 0, mode.height//2)
        mode.hill1.generateHillType0()
        mode.hill2=Hill(mode, mode.hill1.endingX, mode.hill1.endingY)
        mode.hill2.generateHillType1()
        mode.hill3=Hill(mode, mode.hill2.endingX, mode.hill2.endingY)
        mode.hill3.generateHillType0()
        mode.counterForScore=0
        mode.score=0
        mode.currentPlayerHill=None
        mode.didHillSwitch=False
        #SpriteSheet For Player
        playerImage=mode.loadImage("Alto.png")
        mode.playerImage=mode.scaleImage(playerImage, 1/20)
        #For small discrepancy with one of the hills, needs some magic fixing
        #in order to work
        mode.amountPlayerRotated=0
        mode.amountToRotate=0
        #JumpingStuff
        mode.isJumping=False
        mode.jumpingCounter=0
        mode.jumpingDegreesToRotate=0
        mode.playerFalling=False
        mode.cooldown=False
        #misc
        mode.counter=0
        mode.isGameOver=False
        #rock obstacle
        mode.rockCounter=0
        mode.rock=None
        rockImage=mode.loadImage("Rock.png")
        mode.rockImage=mode.scaleImage(rockImage, 1/2)
        mode.generateRock()
        #Snow
        mode.snow=None
        mode.generateSnow()
        mode.snow1=True
        mode.snow2=False
        mode.snow3=False
        #For flips
        mode.didFlip=False
        mode.flip1=False
        mode.flip2=False
        mode.flip3=False
        mode.jumpingDegreesForFlip=0
        mode.jumpInventory=dict()
        mode.numberOfFlips=0
        #For lighting :)
        mode.lightingCounter=0
        mode.lightingEnhancer=1.0
        mode.lightingIncrease=False
        #For coins
        randomX=random.randint(150, 275)
        randomY=random.randint(100, 150)
        mode.coin=Coin(mode.hill3.startingX+randomX, mode.hill3.startingY-\
        randomY)
        mode.coinCounter=0
        coinImage=mode.loadImage("Coin.png")
        mode.coinImage=mode.scaleImage(coinImage, 1/20)
        mode.coinCollected=False
        #For eagle
        x=mode.player.cx+595
        randomY=randomY=random.randint(200, 290)
        #mode.eagle=Eagle(x, randomY)
        mode.eagleImages=[]
        for i in range(3):
            eagleImage=mode.loadImage(f"Fly {i}.png")
            eagleImage=mode.scaleImage(eagleImage, 1/5)
            mode.eagleImages.append(eagleImage)
        mode.eagleCounter=0
        mode.eagleInView=False
        #Possibly make mode.eagleInView=True
        mode.fly1=True
        mode.fly2=False
        mode.fly3=False
        mode.eaglePassedPlayer=False
        mode.blur=False
        mode.blurCounter=0
        #Scarf
        mode.scarf=Scarf(mode.player.cx, mode.player.cy)
        mode.scarfElongated=False
        mode.scarfImage=None
        mode.checkScarfType()
        mode.scarfCounter=0

    def checkScarfType(mode):
        if mode.scarfElongated==False:
            newScarfImage=mode.loadImage("Scarf 1.png")
            newScarfImage=mode.scaleImage(newScarfImage, 1/7)
            mode.scarfImage=newScarfImage
        elif mode.scarfElongated==True:
            newScarfImage=mode.loadImage("Scarf 2.png")
            newScarfImage=mode.scaleImage(newScarfImage, 1/7)
            mode.scarfImage=newScarfImage
    
    def createNewEagle(mode):
        x=mode.player.cx+300
        randomY=random.randint(10, 50)
        mode.eagle=Eagle(x, mode.player.cy-randomY)
        mode.eagleInView=True

    def generateSnow(mode):
        mode.snow=Snow(mode.player.cx-10, mode.player.cy-6)
    
    def generateCoin(mode):
        randomX=random.randint(150, 275)
        randomY=random.randint(100, 200)
        mode.coin=Coin(mode.hill3.startingX+randomX, mode.hill3.startingY-\
        randomY)
        mode.coinCollected=False

    ########################################################################
    #########VERY IMPORTANT FUNCTIONS~HOLDS EVERYTHING TOGETHER#############
    #A bit of calculus is used in order to find the angle between the two
    #horizontal line and the position of the player
    ########################################################################
    def findAngleInBetween(mode, slope1, slope2):
        tantheta=(slope2-slope1)/(1+(slope1*slope2))
        thetaInRadians=math.atan(tantheta)
        thetaInDegrees=thetaInRadians*(180/math.pi)
        return thetaInDegrees

    def derivative3(mode, coeff1, coeff2, coeff3, variable):
        return (3*coeff1*(variable**2))+(2*coeff2*variable)+coeff3

    def derivative5(mode, coeff1, coeff2, coeff3, coeff4, coeff5, variable):
        return (5*coeff1*(variable**4))+(4*coeff2*(variable**3))+\
            (3*coeff3*(variable**2))+(2*coeff4*variable)+coeff5

    ########################################################################
    #########VERY IMPORTANT FUNCTIONS~HOLDS EVERYTHING TOGETHER#############
    #A bit of calculus is used in order to find the angle between the two
    #horizontal line and the position of the player
    ########################################################################

#Copied from: https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    def readFile(path):
        with open(path, "rt") as f:
            return f.read()

#Copied from: https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    def writeFile(mode, path, contents):
        with open(path, "wt") as f:
            f.write(contents)

    #Controls the general movement of the player
    def timerFired(mode):
        if mode.isGameOver==False:
            mode.counterForScore+=250
            if mode.counterForScore%8 and mode.counterForScore!=0:
                mode.score+=1
            if mode.isJumping==True:
                mode.checkForPlayerCoinCollision()
                mode.jumpingCounter+=1
                mode.movePlayerWhileJumping()
                mode.checkIfPlayerHasLanded()
                if mode.didFlip==True:
                    if mode.flip1==True:
                        mode.flip1=False
                        mode.flip2=True
                    elif mode.flip2==True:
                        mode.flip2=False
                        mode.flip3=True
                    elif mode.flip3==True:
                        mode.flip3=False
                        mode.didFlip=False
                        mode.numberOfFlips+=1
                        mode.jumpInventory[mode.numberOfFlips]=1
                        mode.score+=50
                mode.checkIfPlayerFlipped()
            else:
                mode.movePlayer()
                if mode.snow1==True:
                    mode.snow1=False
                    mode.snow2=True
                elif mode.snow2==True:
                    mode.snow2=False
                    mode.snow3=True
                elif mode.snow3==True:
                    mode.snow3=False
                    mode.snow1=True
            mode.createNewHill()
            mode.rockCounter+=1
            mode.coinCounter+=1
            if mode.rockCounter%200==0 and mode.rockCounter!=0:
                mode.generateRock()
            if mode.coinCounter%150==0 and mode.coinCounter!=0:
                mode.generateCoin()
            mode.eagleCounter+=1
            if mode.eagleCounter%225==0 and mode.eagleCounter!=0:
                mode.createNewEagle()
            if mode.eagleInView==True and mode.eaglePassedPlayer==False:
                if mode.fly1==True:
                    mode.fly1=False
                    mode.fly2=True
                elif mode.fly2==True:
                    mode.fly2=False
                    mode.fly3=True
                elif mode.fly3==True:
                    mode.fly3=False
                    mode.fly1=True
                mode.checkForPlayerEagleCollision()
                mode.moveEagle()
            elif mode.eagleInView==True and mode.eaglePassedPlayer==True:
                if mode.fly1==True:
                    mode.fly1=False
                    mode.fly2=True
                elif mode.fly2==True:
                    mode.fly2=False
                    mode.fly3=True
                elif mode.fly3==True:
                    mode.fly3=False
                    mode.fly1=True
                if mode.player.cx-300>mode.eagle.cx:
                    mode.eagleInView=False
                    mode.fly1=True
                    mode.fly2=False
                    mode.fly3=False
                    mode.eaglePassedPlayer=False
                mode.eagle.cx-=30
                mode.eagle.cy-=30
            mode.checkForPlayerRockCollision()
            mode.checkCurrentPlayerHill()
            mode.makePlayerVisible()
            mode.checkIfPlayerInCanyon()
            mode.lightingCounter+=1
            if mode.lightingCounter%100==0 and mode.lightingCounter!=0:
                mode.changeLighting()
            if mode.blur==True:
                mode.blurCounter+=1
                if mode.blurCounter==40:
                    mode.revertBlur()
                    mode.blurCounter=0
            if mode.scarfElongated==True:
                mode.scarfCounter+=1
                if mode.scarfCounter==60:
                    mode.scarfElongated=False
                    mode.scarfCounter=0
        elif mode.isGameOver==True:
            contentToWrite=mode.app.splashScreenMode.username+\
            ","+str(mode.score)
            if mode.app.splashScreenMode.contentToWrite=="":
                mode.app.splashScreenMode.contentToWrite=\
                mode.app.splashScreenMode.contentToWrite+contentToWrite
            else:
                mode.app.splashScreenMode.contentToWrite=\
                mode.app.splashScreenMode.contentToWrite+"\n"+contentToWrite
            mode.writeFile("Leaderboard.txt",\
            mode.app.splashScreenMode.contentToWrite)
            mode.app.setActiveMode(mode.app.gameOverMode)
            mode.app.splashScreenMode.music=False
            mode.app.splashScreenMode.checkMusic()
            mode.app.gameOverMode.appStarted()
    
    #Checks if player hit eagle
    def checkForPlayerEagleCollision(mode):
        if mode.player.cx-20<=mode.eagle.cx<=mode.player.cx+20 and\
        mode.player.cy-20<=mode.eagle.cy<=mode.player.cy+20:
            mode.score-=100
            mode.createGaussianBlur()
            mode.eaglePassedPlayer=True
        elif mode.player.cx-20<=mode.eagle.cx<=mode.player.cx+20:
            mode.eaglePassedPlayer=True

    #Creates blur on screen when hit by eagle
    def createGaussianBlur(mode):
        backgroundImage=mode.backgroundImage
        backgroundImage=\
        backgroundImage.filter(ImageFilter.GaussianBlur(radius=5))
        mode.backgroundImage=backgroundImage
        rockImage=mode.rockImage
        rockImage=rockImage.filter(ImageFilter.GaussianBlur(radius=5))
        mode.rockImage=rockImage
        for eagleImage in mode.eagleImages:
            eagleImage=eagleImage.filter(ImageFilter.GaussianBlur(radius=5))
        coinImage=mode.coinImage
        coinImage=coinImage.filter(ImageFilter.GaussianBlur(radius=5))
        mode.coinImage=coinImage
        mode.blur=True

    #Reverts the gaussian blur
    def revertBlur(mode):
        backgroundImage=mode.loadImage("Background2.png")
        enhancer1=ImageEnhance.Brightness(backgroundImage)
        backgroundImage=enhancer1.enhance(mode.lightingEnhancer)
        mode.backgroundImage=mode.scaleImage(backgroundImage, 7/10)
        rockImage=mode.loadImage("Rock.png")
        enhancer2=ImageEnhance.Brightness(rockImage)
        rockImage=enhancer2.enhance(mode.lightingEnhancer)
        mode.rockImage=mode.scaleImage(rockImage, 1/2)
        coinImage=mode.loadImage("Coin.png")
        coinImage=mode.scaleImage(coinImage, 1/20)
        mode.coinImage=coinImage
    
    #Moves eagle
    def moveEagle(mode):
        if abs(mode.player.cx-mode.eagle.cy)>50 and abs(mode.player.cy-\
        mode.eagle.cy)>50:
            mode.eagle.cx+=(mode.player.cx-mode.eagle.cx)/10
            mode.eagle.cy+=(mode.player.cy-mode.eagle.cy)/10
        else:
            mode.eagle.cx+=(mode.player.cx-mode.eagle.cx)/3
            mode.eagle.cy+=(mode.player.cy-mode.eagle.cy)/3
            
    
    def checkForPlayerCoinCollision(mode):
        if -20+mode.player.cx<=mode.coin.cx<=mode.player.cx+20 and\
        -20+mode.player.cy<=mode.coin.cy<=mode.player.cy+20:
            mode.score+=75
            mode.coinCollected=True
            mode.scarfElongated=True
            mode.scarfCounter=0
    
    #Changes the lighting to make it brighter or darker depending on the
    #brightness before that point
    def changeLighting(mode):
        backgroundImage=mode.loadImage("Background2.png")
        enhancer1=ImageEnhance.Brightness(backgroundImage)
        backgroundImage=enhancer1.enhance(mode.lightingEnhancer)
        mode.backgroundImage=mode.scaleImage(backgroundImage, 7/10)
        rockImage=mode.rockImage
        enhancer2=ImageEnhance.Brightness(rockImage)
        rockImage=enhancer2.enhance(mode.lightingEnhancer)
        mode.rockImage=rockImage
        if mode.lightingIncrease==False:
            mode.lightingEnhancer-=0.1
            if almostEqual(mode.lightingEnhancer, 0.4):
                mode.lightingIncrease=True
        elif mode.lightingIncrease==True:
            mode.lightingEnhancer+=0.1
            if almostEqual(mode.lightingEnhancer, 1.0):
                mode.lightingIncrease=False
    #Checks if player did a flip
    def checkIfPlayerFlipped(mode):
        if abs(mode.jumpingDegreesForFlip)>270:
            mode.didFlip=True
            mode.jumpingDegreesForFlip=0
            mode.flip1=True
            mode.scarfElongated=True
            mode.scarfCounter=0

    def checkForPlayerRockCollision(mode):
        if -15+mode.player.cx<=mode.rock.cx<=mode.player.cx+15 and\
        -20+mode.player.cy<=mode.rock.cy<=mode.player.cy+20:
            mode.isGameOver=True

    #Should put in mode.makerPlayerVisible() possibly
    def generateRock(mode):
        if mode.hill3.type==0:
            rockX=mode.hill3.startingX+random.randint(150, 275)
            rockY=mode.hill3.startingY
            mode.rock=Rock(rockX, rockY, 0)
        elif mode.hill3.type==1:
            randomPosition=random.randint(150, 200)
            polynomialY=2.842171*(10**-14)+0.1285714*(randomPosition)+\
            0.009843537*((randomPosition)**2)-\
            0.00002312925*((randomPosition)**3)
            newSlope=mode.derivative3(0.00002312925, -0.01097279, 0.2102041,\
            randomPosition)
            degreesToRotate=mode.findAngleInBetween(0, newSlope)
            newRockImage=mode.loadImage("Rock.png")
            newRockImage=mode.scaleImage(newRockImage, 1/2)
            newRockImage=newRockImage.rotate(degreesToRotate)
            mode.rockImage=newRockImage
            rockX=mode.hill3.startingX+randomPosition
            rockY=mode.hill3.startingY+polynomialY
            mode.rock=Rock(rockX, rockY, 1)
        elif mode.hill3.type==2:
            randomPosition=random.randint(150, 275)
            polynomialY=-9.094947*(10**-13)-0.875*(randomPosition)+\
            0.06375*((randomPosition)**2)-0.0006416667*((randomPosition)**3)+\
            0.0000025*((randomPosition)**4)-\
            3.333333*(10**-9)*((randomPosition)**5)
            newSlope=mode.derivative5((3.333333*10**-9), -0.0000025, 0.0006416667,\
            -0.06375, 0.875, randomPosition)
            degreesToRotate=mode.findAngleInBetween(0, newSlope)
            newRockImage=mode.loadImage("Rock.png")
            newRockImage=mode.scaleImage(newRockImage, 1/2)
            newRockImage=newRockImage.rotate(degreesToRotate)
            mode.rockImage=newRockImage
            rockX=mode.hill3.startingX+randomPosition
            rockY=mode.hill3.startingY+polynomialY
            mode.rock=Rock(rockX, rockY, 2)
    
    def checkIfPlayerInCanyon(mode):
        if mode.currentPlayerHill==1 and mode.hill1.type==3:
            polynomialType3Y=4.845901*(10**-12)-\
            0.9699877*(mode.player.cx%300)+\
            0.2069631*((mode.player.cx%300)**2)-\
            0.002649587*((mode.player.cx%300)**3)+\
            0.00001137466*((mode.player.cx%300)**4)-\
            1.589777*(10**-8)*((mode.player.cx%300)**5)
            if mode.hill1.startingY+polynomialType3Y-30<=mode.player.cy\
            <=mode.hill1.startingY+polynomialType3Y+30 and\
            (51<=mode.player.cx%300<150 or 256<=mode.player.cx%300<=300):
                mode.isGameOver=True
        elif mode.currentPlayerHill==2 and mode.hill2.type==3:
            polynomialType3Y=4.845901*(10**-12)-\
            0.9699877*(mode.player.cx%300)+\
            0.2069631*((mode.player.cx%300)**2)-\
            0.002649587*((mode.player.cx%300)**3)+\
            0.00001137466*((mode.player.cx%300)**4)-\
            1.589777*(10**-8)*((mode.player.cx%300)**5)
            if mode.hill2.startingY+polynomialType3Y-30<=mode.player.cy\
            <=mode.hill2.startingY+polynomialType3Y+30\
            and (51<=mode.player.cx%300<150 or 256<=mode.player.cx%300<=300):
                mode.isGameOver=True
        elif mode.currentPlayerHill==3 and mode.hill3.type==3:
            polynomialType3Y=4.845901*(10**-12)-\
            0.9699877*(mode.player.cx%300)+\
            0.2069631*((mode.player.cx%300)**2)-\
            0.002649587*((mode.player.cx%300)**3)+\
            0.00001137466*((mode.player.cx%300)**4)-\
            1.589777*(10**-8)*((mode.player.cx%300)**5)
            if mode.hill3.startingY+polynomialType3Y-30<=mode.player.cy\
            <=mode.hill3.startingY+polynomialType3Y+30 and\
            (51<=mode.player.cx%300<=150 or 256<=mode.player.cx%300<=300):
                mode.isGameOver=True
    
    def checkIfPlayerHasLanded(mode):
        if mode.currentPlayerHill==1:
            if mode.hill1.type==0:
                if mode.hill1.startingY-30<=mode.player.cy<=\
                mode.hill1.endingY+30 and mode.playerFalling==True:
                    mode.counter+1
                    if mode.jumpingDegreesToRotate>=0:
                        if -50<=mode.jumpingDegreesToRotate%360<=50 or\
                            310<=mode.jumpingDegreesToRotate%360<360:
                            print(f"successful landing! {mode.counter}")
                        else:
                            print(1)
                            mode.isGameOver=True
                    elif mode.jumpingDegreesToRotate<0:
                        if -50<=mode.jumpingDegreesToRotate%360<=50 or\
                            310<=mode.jumpingDegreesToRotate%360<710:
                            print(f"successful landing! {mode.counter}")
                        else:
                            print(2)
                            mode.isGameOver=True
                    mode.isJumping=False
                    mode.jumpingCounter=0
                    mode.playerFalling=False
            elif mode.hill1.type==1:
                polynomialType1Y=2.842171*(10**-14)+\
                0.1285714*(mode.player.cx%300)+\
                0.009843537*((mode.player.cx%300)**2)-\
                0.00002312925*((mode.player.cx%300)**3)
                if mode.hill1.startingY+polynomialType1Y-20<=mode.player.cy<=\
                mode.hill1.startingY+polynomialType1Y+20\
                and mode.playerFalling==True:
                    mode.counter+=1
                    if 0<=mode.player.cx%300<=40 or 250<=\
                    mode.player.cx%300<=300:               
                        if mode.jumpingDegreesToRotate>=0:
                            if -50<=mode.jumpingDegreesToRotate%360<=50 or\
                            310<=mode.jumpingDegreesToRotate%360<360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(3)
                                mode.isGameOver=True
                        elif mode.jumpingDegreesToRotate<0:
                            if -50<=mode.jumpingDegreesToRotate%360<=50 or\
                            310<=mode.jumpingDegreesToRotate%360<710:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(4)
                                mode.isGameOver=True
                    else:
                        newSlope=mode.derivative3(0.00002312925,\
                        -0.01097279, 0.2102041, mode.player.cx%300)
                        accurateDegreesRotated=\
                        mode.findAngleInBetween(0, newSlope)
                        if mode.jumpingDegreesToRotate>=0:
                            if accurateDegreesRotated-50<=\
                            mode.jumpingDegreesToRotate%360<=\
                            accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(5)
                                mode.isGameOver=True
                        elif mode.jumpingDegreesToRotate<0:
                            if accurateDegreesRotated-50<=\
                            mode.jumpingDegreesToRotate%360<=\
                            accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+710:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(6)
                                mode.isGameOver=True
                    mode.isJumping=False
                    mode.jumpingCounter=0
                    mode.playerFalling=False
            elif mode.hill1.type==2:
                polynomialType2Y=-9.094947*(10**-13)-\
                0.875*(mode.player.cx%300)+0.06375*((mode.player.cx%300)**2)-\
                0.0006416667*((mode.player.cx%300)**3)+\
                0.0000025*((mode.player.cx%300)**4)-\
                3.333333*(10**-9)*((mode.player.cx%300)**5)
                if mode.hill1.startingY+polynomialType2Y-30<=mode.player.cy\
                <=mode.hill1.startingY+polynomialType2Y+30\
                and mode.playerFalling==True:
                    mode.counter+=1
                    if 100<=mode.player.cx%300<=180:
                        if mode.jumpingDegreesToRotate>=0:
                            if -100<=mode.jumpingDegreesToRotate%360<=0 or\
                                260<=mode.jumpingDegreesToRotate%360<360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(7)
                                mode.isGameOver=True
                        elif mode.jumpingDegreesToRotate<0:
                            if -100<=mode.jumpingDegreesToRotate%360<=0 or\
                                260<=mode.jumpingDegreesToRotate%360<360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(8)
                                mode.isGameOver=True
                    else:
                        newSlope=mode.derivative5((3.333333*10**-9), -0.0000025,\
                        0.0006416667, -0.06375, 0.875, mode.player.cx%300)
                        accurateDegreesRotated=\
                        mode.findAngleInBetween(0, newSlope)
                        if mode.jumpingDegreesToRotate>=0:
                            if accurateDegreesRotated-50<=\
                            mode.jumpingDegreesToRotate%360<=\
                            accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(9)
                                mode.isGameOver=True
                        elif mode.jumpingDegreesToRotate<0:
                            if accurateDegreesRotated-50<=\
                            mode.jumpingDegreesToRotate%360<=\
                            accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+710:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(10)
                                mode.isGameOver=True
                    mode.isJumping=False
                    mode.jumpingCounter=0
                    mode.playerFalling=False
            elif mode.hill1.type==3:
                polynomialType3Y=4.845901*(10**-12)-\
                0.9699877*(mode.player.cx%300)+\
                0.2069631*((mode.player.cx%300)**2)-\
                0.002649587*((mode.player.cx%300)**3)+\
                0.00001137466*((mode.player.cx%300)**4)-\
                1.589777*(10**-8)*((mode.player.cx%300)**5)
                if mode.hill1.startingY+polynomialType3Y-30<=mode.player.cy\
                <=mode.hill1.startingY+polynomialType3Y+30\
                and mode.playerFalling==True:
                    mode.counter+=1
                    newSlope=mode.derivative5((1.589777*(10**-8)), -0.000012472,\
                    0.003307988, -0.3277466, 7.576999, mode.player.cx%300)
                    accurateDegreesRotated=mode.findAngleInBetween(0, newSlope)
                    if mode.jumpingDegreesToRotate>=0:
                        if accurateDegreesRotated-50<=\
                        mode.jumpingDegreesToRotate%360<=\
                        accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+360:
                            print(f"successful landing! {mode.counter}")
                        else:
                            print(11)
                            mode.isGameOver=True
                    elif mode.jumpingDegreesToRotate<0:
                        if accurateDegreesRotated-50<=\
                        mode.jumpingDegreesToRotate%360<=\
                        accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+710:
                            print(f"successful landing! {mode.counter}")
                        else:
                            print(12)
                            mode.isGameOver=True
                    mode.isJumping=False
                    mode.jumpingCounter=0
                    mode.playerFalling=False

        elif mode.currentPlayerHill==2:
            if mode.hill2.type==0:
                if mode.hill2.startingY-30<=mode.player.cy<=\
                mode.hill2.endingY+30 and mode.playerFalling==True:
                    mode.counter+=1
                    if mode.jumpingDegreesToRotate>=0:
                        if -50<=mode.jumpingDegreesToRotate%360<=50 or\
                            310<=mode.jumpingDegreesToRotate%360<360:
                            print(f"successful landing! {mode.counter}")
                        else:
                            print(13)
                            mode.isGameOver=True
                    elif mode.jumpingDegreesToRotate<0:
                        if -50<=mode.jumpingDegreesToRotate%360<=50 or\
                            310<=mode.jumpingDegreesToRotate%360<710:
                            print(f"successful landing! {mode.counter}")
                        else:
                            print(14)
                            mode.isGameOver=True
                    mode.isJumping=False
                    mode.jumpingCounter=0
                    mode.playerFalling=False
            elif mode.hill2.type==1:
                polynomialType1Y=2.842171*(10**-14)+\
                0.1285714*(mode.player.cx%300)+\
                0.009843537*((mode.player.cx%300)**2)-\
                0.00002312925*((mode.player.cx%300)**3)
                if mode.hill2.startingY+polynomialType1Y-20<=mode.player.cy<=\
                mode.hill2.startingY+polynomialType1Y+20\
                and mode.playerFalling==True:
                    mode.counter+=1
                    if 0<=mode.player.cx%300<=40 or 250<=\
                    mode.player.cx%300<=300:
                        if mode.jumpingDegreesToRotate>=0:
                            if -50<=mode.jumpingDegreesToRotate%360<=50 or\
                            310<=mode.jumpingDegreesToRotate%360<360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(15)
                                mode.isGameOver=True
                        elif mode.jumpingDegreesToRotate<0:
                            if -50<=mode.jumpingDegreesToRotate%360<=50 or\
                            310<=mode.jumpingDegreesToRotate%360<710:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(16)
                                mode.isGameOver=True
                    else:
                        newSlope=mode.derivative3(0.00002312925,\
                        -0.01097279, 0.2102041, mode.player.cx%300)
                        accurateDegreesRotated=\
                        mode.findAngleInBetween(0, newSlope)
                        if mode.jumpingDegreesToRotate>=0:
                            if accurateDegreesRotated-50<=\
                            mode.jumpingDegreesToRotate%360<=\
                            accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(17)
                                mode.isGameOver=True
                        elif mode.jumpingDegreesToRotate<0:
                            if accurateDegreesRotated-50<=\
                            mode.jumpingDegreesToRotate%360<=\
                            accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+710:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(18)
                                mode.isGameOver=True
                    mode.isJumping=False
                    mode.jumpingCounter=0
                    mode.playerFalling=False
            elif mode.hill2.type==2:
                polynomialType2Y=-9.094947*(10**-13)-\
                0.875*(mode.player.cx%300)+0.06375*((mode.player.cx%300)**2)-\
                .0006416667*((mode.player.cx%300)**3)+\
                0.0000025*((mode.player.cx%300)**4)-\
                3.333333*(10**-9)*((mode.player.cx%300)**5)
                if mode.hill2.startingY+polynomialType2Y-30<=mode.player.cy\
                <=mode.hill2.startingY+polynomialType2Y+30\
                and mode.playerFalling==True:
                    mode.counter+=1
                    if 100<=mode.player.cx%300<=180:
                        if mode.jumpingDegreesToRotate>=0:
                            if -100<=mode.jumpingDegreesToRotate%360<=0 or\
                                260<=mode.jumpingDegreesToRotate%360<360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(19)
                                mode.isGameOver=True
                        elif mode.jumpingDegreesToRotate<0:
                            if -100<=mode.jumpingDegreesToRotate%360<=0 or\
                            260<=mode.jumpingDegreesToRotate%360<360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(20)
                                mode.isGameOver=True
                    else:
                        newSlope=mode.derivative5((3.333333*10**-9), -0.0000025,\
                        0.0006416667, -0.06375, 0.875, mode.player.cx%300)
                        accurateDegreesRotated=\
                        mode.findAngleInBetween(0, newSlope)
                        if mode.jumpingDegreesToRotate>=0:
                            if accurateDegreesRotated-50<=\
                            mode.jumpingDegreesToRotate%360<=\
                            accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(21)
                                mode.isGameOver=True
                        elif mode.jumpingDegreesToRotate<0:
                            if accurateDegreesRotated-50<=\
                            mode.jumpingDegreesToRotate%360<=\
                            accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+710:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(22)
                                mode.isGameOver=True
                    mode.isJumping=False
                    mode.jumpingCounter=0
                    mode.playerFalling=False
            elif mode.hill2.type==3:
                polynomialType3Y=4.845901*(10**-12)-\
                0.9699877*(mode.player.cx%300)+\
                0.2069631*((mode.player.cx%300)**2)-\
                0.002649587*((mode.player.cx%300)**3)+\
                0.00001137466*((mode.player.cx%300)**4)-\
                1.589777*(10**-8)*((mode.player.cx%300)**5)
                if mode.hill2.startingY+polynomialType3Y-30<=mode.player.cy\
                <=mode.hill2.startingY+polynomialType3Y+30\
                and mode.playerFalling==True:
                    mode.counter+=1
                    newSlope=mode.derivative5((1.589777*(10**-8)), -0.000012472,\
                    0.003307988, -0.3277466, 7.576999, mode.player.cx%300)
                    accurateDegreesRotated=mode.findAngleInBetween(0, newSlope)
                    if mode.jumpingDegreesToRotate>=0:
                        if accurateDegreesRotated-50<=\
                        mode.jumpingDegreesToRotate%360<=\
                        accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+360:
                            print(f"successful landing! {mode.counter}")
                        else:
                            print(23)
                            mode.isGameOver=True
                    elif mode.jumpingDegreesToRotate<0:
                        if accurateDegreesRotated-50<=\
                        mode.jumpingDegreesToRotate%360<=\
                        accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+710:
                            print(f"successful landing! {mode.counter}")
                        else:
                            print(24)
                            mode.isGameOver=True
                    mode.isJumping=False
                    mode.jumpingCounter=0
                    mode.playerFalling=False
        elif mode.currentPlayerHill==3:
            if mode.hill3.type==0:
                if mode.hill3.startingY-30<=mode.player.cy<=\
                mode.hill3.endingY+30 and mode.playerFalling==True:
                    mode.counter+=1
                    if mode.jumpingDegreesToRotate>=0:
                        if -50<=mode.jumpingDegreesToRotate%360<=50 or\
                            310<=mode.jumpingDegreesToRotate%360<360:
                            print(f"successful landing! {mode.counter}")
                        else:
                            print(25)
                            mode.isGameOver=True
                    elif mode.jumpingDegreesToRotate<0:
                        if -50<=mode.jumpingDegreesToRotate%360<=50 or\
                            310<=mode.jumpingDegreesToRotate%360<710:
                            print(f"successful landing! {mode.counter}")
                        else:
                            print(26)
                            mode.isGameOver=True
                    mode.isJumping=False
                    mode.jumpingCounter=0
                    mode.playerFalling=False
            elif mode.hill3.type==1:
                polynomialType1Y=2.842171*(10**-14)+\
                0.1285714*(mode.player.cx%300)+\
                0.009843537*((mode.player.cx%300)**2)-\
                0.00002312925*((mode.player.cx%300)**3)
                if mode.hill3.startingY+polynomialType1Y-20<=mode.player.cy<=\
                mode.hill3.startingY+polynomialType1Y+20\
                and mode.playerFalling==True:
                    mode.counter+=1
                    if 0<=mode.player.cx%300<=40 or 250<=\
                    mode.player.cx%300<=300:
                        if mode.jumpingDegreesToRotate>=0:
                            if -50<=mode.jumpingDegreesToRotate%360<=50 or\
                            310<=mode.jumpingDegreesToRotate%360<360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(27)
                                mode.isGameOver=True
                        elif mode.jumpingDegreesToRotate<0:
                            if -50<=mode.jumpingDegreesToRotate%360<=50 or\
                            310<=mode.jumpingDegreesToRotate%360<710:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(28)
                                mode.isGameOver=True
                    else:
                        newSlope=mode.derivative3(0.00002312925,\
                        -0.01097279, 0.2102041, mode.player.cx%300)
                        accurateDegreesRotated=\
                        mode.findAngleInBetween(0, newSlope)
                        if mode.jumpingDegreesToRotate>=0:
                            if accurateDegreesRotated-50<=\
                            mode.jumpingDegreesToRotate%360<=\
                            accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(29)
                                mode.isGameOver=True
                        elif mode.jumpingDegreesToRotate<0:
                            if accurateDegreesRotated-50<=\
                            mode.jumpingDegreesToRotate%360<=\
                            accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+710:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(30)
                                mode.isGameOver=True
                    mode.isJumping=False
                    mode.jumpingCounter=0
                    mode.playerFalling=False
            elif mode.hill3.type==2:
                polynomialType2Y=-9.094947*(10**-13)-\
                0.875*(mode.player.cx%300)+0.06375*((mode.player.cx%300)**2)-\
                0.0006416667*((mode.player.cx%300)**3)+\
                0.0000025*((mode.player.cx%300)**4)-\
                3.333333*(10**-9)*((mode.player.cx%300)**5)
                if mode.hill3.startingY+polynomialType2Y-30<=mode.player.cy\
                <=mode.hill3.startingY+polynomialType2Y+30\
                and mode.playerFalling==True:
                    mode.counter+=1
                    if 100<=mode.player.cx%300<=180:
                        if mode.jumpingDegreesToRotate>=0:
                            if -100<=mode.jumpingDegreesToRotate%360<=0 or\
                                260<=mode.jumpingDegreesToRotate%360<360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(31)
                                mode.isGameOver=True
                        elif mode.jumpingDegreesToRotate<0:
                            if -100<=mode.jumpingDegreesToRotate%360<=0 or\
                            260<=mode.jumpingDegreesToRotate%360<360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(32)
                                mode.isGameOver=True
                    else:
                        newSlope=mode.derivative5((3.333333*10**-9), -0.0000025,\
                        0.0006416667, -0.06375, 0.875, mode.player.cx%300)
                        accurateDegreesRotated=\
                        mode.findAngleInBetween(0, newSlope)
                        if mode.jumpingDegreesToRotate>=0:
                            if accurateDegreesRotated-50<=\
                            mode.jumpingDegreesToRotate%360<=\
                            accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+360:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(33)
                                mode.isGameOver=True
                        elif mode.jumpingDegreesToRotate<0:
                            if accurateDegreesRotated-50<=\
                            mode.jumpingDegreesToRotate%360<=\
                            accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+710:
                                print(f"successful landing! {mode.counter}")
                            else:
                                print(34)
                                mode.isGameOver=True
                    mode.isJumping=False
                    mode.jumpingCounter=0
                    mode.playerFalling=False
            elif mode.hill3.type==3:
                polynomialType3Y=4.845901*(10**-12)-\
                0.9699877*(mode.player.cx%300)+\
                0.2069631*((mode.player.cx%300)**2)-\
                0.002649587*((mode.player.cx%300)**3)+\
                0.00001137466*((mode.player.cx%300)**4)-\
                1.589777*(10**-8)*((mode.player.cx%300)**5)
                if mode.hill3.startingY+polynomialType3Y-30<=mode.player.cy\
                <=mode.hill3.startingY+polynomialType3Y+30\
                and mode.playerFalling==True:
                    mode.counter+=1
                    newSlope=mode.derivative5((1.589777*(10**-8)), -0.000012472,\
                    0.003307988, -0.3277466, 7.576999, mode.player.cx%300)
                    accurateDegreesRotated=mode.findAngleInBetween(0, newSlope)
                    if mode.jumpingDegreesToRotate>=0:
                        if accurateDegreesRotated-50<=\
                        mode.jumpingDegreesToRotate%360<=\
                        accurateDegreesRotated+50 or accurateDegreesRotated\
                        +310<=mode.jumpingDegreesToRotate%360<\
                        accurateDegreesRotated+360:
                            print(f"successful landing! {mode.counter}")
                        else:
                            print(35)
                            mode.isGameOver=True
                    elif mode.jumpingDegreesToRotate<0:
                        if accurateDegreesRotated-50<=\
                        mode.jumpingDegreesToRotate%360<=\
                        accurateDegreesRotated+50 or accurateDegreesRotated\
                            +310<=mode.jumpingDegreesToRotate%360<\
                            accurateDegreesRotated+710:
                            print(f"successful landing! {mode.counter}")
                        else:
                            print(36)
                            mode.isGameOver=True
                    mode.isJumping=False
                    mode.jumpingCounter=0
                    mode.playerFalling=False

    def movePlayerWhileJumping(mode):
        if mode.jumpingCounter<=10:
            mode.player.cy-=10
        elif mode.jumpingCounter>10:
            mode.playerFalling=True
            mode.player.cy+=15
        mode.player.cx+=10

    def movePlayer(mode):
        #For hill 1
        if mode.currentPlayerHill==1:
            if mode.hill1.type==0:
                xChange=10
                newX=mode.player.cx+xChange
                newY=mode.hill1.startingY
                mode.player.cx=newX
                mode.player.cy=newY
                mode.snow.cx=mode.player.cx
                mode.snow.cy=mode.player.cy
                newPlayerImage=mode.loadImage("Alto.png")
                newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                mode.playerImage=newPlayerImage
                if mode.scarfElongated==False:
                    newScarfImage=mode.loadImage("Scarf 1.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    mode.scarfImage=newScarfImage
                elif mode.scarfElongated==True:
                    newScarfImage=mode.loadImage("Scarf 2.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    mode.scarfImage=newScarfImage
            elif mode.hill1.type==1:
                if mode.didHillSwitch==True:
                    oldX=0
                else:
                    oldX=mode.player.cx
                XChange=10
                newX=mode.player.cx+XChange
                polynomialY=2.842171*(10**-14)+0.1285714*(newX%300)+\
                0.009843537*((newX%300)**2)-0.00002312925*((newX%300)**3)
                newSlope=mode.derivative3(0.00002312925, -0.01097279,\
                0.2102041, newX%300)
                if newX%300>=150:
                    mode.amountToRotate=mode.amountToRotate-\
                    mode.amountPlayerRotated/15
                    newPlayerImage=mode.loadImage("Alto.png")
                    newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                    newPlayerImage=\
                    newPlayerImage.rotate(mode.amountToRotate)
                    mode.playerImage=newPlayerImage
                    if mode.scarfElongated==False:
                        newScarfImage=mode.loadImage("Scarf 1.png")
                        newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                        newScarfImage=newScarfImage.rotate(mode.amountToRotate)
                        mode.scarfImage=newScarfImage
                    elif mode.scarfElongated==True:
                        newScarfImage=mode.loadImage("Scarf 1.png")
                        newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                        newScarfImage=newScarfImage.rotate(mode.amountToRotate)
                        mode.scarfImage=newScarfImage
                else:
                    degreesToRotate=mode.findAngleInBetween(0, newSlope)
                    newPlayerImage=mode.loadImage("Alto.png")
                    newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                    newPlayerImage=newPlayerImage.rotate(degreesToRotate)
                    mode.playerImage=newPlayerImage
                    mode.amountPlayerRotated=degreesToRotate
                    mode.amountToRotate=mode.amountPlayerRotated
                    mode.amountScarfRotated=degreesToRotate
                    if mode.scarfElongated==False:
                        newScarfImage=mode.loadImage("Scarf 1.png")
                        newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                        newScarfImage=newScarfImage.rotate(degreesToRotate)
                        mode.scarfImage=newScarfImage
                    elif mode.scarfElongated==True:
                        newScarfImage=mode.loadImage("Scarf 2.png")
                        newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                        newScarfImage=newScarfImage.rotate(degreesToRotate)
                        mode.scarfImage=newScarfImage
                newY=mode.hill1.startingY+polynomialY
                mode.player.cx=newX
                mode.player.cy=newY
                mode.snow.cx=mode.player.cx
                mode.snow.cy=mode.player.cy
            elif mode.hill1.type==2:
                if mode.didHillSwitch==True:
                    oldX=0
                else:
                    oldX=mode.player.cx
                XChange=10
                newX=mode.player.cx+XChange
                polynomialY=-9.094947*(10**-13)-0.875*(newX%300)+\
                0.06375*((newX%300)**2)-0.0006416667*((newX%300)**3)+\
                0.0000025*((newX%300)**4)-3.333333*(10**-9)*((newX%300)**5)
                newSlope=mode.derivative5((3.333333*10**-9), -0.0000025,\
                0.0006416667, -0.06375, 0.875, mode.player.cx%300)
                degreesToRotate=mode.findAngleInBetween(0, newSlope)
                newPlayerImage=mode.loadImage("Alto.png")
                newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                newPlayerImage=newPlayerImage.rotate(degreesToRotate)
                mode.playerImage=newPlayerImage
                mode.amountPlayerRotated=degreesToRotate
                mode.amountToRotate=mode.amountPlayerRotated
                newY=mode.hill1.startingY+polynomialY
                mode.player.cx=newX
                mode.player.cy=newY
                mode.snow.cx=mode.player.cx
                mode.snow.cy=mode.player.cy
                if mode.scarfElongated==False:
                    newScarfImage=mode.loadImage("Scarf 1.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    newScarfImage=newScarfImage.rotate(degreesToRotate)
                    mode.scarfImage=newScarfImage
                elif mode.scarfElongated==True:
                    newScarfImage=mode.loadImage("Scarf 2.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    newScarfImage=newScarfImage.rotate(degreesToRotate)
                    mode.scarfImage=newScarfImage
            elif mode.hill1.type==3:
                if mode.didHillSwitch==True:
                    oldX=0
                else:
                    oldX=mode.player.cx
                XChange=10
                newX=mode.player.cx+XChange
                polynomialY=4.845901*(10**-12)-0.9699877*(newX%300)+\
                0.2069631*((newX%300)**2)-0.002649587*((newX%300)**3)+\
                0.00001137466*((newX%300)**4)-1.589777*(10**-8)*((newX%300)**5)
                newSlope=mode.derivative5((1.589777*(10**-8)), -0.000012472,\
                0.003307988, -0.3277466, 7.576999, newX%300)
                degreesToRotate=mode.findAngleInBetween(0, newSlope)
                newPlayerImage=mode.loadImage("Alto.png")
                newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                newPlayerImage=newPlayerImage.rotate(degreesToRotate)
                mode.playerImage=newPlayerImage
                mode.amountPlayerRotated=degreesToRotate
                mode.amountToRotate=mode.amountPlayerRotated
                newY=mode.hill1.startingY+polynomialY
                mode.player.cx=newX
                mode.player.cy=newY
                mode.snow.cx=mode.player.cx
                mode.snow.cy=mode.player.cy
                if mode.scarfElongated==False:
                    newScarfImage=mode.loadImage("Scarf 1.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    newScarfImage=newScarfImage.rotate(degreesToRotate)
                    mode.scarfImage=newScarfImage
                elif mode.scarfElongated==True:
                    newScarfImage=mode.loadImage("Scarf 2.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    newScarfImage=newScarfImage.rotate(degreesToRotate)
                    mode.scarfImage=newScarfImage
        #For hill 2
        if mode.currentPlayerHill==2:
            if mode.hill2.type==0:
                xChange=10
                newX=mode.player.cx+xChange
                newY=mode.hill2.startingY
                mode.player.cx=newX
                mode.player.cy=newY
                mode.snow.cx=mode.player.cx
                mode.snow.cy=mode.player.cy
                newPlayerImage=mode.loadImage("Alto.png")
                newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                mode.playerImage=newPlayerImage
                if mode.scarfElongated==False:
                    newScarfImage=mode.loadImage("Scarf 1.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    mode.scarfImage=newScarfImage
                elif mode.scarfElongated==True:
                    newScarfImage=mode.loadImage("Scarf 2.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    mode.scarfImage=newScarfImage
            elif mode.hill2.type==1:
                if mode.didHillSwitch==True:
                    oldX=0
                else:
                    oldX=mode.player.cx
                XChange=10
                newX=mode.player.cx+XChange
                polynomialY=2.842171*(10**-14)+0.1285714*(newX%300)+\
                0.009843537*((newX%300)**2)-0.00002312925*((newX%300)**3)
                currentSlope=0.00006*((oldX%300)**2)-\
                0.02194558*(oldX%300)+0.2102041
                newSlope=mode.derivative3(0.00002312925, -0.01097279,\
                0.2102041, newX%300)
                if newX%300>=150:
                    mode.amountToRotate=mode.amountToRotate-\
                    mode.amountPlayerRotated/15
                    newPlayerImage=mode.loadImage("Alto.png")
                    newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                    newPlayerImage=\
                    newPlayerImage.rotate(mode.amountToRotate)
                    mode.playerImage=newPlayerImage
                    if mode.scarfElongated==False:
                        newScarfImage=mode.loadImage("Scarf 1.png")
                        newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                        newScarfImage=newScarfImage.rotate(mode.amountToRotate)
                        mode.scarfImage=newScarfImage
                    elif mode.scarfElongated==True:
                        newScarfImage=mode.loadImage("Scarf 2.png")
                        newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                        newScarfImage=newScarfImage.rotate(mode.amountToRotate)
                        mode.scarfImage=newScarfImage
                else:
                    degreesToRotate=mode.findAngleInBetween(0, newSlope)
                    newPlayerImage=mode.loadImage("Alto.png")
                    newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                    newPlayerImage=newPlayerImage.rotate(degreesToRotate)
                    mode.playerImage=newPlayerImage
                    mode.amountPlayerRotated=degreesToRotate
                    mode.amountToRotate=mode.amountPlayerRotated
                    if mode.scarfElongated==False:
                        newScarfImage=mode.loadImage("Scarf 1.png")
                        newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                        newScarfImage=newScarfImage.rotate(degreesToRotate)
                        mode.scarfImage=newScarfImage
                    elif mode.scarfElongated==True:
                        newScarfImage=mode.loadImage("Scarf 2.png")
                        newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                        newScarfImage=newScarfImage.rotate(degreesToRotate)
                        mode.scarfImage=newScarfImage
                newY=mode.hill2.startingY+polynomialY
                mode.player.cx=newX
                mode.player.cy=newY
                mode.snow.cx=mode.player.cx
                mode.snow.cy=mode.player.cy
            elif mode.hill2.type==2:
                if mode.didHillSwitch==True:
                    oldX=0
                else:
                    oldX=mode.player.cx
                XChange=10
                newX=mode.player.cx+XChange
                polynomialY=-9.094947*(10**-13)-0.875*(newX%300)+\
                0.06375*((newX%300)**2)-0.0006416667*((newX%300)**3)+\
                0.0000025*((newX%300)**4)-3.333333*(10**-9)*((newX%300)**5)
                newSlope=mode.derivative5((3.333333*10**-9), -0.0000025,\
                0.0006416667, -0.06375, 0.875, newX%300)
                degreesToRotate=mode.findAngleInBetween(0, newSlope)
                newPlayerImage=mode.loadImage("Alto.png")
                newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                newPlayerImage=newPlayerImage.rotate(degreesToRotate)
                mode.playerImage=newPlayerImage
                mode.amountPlayerRotated=degreesToRotate
                mode.amountToRotate=mode.amountPlayerRotated
                newY=mode.hill2.startingY+polynomialY
                mode.player.cx=newX
                mode.player.cy=newY
                mode.snow.cx=mode.player.cx
                mode.snow.cy=mode.player.cy
                if mode.scarfElongated==False:
                    newScarfImage=mode.loadImage("Scarf 1.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    newScarfImage=newScarfImage.rotate(degreesToRotate)
                    mode.scarfImage=newScarfImage
                elif mode.scarfElongated==True:
                    newScarfImage=mode.loadImage("Scarf 2.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    newScarfImage=newScarfImage.rotate(degreesToRotate)
                    mode.scarfImage=newScarfImage
            elif mode.hill2.type==3:
                if mode.didHillSwitch==True:
                    oldX=0
                else:
                    oldX=mode.player.cx
                XChange=10
                newX=mode.player.cx+XChange
                polynomialY=4.845901*(10**-12)-0.9699877*(newX%300)+\
                0.2069631*((newX%300)**2)-0.002649587*((newX%300)**3)+\
                0.00001137466*((newX%300)**4)-1.589777*(10**-8)*((newX%300)**5)
                newSlope=mode.derivative5((1.589777*(10**-8)), -0.000012472,\
                0.003307988, -0.3277466, 7.576999, newX%300)
                degreesToRotate=mode.findAngleInBetween(0, newSlope)
                newPlayerImage=mode.loadImage("Alto.png")
                newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                newPlayerImage=newPlayerImage.rotate(degreesToRotate)
                mode.playerImage=newPlayerImage
                mode.amountPlayerRotated=degreesToRotate
                mode.amountToRotate=mode.amountPlayerRotated
                newY=mode.hill2.startingY+polynomialY
                mode.player.cx=newX
                mode.player.cy=newY
                mode.snow.cx=mode.player.cx
                mode.snow.cy=mode.player.cy
                if mode.scarfElongated==False:
                    newScarfImage=mode.loadImage("Scarf 1.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    newScarfImage=newScarfImage.rotate(degreesToRotate)
                    mode.scarfImage=newScarfImage
                elif mode.scarfElongated==True:
                    newScarfImage=mode.loadImage("Scarf 2.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    newScarfImage=newScarfImage.rotate(degreesToRotate)
                    mode.scarfImage=newScarfImage

        #For hill 3
        if mode.currentPlayerHill==3:
            if mode.hill3.type==0:
                xChange=10
                newX=mode.player.cx+xChange
                newY=mode.hill3.startingY
                mode.player.cx=newX
                mode.player.cy=newY
                mode.snow.cx=mode.player.cx
                mode.snow.cy=mode.player.cy
                newPlayerImage=mode.loadImage("Alto.png")
                newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                mode.playerImage=newPlayerImage
                if mode.scarfElongated==False:
                    newScarfImage=mode.loadImage("Scarf 1.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    mode.scarfImage=newScarfImage
                elif mode.scarfElongated==True:
                    newScarfImage=mode.loadImage("Scarf 2.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    mode.scarfImage=newScarfImage
            elif mode.hill3.type==1:
                if mode.didHillSwitch==True:
                    oldX=0
                else:
                    oldX=mode.player.cx
                XChange=10
                newX=mode.player.cx+XChange
                polynomialY=2.842171*(10**-14)+0.1285714*(newX%300)+\
                0.009843537*((newX%300)**2)-0.00002312925*((newX%300)**3)
                newSlope=mode.derivative3(0.00002312925, -0.01097279,\
                0.2102041, newX%300)
                if newX%300>=150:
                    mode.amountToRotate=mode.amountToRotate-\
                    mode.amountPlayerRotated/15
                    newPlayerImage=mode.loadImage("Alto.png")
                    newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                    newPlayerImage=\
                    newPlayerImage.rotate(mode.amountToRotate)
                    mode.playerImage=newPlayerImage
                    if mode.scarfElongated==False:
                        newScarfImage=mode.loadImage("Scarf 1.png")
                        newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                        newScarfImage=newScarfImage.rotate(mode.amountToRotate)
                        mode.scarfImage=newScarfImage
                    elif mode.scarfElongated==True:
                        newScarfImage=mode.loadImage("Scarf 2.png")
                        newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                        newScarfImage=newScarfImage.rotate(mode.amountToRotate)
                        mode.scarfImage=newScarfImage
                else:
                    degreesToRotate=mode.findAngleInBetween(0, newSlope)
                    newPlayerImage=mode.loadImage("Alto.png")
                    newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                    newPlayerImage=newPlayerImage.rotate(degreesToRotate)
                    mode.playerImage=newPlayerImage
                    mode.amountPlayerRotated=degreesToRotate
                    mode.amountToRotate=mode.amountPlayerRotated
                    if mode.scarfElongated==False:
                        newScarfImage=mode.loadImage("Scarf 1.png")
                        newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                        newScarfImage=newScarfImage.rotate(degreesToRotate)
                        mode.scarfImage=newScarfImage
                    elif mode.scarfElongated==True:
                        newScarfImage=mode.loadImage("Scarf 2.png")
                        newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                        newScarfImage=newScarfImage.rotate(degreesToRotate)
                        mode.scarfImage=newScarfImage
                newY=mode.hill3.startingY+polynomialY
                mode.player.cx=newX
                mode.player.cy=newY
                mode.snow.cx=mode.player.cx
                mode.snow.cy=mode.player.cy
            elif mode.hill3.type==2:
                if mode.didHillSwitch==True:
                    oldX=0
                else:
                    oldX=mode.player.cx
                XChange=10
                newX=mode.player.cx+XChange
                polynomialY=-9.094947*(10**-13)-0.875*(newX%300)+\
                0.06375*((newX%300)**2)-0.0006416667*((newX%300)**3)+\
                0.0000025*((newX%300)**4)-3.333333*(10**-9)*((newX%300)**5)
                newSlope=mode.derivative5((3.333333*10**-9), -0.0000025,\
                0.0006416667, -0.06375, 0.875, newX%300)
                degreesToRotate=mode.findAngleInBetween(0, newSlope)
                newPlayerImage=mode.loadImage("Alto.png")
                newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                newPlayerImage=newPlayerImage.rotate(degreesToRotate)
                mode.playerImage=newPlayerImage
                mode.amountPlayerRotated=degreesToRotate
                mode.amountToRotate=mode.amountPlayerRotated
                newY=mode.hill3.startingY+polynomialY
                mode.player.cx=newX
                mode.player.cy=newY
                mode.snow.cx=mode.player.cx
                mode.snow.cy=mode.player.cy
                if mode.scarfElongated==False:
                    newScarfImage=mode.loadImage("Scarf 1.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    newScarfImage=newScarfImage.rotate(degreesToRotate)
                    mode.scarfImage=newScarfImage
                elif mode.scarfElongated==True:
                    newScarfImage=mode.loadImage("Scarf 2.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    newScarfImage=newScarfImage.rotate(degreesToRotate)
                    mode.scarfImage=newScarfImage
            elif mode.hill3.type==3:
                if mode.didHillSwitch==True:
                    oldX=0
                else:
                    oldX=mode.player.cx
                XChange=10
                newX=mode.player.cx+XChange
                polynomialY=4.845901*(10**-12)-0.9699877*(newX%300)+\
                0.2069631*((newX%300)**2)-0.002649587*((newX%300)**3)+\
                0.00001137466*((newX%300)**4)-1.589777*(10**-8)*((newX%300)**5)
                newSlope=mode.derivative5((1.589777*(10**-8)), -0.000012472,\
                0.003307988, -0.3277466, 7.576999, newX%300)
                degreesToRotate=mode.findAngleInBetween(0, newSlope)
                newPlayerImage=mode.loadImage("Alto.png")
                newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
                newPlayerImage=newPlayerImage.rotate(degreesToRotate)
                mode.playerImage=newPlayerImage
                mode.amountPlayerRotated=degreesToRotate
                mode.amountToRotate=mode.amountPlayerRotated
                newY=mode.hill3.startingY+polynomialY
                mode.player.cx=newX
                mode.player.cy=newY
                mode.snow.cx=mode.player.cx
                mode.snow.cy=mode.player.cy
                if mode.scarfElongated==False:
                    newScarfImage=mode.loadImage("Scarf 1.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    newScarfImage=newScarfImage.rotate(degreesToRotate)
                    mode.scarfImage=newScarfImage
                elif mode.scarfElongated==True:
                    newScarfImage=mode.loadImage("Scarf 1.png")
                    newScarfImage=mode.scaleImage(newScarfImage, 1/7)
                    newScarfImage=newScarfImage.rotate(degreesToRotate)
                    mode.scarfImage=newScarfImage

    #Creates a new hill once a player passes a certain value on the canvas
    def createNewHill(mode):
        if mode.currentPlayerHill==3:
            mode.hill1=mode.hill2
            mode.hill2=mode.hill3
            mode.hill3=Hill(mode, mode.hill2.endingX, mode.hill2.endingY)
            typeOfHill=random.randint(0, 3)
            if typeOfHill==0:
                mode.hill3.generateHillType0()
            elif typeOfHill==1:
                mode.hill3.generateHillType1()
            elif typeOfHill==2:
                mode.hill3.generateHillType2()
            elif typeOfHill==3:
                mode.hill3.generateHillType3()

    #Checks which hill the player is on!
    def checkCurrentPlayerHill(mode):
        if mode.hill1.startingX<=mode.player.cx<mode.hill1.endingX-10:
            currentPlayerHill=1
            if mode.currentPlayerHill!=currentPlayerHill:
                mode.currentPlayerHill=currentPlayerHill
                mode.didHillSwitch=True
            else:
                mode.didHillSwitch=False
        elif mode.hill2.startingX-10<=mode.player.cx<mode.hill2.endingX-10:
            currentPlayerHill=2
            if mode.currentPlayerHill!=currentPlayerHill:
                mode.currentPlayerHill=currentPlayerHill
                mode.didHillSwitch=True
            else:
                mode.didHillSwitch=False
        #Add negative 10 to account for timer fired discrepancy
        elif mode.hill3.startingX-10<=mode.player.cx<mode.hill3.endingX:
            currentPlayerHill=3
            if mode.currentPlayerHill!=currentPlayerHill:
                #Slightly alters height of player between hill type 2 and type 0
                if mode.hill3.type==0 and mode.hill2.type==2:
                    mode.player.cy-=2
                mode.currentPlayerHill=currentPlayerHill
                mode.didHillSwitch=True
            else:
                mode.didHillSwitch=False
        #Add negative 10 to account for timer fired discrepancy

    #Basically for the help button, will delete the left right stuff laterrrr
    def keyPressed(mode, event):
        if event.key=="h":
            mode.app.setActiveMode(mode.app.helpMode)
        elif event.key=="Space" and mode.isJumping==False:
            mode.isJumping=True
            mode.jumpingDegreesForFlip=0
        elif event.key=="Space" and mode.isJumping==True and\
        mode.numberOfFlips>0:
            mode.jumpingCounter=0
            del mode.jumpInventory[mode.numberOfFlips]
            mode.numberOfFlips-=1
        elif event.key=="Left" and mode.isJumping==True and\
        mode.cooldown==False:
            mode.jumpingDegreesToRotate+=10
            mode.jumpingDegreesForFlip+=10
            newPlayerImage=mode.loadImage("Alto.png")
            newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
            newPlayerImage=newPlayerImage.rotate(mode.jumpingDegreesToRotate)
            mode.playerImage=newPlayerImage
            mode.cooldown=True
        elif event.key=="Right" and mode.isJumping==True and\
        mode.cooldown==False:
            mode.jumpingDegreesToRotate-=10
            mode.jumpingDegreesForFlip-=10
            newPlayerImage=mode.loadImage("Alto.png")
            newPlayerImage=mode.scaleImage(newPlayerImage, 1/20)
            newPlayerImage=newPlayerImage.rotate(mode.jumpingDegreesToRotate)
            mode.playerImage=newPlayerImage
            mode.cooldown=True
        elif event.key=="k":
            mode.app.setActiveMode(mode.app.gameOverMode)
    
    def keyReleased(mode, event):
        if event.key=="Left" and mode.isJumping==True and mode.cooldown==True:
            mode.cooldown=False
        elif event.key=="Right" and mode.isJumping==True and\
        mode.cooldown==True:
            mode.cooldown=False
    
    #Key element of the game, genuinely makes the player visible lol
    def makePlayerVisible(mode):
        if mode.player.cx>mode.scrollX+mode.width-mode.scrollMarginX:
            mode.scrollX=mode.player.cx-mode.width+mode.scrollMarginX
        if mode.player.cy<mode.scrollY+mode.scrollMarginY:
            mode.scrollY=mode.player.cy-mode.scrollMarginY
        if mode.player.cy>mode.scrollY+mode.height-mode.scrollMarginY:
            mode.scrollY=mode.player.cy-mode.height+mode.scrollMarginY
        if mode.player.cx<5+mode.scrollX:
            mode.scrollX=mode.player.cx-5

    #Draws the player based on scroll
    def drawPlayer(mode, canvas):
        if mode.currentPlayerHill==1:
            if mode.hill1.type==0:
                playerX=mode.player.cx-mode.scrollX
                playerY=mode.player.cy-mode.scrollY-10
                canvas.create_image(playerX, playerY,\
                image=ImageTk.PhotoImage(mode.playerImage))
            elif mode.hill1.type==1:
                playerX=mode.player.cx-mode.scrollX+5
                playerY=mode.player.cy-mode.scrollY-10
                canvas.create_image(playerX, playerY,\
                image=ImageTk.PhotoImage(mode.playerImage))
            elif mode.hill1.type==2:
                playerX=mode.player.cx-mode.scrollX+5
                playerY=mode.player.cy-mode.scrollY-10
                canvas.create_image(playerX, playerY,\
                image=ImageTk.PhotoImage(mode.playerImage))
            elif mode.hill1.type==3:
                if 0<=mode.player.cx%300<100 and mode.isJumping==False:
                    playerX=mode.player.cx-mode.scrollX+12
                    playerY=mode.player.cy-mode.scrollY
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))
                elif 100<=mode.player.cx%300<200 and mode.isJumping==False:
                    playerX=mode.player.cx-mode.scrollX-12
                    playerY=mode.player.cy-mode.scrollY
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))
                elif 200<=mode.player.cx%300<285 and mode.isJumping==False:
                    playerX=mode.player.cx-mode.scrollX+12
                    playerY=mode.player.cy-mode.scrollY
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))
                elif 285<=mode.player.cx%300<300 and mode.isJumping==False:
                    playerX=mode.player.cx-mode.scrollX
                    playerY=mode.player.cy-mode.scrollY-40
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))
                else:
                    playerX=mode.player.cx-mode.scrollX
                    playerY=mode.player.cy-mode.scrollY
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))

        if mode.currentPlayerHill==2:
            if mode.hill2.type==0:
                playerX=mode.player.cx-mode.scrollX
                playerY=mode.player.cy-mode.scrollY-10
                canvas.create_image(playerX, playerY,\
                image=ImageTk.PhotoImage(mode.playerImage))
            elif mode.hill2.type==1:
                playerX=mode.player.cx-mode.scrollX+5
                playerY=mode.player.cy-mode.scrollY-10
                canvas.create_image(playerX, playerY,\
                image=ImageTk.PhotoImage(mode.playerImage))
            elif mode.hill2.type==2:
                playerX=mode.player.cx-mode.scrollX+5
                playerY=mode.player.cy-mode.scrollY-10
                canvas.create_image(playerX, playerY,\
                image=ImageTk.PhotoImage(mode.playerImage))
            elif mode.hill2.type==3:
                if 0<=mode.player.cx%300<100 and mode.isJumping==False:
                    playerX=mode.player.cx-mode.scrollX+12
                    playerY=mode.player.cy-mode.scrollY
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))
                elif 100<=mode.player.cx%300<200 and mode.isJumping==False:
                    playerX=mode.player.cx-mode.scrollX-12
                    playerY=mode.player.cy-mode.scrollY
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))
                elif 200<=mode.player.cx%300<285 and mode.isJumping==False:
                    playerX=mode.player.cx-mode.scrollX+12
                    playerY=mode.player.cy-mode.scrollY
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))
                elif 285<=mode.player.cx%300<300 and mode.isJumping==False:
                    playerX=mode.player.cx-mode.scrollX
                    playerY=mode.player.cy-mode.scrollY-40
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))
                else:
                    playerX=mode.player.cx-mode.scrollX
                    playerY=mode.player.cy-mode.scrollY
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))

        if mode.currentPlayerHill==3:
            if mode.hill3.type==0:
                playerX=mode.player.cx-mode.scrollX
                playerY=mode.player.cy-mode.scrollY-10
                canvas.create_image(playerX, playerY,\
                image=ImageTk.PhotoImage(mode.playerImage))             
            elif mode.hill3.type==1:
                playerX=mode.player.cx-mode.scrollX+5
                playerY=mode.player.cy-mode.scrollY-10
                canvas.create_image(playerX, playerY,\
                image=ImageTk.PhotoImage(mode.playerImage))
            elif mode.hill3.type==2:
                playerX=mode.player.cx-mode.scrollX+5
                playerY=mode.player.cy-mode.scrollY-10
                canvas.create_image(playerX, playerY,\
                image=ImageTk.PhotoImage(mode.playerImage))
            elif mode.hill3.type==3:
                if 0<=mode.player.cx%300<100 and mode.isJumping==False:
                    playerX=mode.player.cx-mode.scrollX+12
                    playerY=mode.player.cy-mode.scrollY
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))
                elif 100<=mode.player.cx%300<200 and mode.isJumping==False:
                    playerX=mode.player.cx-mode.scrollX-12
                    playerY=mode.player.cy-mode.scrollY
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))
                elif 200<=mode.player.cx%300<285 and mode.isJumping==False:
                    playerX=mode.player.cx-mode.scrollX+12
                    playerY=mode.player.cy-mode.scrollY
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))
                elif 285<=mode.player.cx%300<300 and mode.isJumping==False:
                    playerX=mode.player.cx-mode.scrollX
                    playerY=mode.player.cy-mode.scrollY-40
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))
                else:
                    playerX=mode.player.cx-mode.scrollX
                    playerY=mode.player.cy-mode.scrollY
                    canvas.create_image(playerX, playerY,\
                    image=ImageTk.PhotoImage(mode.playerImage))

    #Next three functions will essentially just draw the hill depending on its
    #type, uses a bunch of math and polynomial equations to get it done :)
    def drawHill1(mode, canvas):
        #For hill type 0
        if mode.hill1.type==0:
            x0=mode.hill1.startingX-mode.scrollX
            y0=mode.hill1.startingY-mode.scrollY
            for i in range(1, mode.width//2+1):
                x1=mode.hill1.startingX+i-mode.scrollX
                y1=mode.hill1.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1
        #y of starting x of hill plus mode.player.cx%300
        elif mode.hill1.type==1:
            x0=mode.hill1.startingX-mode.scrollX
            y0=mode.hill1.startingY-mode.scrollY
            for i in range(1, mode.width//2+1):
                x1=mode.hill1.startingX+i-mode.scrollX
                polynomialY=2.842171*(10**-14)+0.1285714*(i)+0.009843537*(i**2)\
            -0.00002312925*(i**3) #lol this equation is icky
                y1=polynomialY+mode.hill1.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1
        elif mode.hill1.type==2:
            x0=mode.hill1.startingX-mode.scrollX
            y0=mode.hill1.startingY-mode.scrollY
            for i in range(1, mode.width//2+1):
                x1=mode.hill1.startingX+i-mode.scrollX
                polynomialY=-9.094947*(10**-13)-0.875*(i)+0.06375*(i**2)\
            -0.0006416667*(i**3)+0.0000025*(i**4)-3.333333*(10**-9)*(i**5)
            #Another icky equation...there seems to be a trend
                y1=polynomialY+mode.hill1.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1
        elif mode.hill1.type==3:
            x0=mode.hill1.startingX-mode.scrollX
            y0=mode.hill1.startingY-mode.scrollY
            for i in range(1, 51):
                x1=mode.hill1.startingX+i-mode.scrollX
                polynomialY=4.845901*(10**-12)-0.9699877*(i)+0.2069631*(i**2)-\
            0.002649587*(i**3)+0.00001137466*(i**4)-1.589777*(10**-8)*(i**5)
                y1=polynomialY+mode.hill1.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1
            x0=mode.hill1.startingX+150-mode.scrollX
            specialPolynomialY=4.845901*(10**-12)-0.9699877*(150)+\
            0.2069631*(150**2)-0.002649587*(150**3)+0.00001137466*(150**4)-\
            1.589777*(10**-8)*(150**5)
            y0=mode.hill1.startingY+specialPolynomialY-mode.scrollY
            for i in range(151, 256):
                x1=mode.hill1.startingX+i-mode.scrollX
                polynomialY=4.845901*(10**-12)-0.9699877*(i)+0.2069631*(i**2)-\
            0.002649587*(i**3)+0.00001137466*(i**4)-1.589777*(10**-8)*(i**5)
                y1=polynomialY+mode.hill1.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1

    #To draw second hill
    def drawHill2(mode, canvas):
        #For hill type 0
        if mode.hill2.type==0:
            x0=mode.hill2.startingX-mode.scrollX
            y0=mode.hill2.startingY-mode.scrollY
            for i in range(1, mode.width//2+1):
                x1=mode.hill2.startingX+i-mode.scrollX
                y1=mode.hill2.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1
        elif mode.hill2.type==1:
            x0=mode.hill2.startingX-mode.scrollX
            y0=mode.hill2.startingY-mode.scrollY
            for i in range(1, mode.width//2+1):
                x1=mode.hill2.startingX+i-mode.scrollX
                polynomialY=2.842171*(10**-14)+0.1285714*(i)+0.009843537*(i**2)\
            -0.00002312925*(i**3) #lol this equation is icky
                y1=polynomialY+mode.hill2.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1
        elif mode.hill2.type==2:
            x0=mode.hill2.startingX-mode.scrollX
            y0=mode.hill2.startingY-mode.scrollY
            for i in range(1, mode.width//2+1):
                x1=mode.hill2.startingX+i-mode.scrollX
                polynomialY=-9.094947*(10**-13)-0.875*(i)+0.06375*(i**2)\
            -0.0006416667*(i**3)+0.0000025*(i**4)-3.333333*(10**-9)*(i**5)
                y1=polynomialY+mode.hill2.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1
        elif mode.hill2.type==3:
            x0=mode.hill2.startingX-mode.scrollX
            y0=mode.hill2.startingY-mode.scrollY
            for i in range(1, 51):
                x1=mode.hill2.startingX+i-mode.scrollX
                polynomialY=4.845901*(10**-12)-0.9699877*(i)+0.2069631*(i**2)-\
            0.002649587*(i**3)+0.00001137466*(i**4)-1.589777*(10**-8)*(i**5)
                y1=polynomialY+mode.hill2.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1
            x0=mode.hill2.startingX+150-mode.scrollX
            specialPolynomialY=4.845901*(10**-12)-0.9699877*(150)+\
            0.2069631*(150**2)-0.002649587*(150**3)+0.00001137466*(150**4)-\
            1.589777*(10**-8)*(150**5)
            y0=mode.hill2.startingY+specialPolynomialY-mode.scrollY
            for i in range(151, 255):
                x1=mode.hill2.startingX+i-mode.scrollX
                polynomialY=4.845901*(10**-12)-0.9699877*(i)+0.2069631*(i**2)-\
            0.002649587*(i**3)+0.00001137466*(i**4)-1.589777*(10**-8)*(i**5)
                y1=polynomialY+mode.hill2.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1

    #To draw third hill
    def drawHill3(mode, canvas):
        #For hill type 0
        if mode.hill3.type==0:
            x0=mode.hill3.startingX-mode.scrollX
            y0=mode.hill3.startingY-mode.scrollY
            for i in range(1, mode.width//2+1):
                x1=mode.hill3.startingX+i-mode.scrollX
                y1=mode.hill3.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1
        #For hill type 1
        elif mode.hill3.type==1:
            x0=mode.hill3.startingX-mode.scrollX
            y0=mode.hill3.startingY-mode.scrollY
            for i in range(1, mode.width//2+1):
                x1=mode.hill3.startingX+i-mode.scrollX
                polynomialY=2.842171*(10**-14)+0.1285714*(i)+0.009843537*(i**2)\
            -0.00002312925*(i**3) #lol this equation is icky
                y1=polynomialY+mode.hill3.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1
        elif mode.hill3.type==2:
            x0=mode.hill3.startingX-mode.scrollX
            y0=mode.hill3.startingY-mode.scrollY
            for i in range(1, mode.width//2+1):
                x1=mode.hill3.startingX+i-mode.scrollX
                polynomialY=-9.094947*(10**-13)-0.875*(i)+0.06375*(i**2)\
            -0.0006416667*(i**3)+0.0000025*(i**4)-3.333333*(10**-9)*(i**5)
                y1=polynomialY+mode.hill3.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1
        elif mode.hill3.type==3:
            x0=mode.hill3.startingX-mode.scrollX
            y0=mode.hill3.startingY-mode.scrollY
            for i in range(1, 51):
                x1=mode.hill3.startingX+i-mode.scrollX
                polynomialY=4.845901*(10**-12)-0.9699877*(i)+0.2069631*(i**2)-\
            0.002649587*(i**3)+0.00001137466*(i**4)-1.589777*(10**-8)*(i**5)
                y1=polynomialY+mode.hill3.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1
            x0=mode.hill3.startingX+150-mode.scrollX
            specialPolynomialY=4.845901*(10**-12)-0.9699877*(150)+\
            0.2069631*(150**2)-0.002649587*(150**3)+0.00001137466*(150**4)-\
            1.589777*(10**-8)*(150**5)
            y0=mode.hill3.startingY+specialPolynomialY-mode.scrollY
            for i in range(151, 255):
                x1=mode.hill3.startingX+i-mode.scrollX
                polynomialY=4.845901*(10**-12)-0.9699877*(i)+0.2069631*(i**2)-\
            0.002649587*(i**3)+0.00001137466*(i**4)-1.589777*(10**-8)*(i**5)
                y1=polynomialY+mode.hill3.startingY-mode.scrollY
                canvas.create_line(x0, y0, x1, y1)
                x0=x1
                y0=y1
    
    def drawRock(mode, canvas):
        if mode.rock.hillType==0:
            x=mode.rock.cx-mode.scrollX
            y=mode.rock.cy-mode.scrollY-11
            canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.rockImage))
        elif mode.rock.hillType==1:
            x=mode.rock.cx-mode.scrollX+5
            y=mode.rock.cy-mode.scrollY-10
            canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.rockImage))
        elif mode.rock.hillType==2:
            x=mode.rock.cx-mode.scrollX+5
            y=mode.rock.cy-mode.scrollY-10
            canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.rockImage))
    
    def drawSnow1(mode, canvas):
        x=mode.player.cx-mode.scrollX
        y=mode.player.cy-mode.scrollY
        if mode.currentPlayerHill==1 and mode.isJumping==False:
            if mode.hill1.type==0:
                canvas.create_oval(x-15, y-7,\
                x-15+200/30, y-7+200/30)
                canvas.create_polygon(x-15,\
                y-7+100/30, x-15+100/30,\
                y-7, x-15+200/30,\
                y-7+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-15,\
                y-7+100/30, x-15+100/30,\
                y-7+200/30, x-15+200/30,\
                y-7+200/30, fill="white", outline="light blue")
                canvas.create_line(x-15+1, y-7+1,\
                x-15+170/30, y-7+170/30)
                canvas.create_line(x-15+1,\
                y-7+170/30, x-15+170/30,\
                y-7+1)
            elif mode.hill1.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-15, y-7,\
                    x-15+200/30, y-7+200/30)
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7, x-15+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7+200/30, x-15+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-7+1,\
                    x-15+170/30, y-7+170/30)
                    canvas.create_line(x-15+1,\
                    y-7+170/30, x-15+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-15, y-20,\
                    x-15+200/30, y-20+200/30)
                    canvas.create_polygon(x-15,\
                    y-20+100/30, x-15+100/30,\
                    y-20, x-15+200/30,\
                    y-20+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-20+100/30, x-15+100/30,\
                    y-20+200/30, x-15+200/30,\
                    y-20+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-20+1,\
                    x-15+170/30, y-20+170/30)
                    canvas.create_line(x-15+1,\
                    y-20+170/30, x-15+170/30,\
                    y-20+1)
            elif mode.hill1.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-12, y-22,\
                    x-12+200/30, y-22+200/30)
                    canvas.create_polygon(x-12,\
                    y-22+100/30, x-12+100/30,\
                    y-22, x-12+200/30,\
                    y-22+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-12,\
                    y-22+100/30, x-12+100/30,\
                    y-22+200/30, x-12+200/30,\
                    y-22+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-12+1, y-22+1,\
                    x-12+170/30, y-22+170/30)
                    canvas.create_line(x-12+1,\
                    y-22+170/30, x-12+170/30,\
                    y-22+1)
                else:
                    canvas.create_oval(x-15, y-7,\
                    x-15+200/30, y-7+200/30)
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7, x-15+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7+200/30, x-15+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-7+1,\
                    x-15+170/30, y-7+170/30)
                    canvas.create_line(x-15+1,\
                    y-7+170/30, x-15+170/30,\
                    y-7+1)
            elif mode.hill1.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-15, y+7,\
                    x-15+200/30, y+7+200/30)
                    canvas.create_polygon(x-15,\
                    y+7+100/30, x-15+100/30,\
                    y+7, x-15+200/30,\
                    y+7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y+7+100/30, x-15+100/30,\
                    y+7+200/30, x-15+200/30,\
                    y+7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y+7+1,\
                    x-15+170/30, y+7+170/30)
                    canvas.create_line(x-15+1,\
                    y+7+170/30, x-15+170/30,\
                    y+7+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-15, y-7,\
                    x-15+200/30, y-7+200/30)
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7, x-15+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7+200/30, x-15+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-7+1,\
                    x-15+170/30, y-7+170/30)
                    canvas.create_line(x-15+1,\
                    y-7+170/30, x-15+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-12, y-22,\
                    x-12+200/30, y-22+200/30)
                    canvas.create_polygon(x-12,\
                    y-22+100/30, x-12+100/30,\
                    y-22, x-12+200/30,\
                    y-22+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-12,\
                    y-22+100/30, x-12+100/30,\
                    y-22+200/30, x-12+200/30,\
                    y-22+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-12+1, y-22+1,\
                    x-12+170/30, y-22+170/30)
                    canvas.create_line(x-12+1,\
                    y-22+170/30, x-12+170/30,\
                    y-22+1)

        elif mode.currentPlayerHill==2 and mode.isJumping==False:
            if mode.hill2.type==0:
                canvas.create_oval(x-15, y-7,\
                x-15+200/30, y-7+200/30)
                canvas.create_polygon(x-15,\
                y-7+100/30, x-15+100/30,\
                y-7, x-15+200/30,\
                y-7+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-15,\
                y-7+100/30, x-15+100/30,\
                y-7+200/30, x-15+200/30,\
                y-7+200/30, fill="white", outline="light blue")
                canvas.create_line(x-15+1, y-7+1,\
                x-15+170/30, y-7+170/30)
                canvas.create_line(x-15+1,\
                y-7+170/30, x-15+170/30,\
                y-7+1)
            elif mode.hill2.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-15, y-7,\
                    x-15+200/30, y-7+200/30)
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7, x-15+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7+200/30, x-15+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-7+1,\
                    x-15+170/30, y-7+170/30)
                    canvas.create_line(x-15+1,\
                    y-7+170/30, x-15+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-15, y-20,\
                    x-15+200/30, y-20+200/30)
                    canvas.create_polygon(x-15,\
                    y-20+100/30, x-15+100/30,\
                    y-20, x-15+200/30,\
                    y-20+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-20+100/30, x-15+100/30,\
                    y-20+200/30, x-15+200/30,\
                    y-20+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-20+1,\
                    x-15+170/30, y-20+170/30)
                    canvas.create_line(x-15+1,\
                    y-20+170/30, x-15+170/30,\
                    y-20+1)
            elif mode.hill2.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-12, y-22,\
                    x-12+200/30, y-22+200/30)
                    canvas.create_polygon(x-12,\
                    y-22+100/30, x-12+100/30,\
                    y-22, x-12+200/30,\
                    y-22+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-12,\
                    y-22+100/30, x-12+100/30,\
                    y-22+200/30, x-12+200/30,\
                    y-22+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-12+1, y-22+1,\
                    x-12+170/30, y-22+170/30)
                    canvas.create_line(x-12+1,\
                    y-22+170/30, x-12+170/30,\
                    y-22+1)
                else:
                    canvas.create_oval(x-15, y-7,\
                    x-15+200/30, y-7+200/30)
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7, x-15+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7+200/30, x-15+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-7+1,\
                    x-15+170/30, y-7+170/30)
                    canvas.create_line(x-15+1,\
                    y-7+170/30, x-15+170/30,\
                    y-7+1)
            elif mode.hill2.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-15, y+7,\
                    x-15+200/30, y+7+200/30)
                    canvas.create_polygon(x-15,\
                    y+7+100/30, x-15+100/30,\
                    y+7, x-15+200/30,\
                    y+7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y+7+100/30, x-15+100/30,\
                    y+7+200/30, x-15+200/30,\
                    y+7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y+7+1,\
                    x-15+170/30, y+7+170/30)
                    canvas.create_line(x-15+1,\
                    y+7+170/30, x-15+170/30,\
                    y+7+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-15, y-7,\
                    x-15+200/30, y-7+200/30)
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7, x-15+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7+200/30, x-15+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-7+1,\
                    x-15+170/30, y-7+170/30)
                    canvas.create_line(x-15+1,\
                    y-7+170/30, x-15+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-12, y-22,\
                    x-12+200/30, y-22+200/30)
                    canvas.create_polygon(x-12,\
                    y-22+100/30, x-12+100/30,\
                    y-22, x-12+200/30,\
                    y-22+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-12,\
                    y-22+100/30, x-12+100/30,\
                    y-22+200/30, x-12+200/30,\
                    y-22+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-12+1, y-22+1,\
                    x-12+170/30, y-22+170/30)
                    canvas.create_line(x-12+1,\
                    y-22+170/30, x-12+170/30,\
                    y-22+1)
                    

        elif mode.currentPlayerHill==3 and mode.isJumping==False:
            if mode.hill3.type==0:
                canvas.create_oval(x-15, y-7,\
                x-15+200/30, y-7+200/30)
                canvas.create_polygon(x-15,\
                y-7+100/30, x-15+100/30,\
                y-7, x-15+200/30,\
                y-7+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-15,\
                y-7+100/30, x-15+100/30,\
                y-7+200/30, x-15+200/30,\
                y-7+200/30, fill="white", outline="light blue")
                canvas.create_line(x-15+1, y-7+1,\
                x-15+170/30, y-7+170/30)
                canvas.create_line(x-15+1,\
                y-7+170/30, x-15+170/30,\
                y-7+1)
            elif mode.hill3.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-15, y-7,\
                    x-15+200/30, y-7+200/30)
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7, x-15+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7+200/30, x-15+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-7+1,\
                    x-15+170/30, y-7+170/30)
                    canvas.create_line(x-15+1,\
                    y-7+170/30, x-15+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-15, y-20,\
                    x-15+200/30, y-20+200/30)
                    canvas.create_polygon(x-15,\
                    y-20+100/30, x-15+100/30,\
                    y-20, x-15+200/30,\
                    y-20+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-20+100/30, x-15+100/30,\
                    y-20+200/30, x-15+200/30,\
                    y-20+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-20+1,\
                    x-15+170/30, y-20+170/30)
                    canvas.create_line(x-15+1,\
                    y-20+170/30, x-15+170/30,\
                    y-20+1)
            elif mode.hill3.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-12, y-22,\
                    x-12+200/30, y-22+200/30)
                    canvas.create_polygon(x-12,\
                    y-22+100/30, x-12+100/30,\
                    y-22, x-12+200/30,\
                    y-22+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-12,\
                    y-22+100/30, x-12+100/30,\
                    y-22+200/30, x-12+200/30,\
                    y-22+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-12+1, y-22+1,\
                    x-12+170/30, y-22+170/30)
                    canvas.create_line(x-12+1,\
                    y-22+170/30, x-12+170/30,\
                    y-22+1)
                else:
                    canvas.create_oval(x-15, y-7,\
                    x-15+200/30, y-7+200/30)
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7, x-15+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7+200/30, x-15+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-7+1,\
                    x-15+170/30, y-7+170/30)
                    canvas.create_line(x-15+1,\
                    y-7+170/30, x-15+170/30,\
                    y-7+1)
            elif mode.hill3.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-15, y+7,\
                    x-15+200/30, y+7+200/30)
                    canvas.create_polygon(x-15,\
                    y+7+100/30, x-15+100/30,\
                    y+7, x-15+200/30,\
                    y+7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y+7+100/30, x-15+100/30,\
                    y+7+200/30, x-15+200/30,\
                    y+7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y+7+1,\
                    x-15+170/30, y+7+170/30)
                    canvas.create_line(x-15+1,\
                    y+7+170/30, x-15+170/30,\
                    y+7+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-15, y-7,\
                    x-15+200/30, y-7+200/30)
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7, x-15+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-7+100/30, x-15+100/30,\
                    y-7+200/30, x-15+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-7+1,\
                    x-15+170/30, y-7+170/30)
                    canvas.create_line(x-15+1,\
                    y-7+170/30, x-15+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-12, y-22,\
                    x-12+200/30, y-22+200/30)
                    canvas.create_polygon(x-12,\
                    y-22+100/30, x-12+100/30,\
                    y-22, x-12+200/30,\
                    y-22+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-12,\
                    y-22+100/30, x-12+100/30,\
                    y-22+200/30, x-12+200/30,\
                    y-22+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-12+1, y-22+1,\
                    x-12+170/30, y-22+170/30)
                    canvas.create_line(x-12+1,\
                    y-22+170/30, x-12+170/30,\
                    y-22+1)
    
    def drawSnow2(mode, canvas):
        x=mode.player.cx-mode.scrollX
        y=mode.player.cy-mode.scrollY
        if mode.currentPlayerHill==1 and mode.isJumping==False:
            if mode.hill1.type==0:
                canvas.create_oval(x-20, y-12,\
                x-20+200/30, y-12+200/30)
                canvas.create_polygon(x-20,\
                y-12+100/30, x-20+100/30,\
                y-12, x-20+200/30,\
                y-12+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-20,\
                y-12+100/30, x-20+100/30,\
                y-12+200/30, x-20+200/30,\
                y-12+200/30, fill="white", outline="light blue")
                canvas.create_line(x-20+1, y-12+1,\
                x-20+170/30, y-12+170/30)
                canvas.create_line(x-20+1,\
                y-12+170/30, x-20+170/30,\
                y-12+1)
            elif mode.hill1.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-20, y-12,\
                    x-20+200/30, y-12+200/30)
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12, x-20+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12+200/30, x-20+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-12+1,\
                    x-20+170/30, y-12+170/30)
                    canvas.create_line(x-20+1,\
                    y-12+170/30, x-20+170/30,\
                    y-12+1)
                else:
                    canvas.create_oval(x-10, y-27,\
                    x-10+200/30, y-27+200/30)
                    canvas.create_polygon(x-10,\
                    y-27+100/30, x-10+100/30,\
                    y-27, x-10+200/30,\
                    y-27+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-10,\
                    y-27+100/30, x-10+100/30,\
                    y-27+200/30, x-10+200/30,\
                    y-27+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-10+1, y-27+1,\
                    x-10+170/30, y-27+170/30)
                    canvas.create_line(x-10+1,\
                    y-27+170/30, x-10+170/30,\
                    y-27+1)
            elif mode.hill1.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-8, y-29,\
                    x-8+200/30, y-29+200/30)
                    canvas.create_polygon(x-8,\
                    y-29+100/30, x-8+100/30,\
                    y-29, x-8+200/30,\
                    y-29+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-8,\
                    y-29+100/30, x-8+100/30,\
                    y-29+200/30, x-8+200/30,\
                    y-29+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-8+1, y-29+1,\
                    x-8+170/30, y-29+170/30)
                    canvas.create_line(x-8+1,\
                    y-29+170/30, x-8+170/30,\
                    y-29+1)
                else:
                    canvas.create_oval(x-20, y-12,\
                    x-20+200/30, y-12+200/30)
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12, x-20+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12+200/30, x-20+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-12+1,\
                    x-20+170/30, y-12+170/30)
                    canvas.create_line(x-20+1,\
                    y-12+170/30, x-20+170/30,\
                    y-12+1)
            elif mode.hill1.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-20, y+12,\
                    x-20+200/30, y+12+200/30)
                    canvas.create_polygon(x-20,\
                    y+12+100/30, x-20+100/30,\
                    y+12, x-20+200/30,\
                    y+12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y+12+100/30, x-20+100/30,\
                    y+12+200/30, x-20+200/30,\
                    y+12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y+12+1,\
                    x-20+170/30, y+12+170/30)
                    canvas.create_line(x-20+1,\
                    y+12+170/30, x-20+170/30,\
                    y+12+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-20, y-12,\
                    x-20+200/30, y-12+200/30)
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12, x-20+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12+200/30, x-20+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-12+1,\
                    x-20+170/30, y-12+170/30)
                    canvas.create_line(x-20+1,\
                    y-12+170/30, x-20+170/30,\
                    y-12+1)
                else:
                    canvas.create_oval(x-8, y-29,\
                    x-8+200/30, y-29+200/30)
                    canvas.create_polygon(x-8,\
                    y-29+100/30, x-8+100/30,\
                    y-29, x-8+200/30,\
                    y-29+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-8,\
                    y-29+100/30, x-8+100/30,\
                    y-29+200/30, x-8+200/30,\
                    y-29+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-8+1, y-29+1,\
                    x-8+170/30, y-29+170/30)
                    canvas.create_line(x-8+1,\
                    y-29+170/30, x-8+170/30,\
                    y-29+1)
        elif mode.currentPlayerHill==2 and mode.isJumping==False:
            if mode.hill2.type==0:
                canvas.create_oval(x-20, y-12,\
                x-20+200/30, y-12+200/30)
                canvas.create_polygon(x-20,\
                y-12+100/30, x-20+100/30,\
                y-12, x-20+200/30,\
                y-12+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-20,\
                y-12+100/30, x-20+100/30,\
                y-12+200/30, x-20+200/30,\
                y-12+200/30, fill="white", outline="light blue")
                canvas.create_line(x-20+1, y-12+1,\
                x-20+170/30, y-12+170/30)
                canvas.create_line(x-20+1,\
                y-12+170/30, x-20+170/30,\
                y-12+1)
            elif mode.hill2.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-20, y-12,\
                    x-20+200/30, y-12+200/30)
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12, x-20+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12+200/30, x-20+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-12+1,\
                    x-20+170/30, y-12+170/30)
                    canvas.create_line(x-20+1,\
                    y-12+170/30, x-20+170/30,\
                    y-12+1)
                else:
                    canvas.create_oval(x-10, y-27,\
                    x-10+200/30, y-27+200/30)
                    canvas.create_polygon(x-10,\
                    y-27+100/30, x-10+100/30,\
                    y-27, x-10+200/30,\
                    y-27+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-10,\
                    y-27+100/30, x-10+100/30,\
                    y-27+200/30, x-10+200/30,\
                    y-27+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-10+1, y-27+1,\
                    x-10+170/30, y-27+170/30)
                    canvas.create_line(x-10+1,\
                    y-27+170/30, x-10+170/30,\
                    y-27+1)
            elif mode.hill2.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-8, y-29,\
                    x-8+200/30, y-29+200/30)
                    canvas.create_polygon(x-8,\
                    y-29+100/30, x-8+100/30,\
                    y-29, x-8+200/30,\
                    y-29+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-8,\
                    y-29+100/30, x-8+100/30,\
                    y-29+200/30, x-8+200/30,\
                    y-29+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-8+1, y-29+1,\
                    x-8+170/30, y-29+170/30)
                    canvas.create_line(x-8+1,\
                    y-29+170/30, x-8+170/30,\
                    y-29+1)
                else:
                    canvas.create_oval(x-20, y-12,\
                    x-20+200/30, y-12+200/30)
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12, x-20+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12+200/30, x-20+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-12+1,\
                    x-20+170/30, y-12+170/30)
                    canvas.create_line(x-20+1,\
                    y-12+170/30, x-20+170/30,\
                    y-12+1)
            elif mode.hill2.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-20, y+12,\
                    x-20+200/30, y+12+200/30)
                    canvas.create_polygon(x-20,\
                    y+12+100/30, x-20+100/30,\
                    y+12, x-20+200/30,\
                    y+12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y+12+100/30, x-20+100/30,\
                    y+12+200/30, x-20+200/30,\
                    y+12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y+12+1,\
                    x-20+170/30, y+12+170/30)
                    canvas.create_line(x-20+1,\
                    y+12+170/30, x-20+170/30,\
                    y+12+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-20, y-12,\
                    x-20+200/30, y-12+200/30)
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12, x-20+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12+200/30, x-20+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-12+1,\
                    x-20+170/30, y-12+170/30)
                    canvas.create_line(x-20+1,\
                    y-12+170/30, x-20+170/30,\
                    y-12+1)
                else:
                    canvas.create_oval(x-8, y-29,\
                    x-8+200/30, y-29+200/30)
                    canvas.create_polygon(x-8,\
                    y-29+100/30, x-8+100/30,\
                    y-29, x-8+200/30,\
                    y-29+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-8,\
                    y-29+100/30, x-8+100/30,\
                    y-29+200/30, x-8+200/30,\
                    y-29+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-8+1, y-29+1,\
                    x-8+170/30, y-29+170/30)
                    canvas.create_line(x-8+1,\
                    y-29+170/30, x-8+170/30,\
                    y-29+1)
        elif mode.currentPlayerHill==3 and mode.isJumping==False:
            if mode.hill3.type==0:
                canvas.create_oval(x-20, y-12,\
                x-20+200/30, y-12+200/30)
                canvas.create_polygon(x-20,\
                y-12+100/30, x-20+100/30,\
                y-12, x-20+200/30,\
                y-12+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-20,\
                y-12+100/30, x-20+100/30,\
                y-12+200/30, x-20+200/30,\
                y-12+200/30, fill="white", outline="light blue")
                canvas.create_line(x-20+1, y-12+1,\
                x-20+170/30, y-12+170/30)
                canvas.create_line(x-20+1,\
                y-12+170/30, x-20+170/30,\
                y-12+1)
            elif mode.hill3.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-20, y-12,\
                    x-20+200/30, y-12+200/30)
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12, x-20+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12+200/30, x-20+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-12+1,\
                    x-20+170/30, y-12+170/30)
                    canvas.create_line(x-20+1,\
                    y-12+170/30, x-20+170/30,\
                    y-12+1)
                else:
                    canvas.create_oval(x-10, y-27,\
                    x-10+200/30, y-27+200/30)
                    canvas.create_polygon(x-10,\
                    y-27+100/30, x-10+100/30,\
                    y-27, x-10+200/30,\
                    y-27+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-10,\
                    y-27+100/30, x-10+100/30,\
                    y-27+200/30, x-10+200/30,\
                    y-27+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-10+1, y-27+1,\
                    x-10+170/30, y-27+170/30)
                    canvas.create_line(x-10+1,\
                    y-27+170/30, x-10+170/30,\
                    y-27+1)
            elif mode.hill3.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-8, y-29,\
                    x-8+200/30, y-29+200/30)
                    canvas.create_polygon(x-8,\
                    y-29+100/30, x-8+100/30,\
                    y-29, x-8+200/30,\
                    y-29+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-8,\
                    y-29+100/30, x-8+100/30,\
                    y-29+200/30, x-8+200/30,\
                    y-29+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-8+1, y-29+1,\
                    x-8+170/30, y-29+170/30)
                    canvas.create_line(x-8+1,\
                    y-29+170/30, x-8+170/30,\
                    y-29+1)
                else:
                    canvas.create_oval(x-20, y-12,\
                    x-20+200/30, y-12+200/30)
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12, x-20+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12+200/30, x-20+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-12+1,\
                    x-20+170/30, y-12+170/30)
                    canvas.create_line(x-20+1,\
                    y-12+170/30, x-20+170/30,\
                    y-12+1)
            elif mode.hill3.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-20, y+12,\
                    x-20+200/30, y+12+200/30)
                    canvas.create_polygon(x-20,\
                    y+12+100/30, x-20+100/30,\
                    y+12, x-20+200/30,\
                    y+12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y+12+100/30, x-20+100/30,\
                    y+12+200/30, x-20+200/30,\
                    y+12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y+12+1,\
                    x-20+170/30, y+12+170/30)
                    canvas.create_line(x-20+1,\
                    y+12+170/30, x-20+170/30,\
                    y+12+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-20, y-12,\
                    x-20+200/30, y-12+200/30)
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12, x-20+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-12+100/30, x-20+100/30,\
                    y-12+200/30, x-20+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-12+1,\
                    x-20+170/30, y-12+170/30)
                    canvas.create_line(x-20+1,\
                    y-12+170/30, x-20+170/30,\
                    y-12+1)
                else:
                    canvas.create_oval(x-8, y-29,\
                    x-8+200/30, y-29+200/30)
                    canvas.create_polygon(x-8,\
                    y-29+100/30, x-8+100/30,\
                    y-29, x-8+200/30,\
                    y-29+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-8,\
                    y-29+100/30, x-8+100/30,\
                    y-29+200/30, x-8+200/30,\
                    y-29+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-8+1, y-29+1,\
                    x-8+170/30, y-29+170/30)
                    canvas.create_line(x-8+1,\
                    y-29+170/30, x-8+170/30,\
                    y-29+1)

    def drawSnow3(mode, canvas):
        x=mode.player.cx-mode.scrollX
        y=mode.player.cy-mode.scrollY
        if mode.currentPlayerHill==1 and mode.isJumping==False:
            if mode.hill1.type==0:
                canvas.create_oval(x-20, y-7,\
                x-20+200/30, y-7+200/30)
                canvas.create_polygon(x-20,\
                y-7+100/30, x-20+100/30,\
                y-7, x-20+200/30,\
                y-7+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-20,\
                y-7+100/30, x-20+100/30,\
                y-7+200/30, x-20+200/30,\
                y-7+200/30, fill="white", outline="light blue")
                canvas.create_line(x-20+1, y-7+1,\
                x-20+170/30, y-7+170/30)
                canvas.create_line(x-20+1,\
                y-7+170/30, x-20+170/30,\
                y-7+1)
            elif mode.hill1.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-20, y-7,\
                    x-20+200/30, y-7+200/30)
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7, x-20+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7+200/30, x-20+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-7+1,\
                    x-20+170/30, y-7+170/30)
                    canvas.create_line(x-20+1,\
                    y-7+170/30, x-20+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-15, y-27,\
                    x-15+200/30, y-27+200/30)
                    canvas.create_polygon(x-15,\
                    y-27+100/30, x-15+100/30,\
                    y-27, x-15+200/30,\
                    y-27+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-27+100/30, x-15+100/30,\
                    y-27+200/30, x-15+200/30,\
                    y-27+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-27+1,\
                    x-15+170/30, y-27+170/30)
                    canvas.create_line(x-15+1,\
                    y-27+170/30, x-15+170/30,\
                    y-27+1)
            elif mode.hill1.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-15, y-29,\
                    x-15+200/30, y-29+200/30)
                    canvas.create_polygon(x-15,\
                    y-29+100/30, x-15+100/30,\
                    y-29, x-15+200/30,\
                    y-29+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-29+100/30, x-15+100/30,\
                    y-29+200/30, x-15+200/30,\
                    y-29+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-29+1,\
                    x-15+170/30, y-29+170/30)
                    canvas.create_line(x-15+1,\
                    y-29+170/30, x-15+170/30,\
                    y-29+1)
                else:
                    canvas.create_oval(x-20, y-7,\
                    x-20+200/30, y-7+200/30)
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7, x-20+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7+200/30, x-20+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-7+1,\
                    x-20+170/30, y-7+170/30)
                    canvas.create_line(x-20+1,\
                    y-7+170/30, x-20+170/30,\
                    y-7+1)
            elif mode.hill1.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-15, y+15,\
                    x-15+200/30, y+15+200/30)
                    canvas.create_polygon(x-15,\
                    y+15+100/30, x-15+100/30,\
                    y+15, x-15+200/30,\
                    y+15+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y+15+100/30, x-15+100/30,\
                    y+15+200/30, x-15+200/30,\
                    y+15+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y+15+1,\
                    x-15+170/30, y+15+170/30)
                    canvas.create_line(x-15+1,\
                    y+15+170/30, x-15+170/30,\
                    y+15+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-20, y-7,\
                    x-20+200/30, y-7+200/30)
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7, x-20+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7+200/30, x-20+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-7+1,\
                    x-20+170/30, y-7+170/30)
                    canvas.create_line(x-20+1,\
                    y-7+170/30, x-20+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-15, y-29,\
                    x-15+200/30, y-29+200/30)
                    canvas.create_polygon(x-15,\
                    y-29+100/30, x-15+100/30,\
                    y-29, x-15+200/30,\
                    y-29+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-29+100/30, x-15+100/30,\
                    y-29+200/30, x-15+200/30,\
                    y-29+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-29+1,\
                    x-15+170/30, y-29+170/30)
                    canvas.create_line(x-15+1,\
                    y-29+170/30, x-15+170/30,\
                    y-29+1)

        elif mode.currentPlayerHill==2 and mode.isJumping==False:
            if mode.hill2.type==0:
                canvas.create_oval(x-20, y-7,\
                x-20+200/30, y-7+200/30)
                canvas.create_polygon(x-20,\
                y-7+100/30, x-20+100/30,\
                y-7, x-20+200/30,\
                y-7+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-20,\
                y-7+100/30, x-20+100/30,\
                y-7+200/30, x-20+200/30,\
                y-7+200/30, fill="white", outline="light blue")
                canvas.create_line(x-20+1, y-7+1,\
                x-20+170/30, y-7+170/30)
                canvas.create_line(x-20+1,\
                y-7+170/30, x-20+170/30,\
                y-7+1)
            elif mode.hill2.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-20, y-7,\
                    x-20+200/30, y-7+200/30)
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7, x-20+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7+200/30, x-20+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-7+1,\
                    x-20+170/30, y-7+170/30)
                    canvas.create_line(x-20+1,\
                    y-7+170/30, x-20+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-15, y-27,\
                    x-15+200/30, y-27+200/30)
                    canvas.create_polygon(x-15,\
                    y-27+100/30, x-15+100/30,\
                    y-27, x-15+200/30,\
                    y-27+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-27+100/30, x-15+100/30,\
                    y-27+200/30, x-15+200/30,\
                    y-27+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-27+1,\
                    x-15+170/30, y-27+170/30)
                    canvas.create_line(x-15+1,\
                    y-27+170/30, x-15+170/30,\
                    y-27+1)
            elif mode.hill2.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-15, y-29,\
                    x-15+200/30, y-29+200/30)
                    canvas.create_polygon(x-15,\
                    y-29+100/30, x-15+100/30,\
                    y-29, x-15+200/30,\
                    y-29+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-29+100/30, x-15+100/30,\
                    y-29+200/30, x-15+200/30,\
                    y-29+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-29+1,\
                    x-15+170/30, y-29+170/30)
                    canvas.create_line(x-15+1,\
                    y-29+170/30, x-15+170/30,\
                    y-29+1)
                else:
                    canvas.create_oval(x-20, y-7,\
                    x-20+200/30, y-7+200/30)
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7, x-20+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7+200/30, x-20+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-7+1,\
                    x-20+170/30, y-7+170/30)
                    canvas.create_line(x-20+1,\
                    y-7+170/30, x-20+170/30,\
                    y-7+1)
            elif mode.hill2.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-15, y+15,\
                    x-15+200/30, y+15+200/30)
                    canvas.create_polygon(x-15,\
                    y+15+100/30, x-15+100/30,\
                    y+15, x-15+200/30,\
                    y+15+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y+15+100/30, x-15+100/30,\
                    y+15+200/30, x-15+200/30,\
                    y+15+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y+15+1,\
                    x-15+170/30, y+15+170/30)
                    canvas.create_line(x-15+1,\
                    y+15+170/30, x-15+170/30,\
                    y+15+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-20, y-7,\
                    x-20+200/30, y-7+200/30)
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7, x-20+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7+200/30, x-20+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-7+1,\
                    x-20+170/30, y-7+170/30)
                    canvas.create_line(x-20+1,\
                    y-7+170/30, x-20+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-15, y-29,\
                    x-15+200/30, y-29+200/30)
                    canvas.create_polygon(x-15,\
                    y-29+100/30, x-15+100/30,\
                    y-29, x-15+200/30,\
                    y-29+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-29+100/30, x-15+100/30,\
                    y-29+200/30, x-15+200/30,\
                    y-29+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-29+1,\
                    x-15+170/30, y-29+170/30)
                    canvas.create_line(x-15+1,\
                    y-29+170/30, x-15+170/30,\
                    y-29+1)
        elif mode.currentPlayerHill==3 and mode.isJumping==False:
            if mode.hill3.type==0:
                canvas.create_oval(x-20, y-7,\
                x-20+200/30, y-7+200/30)
                canvas.create_polygon(x-20,\
                y-7+100/30, x-20+100/30,\
                y-7, x-20+200/30,\
                y-7+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-20,\
                y-7+100/30, x-20+100/30,\
                y-7+200/30, x-20+200/30,\
                y-7+200/30, fill="white", outline="light blue")
                canvas.create_line(x-20+1, y-7+1,\
                x-20+170/30, y-7+170/30)
                canvas.create_line(x-20+1,\
                y-7+170/30, x-20+170/30,\
                y-7+1)
            elif mode.hill3.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-20, y-7,\
                    x-20+200/30, y-7+200/30)
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7, x-20+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7+200/30, x-20+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-7+1,\
                    x-20+170/30, y-7+170/30)
                    canvas.create_line(x-20+1,\
                    y-7+170/30, x-20+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-15, y-27,\
                    x-15+200/30, y-27+200/30)
                    canvas.create_polygon(x-15,\
                    y-27+100/30, x-15+100/30,\
                    y-27, x-15+200/30,\
                    y-27+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-27+100/30, x-15+100/30,\
                    y-27+200/30, x-15+200/30,\
                    y-27+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-27+1,\
                    x-15+170/30, y-27+170/30)
                    canvas.create_line(x-15+1,\
                    y-27+170/30, x-15+170/30,\
                    y-27+1)
            elif mode.hill3.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-15, y-29,\
                    x-15+200/30, y-29+200/30)
                    canvas.create_polygon(x-15,\
                    y-29+100/30, x-15+100/30,\
                    y-29, x-15+200/30,\
                    y-29+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-29+100/30, x-15+100/30,\
                    y-29+200/30, x-15+200/30,\
                    y-29+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-29+1,\
                    x-15+170/30, y-29+170/30)
                    canvas.create_line(x-15+1,\
                    y-29+170/30, x-15+170/30,\
                    y-29+1)
                else:
                    canvas.create_oval(x-20, y-7,\
                    x-20+200/30, y-7+200/30)
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7, x-20+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7+200/30, x-20+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-7+1,\
                    x-20+170/30, y-7+170/30)
                    canvas.create_line(x-20+1,\
                    y-7+170/30, x-20+170/30,\
                    y-7+1)
            elif mode.hill3.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-15, y+15,\
                    x-15+200/30, y+15+200/30)
                    canvas.create_polygon(x-15,\
                    y+15+100/30, x-15+100/30,\
                    y+15, x-15+200/30,\
                    y+15+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y+15+100/30, x-15+100/30,\
                    y+15+200/30, x-15+200/30,\
                    y+15+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y+15+1,\
                    x-15+170/30, y+15+170/30)
                    canvas.create_line(x-15+1,\
                    y+15+170/30, x-15+170/30,\
                    y+15+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-20, y-7,\
                    x-20+200/30, y-7+200/30)
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7, x-20+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-7+100/30, x-20+100/30,\
                    y-7+200/30, x-20+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-7+1,\
                    x-20+170/30, y-7+170/30)
                    canvas.create_line(x-20+1,\
                    y-7+170/30, x-20+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-15, y-29,\
                    x-15+200/30, y-29+200/30)
                    canvas.create_polygon(x-15,\
                    y-29+100/30, x-15+100/30,\
                    y-29, x-15+200/30,\
                    y-29+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-15,\
                    y-29+100/30, x-15+100/30,\
                    y-29+200/30, x-15+200/30,\
                    y-29+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-15+1, y-29+1,\
                    x-15+170/30, y-29+170/30)
                    canvas.create_line(x-15+1,\
                    y-29+170/30, x-15+170/30,\
                    y-29+1)

    def drawSnow4(mode, canvas):
        x=mode.player.cx-mode.scrollX
        y=mode.player.cy-mode.scrollY
        if mode.currentPlayerHill==1 and mode.isJumping==False:
            if mode.hill1.type==0:
                canvas.create_oval(x-25, y-12,\
                x-25+200/30, y-12+200/30)
                canvas.create_polygon(x-25,\
                y-12+100/30, x-25+100/30,\
                y-12, x-25+200/30,\
                y-12+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-25,\
                y-12+100/30, x-25+100/30,\
                y-12+200/30, x-25+200/30,\
                y-12+200/30, fill="white", outline="light blue")
                canvas.create_line(x-25+1, y-12+1,\
                x-25+170/30, y-12+170/30)
                canvas.create_line(x-25+1,\
                y-12+170/30, x-25+170/30,\
                y-12+1)
            elif mode.hill1.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-25, y-12,\
                    x-25+200/30, y-12+200/30)
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12, x-25+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12+200/30, x-25+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-12+1,\
                    x-25+170/30, y-12+170/30)
                    canvas.create_line(x-25+1,\
                    y-12+170/30, x-25+170/30,\
                    y-12+1)
                else:
                    canvas.create_oval(x-13, y-35,\
                    x-13+200/30, y-35+200/30)
                    canvas.create_polygon(x-13,\
                    y-35+100/30, x-13+100/30,\
                    y-35, x-13+200/30,\
                    y-35+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-13,\
                    y-35+100/30, x-13+100/30,\
                    y-35+200/30, x-13+200/30,\
                    y-35+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-13+1, y-35+1,\
                    x-13+170/30, y-35+170/30)
                    canvas.create_line(x-13+1,\
                    y-35+170/30, x-13+170/30,\
                    y-35+1)
            elif mode.hill1.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-11, y-36,\
                    x-11+200/30, y-36+200/30)
                    canvas.create_polygon(x-11,\
                    y-36+100/30, x-11+100/30,\
                    y-36, x-11+200/30,\
                    y-36+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-11,\
                    y-36+100/30, x-11+100/30,\
                    y-36+200/30, x-11+200/30,\
                    y-36+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-11+1, y-36+1,\
                    x-11+170/30, y-36+170/30)
                    canvas.create_line(x-11+1,\
                    y-36+170/30, x-11+170/30,\
                    y-36+1)
                else:
                    canvas.create_oval(x-25, y-12,\
                    x-25+200/30, y-12+200/30)
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12, x-25+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12+200/30, x-25+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-12+1,\
                    x-25+170/30, y-12+170/30)
                    canvas.create_line(x-25+1,\
                    y-12+170/30, x-25+170/30,\
                    y-12+1)
            elif mode.hill1.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-23, y+19,\
                    x-23+200/30, y+19+200/30)
                    canvas.create_polygon(x-23,\
                    y+19+100/30, x-23+100/30,\
                    y+19, x-23+200/30,\
                    y+19+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-23,\
                    y+19+100/30, x-23+100/30,\
                    y+19+200/30, x-23+200/30,\
                    y+19+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-23+1, y+19+1,\
                    x-23+170/30, y+19+170/30)
                    canvas.create_line(x-23+1,\
                    y+19+170/30, x-23+170/30,\
                    y+19+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-25, y-12,\
                    x-25+200/30, y-12+200/30)
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12, x-25+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12+200/30, x-25+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-12+1,\
                    x-25+170/30, y-12+170/30)
                    canvas.create_line(x-25+1,\
                    y-12+170/30, x-25+170/30,\
                    y-12+1)
                else:
                    canvas.create_oval(x-11, y-36,\
                    x-11+200/30, y-36+200/30)
                    canvas.create_polygon(x-11,\
                    y-36+100/30, x-11+100/30,\
                    y-36, x-11+200/30,\
                    y-36+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-11,\
                    y-36+100/30, x-11+100/30,\
                    y-36+200/30, x-11+200/30,\
                    y-36+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-11+1, y-36+1,\
                    x-11+170/30, y-36+170/30)
                    canvas.create_line(x-11+1,\
                    y-36+170/30, x-11+170/30,\
                    y-36+1)

        elif mode.currentPlayerHill==2 and mode.isJumping==False:
            if mode.hill2.type==0:
                canvas.create_oval(x-25, y-12,\
                x-25+200/30, y-12+200/30)
                canvas.create_polygon(x-25,\
                y-12+100/30, x-25+100/30,\
                y-12, x-25+200/30,\
                y-12+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-25,\
                y-12+100/30, x-25+100/30,\
                y-12+200/30, x-25+200/30,\
                y-12+200/30, fill="white", outline="light blue")
                canvas.create_line(x-25+1, y-12+1,\
                x-25+170/30, y-12+170/30)
                canvas.create_line(x-25+1,\
                y-12+170/30, x-25+170/30,\
                y-12+1)
            elif mode.hill2.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-25, y-12,\
                    x-25+200/30, y-12+200/30)
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12, x-25+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12+200/30, x-25+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-12+1,\
                    x-25+170/30, y-12+170/30)
                    canvas.create_line(x-25+1,\
                    y-12+170/30, x-25+170/30,\
                    y-12+1)
                else:
                    canvas.create_oval(x-13, y-35,\
                    x-13+200/30, y-35+200/30)
                    canvas.create_polygon(x-13,\
                    y-35+100/30, x-13+100/30,\
                    y-35, x-13+200/30,\
                    y-35+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-13,\
                    y-35+100/30, x-13+100/30,\
                    y-35+200/30, x-13+200/30,\
                    y-35+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-13+1, y-35+1,\
                    x-13+170/30, y-35+170/30)
                    canvas.create_line(x-13+1,\
                    y-35+170/30, x-13+170/30,\
                    y-35+1)
            elif mode.hill2.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-11, y-36,\
                    x-11+200/30, y-36+200/30)
                    canvas.create_polygon(x-11,\
                    y-36+100/30, x-11+100/30,\
                    y-36, x-11+200/30,\
                    y-36+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-11,\
                    y-36+100/30, x-11+100/30,\
                    y-36+200/30, x-11+200/30,\
                    y-36+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-11+1, y-36+1,\
                    x-11+170/30, y-36+170/30)
                    canvas.create_line(x-11+1,\
                    y-36+170/30, x-11+170/30,\
                    y-36+1)
                else:
                    canvas.create_oval(x-25, y-12,\
                    x-25+200/30, y-12+200/30)
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12, x-25+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12+200/30, x-25+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-12+1,\
                    x-25+170/30, y-12+170/30)
                    canvas.create_line(x-25+1,\
                    y-12+170/30, x-25+170/30,\
                    y-12+1)
            elif mode.hill2.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-23, y+19,\
                    x-23+200/30, y+19+200/30)
                    canvas.create_polygon(x-23,\
                    y+19+100/30, x-23+100/30,\
                    y+19, x-23+200/30,\
                    y+19+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-23,\
                    y+19+100/30, x-23+100/30,\
                    y+19+200/30, x-23+200/30,\
                    y+19+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-23+1, y+19+1,\
                    x-23+170/30, y+19+170/30)
                    canvas.create_line(x-23+1,\
                    y+19+170/30, x-23+170/30,\
                    y+19+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-25, y-12,\
                    x-25+200/30, y-12+200/30)
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12, x-25+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12+200/30, x-25+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-12+1,\
                    x-25+170/30, y-12+170/30)
                    canvas.create_line(x-25+1,\
                    y-12+170/30, x-25+170/30,\
                    y-12+1)
                else:
                    canvas.create_oval(x-11, y-36,\
                    x-11+200/30, y-36+200/30)
                    canvas.create_polygon(x-11,\
                    y-36+100/30, x-11+100/30,\
                    y-36, x-11+200/30,\
                    y-36+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-11,\
                    y-36+100/30, x-11+100/30,\
                    y-36+200/30, x-11+200/30,\
                    y-36+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-11+1, y-36+1,\
                    x-11+170/30, y-36+170/30)
                    canvas.create_line(x-11+1,\
                    y-36+170/30, x-11+170/30,\
                    y-36+1)
        elif mode.currentPlayerHill==3 and mode.isJumping==False:
            if mode.hill3.type==0:
                canvas.create_oval(x-25, y-12,\
                x-25+200/30, y-12+200/30)
                canvas.create_polygon(x-25,\
                y-12+100/30, x-25+100/30,\
                y-12, x-25+200/30,\
                y-12+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-25,\
                y-12+100/30, x-25+100/30,\
                y-12+200/30, x-25+200/30,\
                y-12+200/30, fill="white", outline="light blue")
                canvas.create_line(x-25+1, y-12+1,\
                x-25+170/30, y-12+170/30)
                canvas.create_line(x-25+1,\
                y-12+170/30, x-25+170/30,\
                y-12+1)
            elif mode.hill3.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-25, y-12,\
                    x-25+200/30, y-12+200/30)
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12, x-25+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12+200/30, x-25+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-12+1,\
                    x-25+170/30, y-12+170/30)
                    canvas.create_line(x-25+1,\
                    y-12+170/30, x-25+170/30,\
                    y-12+1)
                else:
                    canvas.create_oval(x-13, y-35,\
                    x-13+200/30, y-35+200/30)
                    canvas.create_polygon(x-13,\
                    y-35+100/30, x-13+100/30,\
                    y-35, x-13+200/30,\
                    y-35+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-13,\
                    y-35+100/30, x-13+100/30,\
                    y-35+200/30, x-13+200/30,\
                    y-35+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-13+1, y-35+1,\
                    x-13+170/30, y-35+170/30)
                    canvas.create_line(x-13+1,\
                    y-35+170/30, x-13+170/30,\
                    y-35+1)
            elif mode.hill3.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-11, y-36,\
                    x-11+200/30, y-36+200/30)
                    canvas.create_polygon(x-11,\
                    y-36+100/30, x-11+100/30,\
                    y-36, x-11+200/30,\
                    y-36+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-11,\
                    y-36+100/30, x-11+100/30,\
                    y-36+200/30, x-11+200/30,\
                    y-36+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-11+1, y-36+1,\
                    x-11+170/30, y-36+170/30)
                    canvas.create_line(x-11+1,\
                    y-36+170/30, x-11+170/30,\
                    y-36+1)
                else:
                    canvas.create_oval(x-25, y-12,\
                    x-25+200/30, y-12+200/30)
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12, x-25+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12+200/30, x-25+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-12+1,\
                    x-25+170/30, y-12+170/30)
                    canvas.create_line(x-25+1,\
                    y-12+170/30, x-25+170/30,\
                    y-12+1)
            elif mode.hill3.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-23, y+19,\
                    x-23+200/30, y+19+200/30)
                    canvas.create_polygon(x-23,\
                    y+19+100/30, x-23+100/30,\
                    y+19, x-23+200/30,\
                    y+19+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-23,\
                    y+19+100/30, x-23+100/30,\
                    y+19+200/30, x-23+200/30,\
                    y+19+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-23+1, y+19+1,\
                    x-23+170/30, y+19+170/30)
                    canvas.create_line(x-23+1,\
                    y+19+170/30, x-23+170/30,\
                    y+19+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-25, y-12,\
                    x-25+200/30, y-12+200/30)
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12, x-25+200/30,\
                    y-12+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-12+100/30, x-25+100/30,\
                    y-12+200/30, x-25+200/30,\
                    y-12+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-12+1,\
                    x-25+170/30, y-12+170/30)
                    canvas.create_line(x-25+1,\
                    y-12+170/30, x-25+170/30,\
                    y-12+1)
                else:
                    canvas.create_oval(x-11, y-36,\
                    x-11+200/30, y-36+200/30)
                    canvas.create_polygon(x-11,\
                    y-36+100/30, x-11+100/30,\
                    y-36, x-11+200/30,\
                    y-36+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-11,\
                    y-36+100/30, x-11+100/30,\
                    y-36+200/30, x-11+200/30,\
                    y-36+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-11+1, y-36+1,\
                    x-11+170/30, y-36+170/30)
                    canvas.create_line(x-11+1,\
                    y-36+170/30, x-11+170/30,\
                    y-36+1)
    
    def drawSnow5(mode, canvas):
        x=mode.player.cx-mode.scrollX
        y=mode.player.cy-mode.scrollY
        if mode.currentPlayerHill==1 and mode.isJumping==False:
            if mode.hill1.type==0:
                canvas.create_oval(x-25, y-7,\
                x-25+200/30, y-7+200/30)
                canvas.create_polygon(x-25,\
                y-7+100/30, x-25+100/30,\
                y-7, x-25+200/30,\
                y-7+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-25,\
                y-7+100/30, x-25+100/30,\
                y-7+200/30, x-25+200/30,\
                y-7+200/30, fill="white", outline="light blue")
                canvas.create_line(x-25+1, y-7+1,\
                x-25+170/30, y-7+170/30)
                canvas.create_line(x-25+1,\
                y-7+170/30, x-25+170/30,\
                y-7+1)
            elif mode.hill1.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-25, y-7,\
                    x-25+200/30, y-7+200/30)
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7, x-25+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7+200/30, x-25+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-7+1,\
                    x-25+170/30, y-7+170/30)
                    canvas.create_line(x-25+1,\
                    y-7+170/30, x-25+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-20, y-33,\
                    x-20+200/30, y-33+200/30)
                    canvas.create_polygon(x-20,\
                    y-33+100/30, x-20+100/30,\
                    y-33, x-20+200/30,\
                    y-33+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-33+100/30, x-20+100/30,\
                    y-33+200/30, x-20+200/30,\
                    y-33+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-33+1,\
                    x-20+170/30, y-33+170/30)
                    canvas.create_line(x-20+1,\
                    y-33+170/30, x-20+170/30,\
                    y-33+1)
            elif mode.hill1.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-18, y-36,\
                    x-18+200/30, y-36+200/30)
                    canvas.create_polygon(x-18,\
                    y-36+100/30, x-18+100/30,\
                    y-36, x-18+200/30,\
                    y-36+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-18,\
                    y-36+100/30, x-18+100/30,\
                    y-36+200/30, x-18+200/30,\
                    y-36+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-18+1, y-36+1,\
                    x-18+170/30, y-36+170/30)
                    canvas.create_line(x-18+1,\
                    y-36+170/30, x-18+170/30,\
                    y-36+1)
                else:
                    canvas.create_oval(x-25, y-7,\
                    x-25+200/30, y-7+200/30)
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7, x-25+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7+200/30, x-25+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-7+1,\
                    x-25+170/30, y-7+170/30)
                    canvas.create_line(x-25+1,\
                    y-7+170/30, x-25+170/30,\
                    y-7+1)
            elif mode.hill1.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-20, y+23,\
                    x-20+200/30, y+23+200/30)
                    canvas.create_polygon(x-20,\
                    y+23+100/30, x-20+100/30,\
                    y+23, x-20+200/30,\
                    y+23+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y+23+100/30, x-20+100/30,\
                    y+23+200/30, x-20+200/30,\
                    y+23+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y+23+1,\
                    x-20+170/30, y+23+170/30)
                    canvas.create_line(x-20+1,\
                    y+23+170/30, x-20+170/30,\
                    y+23+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-25, y-7,\
                    x-25+200/30, y-7+200/30)
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7, x-25+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7+200/30, x-25+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-7+1,\
                    x-25+170/30, y-7+170/30)
                    canvas.create_line(x-25+1,\
                    y-7+170/30, x-25+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-18, y-36,\
                    x-18+200/30, y-36+200/30)
                    canvas.create_polygon(x-18,\
                    y-36+100/30, x-18+100/30,\
                    y-36, x-18+200/30,\
                    y-36+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-18,\
                    y-36+100/30, x-18+100/30,\
                    y-36+200/30, x-18+200/30,\
                    y-36+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-18+1, y-36+1,\
                    x-18+170/30, y-36+170/30)
                    canvas.create_line(x-18+1,\
                    y-36+170/30, x-18+170/30,\
                    y-36+1)
        elif mode.currentPlayerHill==2 and mode.isJumping==False:
            if mode.hill2.type==0:
                canvas.create_oval(x-25, y-7,\
                x-25+200/30, y-7+200/30)
                canvas.create_polygon(x-25,\
                y-7+100/30, x-25+100/30,\
                y-7, x-25+200/30,\
                y-7+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-25,\
                y-7+100/30, x-25+100/30,\
                y-7+200/30, x-25+200/30,\
                y-7+200/30, fill="white", outline="light blue")
                canvas.create_line(x-25+1, y-7+1,\
                x-25+170/30, y-7+170/30)
                canvas.create_line(x-25+1,\
                y-7+170/30, x-25+170/30,\
                y-7+1)
            elif mode.hill2.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-25, y-7,\
                    x-25+200/30, y-7+200/30)
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7, x-25+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7+200/30, x-25+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-7+1,\
                    x-25+170/30, y-7+170/30)
                    canvas.create_line(x-25+1,\
                    y-7+170/30, x-25+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-20, y-33,\
                    x-20+200/30, y-33+200/30)
                    canvas.create_polygon(x-20,\
                    y-33+100/30, x-20+100/30,\
                    y-33, x-20+200/30,\
                    y-33+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-33+100/30, x-20+100/30,\
                    y-33+200/30, x-20+200/30,\
                    y-33+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-33+1,\
                    x-20+170/30, y-33+170/30)
                    canvas.create_line(x-20+1,\
                    y-33+170/30, x-20+170/30,\
                    y-33+1)
            elif mode.hill2.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-18, y-36,\
                    x-18+200/30, y-36+200/30)
                    canvas.create_polygon(x-18,\
                    y-36+100/30, x-18+100/30,\
                    y-36, x-18+200/30,\
                    y-36+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-18,\
                    y-36+100/30, x-18+100/30,\
                    y-36+200/30, x-18+200/30,\
                    y-36+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-18+1, y-36+1,\
                    x-18+170/30, y-36+170/30)
                    canvas.create_line(x-18+1,\
                    y-36+170/30, x-18+170/30,\
                    y-36+1)
                else:
                    canvas.create_oval(x-25, y-7,\
                    x-25+200/30, y-7+200/30)
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7, x-25+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7+200/30, x-25+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-7+1,\
                    x-25+170/30, y-7+170/30)
                    canvas.create_line(x-25+1,\
                    y-7+170/30, x-25+170/30,\
                    y-7+1)
            elif mode.hill2.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-20, y+23,\
                    x-20+200/30, y+23+200/30)
                    canvas.create_polygon(x-20,\
                    y+23+100/30, x-20+100/30,\
                    y+23, x-20+200/30,\
                    y+23+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y+23+100/30, x-20+100/30,\
                    y+23+200/30, x-20+200/30,\
                    y+23+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y+23+1,\
                    x-20+170/30, y+23+170/30)
                    canvas.create_line(x-20+1,\
                    y+23+170/30, x-20+170/30,\
                    y+23+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-25, y-7,\
                    x-25+200/30, y-7+200/30)
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7, x-25+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7+200/30, x-25+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-7+1,\
                    x-25+170/30, y-7+170/30)
                    canvas.create_line(x-25+1,\
                    y-7+170/30, x-25+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-18, y-36,\
                    x-18+200/30, y-36+200/30)
                    canvas.create_polygon(x-18,\
                    y-36+100/30, x-18+100/30,\
                    y-36, x-18+200/30,\
                    y-36+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-18,\
                    y-36+100/30, x-18+100/30,\
                    y-36+200/30, x-18+200/30,\
                    y-36+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-18+1, y-36+1,\
                    x-18+170/30, y-36+170/30)
                    canvas.create_line(x-18+1,\
                    y-36+170/30, x-18+170/30,\
                    y-36+1)
        elif mode.currentPlayerHill==3 and mode.isJumping==False:
            if mode.hill3.type==0:
                canvas.create_oval(x-25, y-7,\
                x-25+200/30, y-7+200/30)
                canvas.create_polygon(x-25,\
                y-7+100/30, x-25+100/30,\
                y-7, x-25+200/30,\
                y-7+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-25,\
                y-7+100/30, x-25+100/30,\
                y-7+200/30, x-25+200/30,\
                y-7+200/30, fill="white", outline="light blue")
                canvas.create_line(x-25+1, y-7+1,\
                x-25+170/30, y-7+170/30)
                canvas.create_line(x-25+1,\
                y-7+170/30, x-25+170/30,\
                y-7+1)
            elif mode.hill3.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-25, y-7,\
                    x-25+200/30, y-7+200/30)
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7, x-25+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7+200/30, x-25+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-7+1,\
                    x-25+170/30, y-7+170/30)
                    canvas.create_line(x-25+1,\
                    y-7+170/30, x-25+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-20, y-33,\
                    x-20+200/30, y-33+200/30)
                    canvas.create_polygon(x-20,\
                    y-33+100/30, x-20+100/30,\
                    y-33, x-20+200/30,\
                    y-33+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-33+100/30, x-20+100/30,\
                    y-33+200/30, x-20+200/30,\
                    y-33+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-33+1,\
                    x-20+170/30, y-33+170/30)
                    canvas.create_line(x-20+1,\
                    y-33+170/30, x-20+170/30,\
                    y-33+1)
            elif mode.hill3.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-18, y-36,\
                    x-18+200/30, y-36+200/30)
                    canvas.create_polygon(x-18,\
                    y-36+100/30, x-18+100/30,\
                    y-36, x-18+200/30,\
                    y-36+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-18,\
                    y-36+100/30, x-18+100/30,\
                    y-36+200/30, x-18+200/30,\
                    y-36+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-18+1, y-36+1,\
                    x-18+170/30, y-36+170/30)
                    canvas.create_line(x-18+1,\
                    y-36+170/30, x-18+170/30,\
                    y-36+1)
                else:
                    canvas.create_oval(x-25, y-7,\
                    x-25+200/30, y-7+200/30)
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7, x-25+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7+200/30, x-25+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-7+1,\
                    x-25+170/30, y-7+170/30)
                    canvas.create_line(x-25+1,\
                    y-7+170/30, x-25+170/30,\
                    y-7+1)
            elif mode.hill3.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-20, y+23,\
                    x-20+200/30, y+23+200/30)
                    canvas.create_polygon(x-20,\
                    y+23+100/30, x-20+100/30,\
                    y+23, x-20+200/30,\
                    y+23+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y+23+100/30, x-20+100/30,\
                    y+23+200/30, x-20+200/30,\
                    y+23+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y+23+1,\
                    x-20+170/30, y+23+170/30)
                    canvas.create_line(x-20+1,\
                    y+23+170/30, x-20+170/30,\
                    y+23+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-25, y-7,\
                    x-25+200/30, y-7+200/30)
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7, x-25+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-25,\
                    y-7+100/30, x-25+100/30,\
                    y-7+200/30, x-25+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-25+1, y-7+1,\
                    x-25+170/30, y-7+170/30)
                    canvas.create_line(x-25+1,\
                    y-7+170/30, x-25+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-18, y-36,\
                    x-18+200/30, y-36+200/30)
                    canvas.create_polygon(x-18,\
                    y-36+100/30, x-18+100/30,\
                    y-36, x-18+200/30,\
                    y-36+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-18,\
                    y-36+100/30, x-18+100/30,\
                    y-36+200/30, x-18+200/30,\
                    y-36+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-18+1, y-36+1,\
                    x-18+170/30, y-36+170/30)
                    canvas.create_line(x-18+1,\
                    y-36+170/30, x-18+170/30,\
                    y-36+1)
    
    def drawSnow6(mode, canvas):
        x=mode.player.cx-mode.scrollX
        y=mode.player.cy-mode.scrollY
        if mode.currentPlayerHill==1 and mode.isJumping==False:
            if mode.hill1.type==0:
                canvas.create_oval(x-30, y-7,\
                x-30+200/30, y-7+200/30)
                canvas.create_polygon(x-30,\
                y-7+100/30, x-30+100/30,\
                y-7, x-30+200/30,\
                y-7+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-30,\
                y-7+100/30, x-30+100/30,\
                y-7+200/30, x-30+200/30,\
                y-7+200/30, fill="white", outline="light blue")
                canvas.create_line(x-30+1, y-7+1,\
                x-30+170/30, y-7+170/30)
                canvas.create_line(x-30+1,\
                y-7+170/30, x-30+170/30,\
                y-7+1)
            elif mode.hill1.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-30, y-7,\
                    x-30+200/30, y-7+200/30)
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7, x-30+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7+200/30, x-30+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-30+1, y-7+1,\
                    x-30+170/30, y-7+170/30)
                    canvas.create_line(x-30+1,\
                    y-7+170/30, x-30+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-23, y-40,\
                    x-23+200/30, y-40+200/30)
                    canvas.create_polygon(x-23,\
                    y-40+100/30, x-23+100/30,\
                    y-40, x-23+200/30,\
                    y-40+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-23,\
                    y-40+100/30, x-23+100/30,\
                    y-40+200/30, x-23+200/30,\
                    y-40+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-23+1, y-40+1,\
                    x-23+170/30, y-40+170/30)
                    canvas.create_line(x-23+1,\
                    y-40+170/30, x-23+170/30,\
                    y-40+1)
            elif mode.hill1.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-20, y-43,\
                    x-20+200/30, y-43+200/30)
                    canvas.create_polygon(x-20,\
                    y-43+100/30, x-20+100/30,\
                    y-43, x-20+200/30,\
                    y-43+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-43+100/30, x-20+100/30,\
                    y-43+200/30, x-20+200/30,\
                    y-43+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-43+1,\
                    x-20+170/30, y-43+170/30)
                    canvas.create_line(x-20+1,\
                    y-43+170/30, x-20+170/30,\
                    y-43+1)
                else:
                    canvas.create_oval(x-30, y-7,\
                    x-30+200/30, y-7+200/30)
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7, x-30+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7+200/30, x-30+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-30+1, y-7+1,\
                    x-30+170/30, y-7+170/30)
                    canvas.create_line(x-30+1,\
                    y-7+170/30, x-30+170/30,\
                    y-7+1)
            elif mode.hill1.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-23, y+30,\
                    x-23+200/30, y+30+200/30)
                    canvas.create_polygon(x-23,\
                    y+30+100/30, x-23+100/30,\
                    y+30, x-23+200/30,\
                    y+30+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-23,\
                    y+30+100/30, x-23+100/30,\
                    y+30+200/30, x-23+200/30,\
                    y+30+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-23+1, y+30+1,\
                    x-23+170/30, y+30+170/30)
                    canvas.create_line(x-23+1,\
                    y+30+170/30, x-23+170/30,\
                    y+30+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-30, y-7,\
                    x-30+200/30, y-7+200/30)
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7, x-30+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7+200/30, x-30+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-30+1, y-7+1,\
                    x-30+170/30, y-7+170/30)
                    canvas.create_line(x-  30+1,\
                    y-7+170/30, x-30+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-20, y-43,\
                    x-20+200/30, y-43+200/30)
                    canvas.create_polygon(x-20,\
                    y-43+100/30, x-20+100/30,\
                    y-43, x-20+200/30,\
                    y-43+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-43+100/30, x-20+100/30,\
                    y-43+200/30, x-20+200/30,\
                    y-43+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-43+1,\
                    x-20+170/30, y-43+170/30)
                    canvas.create_line(x-20+1,\
                    y-43+170/30, x-20+170/30,\
                    y-43+1)
        elif mode.currentPlayerHill==2 and mode.isJumping==False:
            if mode.hill2.type==0:
                canvas.create_oval(x-30, y-7,\
                x-30+200/30, y-7+200/30)
                canvas.create_polygon(x-30,\
                y-7+100/30, x-30+100/30,\
                y-7, x-30+200/30,\
                y-7+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-30,\
                y-7+100/30, x-30+100/30,\
                y-7+200/30, x-30+200/30,\
                y-7+200/30, fill="white", outline="light blue")
                canvas.create_line(x-30+1, y-7+1,\
                x-30+170/30, y-7+170/30)
                canvas.create_line(x-30+1,\
                y-7+170/30, x-30+170/30,\
                y-7+1)
            elif mode.hill2.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-30, y-7,\
                    x-30+200/30, y-7+200/30)
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7, x-30+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7+200/30, x-30+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-30+1, y-7+1,\
                    x-30+170/30, y-7+170/30)
                    canvas.create_line(x-30+1,\
                    y-7+170/30, x-30+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-23, y-40,\
                    x-23+200/30, y-40+200/30)
                    canvas.create_polygon(x-23,\
                    y-40+100/30, x-23+100/30,\
                    y-40, x-23+200/30,\
                    y-40+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-23,\
                    y-40+100/30, x-23+100/30,\
                    y-40+200/30, x-23+200/30,\
                    y-40+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-23+1, y-40+1,\
                    x-23+170/30, y-40+170/30)
                    canvas.create_line(x-23+1,\
                    y-40+170/30, x-23+170/30,\
                    y-40+1)
            elif mode.hill2.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-20, y-43,\
                    x-20+200/30, y-43+200/30)
                    canvas.create_polygon(x-20,\
                    y-43+100/30, x-20+100/30,\
                    y-43, x-20+200/30,\
                    y-43+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-43+100/30, x-20+100/30,\
                    y-43+200/30, x-20+200/30,\
                    y-43+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-43+1,\
                    x-20+170/30, y-43+170/30)
                    canvas.create_line(x-20+1,\
                    y-43+170/30, x-20+170/30,\
                    y-43+1)
                else:
                    canvas.create_oval(x-30, y-7,\
                    x-30+200/30, y-7+200/30)
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7, x-30+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7+200/30, x-30+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-30+1, y-7+1,\
                    x-30+170/30, y-7+170/30)
                    canvas.create_line(x-30+1,\
                    y-7+170/30, x-30+170/30,\
                    y-7+1)
            elif mode.hill2.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-23, y+30,\
                    x-23+200/30, y+30+200/30)
                    canvas.create_polygon(x-23,\
                    y+30+100/30, x-23+100/30,\
                    y+30, x-23+200/30,\
                    y+30+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-23,\
                    y+30+100/30, x-23+100/30,\
                    y+30+200/30, x-23+200/30,\
                    y+30+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-23+1, y+30+1,\
                    x-23+170/30, y+30+170/30)
                    canvas.create_line(x-23+1,\
                    y+30+170/30, x-23+170/30,\
                    y+30+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-30, y-7,\
                    x-30+200/30, y-7+200/30)
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7, x-30+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7+200/30, x-30+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-30+1, y-7+1,\
                    x-30+170/30, y-7+170/30)
                    canvas.create_line(x-  30+1,\
                    y-7+170/30, x-30+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-20, y-43,\
                    x-20+200/30, y-43+200/30)
                    canvas.create_polygon(x-20,\
                    y-43+100/30, x-20+100/30,\
                    y-43, x-20+200/30,\
                    y-43+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-43+100/30, x-20+100/30,\
                    y-43+200/30, x-20+200/30,\
                    y-43+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-43+1,\
                    x-20+170/30, y-43+170/30)
                    canvas.create_line(x-20+1,\
                    y-43+170/30, x-20+170/30,\
                    y-43+1)
        elif mode.currentPlayerHill==3 and mode.isJumping==False:
            if mode.hill3.type==0:
                canvas.create_oval(x-30, y-7,\
                x-30+200/30, y-7+200/30)
                canvas.create_polygon(x-30,\
                y-7+100/30, x-30+100/30,\
                y-7, x-30+200/30,\
                y-7+100/30, fill="white", outline="light blue")
                canvas.create_polygon(x-30,\
                y-7+100/30, x-30+100/30,\
                y-7+200/30, x-30+200/30,\
                y-7+200/30, fill="white", outline="light blue")
                canvas.create_line(x-30+1, y-7+1,\
                x-30+170/30, y-7+170/30)
                canvas.create_line(x-30+1,\
                y-7+170/30, x-30+170/30,\
                y-7+1)
            elif mode.hill3.type==1:
                if 0<=mode.snow.cx%300<=55 or 235<=mode.snow.cx%300<=\
                300:
                    canvas.create_oval(x-30, y-7,\
                    x-30+200/30, y-7+200/30)
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7, x-30+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7+200/30, x-30+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-30+1, y-7+1,\
                    x-30+170/30, y-7+170/30)
                    canvas.create_line(x-30+1,\
                    y-7+170/30, x-30+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-23, y-40,\
                    x-23+200/30, y-40+200/30)
                    canvas.create_polygon(x-23,\
                    y-40+100/30, x-23+100/30,\
                    y-40, x-23+200/30,\
                    y-40+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-23,\
                    y-40+100/30, x-23+100/30,\
                    y-40+200/30, x-23+200/30,\
                    y-40+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-23+1, y-40+1,\
                    x-23+170/30, y-40+170/30)
                    canvas.create_line(x-23+1,\
                    y-40+170/30, x-23+170/30,\
                    y-40+1)
            elif mode.hill3.type==2:
                if 25<=mode.snow.cx%300<=95 or 205<=mode.snow.cx%300<=285:
                    canvas.create_oval(x-20, y-43,\
                    x-20+200/30, y-43+200/30)
                    canvas.create_polygon(x-20,\
                    y-43+100/30, x-20+100/30,\
                    y-43, x-20+200/30,\
                    y-43+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-43+100/30, x-20+100/30,\
                    y-43+200/30, x-20+200/30,\
                    y-43+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-43+1,\
                    x-20+170/30, y-43+170/30)
                    canvas.create_line(x-20+1,\
                    y-43+170/30, x-20+170/30,\
                    y-43+1)
                else:
                    canvas.create_oval(x-30, y-7,\
                    x-30+200/30, y-7+200/30)
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7, x-30+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7+200/30, x-30+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-30+1, y-7+1,\
                    x-30+170/30, y-7+170/30)
                    canvas.create_line(x-30+1,\
                    y-7+170/30, x-30+170/30,\
                    y-7+1)
            elif mode.hill3.type==3:
                if 0<=mode.snow.cx%300<=195:
                    canvas.create_oval(x-23, y+30,\
                    x-23+200/30, y+30+200/30)
                    canvas.create_polygon(x-23,\
                    y+30+100/30, x-23+100/30,\
                    y+30, x-23+200/30,\
                    y+30+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-23,\
                    y+30+100/30, x-23+100/30,\
                    y+30+200/30, x-23+200/30,\
                    y+30+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-23+1, y+30+1,\
                    x-23+170/30, y+30+170/30)
                    canvas.create_line(x-23+1,\
                    y+30+170/30, x-23+170/30,\
                    y+30+1)
                elif 205<=mode.snow.cx%300<225:
                    canvas.create_oval(x-30, y-7,\
                    x-30+200/30, y-7+200/30)
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7, x-30+200/30,\
                    y-7+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-30,\
                    y-7+100/30, x-30+100/30,\
                    y-7+200/30, x-30+200/30,\
                    y-7+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-30+1, y-7+1,\
                    x-30+170/30, y-7+170/30)
                    canvas.create_line(x-  30+1,\
                    y-7+170/30, x-30+170/30,\
                    y-7+1)
                else:
                    canvas.create_oval(x-20, y-43,\
                    x-20+200/30, y-43+200/30)
                    canvas.create_polygon(x-20,\
                    y-43+100/30, x-20+100/30,\
                    y-43, x-20+200/30,\
                    y-43+100/30, fill="white", outline="light blue")
                    canvas.create_polygon(x-20,\
                    y-43+100/30, x-20+100/30,\
                    y-43+200/30, x-20+200/30,\
                    y-43+200/30, fill="white", outline="light blue")
                    canvas.create_line(x-20+1, y-43+1,\
                    x-20+170/30, y-43+170/30)
                    canvas.create_line(x-20+1,\
                    y-43+170/30, x-20+170/30,\
                    y-43+1)
    
    def drawCoin(mode, canvas):
        x=mode.coin.cx-mode.scrollX
        y=mode.coin.cy-mode.scrollY
        canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.coinImage))

    def drawFlip1(mode, canvas):
        x=mode.player.cx-mode.scrollX+2
        y=mode.player.cy-mode.scrollY-12
        canvas.create_oval(x-15, y-15, x+15, y+15, outline="cyan")
    
    def drawFlip2(mode, canvas):
        x=mode.player.cx-mode.scrollX+2
        y=mode.player.cy-mode.scrollY-12
        canvas.create_oval(x-10, y-10, x+10, y+10, outline="cyan")
    
    def drawFlip3(mode, canvas):
        x=mode.player.cx-mode.scrollX+2
        y=mode.player.cy-mode.scrollY-12
        canvas.create_oval(x-5, y-5, x+5, y+5, outline="cyan")

    def drawFly1(mode, canvas):
        x=mode.eagle.cx-mode.scrollX
        y=mode.eagle.cy-mode.scrollY
        canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.eagleImages[0]))
    
    def drawFly2(mode, canvas):
        x=mode.eagle.cx-mode.scrollX
        y=mode.eagle.cy-mode.scrollY
        canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.eagleImages[1]))
    
    def drawFly3(mode, canvas):
        x=mode.eagle.cx-mode.scrollX
        y=mode.eagle.cy-mode.scrollY
        canvas.create_image(x, y, image=ImageTk.PhotoImage(mode.eagleImages[1]))
    
    def drawScarf(mode, canvas):
        if mode.currentPlayerHill==1:
            if mode.hill1.type==0:
                if 0<=mode.player.cx%300<=300:
                    x=mode.player.cx-mode.scrollX-8
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
            elif mode.hill1.type==1:
                if 0<=mode.player.cx%300<=5:
                    x=mode.player.cx-mode.scrollX-5
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 5<=mode.player.cx%300<=15:
                    x=mode.player.cx-mode.scrollX
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 15<=mode.player.cx%300<=25:
                    x=mode.player.cx-mode.scrollX
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 25<=mode.player.cx%300<=35:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-20
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 35<=mode.player.cx%300<=45:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 45<=mode.player.cx%300<=55:
                    x=mode.player.cx-mode.scrollX+3
                    y=mode.player.cy-mode.scrollY-22
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 55<=mode.player.cx%300<=65:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-22
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 65<=mode.player.cx%300<=75:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 65<=mode.player.cx%300<=75:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-20
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 75<=mode.player.cx%300<=165:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-22
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 165<=mode.player.cx%300<=175:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 175<=mode.player.cx%300<=195:
                    x=mode.player.cx-mode.scrollX+3
                    y=mode.player.cy-mode.scrollY-22
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 195<=mode.player.cx%300<=215:
                    x=mode.player.cx-mode.scrollX+3
                    y=mode.player.cy-mode.scrollY-20
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 215<=mode.player.cx%300<=225:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-18
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 225<=mode.player.cx%300<=235:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 235<=mode.player.cx%300<=245:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 245<=mode.player.cx%300<=255:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-18
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 255<=mode.player.cx%300<=265:
                    x=mode.player.cx-mode.scrollX+1
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 265<=mode.player.cx%300<=275:
                    x=mode.player.cx-mode.scrollX
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 285<=mode.player.cx%300<=295:
                    x=mode.player.cx-mode.scrollX-3
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
            elif mode.hill1.type==2:
                if 0<=mode.player.cx%300<=5:
                    x=mode.player.cx-mode.scrollX-5
                    y=mode.player.cy-mode.scrollY-16
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 5<=mode.player.cx%300<=15:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 15<=mode.player.cx%300<=25:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 25<=mode.player.cx%300<=75:
                    x=mode.player.cx-mode.scrollX+8
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 75<=mode.player.cx%300<=85:
                    x=mode.player.cx-mode.scrollX+7
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 85<=mode.player.cx%300<=95:
                    x=mode.player.cx-mode.scrollX+6
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 95<=mode.player.cx%300<=105:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 105<=mode.player.cx%300<=115:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 115<=mode.player.cx%300<=125:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-18
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 125<=mode.player.cx%300<=175:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-18
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 175<=mode.player.cx%300<=185:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 185<=mode.player.cx%300<=195:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 195<=mode.player.cx%300<=205:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 205<=mode.player.cx%300<=215:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 215<=mode.player.cx%300<=275:
                    x=mode.player.cx-mode.scrollX+6
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 275<=mode.player.cx%300<=285:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 285<=mode.player.cx%300<=295:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                
        elif mode.currentPlayerHill==2:
            if mode.hill2.type==0:
                if 0<=mode.player.cx%300<=300:
                    x=mode.player.cx-mode.scrollX-8
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
            elif mode.hill2.type==1:
                if 0<=mode.player.cx%300<=5:
                    x=mode.player.cx-mode.scrollX-5
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 5<=mode.player.cx%300<=15:
                    x=mode.player.cx-mode.scrollX
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 15<=mode.player.cx%300<=25:
                    x=mode.player.cx-mode.scrollX
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 25<=mode.player.cx%300<=35:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-20
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 35<=mode.player.cx%300<=45:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 45<=mode.player.cx%300<=55:
                    x=mode.player.cx-mode.scrollX+3
                    y=mode.player.cy-mode.scrollY-22
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 55<=mode.player.cx%300<=65:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-22
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 65<=mode.player.cx%300<=75:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 65<=mode.player.cx%300<=75:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-20
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 75<=mode.player.cx%300<=165:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-22
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 165<=mode.player.cx%300<=175:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 175<=mode.player.cx%300<=195:
                    x=mode.player.cx-mode.scrollX+3
                    y=mode.player.cy-mode.scrollY-22
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 195<=mode.player.cx%300<=215:
                    x=mode.player.cx-mode.scrollX+3
                    y=mode.player.cy-mode.scrollY-20
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 215<=mode.player.cx%300<=225:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-18
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 225<=mode.player.cx%300<=235:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 235<=mode.player.cx%300<=245:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 245<=mode.player.cx%300<=255:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-18
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 255<=mode.player.cx%300<=265:
                    x=mode.player.cx-mode.scrollX+1
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 265<=mode.player.cx%300<=275:
                    x=mode.player.cx-mode.scrollX
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 285<=mode.player.cx%300<=295:
                    x=mode.player.cx-mode.scrollX-3
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
            elif mode.hill2.type==2:
                if 0<=mode.player.cx%300<=5:
                    x=mode.player.cx-mode.scrollX-5
                    y=mode.player.cy-mode.scrollY-16
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 5<=mode.player.cx%300<=15:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 15<=mode.player.cx%300<=25:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 25<=mode.player.cx%300<=75:
                    x=mode.player.cx-mode.scrollX+8
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 75<=mode.player.cx%300<=85:
                    x=mode.player.cx-mode.scrollX+7
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 85<=mode.player.cx%300<=95:
                    x=mode.player.cx-mode.scrollX+6
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 95<=mode.player.cx%300<=105:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 105<=mode.player.cx%300<=115:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 115<=mode.player.cx%300<=125:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-18
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 125<=mode.player.cx%300<=175:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-18
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 175<=mode.player.cx%300<=185:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 185<=mode.player.cx%300<=195:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 195<=mode.player.cx%300<=205:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 205<=mode.player.cx%300<=215:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 215<=mode.player.cx%300<=275:
                    x=mode.player.cx-mode.scrollX+6
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 275<=mode.player.cx%300<=285:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 285<=mode.player.cx%300<=295:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
            elif mode.hill2.type==3:
                if 25<=mode.player.cx%300<=55:
                    x=mode.player.cx-mode.scrollX+18
                    y=mode.player.cy-mode.scrollY-6
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 155<=mode.snow.cx%300<=185:
                    x=mode.snow.cx-mode.scrollX-19
                    y=mode.snow.cy-mode.scrollY+2
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 225<=mode.snow.cx%300<=255:
                    x=mode.snow.cx-mode.scrollX+17
                    y=mode.snow.cy-mode.scrollY-6
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                
        elif mode.currentPlayerHill==3:
            if mode.hill3.type==0:
                if 0<=mode.player.cx%300<=300:
                    x=mode.player.cx-mode.scrollX-8
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
            elif mode.hill3.type==1:
                if 0<=mode.player.cx%300<=5:
                    x=mode.player.cx-mode.scrollX-5
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 5<=mode.player.cx%300<=15:
                    x=mode.player.cx-mode.scrollX
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 15<=mode.player.cx%300<=25:
                    x=mode.player.cx-mode.scrollX
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 25<=mode.player.cx%300<=35:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-20
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 35<=mode.player.cx%300<=45:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 45<=mode.player.cx%300<=55:
                    x=mode.player.cx-mode.scrollX+3
                    y=mode.player.cy-mode.scrollY-22
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 55<=mode.player.cx%300<=65:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-22
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 65<=mode.player.cx%300<=75:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 65<=mode.player.cx%300<=75:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-20
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 75<=mode.player.cx%300<=165:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-22
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 165<=mode.player.cx%300<=175:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 175<=mode.player.cx%300<=195:
                    x=mode.player.cx-mode.scrollX+3
                    y=mode.player.cy-mode.scrollY-22
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 195<=mode.player.cx%300<=215:
                    x=mode.player.cx-mode.scrollX+3
                    y=mode.player.cy-mode.scrollY-20
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 215<=mode.player.cx%300<=225:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-18
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 225<=mode.player.cx%300<=235:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 235<=mode.player.cx%300<=245:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 245<=mode.player.cx%300<=255:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-18
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 255<=mode.player.cx%300<=265:
                    x=mode.player.cx-mode.scrollX+1
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 265<=mode.player.cx%300<=275:
                    x=mode.player.cx-mode.scrollX
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 285<=mode.player.cx%300<=295:
                    x=mode.player.cx-mode.scrollX-3
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
            elif mode.hill3.type==2:
                if 0<=mode.player.cx%300<=5:
                    x=mode.player.cx-mode.scrollX-5
                    y=mode.player.cy-mode.scrollY-16
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 5<=mode.player.cx%300<=15:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 15<=mode.player.cx%300<=25:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 25<=mode.player.cx%300<=75:
                    x=mode.player.cx-mode.scrollX+8
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 75<=mode.player.cx%300<=85:
                    x=mode.player.cx-mode.scrollX+7
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 85<=mode.player.cx%300<=95:
                    x=mode.player.cx-mode.scrollX+6
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 95<=mode.player.cx%300<=105:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 105<=mode.player.cx%300<=115:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 115<=mode.player.cx%300<=125:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-18
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 125<=mode.player.cx%300<=175:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-18
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 175<=mode.player.cx%300<=185:
                    x=mode.player.cx-mode.scrollX+2
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 185<=mode.player.cx%300<=195:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 195<=mode.player.cx%300<=205:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 205<=mode.player.cx%300<=215:
                    x=mode.player.cx-mode.scrollX+5
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 215<=mode.player.cx%300<=275:
                    x=mode.player.cx-mode.scrollX+6
                    y=mode.player.cy-mode.scrollY-21
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 275<=mode.player.cx%300<=285:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-19
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))
                elif 285<=mode.player.cx%300<=295:
                    x=mode.player.cx-mode.scrollX+4
                    y=mode.player.cy-mode.scrollY-17
                    canvas.create_image(x, y,\
                    image=ImageTk.PhotoImage(mode.scarfImage))

    #Draws classic scoring system
    def drawInfoBoard(mode, canvas):
        canvas.create_text(mode.width*5/6, mode.height*1/12,\
        text=f"Score: {mode.score}", font="Arial 10 bold underline")
        canvas.create_text(mode.width*5/6, mode.height*1/6-20,\
        text=f"Double Jumps: {mode.numberOfFlips}",\
        font="Arial 10 bold underline")

    def redrawAll(mode, canvas):
        if mode.isGameOver==False:
            if mode.snow1==True:
                canvas.create_image(mode.width*2/5, mode.height/2,\
                image=ImageTk.PhotoImage(mode.backgroundImage))
                mode.drawPlayer(canvas)
                mode.drawHill1(canvas)
                mode.drawHill2(canvas)
                mode.drawHill3(canvas)
                mode.drawRock(canvas)
                mode.drawSnow1(canvas)
                mode.drawSnow2(canvas)
                mode.drawSnow4(canvas)
                if mode.isJumping==False:
                    mode.drawScarf(canvas)
                mode.drawInfoBoard(canvas)
                if mode.didFlip==True and mode.flip1==True:
                    mode.drawFlip1(canvas)
                elif mode.didFlip==True and mode.flip2==True:
                    mode.drawFlip2(canvas)
                elif mode.didFlip==True and mode.flip3==True:
                    mode.drawFlip3(canvas)
                if mode.coinCollected==False:
                    mode.drawCoin(canvas)
                if mode.eagleInView==True:
                    if mode.fly1==True:
                        mode.drawFly1(canvas)
                    elif mode.fly2==True:
                        mode.drawFly2(canvas)
                    elif mode.fly3==True:
                        mode.drawFly3(canvas)
            elif mode.snow2==True:
                canvas.create_image(mode.width*2/5, mode.height/2,\
                image=ImageTk.PhotoImage(mode.backgroundImage))
                mode.drawPlayer(canvas)
                mode.drawHill1(canvas)
                mode.drawHill2(canvas)
                mode.drawHill3(canvas)
                mode.drawRock(canvas)
                mode.drawSnow3(canvas)
                mode.drawSnow4(canvas)
                if mode.isJumping==False:
                    mode.drawScarf(canvas)
                mode.drawInfoBoard(canvas)
                if mode.didFlip==True and mode.flip1==True:
                    mode.drawFlip1(canvas)
                elif mode.didFlip==True and mode.flip2==True:
                    mode.drawFlip2(canvas)
                elif mode.didFlip==True and mode.flip3==True:
                    mode.drawFlip3(canvas)
                if mode.coinCollected==False:
                    mode.drawCoin(canvas)
                if mode.eagleInView==True:
                    if mode.fly1==True:
                        mode.drawFly1(canvas)
                    elif mode.fly2==True:
                        mode.drawFly2(canvas)
                    elif mode.fly3==True:
                        mode.drawFly3(canvas)
            elif mode.snow3==True:
                canvas.create_image(mode.width*2/5, mode.height/2,\
                image=ImageTk.PhotoImage(mode.backgroundImage))
                mode.drawPlayer(canvas)
                mode.drawHill1(canvas)
                mode.drawHill2(canvas)
                mode.drawHill3(canvas)
                mode.drawRock(canvas)
                mode.drawSnow5(canvas)
                mode.drawSnow6(canvas)
                if mode.isJumping==False:
                    mode.drawScarf(canvas)
                mode.drawInfoBoard(canvas)
                if mode.didFlip==True and mode.flip1==True:
                    mode.drawFlip1(canvas)
                elif mode.didFlip==True and mode.flip2==True:
                    mode.drawFlip2(canvas)
                elif mode.didFlip==True and mode.flip3==True:
                    mode.drawFlip3(canvas)
                if mode.coinCollected==False:
                    mode.drawCoin(canvas)
                if mode.eagleInView==True:
                    if mode.fly1==True:
                        mode.drawFly1(canvas)
                    elif mode.fly2==True:
                        mode.drawFly2(canvas)
                    elif mode.fly3==True:
                        mode.drawFly3(canvas)

class GameOverMode(Mode):
    def appStarted(mode):
        mode.app.splashScreenMode.music=False
        mode.app.splashScreenMode.checkMusic()
        backgroundImage=mode.loadImage("Alto's Adventure Title Screen.jpg")
        mode.spriteBackground=mode.scaleImage(backgroundImage, 5/6)
        mode.playerAndScoreDictionary=mode.getPlayerAndScores()
    
    def getPlayerAndScores(mode):
        playerAndScoreDictionary=dict()
        contents=mode.readFile("Leaderboard.txt").splitlines()
        for playerScore in contents:
            playerScoreList=playerScore.split(",")
            player=playerScoreList[0]
            score=int(playerScoreList[1])
            if player in playerAndScoreDictionary.keys():
                currentScore=playerAndScoreDictionary[player]
                if score>currentScore:
                    playerAndScoreDictionary[player]=score
            else:
                playerAndScoreDictionary[player]=score
        return playerAndScoreDictionary

#Copied from: https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    def readFile(mode, path):
        with open(path, "rt") as f:
            return f.read()

#Copied from: https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    def writeFile(mode, path, contents):
        with open(path, "wt") as f:
            f.write(contents)

    def drawLeaderboard(mode, canvas):
        playerCounter=0
        canvas.create_rectangle(mode.width/50, mode.height/3-40,\
        mode.width*3/10-30, mode.height*2/3, fill="white")
        canvas.create_text(mode.width/10+20, mode.height/3-30,\
        text="Leaderboard", font="Arial 10 bold")
        for player in mode.playerAndScoreDictionary:
            score=mode.playerAndScoreDictionary[player]
            text=player+": "+str(score)
            canvas.create_text(mode.width/8, mode.height/3+30*playerCounter,\
            text=text, font="Arial 12 bold", fill="maroon")
            playerCounter+=1
    
    def redrawAll(mode, canvas):
        canvas.create_image(mode.width/2, mode.height/2,\
        image=ImageTk.PhotoImage(mode.spriteBackground))
        font="Arial 20 bold"
        canvas.create_text(mode.width/2, mode.height/2,\
        text=f"Final Score: {mode.app.gameMode.score}",\
        font=font, fill="black")
        canvas.create_text(mode.width/2, mode.height/2+100,\
        text="Press 'r' to restart", font=font, fill="black")
        canvas.create_text(mode.width/2, mode.height/2+200,\
        text="Press 's' to return to the main menu", font=font, fill="black")
        mode.drawLeaderboard(canvas)

    def keyPressed(mode, event):
        if event.key=="r":
            mode.app.gameMode.appStarted()
            mode.app.setActiveMode(mode.app.gameMode)
            mode.app.splashScreenMode.music=True
            mode.app.splashScreenMode.checkMusic()
        elif event.key=="s":
            mode.app.gameMode.appStarted()
            mode.app.setActiveMode(mode.app.splashScreenMode)
            mode.app.splashScreenMode.music=False
            mode.app.splashScreenMode.checkMusic()

class Scarf(object):
    def __init__(self, cx, cy):
        self.cx=cx
        self.cy=cy

class Eagle(object):
    def __init__(self, cx, cy):
        self.cx=cx
        self.cy=cy

class Coin(object):
    def __init__(self, cx, cy):
        self.cx=cx
        self.cy=cy

class Snow(object):
    def __init__(self, cx, cy):
        self.cx=cx
        self.cy=cy

class Player(object):
    def __init__(self, cx, cy):
        self.cx=cx
        self.cy=cy

class Rock(object):
    def __init__(self, cx, cy, hillType):
        self.cx=cx
        self.cy=cy
        self.hillType=hillType

class Hill(object):
    def __init__(self, app, startingX, startingY):
        self.app=app
        self.startingX=startingX
        self.startingY=startingY
        self.endingX=None
        self.endingY=None
        self.type=None

    def generateHillType0(self):
        #Hill Type 0: equation is y=self.app.width
        #Derivative is y=0
        self.endingX=self.startingX+self.app.width//2
        self.endingY=self.startingY
        self.type=0

    def generateHillType1(self):
        #Hill Type 1: equation is y=2.842171*(10**-14)+0.1285714*x
        #+0.009843537*x^2-0.00002312925*x^3 FOR LINE RIDING
        #equation is y=300+0.2102041*x-0.01097279*x^2+0.00002312925*x^3
        #and derivative is y=0.00006x^2-0.02194558x+0.2102041
        endingX=self.startingX+self.app.width//2
        endingY=2.842171*(10**-14)+0.1285714*(300)+0.009843537*(300**2)\
        -0.00002312925*(300**3)
        self.endingX=endingX
        self.endingY=self.startingY+endingY
        self.type=1
    
    #One with two hills
    def generateHillType2(self):
        #Hill Type 2: equation is y =-9.094947*(10**-13)-0.875*x+0.06375*x^2 
        #-0.0006416667*x^3+0.0000025*x^4-3.333333*(10**-9)*x^5 FOR LINE RIDING
        #equation is y=300+0.875*x-0.06375*x^2+0.0006416667*x^3-0.0000025*x^4
        #+(3.333333*10^-9)*x^5 and derivative is y=1.66667**(10**-8)*x^4
        #-0.00001x^3+0.0019250001x^2-0.1275x+0.875 FOR SLOPE
        endingX=self.startingX+self.app.width//2
        endingY=-9.094947*(10**-13)-0.875*(300)+0.06375*(300**2)\
        -0.0006416667*(300**3)+0.0000025*(300**4)-3.333333*(10**-9)*(300**5)
        self.endingX=endingX
        self.endingY=roundHalfUp(self.startingY+endingY)
        self.type=2

    #One with big canyon in the middle
    def generateHillType3(self):
    #FOR SLOPE
    #Equation
    #y=300+7.576999*x-0.3277466*x^2+0.003307988*x^3-0.000012472*x^4+1.589777e-8*x^5
    #Derivative
    #y=7.94889*(10^-8)x^4-0.000049888x^3+0.009923964x^2-0.6554932x+7.576999
    #FOR LINE RIDER
    #Equation
    #y=4.845901*(10^-12)-0.9699877*x+0.2069631*x^2-0.002649587*x^3+
    #0.00001137466*x^4-1.589777*(10^-8)*x^5
        endingX=self.startingX+self.app.width//2
        endingY=4.845901*(10**-12)-0.9699877*(300)+0.2069631*(300**2)-\
        0.002649587*(300**3)+0.00001137466*(300**4)-1.589777*(10**-8)*(300**5)
        self.endingX=endingX
        self.endingY=self.startingY+endingY
        self.type=3
app=MyModalApp(width=600, height=600)