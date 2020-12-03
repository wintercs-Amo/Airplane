import pygame
from pygame.locals import *
import random
# 飞行物类   是英雄机 敌机 子弹  小蜜蜂 的基类
class Flyer():
    def __init__(self,x,y,image,speed):
        self.x = x
        self.y = y
        self.image = image
        self.speed = speed

    def fly(self):
        self.y += self.speed

#子弹类
class Bullet(Flyer):
    def __init__(self,x,y,image,speed):
        super().__init__(x,y,image,speed)


#英雄机
class Hero(Flyer):
    def __init__(self,x,y,image,speed):
        super().__init__(x,y,image,speed)

    def flyleft(self):
        self.x -= self.speed

    def flyright(self):
        self.x += self.speed

    def flyup(self):
        self.y -= self.speed

    def flydown(self):
        self.y += self.speed

    def shoot(self,bulletimg):
        return Bullet(self.x+self.image.get_rect().width/2-5,self.y-10,bulletimg,-5)

#敌机
class Enemy(Flyer):
    def __init__(self,x,y,image,speed,type):
        super().__init__(x,y,image,speed)
        self.type = type

#奖励
class Gift(Flyer):
    def __init__(self,x,y,image,speed):
        super().__init__(x,y,image,speed)
    def flydown(self):
        self.y = self.y - 10


class AirPlane():
    def __init__(self):
        pygame.init()
        self.enemyimg = []
        self.bullets = []
        self.enemies = []
        self.hitenemyimg = []
        self.hitenemis = []
        self.load()
        rect = self.background.get_rect()
        self.window = pygame.display.set_mode((rect.width,rect.height))
        self.hero = Hero(rect.width/2-50,rect.height/2,self.heroimage[0],6)

        self.n = 0


    def swap(self):
        if self.n%2 == 0:
            self.hero.image = self.heroimage[0]
        else:
            self.hero.image = self.heroimage[1]

    def paint(self):
        self.window.blit(self.background,(0,0))
        self.window.blit(self.hero.image,(self.hero.x,self.hero.y))

        self.swap()
        self.n += 1
        for b in self.bullets:
            self.window.blit(b.image,(b.x,b.y))
        for e in self.enemies:
            self.window.blit(e.image,(e.x,e.y))

        for e in self.hitenemis:
            self.window.blit(e.image,(e.x,e.y))
            if self.n%3 == 0:
                e.num = e.num + 1
            if e.num >= len(self.hitenemyimg[e.type]):
                self.hitenemis.remove(e)
            else:
                e.image = self.hitenemyimg[e.type][e.num]

        pygame.display.update()

    def load(self):
        self.background = pygame.image.load('./images/background.png')
        self.bigbomb = pygame.image.load('./images/dog.png')
        self.gift = pygame.image.load('./images/bomb-1.gif')
        self.heroimage = []
        for i in range(1,3):
            img = pygame.image.load('./images/hero%d.png'%i)
            self.heroimage.append(img)
        self.bulletimg = pygame.image.load('./images/bullet1.png')
        for i in range(3):
            img = pygame.image.load('./images/enemy%d.png'%i)
            self.enemyimg.append(img)

        for i in range(3):
            images = []
            if i < 2:
                for j in range(1,5):
                    img = pygame.image.load('./images/enemy%d_down%d.png'%(i,j))
                    images.append(img)
            else:
                for j in range(1,7):
                    img = pygame.image.load('./images/enemy%d_down%d.png'%(i,j))
                    images.append(img)
            self.hitenemyimg.append(images)


    def kingfinger(self):
        for e in self.enemies:
            self.enemies.remove(e)
            self.window.blit(self.bigbomb, (0, 11))
        pygame.display.update()

    def event(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            self.hero.flyleft()
        if keys[K_RIGHT]:
            self.hero.flyright()
        if keys[K_DOWN]:
            self.hero.flydown()
        if keys[K_UP]:
            self.hero.flyup()
        if keys[K_5]:
            self.kingfinger()

        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_LEFT:
                    self.hero.flyleft()
                if e.key == K_RIGHT:
                    self.hero.flyright()
                if e.key == K_DOWN:
                    self.hero.flydown()
                if e.key == K_UP:
                    self.hero.flyup()
                if e.key == K_5:
                    self.kingfinger()
                elif e.key == K_SPACE:
                    b = self.hero.shoot(self.bulletimg)
                    self.bullets.append(b)

    def fly(self):
        for b in self.bullets:
            b.fly()
        for e in self.enemies:
            e.fly()

    def makeenemy(self):
        type = random.randint(0,2)
        e = Enemy(random.randint(0,self.background.get_rect().width-self.enemyimg[type].get_rect().width),-self.enemyimg[type].get_rect().height,self.enemyimg[type],type+1,type)
        self.enemies.append(e)

    def destroyoutboundsflyer(self):
        for b in self.bullets:
            if b.y < -b.image.get_rect().height:
                self.bullets.remove(b)
        for e in self.enemies:
            if e.y > self.background.get_rect().height:
                self.enemies.remove(e)

    def check(self,bullet,enemy):
        if bullet.x  <= enemy.x:
            return False
        if bullet.x >= enemy.x + enemy.image.get_rect().width:
            return False
        if bullet.y  <= enemy.y:
            return False
        if bullet.y >= enemy.y + enemy.image.get_rect().height:
            return False
        return True


    def hit(self):
        hitbullets = []
        hitenemies = []
        for b in self.bullets:
            for e in self.enemies:
                if self.check(b,e):
                    hitbullets.append(b)
                    hitenemies.append(e)
                    break
        for b in hitbullets:
            self.bullets.remove(b)

        for e in hitenemies:
            e.num = 0
            e.image = self.hitenemyimg[e.type][0]
            self.hitenemis.append(e)
            self.enemies.remove(e)

    def crash(self,hero,enemy):
        if hero.x + hero.image.get_rect().width<= enemy.x:
            return False
        if hero.x >= enemy.x + enemy.image.get_rect().width:
            return False
        if hero.y + hero.image.get_rect().height<= 10+enemy.y:
            return False
        if hero.y >= enemy.y + enemy.image.get_rect().height:
            return False
        return True

    def iscrash(self):
        hitenemies = []
        for e in self.enemies:
            if self.crash(self.hero,e):
                print('撞烂他们！！')
                hitenemies.append(e)
                break
        for e in hitenemies:
            e.num = 0
            e.image = self.hitenemyimg[e.type][0]
            self.hitenemis.append(e)
            self.enemies.remove(e)

    def stranger(self):
        pass

    def isstranger(self):
        pass

    def makegift(self):
        self.window.blit(self.gift,(300,20))
        print('奖励')
        #self.window.blit('stringqweqe',(0,5))
        self.gift.flydown()
        pygame.display.update()

    def start(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(60)
            if self.n % 4 == 0 and random.randint(0,4) == 0:
                self.makeenemy()
            self.fly()

            self.hit()
            self.stranger()
            self.iscrash()
            self.event()
            #把飞出屏幕外的子弹和敌机删除
            self.destroyoutboundsflyer()
            self.makegift
            self.paint()


if __name__ == '__main__':
    airplane = AirPlane()
    airplane.start()