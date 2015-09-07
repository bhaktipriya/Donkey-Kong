#This file consists of all global variables, used throughout the game
import pygame
import sys
import random
import os
from animation import *
from sprite import *
from player import *
from vector import *
from score import *

# Variables
GameScore = Score()
tbonus = 5000
bonus_timer, score, mario_num_lives = 0, 0, 3

# screen descriptions
WIDTH = 1200
HEIGHT = 640
SIZE = (WIDTH, HEIGHT)

# pygame definitions
pygame.init()
surface = pygame.display.set_mode(SIZE)
# fonts
bigfont = pygame.font.SysFont("comicsansms", 50)
smallfont = pygame.font.SysFont("comicsansms", 25)
# colors
RED = (33, 255, 33)
BLACK = (140, 48, 159)
YELLOW = (255, 204, 0)
WHITE = (255, 255, 255)
PINK =(255,0,128)
BLUE=(0,0,255)
MAGENTA=(153,0,0)
LIGHTPINK=(255,0,0)
# images
DKl1=pygame.image.load("images/dkl1.gif").convert_alpha()
logoImage = pygame.image.load("images/Donkey_Kong_logo.png")
logoImage = pygame.transform.scale(logoImage, (WIDTH - 100, 250))
logoBarrel = pygame.image.load("images/DKBarrelReturns.gif").convert_alpha()
logoBarrel = pygame.transform.scale(logoBarrel, (150, 250))
#logo animation
n1,n2="images/frame_","_delay-s.gif"
lg=[]
for i in xrange(14):
    fr=pygame.image.load(n1+str(i)+n2)
    fr=pygame.transform.scale(fr,(WIDTH,HEIGHT))
    lg.append(fr)
#welcome frames animation
welcome=[]
n1,n2="images/welcome/frame_","_delay-0.1s.gif"
for i in xrange(19):
    fr=pygame.image.load(n1+str(i)+n2)
    fr=pygame.transform.scale(fr,(WIDTH,HEIGHT))
    welcome.append(fr)
authorImage = pygame.image.load("images/author.png")
grass = pygame.image.load("images/grass.jpg")
wid = grass.get_width()
heig = grass.get_height()

playerWalkingRts = pygame.image.load("images/mario_running_right3.png")
playerWalkingLts = pygame.image.load("images/mario_running_left3.png")
#princess cry animation
princesscry=[]
n1,n2="images/princess/frame_","_delay-0.07s.gif"
for i in xrange(5):
    fr=pygame.image.load(n1+str(i)+n2)
    fr=pygame.transform.scale(fr,(WIDTH,HEIGHT))
    princesscry.append(fr)

#mario dance animation
mariodance=[]
n1,n2="images/mariodance/frame_","_delay-0.08s.gif"
for i in xrange(25):
    fr=pygame.image.load(n1+str(i)+n2).convert_alpha()
    mariodance.append(fr)

#Load images
frame1,frame2= pygame.image.load("images/frame_0.gif"),pygame.image.load("images/frame_1.gif")
frame3,frame4 = pygame.image.load("images/frame_2.gif"), pygame.image.load("images/frame_3.gif")
frame5 = pygame.image.load("images/frame_4.gif")
#coin images
coin0_s,coin1_s = pygame.image.load("images/coin0.gif"),pygame.image.load("images/coin1.gif")
coin2_s,coin3_s = pygame.image.load("images/coin2.gif"),pygame.image.load("images/coin3.gif")
playerClimbingUps,playerClimbingDowns=pygame.image.load("images/mario_climbing.png"),pygame.image.load("images/mario_climbing2.png")
pointer = pygame.image.load("images/pointer.gif").convert_alpha()
playerLifes = pygame.image.load("images/mario_lives.png")
playerWithHammerLefts,playerWithHammerRights=pygame.image.load("images/mario_brown_hammer.png"),pygame.image.load("images/mario_brown_hammer2.png")
startButton,scoresButton = pygame.image.load("images/startbutton.png"),pygame.image.load("images/scoresbutton.png")
donkeyKongs,princys = pygame.image.load("images/donkey_kong.png"),pygame.image.load("images/pauline.png")
ladPlats,lads = pygame.image.load("images/ladder_platforms2.png"),pygame.image.load("images/white_ladder.png")
barrels,blbarrelfirehammers=pygame.image.load("images/barrel_cement_flower.png"),pygame.image.load("images/bluebarrel_fireball_hammer.png")
fireball,oilBarrelFires = pygame.image.load("images/fireballz.gif"),pygame.image.load("images/fire_oil_explosion.png")
#Create Animation objects
pointerRect,coinRect = pointer.get_rect(),coin0_s.get_rect()
redPlatformanim ,playerFacingRightanim= Animation(ladPlats, 260, 280, 20, 1),Animation(playerWalkingRts, 0, 40, 40, 0)
playerFacingLeftanim, playerWalkingRightanim= Animation(playerWalkingLts, 0, 40,40, 0),Animation(playerWalkingRts, 0, 120, 40, 15)
whiteLadderTopanim = Animation(lads, 16, 32, 16, 0)
playerWalkingLeftanim,whiteLadderMiddleanim= Animation(playerWalkingLts, 0, 120,40, 15),Animation(ladPlats, 20, 40, 20, 0)
playerRunningRrightanim,whiteLadderBotanim = Animation(playerWalkingRts, 0, 120,40, 20),Animation(lads, 32, 48, 16, 0)
playerRunningLeftanim = Animation(playerWalkingLts, 0, 120, 40, 20)
playerJumpFacingRightanim = Animation(playerWalkingRts, 80, 120, 40, 0)
oilBarrelanim,playerJumpFacingleftanim = Animation(oilBarrelFires, 160, 200, 40,0),Animation(playerWalkingLts, 80, 120, 40,  0)
playerClimbupanim = Animation(playerClimbingUps, 0, 80, 40, 4)
playerClimbDownanim = Animation(playerClimbingDowns, 120, 200, 40, 4)
oilBarrelFireanim = Animation(oilBarrelFires, 0, 160, 40, 7)
playerClimbstillanim = Animation(playerClimbingDowns, 120, 160, 40, 0)
playerFacingBackanim = Animation(playerClimbingDowns, 0, 40, 40, 0)
explosionAnim = Animation(oilBarrelFires, 200, 400, 40, 15)
mario_with_hammer_left_an = Animation(playerWithHammerLefts, 0, 360, 60, 20)
mario_with_hammer_right_an = Animation(playerWithHammerRights, 0, 360, 60,  20)
barrel_sideways_an = Animation(barrels, 0, 160, 40, 4)
barrel_wide_an = Animation(barrels, 160, 240, 40, 4)
barrel_vertical_an = Animation(barrels, 240, 280, 40, 0)
dkstompanim = Animation(donkeyKongs, 0, 600, 100,  3)
dkdead = Animation(donkeyKongs, 600, 900, 100, 0)
dkcarryprincyanim = Animation(donkeyKongs, 900, 1200, 100, 0)
dkthrowbarrel = Animation(donkeyKongs, 1200, 1400, 100, 0)
bluebarrel_sideways_an = Animation(blbarrelfirehammers, 0, 160, 40, 4)
bluebarrel_wide_an = Animation(blbarrelfirehammers, 160, 240, 40, 4)
bluebarrel_vertical_an = Animation(blbarrelfirehammers, 240, 280, 40, 0)
hammeranim = Animation(blbarrelfirehammers, 360, 400, 40, 0)
fireballanim = Animation(blbarrelfirehammers, 280, 360, 40, 2)
vec0=Vector((0,0))
#Create Sprite objects
hammer1 = Hammer(Vector((1000, 400)), vec0, vec0, hammeranim)
hammer2 = Hammer(Vector((500, 200)), vec0, vec0, hammeranim)
coin_an0 = Animation(coin0_s, 0, 50, 40, 1)
princystillanim = Animation(princys, 0, 50, 50, 0)
pauline = Pauline(Vector((WIDTH / 2 - 100, 140)),Vector((0, 0)), Vector((0, 0)), princystillanim)
princyMoveanim = Animation(princys, 0, 150, 50, 0)
mario = Mario(Vector((100, HEIGHT - 59)), vec0,"face_right", playerWalkingRightanim)
donkeykong = DonkeyKong(Vector((30, 160)), vec0, vec0, dkstompanim)
# List of Coins
coin1 = Coin(Vector((0, 0)),vec0, vec0, coin_an0,0)
coinlist = []
cx = [random.randint(50, 1200) for x in range(25)]
cy = [random.randint(100, 600) for x in range(25)]
for i in xrange(20):
    coinlist.append(Coin(Vector((cx[i], cy[i])), Vector(
        (0, 0)), Vector((0, 0)), coin_an0,i%6))

oilDrum = OilDrum(Vector((20, HEIGHT - 60)), Vector((0, 0)),
                  Vector((0, 0)), oilBarrelanim)
blue_barrels = BlueBarrelList()
regular_barrels = RegularBarrelList()
oilDrumFire = OilDrumFire(Vector((20, HEIGHT - 95)),
                          Vector((0, 0)), Vector((0, 0)), oilBarrelFireanim)
num_stacked_barrels,stBarrels =4,[]
sb1 = RegularBarrel(Vector((6, 166)), Vector((0, 0)),
                    Vector((0, 0)), barrel_vertical_an, 1)
stBarrels.append(sb1)
sb2 = RegularBarrel(Vector((36, 166)), Vector((0, 0)),
                    Vector((0, 0)), barrel_vertical_an, 1)
stBarrels.append(sb2)
sb3 = RegularBarrel(Vector((6, 201)), Vector((0, 0)),
                    Vector((0, 0)), barrel_vertical_an, 1)
stBarrels.append(sb3)
sb4 = RegularBarrel(Vector((36, 201)), Vector((0, 0)),
                    Vector((0, 0)), barrel_vertical_an, 1)
stBarrels.append(sb4)

# music
playerDeadMusic = pygame.mixer.Sound(os.path.join('sounds','sad.wav'))
playerDeadMusic.set_volume(1.5)
cryMusic = pygame.mixer.Sound(os.path.join('sounds','cry.wav'))
Lev1Music=pygame.mixer.Sound("sounds/game.wav")
menusound= pygame.mixer.Sound(os.path.join('sounds','cool.wav'))
HammerMusic = pygame.mixer.Sound("sounds/hammer.mp3")
JumpMusic = pygame.mixer.Sound("sounds/jump.wav")
WinMusic = pygame.mixer.Sound("sounds/win_converted.wav")
coinMusic = pygame.mixer.Sound("sounds/coin.wav")
