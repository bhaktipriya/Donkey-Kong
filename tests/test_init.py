import pytest,pygame
from vector import Vector
import globals
import player
import levelOne
import sprite

@pytest.fixture
def mar():
    vec0=Vector((0,0))
    return player.Mario(Vector((100, globals.HEIGHT - 59)), vec0,"face_right",globals.playerWalkingRightanim)

@pytest.fixture
def lev1():
    levelone = levelOne.LevelOne()
    levelone.create()
    return levelone

@pytest.fixture
def coin():
    return globals.coinlist[0]

@pytest.fixture
def princess():
    return globals.pauline

@pytest.fixture
def fb():
    globals.blue_barrels.reset(1)
    globals.blue_barrels.activate()
    return globals.blue_barrels.barrels


def test_player_properly_initialized(mar):
    assert mar.animationstate == "face_right"
    assert mar.actionstate == "on_ground"
    assert mar.jumptime ==0
    assert mar.hammer_time == 0
    assert mar.pos.x == 100
    assert mar.pos.y == (640 - 59)


def test_player_move_right(mar):
    y=mar.pos.y
    x=mar.pos.x
    mar.setAnimationState("walk_right")
    mar.applyGroundForce(Vector((1.5,0)),1)
    mar.move(1)
    assert mar.pos.x > x
    assert mar.pos.y == y

def test_player_move_left(mar):
    x=mar.pos.x
    y=mar.pos.y
    mar.setAnimationState("walk_left")
    mar.applyGroundForce(Vector((-1.5,0)),1)
    mar.move(1)
    assert mar.pos.x < x
    assert mar.pos.y == y

def test_player_jump(mar):
    x=mar.pos.x
    y=mar.pos.y
    mar.actionstate="jumping"
    #print mar.pos.x,mar.pos.y
    mar.applyGravity(2)
    mar.applyJump(2)
    #mar.applyGroundForce(Vector((-1.5,0)),1)
    mar.move(2)
    #print mar.pos.x,mar.pos.y
    assert mar.pos.x == x
    assert mar.pos.y < y

def test_player_jump(mar):
    x=mar.pos.x
    y=mar.pos.y
    mar.actionstate="jumping"
    #print mar.pos.x,mar.pos.y
    mar.applyGravity(2)
    mar.applyJump(2)
    #mar.applyGroundForce(Vector((-1.5,0)),1)
    mar.move(2)
    #print mar.pos.x,mar.pos.y
    assert mar.pos.x == x
    assert mar.pos.y < y

def test_player_climb_up(mar,lev1):
    mar.pos.x,mar.pos.y=(globals.WIDTH * 0.8+0.2, globals.HEIGHT * 0.815)
    x=mar.pos.x
    y=mar.pos.y
    #,(WIDTH * 0.8, HEIGHT * 0.954)
    #print mar.pos.x,mar.pos.y
    mar.actionstate="on_ladder"
    mar.climb(lev1.ladderlines,"up")
    mar.applyVerticalForce(Vector((0,-1.5)),2)
    mar.move(2)
    #print mar.pos.x,mar.pos.y
    assert mar.pos.x == x
    assert mar.pos.y < y

def test_player_climb_up(mar,lev1):
    mar.pos.x,mar.pos.y=(globals.WIDTH * 0.8+0.2, globals.HEIGHT * 0.954)
    x=mar.pos.x
    y=mar.pos.y
    #,(WIDTH * 0.8, HEIGHT * 0.954)
    #print mar.pos.x,mar.pos.y
    mar.actionstate="on_ladder"
    mar.climb(lev1.ladderlines,"up")
    mar.applyVerticalForce(Vector((0,1.5)),2)
    mar.move(2)
    #print mar.pos.x,mar.pos.y
    assert mar.pos.x == x
    assert mar.pos.y > y

def test_player_collect_coin(mar,coin):
    
    mar.pos=coin.pos
    prev=globals.score
    surface = pygame.display.set_mode(globals.SIZE)
    mar.collectCoin(coin,surface)
    assert coin.picked_up == True
    assert globals.score == prev+10

def test_player_fireball_collision(mar,fb):
    mar.pos=fb[0].pos
    prevlife=globals.mario_num_lives
    assert mar.barrelCollision(fb) == 1
    assert globals.mario_num_lives == prevlife-1
    assert mar.animationstate == "face_right"
    assert mar.actionstate == "on_ground"
    assert mar.jumptime ==0
    assert mar.hammer_time == 0
    assert mar.pos.x == 100
    assert mar.pos.y == (640 - 60)

def test_player_princess_collision(mar,princess):
    mar.pos=princess.pos
    assert mar.reachPaulineWin(princess) == True


def test_an_exception():
        with pytest.raises(IndexError):
                    # Indexing the 30th item in a 3 item list
                            [5, 10, 15][30]

