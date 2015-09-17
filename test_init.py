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

@pytest.fixture
def vec():
    return Vector((0,0))

@pytest.fixture
def  donkey():
    return sprite.DonkeyKong(Vector((30, 160)), Vector((0,0)), Vector((0,0)), globals.dkstompanim)

def check_boundaries(x,y):
    if(x>globals.WIDTH or x<0 or y<0 or y>globals.HEIGHT):
        raise IndexError('Out of bounds')

class TestPlayer:
        def test_player_properly_initialized(self,mar):
            assert mar.animationstate == "face_right"
            assert mar.actionstate == "on_ground"
            assert mar.jumptime ==0
            assert mar.hammer_time == 0
            assert mar.pos.x == 100
            assert mar.pos.y == (640 - 59)

        def test_player_move_right(self,mar):
            y=mar.pos.y
            x=mar.pos.x
            mar.setAnimationState("walk_right")
            mar.applyGroundForce(Vector((1.5,0)),1)
            mar.move(1)
            assert mar.pos.x > x
            assert mar.pos.y == y

        def test_player_move_left(self,mar):
            x=mar.pos.x
            y=mar.pos.y
            mar.setAnimationState("walk_left")
            mar.applyGroundForce(Vector((-1.5,0)),1)
            mar.move(1)
            assert mar.pos.x < x
            assert mar.pos.y == y

        def test_player_jump(self,mar):
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

        def test_player_jump(self,mar):
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

        def test_player_climb_up(self,mar,lev1):
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

        def test_player_climb_down(self,mar,lev1):
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

        def test_out_of_bound_exception_mario(self,mar):
            with pytest.raises(IndexError) as execinfo:
                mar.pos.x=-1
                check_boundaries(mar.pos.x,mar.pos.y)
            assert execinfo.value.message == 'Out of bounds'


class TestCoin:
        def test_player_collect_coin(self,mar,coin):
            mar.pos=coin.pos
            prev=globals.score
            surface = pygame.display.set_mode(globals.SIZE)
            mar.collectCoin(coin,surface)
            assert coin.picked_up == True
            assert globals.score == prev+10

        def test_out_of_bound_exception_random_coins(self,coin):
            with pytest.raises(IndexError) as execinfo:
                coin.pos.y=globals.HEIGHT+1
                check_boundaries(coin.pos.x,coin.pos.y)
            assert execinfo.value.message == 'Out of bounds'

class TestFireball:
        def test_player_fireball_collision(self,mar,fb):
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

        def test_out_of_bound_exception_random_fireballs(self,fb):
            with pytest.raises(IndexError) as execinfo:
                fb[0].pos.y=globals.HEIGHT+1
                check_boundaries(fb[0].pos.x,fb[0].pos.y)
            assert execinfo.value.message == 'Out of bounds'


class TestPrincess:
        def test_player_princess_collision(self,mar,princess):
            mar.pos=princess.pos
            assert mar.reachPaulineWin(princess) == True

        def test_out_of_bound_exception_princess(self,princess):
            with pytest.raises(IndexError) as execinfo:
                princess.pos.y=globals.HEIGHT+5
                check_boundaries(princess.pos.x,princess.pos.y)
            assert execinfo.value.message == 'Out of bounds'

class TestDonkey:

        def test_player_properly_initialized(self,donkey):
            assert donkey.pos.x == 30
            assert donkey.pos.y == 160
            assert donkey.acc.x == 0
            assert donkey.vel.x == 0
            assert donkey.acc.y == 0
            assert donkey.vel.y == 0



        def test_out_of_bound_exception_donkey(self,donkey):
            with pytest.raises(IndexError) as execinfo:
                donkey.pos.x=globals.WIDTH+5
                check_boundaries(donkey.pos.x,donkey.pos.y)
            assert execinfo.value.message == 'Out of bounds'

class TestVector:

        def checkTypeVector(vec1,vec2):

            if isinstance(vec1,Vector) and isinstance(vec2,Vector):
             return 
            else :
                raise TypeError('Operands are not Vectors')


        def test_out_of_bound_exception_vector_operations_add(self,vec):
            vec1=vec
            vec2=(5,6) 
            with pytest.raises(TypeError):
                vec3=vec2+vec1

        def test_out_of_bound_exception_vector_operations_mul(self,vec):
            vec1=vec
            vec2=(5,6) 
            with pytest.raises(TypeError):
                vec3=vec2*vec1

        def test_div_by_zero_err_vector_operations_div(self,vec):
            k=0
            with pytest.raises(ZeroDivisionError):
                vec3=vec/k
