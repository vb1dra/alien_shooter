from random import randint
from pygame import *

win_X = 700
win_Y = 500

window = display.set_mode((win_X,win_Y))
display.set_caption('shooter')
background = transform.scale(image.load('galaxy.jpg'),(win_X,win_Y))

class GameSprite(sprite.Sprite):
    def __init__(self, player_picture, player_x, player_y, player_speed, rX, rY):
        super().__init__()
        self.image = transform.scale(image.load(player_picture),(rX,rY))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.rX = rX
        self.rY = rY
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        global tik
        global tNowPlayer
        global bulletNum
        global bulletNumMax
        if keys_pressed[K_RIGHT] and self.rect.x < win_X-self.rX:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if tik-tNowPlayer >= 15:
            if bulletNum < bulletNumMax:
                bulletNum += 1
            tNowPlayer = tik
    def fire(self):
        global bulletNum
        if bulletNum >= 1:
            bullet = Bullet('bullet.png', self.rect.centerx - 7, self.rect.top, 15, 15, 20)
            fire.play()
            bullets.add(bullet)
            bulletNum -= 1
class Enemys(GameSprite):
    def update(self):
        if self.rect.y < win_Y:
            self.rect.y += self.speed
            if randint(1,2) == 1:
                self.rect.x += randint(0,5)
            else:
                self.rect.x -= randint(0,5)
        else:
            global lost
            lost += 1
            self.rect.y = randint(self.rY,self.rY*2) * -1
            self.rect.x = randint(self.rX,win_X-self.rX)
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > win_X-self.rX:
            self.rect.x = win_X-self.rX
class Asteroid(GameSprite):
    def update(self):
        if self.rect.y < win_Y:
            self.rect.y += self.speed
        else:
            if finish == False:
                xsM = randint(40,120)
                ysM = xsM
                self.rect.y = randint(2,10)*self.rY* -1
                self.rect.x = randint(self.rX,win_X-self.rX)
            if finish == 'bossFight':
                global score
                score += 1 
                self.kill()
class Bullet(GameSprite):
    def update(self):
            self.rect.y -= self.speed
            if self.rect.y == self.rY * -1:
                self.kill()
class EnemyBoss(GameSprite):
    def atack(self):
        global bossNumAtk
        global score
        global max_score
        global tik
        global tNowBoss
        global fI
        global fI_2
        
        if bossNumAtk == 0:
            bossNumAtk = randint(1,3)
        
        if bossNumAtk == 1:
            score = 0
            max_score = 10
            for i in range(max_score):
                asteroidCreate()
            bossNumAtk = -1
        
        if bossNumAtk == 2:
            score = 0
            max_score = 10
            for i in range(max_score):
                enemyCreate()
            bossNumAtk = -1

        if bossNumAtk == 3:
            score = 0
            max_score = 10
            fI = randint(2,8)
            fI_2 = max_score - fI
            for i in range(fI):
                enemyCreate()
            for i in range(fI_2):
                asteroidCreate()
            bossNumAtk = -1

        if bossNumAtk == -2:
            score = 0
            if self.rect.y < 0:
                self.rect.y += self.speed
            else:
                bossNumAtk = -3
                tNowBoss = tik

        if bossNumAtk == -3:
            if tNowBoss+90 <= tik:
                if self.rect.y > -320:
                    self.rect.y -= self.speed
                else:
                    bossNumAtk = 0
            
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
fire = mixer.Sound('fire.ogg')

player = Player('rocket.png', win_X/2, win_Y-70, 10, 50, 70)

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()

bulletNumMax = 10
tNowPlayer = 0
bulletNum = bulletNumMax
bossHP = 100
bossFight = -1
bossNumAtk = -1
qwe = 3
fnum = 0
lost = 0
max_lost = 16
score = 0
max_score = 99
max_HP = 16
hp = max_HP
speed = 0
tik = 1

def asteroidCreate():
    global speed
    xsM = randint(40,120)
    ysM = randint(40,120)
    if ysM+xsM >= 80 and ysM+xsM <= 119:
        speed = randint(12,15)
    elif ysM+xsM >= 120 and ysM+xsM <= 159:
        speed = randint(9,12)
    elif ysM+xsM >= 160 and ysM+xsM <= 199:
        speed = randint(6,9)
    elif ysM+xsM >= 200 and ysM+xsM <= 240:
        speed = randint(3,6)
    asteroid = Asteroid('asteroid.png', randint(xsM,win_X-xsM), randint(2,10)*ysM*-1, speed, xsM, ysM)
    asteroids.add(asteroid)
def enemyCreate():
    monster = Enemys('ufo.png', randint(80,620), randint(40,80) * -1, randint(1,5), 80, 40)
    monsters.add(monster)

for i in range(6):
    enemyCreate()
for i in range(1):
    asteroidCreate()

font.init()
font1 = font.SysFont('Arial', 20)
font2 = font.SysFont('Arial', 30)

FPS = 60
clock = time.Clock()
clock.tick(FPS)
game = True
finish = False
while game:
    bulletBord = font1.render('Боеприпасы:' + str(bulletNum) + '/' + str(bulletNumMax), False, (255, 255, 255))
    scorebord = font1.render('Счёт:' + str(score) + '/' + str(max_score), False, (255, 255, 255))
    missed = font1.render('Пропушенно:' + str(lost) + '/' + str(max_lost), False, (255, 255, 255))
    healPoint = font1.render('Прочность:' + str(hp) + '/' + str(max_HP), False, (255, 255, 255))
    bossbar = font1.render('Прочность босса:' + str(bossHP) + '/' + '100', False, (255, 255, 255))
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key == K_UP and fnum == 0 and finish != True:
                player.fire()
                fnum = 1
        elif i.type == KEYUP:
            if i.key in [K_UP]:
                fnum = 0

    keys_pressed = key.get_pressed()
    collide_player = sprite.spritecollide(player, monsters, True)
    collide_asteroid = sprite.spritecollide(player, asteroids, True)
    collide_enemy = sprite.groupcollide(monsters, bullets, True, True)

    window.blit(background,(0,0))
    if collide_player:
        hp -= 1
        enemyCreate()
    if collide_asteroid:
        hp -= 1
    if lost == max_lost:
        finish = True
        mixer.music.stop()
        window.blit(background,(0,0))
        window.blit(font1.render('Вы проиграли!', False, (255, 0, 0)),(0,80))
        window.blit(font1.render('Инопланетяне добрались до вашей базы.', False, (255, 0, 0)),(0,100))
    if hp == 0:
        finish = True
        mixer.music.stop()
        window.blit(background,(0,0))
        window.blit(font1.render('Вы проиграли!', False, (255, 0, 0)),(0,80))
        window.blit(font1.render('Ваш корабль разрушен.', False, (255, 0, 0)),(0,100))
    if bossHP <= 0:
        finish == True
        bossFight = False
        mixer.music.stop()
        window.blit(background,(0,0))
        window.blit(font1.render('Вы победили!', False, (0, 255, 0)),(0,80))
        window.blit(font1.render('Босс был повержен.', False, (0, 255, 0)),(0,100))

    if finish == False:
        if score == max_score:
            finish = 'bossFight'
            for monster in monsters:
                monster.kill()
            for asteroid in asteroids:
                asteroid.kill()
        for i in collide_enemy:
            score += 1
            enemyCreate()
        for i in collide_asteroid:
            asteroidCreate()
        bullets.update()
        bullets.draw(window)
        player.reset()
        player.update()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        window.blit(scorebord,(0,60))
    if finish == 'bossFight':
        while qwe != 0:
            window.blit(background,(0,0))
            window.blit(font1.render('Внимание!', False, (255, 0, 0)),(0,80))
            window.blit(font1.render('Приближается босс.', False, (255, 0, 0)),(0,100))
            window.blit(font2.render(str(qwe) + '...', False, (255, 255, 255)),(350,250))
            display.update()
            qwe -= 1
            time.delay(1000)
            if qwe == 0:
                boss = EnemyBoss('ufo.png', (win_X - 600)/2, -300, 10, 600, 300)
                bossFight = True
                score = 0
                max_score = 10
                bossNumAtk = -2
        if bossFight == True:
            collide_boss = sprite.spritecollide(boss, bullets, True)  
            if score >= max_score:
                bossNumAtk = -2
            for i in collide_enemy:
                score += 1
            for i in collide_asteroid:
                score += 1
            if collide_player:
                score += 1
            boss.reset()
            boss.atack()
            monsters.update()
            monsters.draw(window)
            asteroids.update()
            asteroids.draw(window)
            bullets.update()
            bullets.draw(window)
            player.reset()
            player.update()
            window.blit(bossbar,(0,60))
            if collide_boss:
                bossHP -= 1

    window.blit(missed,(0,20))
    window.blit(healPoint,(0,0))
    window.blit(bulletBord,(0,40))
    tik += 1
    #window.blit(font1.render(str(tik), False, (255, 255, 255)),(0,120))

    time.delay(25)
    display.update()