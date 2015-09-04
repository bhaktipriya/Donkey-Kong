import pygame,vector
import copy,random
import globals

class Sprite(object):

    def __init__(self, pos, vel, acc, animation):
        self.vel, self.acc, self.animation = vel, acc, animation
        self.__activate = 1
        self.pos=pos
    def draw(self, surface):
        if self.__activate:
            self.animation.draw(surface, self.pos.x, self.pos.y)
    
    def update(self, dt):
        if self.__activate:
            self.animation.update(dt)

    def move(self):
        self.__activate += 1

        
class Platform(Sprite):

    def __init__(self, pos, vel, acc, animation):
        self.__lines = 1
        super(Platform, self).__init__(pos, vel, acc, animation)

    def move(self):
        self.__lines += 1
        super(Platform, self).move()

    def update(self, dt):
        self.__lines += 1
        super(Platform, self).update(dt)

    def draw(self, surface):
        if self.__lines:
            super(Platform, self).draw(surface)


class OilDrum(Sprite):

    def __init__(self, pos, vel, acc, animation):
        self.__qty = 1
        super(OilDrum, self).__init__(pos, vel, acc, animation)

    def move(self):
        self.__qty += 1
        super(OilDrum, self).move()

    def update(self, dt):
        self.__qty += 1
        super(OilDrum, self).update(dt)

    def draw(self, surface):
        if self.__qty:
            super(OilDrum, self).draw(surface)


class OilDrumFire(Sprite):

    def __init__(self, pos, vel, acc, animation):
        self.burn = 1
        super(OilDrumFire, self).__init__(pos, vel, acc, animation)

    def move(self):
        if self.burn:
            super(OilDrumFire, self).move()

    def update(self, dt):
        if self.burn:
            super(OilDrumFire, self).update(dt)

    def draw(self, surface):
        if self.burn:
            super(OilDrumFire, self).draw(surface)


class FireBall(Sprite):

    def __init__(self, pos, vel, acc, animation):
        sel.__burn = 1
        super(FireBall, self).__init__(pos, vel, acc, animation)

    def move(self):
        self.__burn += 1

    def update(self, dt):
        if self.__burn:
            super(FireBall, self).update(dt)

    def draw(self, surface):
        if self.__burn:
            super(FireBall, self).draw(surface)


class RegularBarrel(Sprite):

    def __init__(self, pos, vel, acc, animation, a=0):

        self.rolling = 1
        super(RegularBarrel, self).__init__(pos, vel, acc, animation)
        self.active = a

    def reset(self):
        self.rolling = 1
        self.active, self.pos.x, self.pos.y = 0, 20, 200

    def wallCollision(self):
        if self.rolling:
            w = self.animation._rect.w
            if globals.WIDTH < self.pos.x + w:
                self.vel.x, self.pos.x = -self.vel.x, globals.WIDTH - w

            if self.pos.y < globals.HEIGHT - 100:
                if self.pos.x < -15:
                    self.pos.x = -15
                    self.vel.x = -self.vel.x

            if globals.HEIGHT < self.pos.y:
                self.reset()

    def move(self, dt):
        self.pos = self.pos + self.vel * dt

    def applyGravity(self, dt):
        self.vel.y = self.vel.y + (0.05 * dt)

    def objectCollision(self, objects):

        for obj in objects:
            for line in obj:
                v3 = copy.deepcopy(self.pos)
                v1, v2 = vector.Vector(line[0]), vector.Vector(line[1])
                v3.y,v3.x = v3.y + self.animation._rect.h, v3.x + self.animation._rect.w / 2
                t2, t1 = v3 - v1, v2 - v1
                t = (vector.vecDot(t1, t2))
                t /= (vector.vecDot(t1, t1))
                v = t1 * t
                v += v1
                distance = vector.vecDist(v3, v)
                left_obj = min(line[1][0], line[0][0])
                right_obj = max(line[1][0], line[0][0])
                if distance < 5:
                    if v3.x >= left_obj:
                        if v3.x <= right_obj:
                            self.pos.y = v.y - self.animation._rect.h
                            self.vel.y, self.acc.y = 0, 0

    def applyForce(self, force, acc):
        self.vel, self.acc, self.active = force, acc, 1

    def update(self, dt):

        if self.active != 0:
            self.move(dt)
            self.applyGravity(dt)
            self.wallCollision()
            self.animation.update(dt)

    def draw(self, surface):

        if self.active != 0:
            super(RegularBarrel, self).draw(surface)


class BlueBarrel(RegularBarrel):

    def __init__(self, pos, vel, acc, animation, a=0):
        self.bbl = 1
        super(BlueBarrel, self).__init__(pos, vel, acc, animation, a)

    def reset(self):
        self.bbl = 1
        super(BlueBarrel, self).reset()

    def wallCollision(self):
        if self.bbl:
            super(BlueBarrel, self).wallCollision()

    def applyGravity(self, dt):
        if self.bbl:
            super(BlueBarrel, self).applyGravity(dt)

    def move(self, dt):
        if self.bbl:
            super(BlueBarrel, self).move(dt)

    def objectCollision(self, objects):
        if self.bbl:
            super(BlueBarrel, self).objectCollision(objects)

    def applyForce(self, force, acc):
        if self.bbl:
            super(BlueBarrel, self).applyForce(force, acc)

    def update(self, dt):
        self.bbl += 1
        super(BlueBarrel, self).update(dt)

    def draw(self, surface):
        if self.bbl:
            super(BlueBarrel, self).draw(surface)


class BarrelList(object):

    def __init__(self):
        self.insert_flag, self.clock_time = 0, 0
        self.barrels = []
        self._empty = 1

    def activate(self):
        self._empty = 1

    def update(self, timer, flag):
        if self._empty:
            self.clock_time = self.clock_time + timer.dt2
            map(lambda barrel: barrel.update(timer.dt), self.barrels)
            self.remove()
            self.reset(flag)

    def checkCollisions(self, levelOne):
        map(lambda barrel: barrel.objectCollision(levelOne.lines), self.barrels)

    def remove(self):
        for barrel in self.barrels:
            if self._empty:
                if barrel.active == 0:
                    del barrel

    def reset(self, flag):
        if flag:
            self.clock_time, self.insert_flag = 0, 0
            del self.barrels[0:len(self.barrels)]

    def draw(self, surface):
        map(lambda barrel: barrel.draw(surface), self.barrels)


class RegularBarrelList(BarrelList):

    def __init__(self):
        self.__qty = 1
        super(RegularBarrelList, self).__init__()

    def activate(self):
        fact = 1000
        if (self.clock_time / fact) % 4 != 0:
            self.insert_flag = 0

        if (self.clock_time / fact) % 4 == 0:
            if self.insert_flag == 0:
                self.insert_flag = 1
                v1=vector.Vector((20, 200))
                v2=vector.Vector((2.8, 0))
                self.barrels.append(RegularBarrel(v1,v2,v2, globals.barrel_sideways_an, 1))

    def update(self, timer, flag):
        if self.__qty:
            super(RegularBarrelList, self).update(timer, flag)

    def checkCollisions(self, levelOne):
        if self.__qty:
            super(RegularBarrelList, self).checkCollisions(levelOne)

    def remove(self):
        if self.__qty:
            super(RegularBarrelList, self).remove()

    def reset(self, flag):
        self.__qty = 1
        super(RegularBarrelList, self).reset(flag)

    def draw(self, surface):
        if self.__qty:
            super(RegularBarrelList, self).draw(surface)


class BlueBarrelList(BarrelList):

    def __init__(self):
        self.bbl = 1
        super(BlueBarrelList, self).__init__()

    def activate(self):
        fact = 1000
        if (self.clock_time / fact) % 4 != 0:
            self.insert_flag = 0

        if (self.clock_time / fact) % 4 == 0:
            if self.insert_flag == 0:
                v1=vector.Vector((20, 200))
                v2=vector.Vector((2.8, 0))
                self.insert_flag = 1
                self.barrels.append(BlueBarrel(v1,v2, v2, globals.bluebarrel_sideways_an, 1))

    def update(self, timer, flag):
        self.bbl += 1
        super(BlueBarrelList, self).update(timer, flag)

    def checkCollisions(self, levelOne):
        if self.bbl:
            super(BlueBarrelList, self).checkCollisions(levelOne)

    def remove(self):
        if self.bbl:
            super(BlueBarrelList, self).remove()

    def reset(self, flag):
        self.bbl = 1
        super(BlueBarrelList, self).reset(flag)

    def draw(self, surface):
        if self.bbl:
            super(BlueBarrelList, self).draw(surface)


class Hammer(Sprite):

    def __init__(self, pos, vel, acc, animation):
        self.reset_pos, self.reset_vel, self.reset_acc, self.reset_animation = pos, vel, acc, animation
        super(Hammer, self).__init__(pos, vel, acc, animation)
        self.picked_up = False
        self.pts = 1

    def reset(self):
        self.picked_up = False
        self.pos, self.vel, self.acc, self.animation = self.reset_pos, self.reset_vel, self.reset_acc, self.reset_animation

    def update(self, dt):
        self.pts += 1
        super(Hammer, self).update(dt)

    def draw(self, surface):
        if self.picked_up == True:
            return
        super(Hammer, self).draw(surface)


class Coin(Sprite):

    def __init__(self, pos, vel, acc, animation,com):
        self.reset_pos, self.reset_vel, self.reset_acc, self.reset_animation = pos, vel, acc, animation
        super(Coin, self).__init__(pos, vel, acc, animation)
        self.picked_up = False
        self.great=False
        self.t=100/2
        s=["Awesome!","Speechless!","Flawless!","Great!","Marvellous!","Amazing!"]
        self.k=com
        self.comment=s[self.k]

    def reset(self):
        self.picked_up = False
        self.great=False
        self.t=100/2
        s=["Awesome!","Speechless!","Flawless!","Great!","Marvellous!","Amazing!"]
        self.comment=s[self.k]
        self.pos, self.vel, self.acc, self.animation = self.reset_pos, self.reset_vel, self.reset_acc, self.reset_animation

    def update(self, dt):

        super(Coin, self).update(dt)

    def draw(self, surface, coin_step):
        step=40
        src = pygame.Rect(0, 0, step, globals.coinRect.h)
        dest = pygame.Rect(self.pos.x, self.pos.y, step, src.h)
        if self.picked_up==True:
            if self.great==False:
                globals.coinMusic.play(0)
                gotcoin=globals.smallfont.render(self.comment,1,globals.LIGHTPINK)
                posi=min(self.pos.x+150,globals.WIDTH-200)
                posi=max(0,posi)
                surface.blit(gotcoin,(posi,self.pos.y))
                self.t-=1
                if self.t==0:
                    self.great=True
                

        if self.picked_up == False:
            step = 40
            if coin_step == 0:
                surface.blit(globals.coin0_s, dest, src)
            if coin_step == 1:
                surface.blit(globals.coin1_s, dest, src)
            if coin_step == 2:
                surface.blit(globals.coin2_s, dest, src)
            if coin_step == 3:
                surface.blit(globals.coin3_s, dest, src)


class Pauline(Sprite):

    def __init__(self, pos, vel, acc, animation):
        self.__resc = 0
        super(Pauline, self).__init__(pos, vel, acc, animation)

    def move(self):
        self.__resc = 0

    def update(self, dt):
        if not self.__resc:
            super(Pauline, self).update(dt)

    def draw(self, surface):
        if not self.__resc:
            super(Pauline, self).draw(surface)


class DonkeyKong(Sprite):

    def __init__(self, pos, vel, acc, animation):
        self.__mv = 1
        super(DonkeyKong, self).__init__(pos, vel, acc, animation)

    def move(self):
        self.__mv += 1

    def update(self, dt):
        self.__mv += 1
        super(DonkeyKong, self).update(dt)

    def draw(self, surface):
        if self.__mv:
            super(DonkeyKong, self).draw(surface)
