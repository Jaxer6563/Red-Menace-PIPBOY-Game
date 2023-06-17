#!/usr/bin/env python3
# by Jackson Syring

## GPLv3
# This program is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''IMPORT STATEMENTS'''
import pygame
import sys
import os


'''VARIABLES'''
#Pygame
ScreenX = 640 #Window Dimensions
ScreenY = 480 #Window Dimensions
fps = 40 #Frames Per Second
ani = 4 #Animation Cycles
running = True
#Colors
BLUE  = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)

'''OBJECT CLASSES'''
class Player(pygame.sprite.Sprite):
    
    '''Spawn a player'''

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = []

        stand = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Player','Vault_Boy_Stand.png')).convert(),[28,52])
        left = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Player','Vault_Boy_Run_Left.png')).convert(),[28,52])
        right = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Player','Vault_Boy_Run_Right.png')).convert(),[28,52])
        Die = pygame.transform.scale(pygame.image.load(os.path.join('Assets','Player','Nuke_Explode.png')).convert(),[28,52])
        self.images.append(stand)
        self.images.append(left)
        self.images.append(right)
        self.images.append(Die)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.lives = 3
        self.movex = 0
        self.movey = 0
        self.frame = 0
        self.direction = 'left'
        self.is_Jumping = False
        self.is_Falling = False
    
    def control(self, x, y):
        '''Player Movement Controls'''
        self.movex += x
        self.movey += y

    def jump(self):
        if self.is_Jumping is False:
            self.is_Falling = False
            self.is_Jumping = True     
    
    def gravity(self):
        if self.is_Jumping:
            self.movey += 3.2 #Speed that the player falls

    def lives(self):
        pass

    def update(self):
        #Moving Left
        if self.movex < 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = self.images[1]
            self.direction = 'right'
        
        if self.movex > 0:
            self.frame += 1
            if self.frame > 3 * ani:
                self.frame = 0
            self.image = self.images[2]
            self.direction = 'left'
        if self.movex == 0:
            if self.direction == 'right':
                self.image = pygame.transform.flip(self.images[0], True, False)
            if self.direction == 'left':
                self.image = self.images[0]

        ground_hit_list = pygame.sprite.spritecollide(self, ground_list, False)
        for g in ground_hit_list:
            self.movey = 0
            self.rect.bottom = g.rect.top
            self.is_Jumping = False
            self.is_Jumping = False

        # fall off the world
        if self.rect.y > ScreenY:
            self.rect.x = tx
            self.rect.y = ty
  

        plat_hit_list = pygame.sprite.spritecollide(self, Plat_list, False)
        for p in plat_hit_list:
            self.is_Jumping = False
            self.is_Falling = False
            self.movey = 0

            # approach from below
            if self.rect.bottom <= p.rect.bottom:
               self.rect.bottom = p.rect.top
            else:
               self.movey += 3.2

        if self.is_Jumping and self.is_Falling is False:
            self.is_Falling = True
            self.movey -= 25

        self.rect.y += self.movey
        self.rect.x += self.movex

class Enemy_throwable(pygame.sprite.Sprite):
    '''Spawn Enemy'''
    def __init__(self, x,y, img,):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(img), [30, 30])
        self.rect = self.image.get_rect()
        self.nose = self.rect.centery, self.rect.x + 30
        self.target = player.rect.x, player.rect.y
        print(self.nose)
        

class Decor(pygame.sprite.Sprite):
    def __init__(self, x, y, img, scalex, scaley):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(img), [scalex,scaley])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Level:
    def ground(lvl, gloc, tx, ty):
        ground_list = pygame.sprite.Group()
        i = 0
        if lvl == 1:
            while i < len(gloc):
                ground = Platform(gloc[i], ScreenY - ty, tx, ty, 'Assets\Level\RebarPlatformBasic28x28.png')
                ground_list.add(ground)
                i = i + 1

        if lvl == 2:
            print("Level " + str(lvl))

        return ground_list

    def bad(lvl, eloc):
        if lvl == 1:
            enemy = Enemy(eloc[0], eloc[1], 'enemy.png')
            enemy_list = pygame.sprite.Group()
            enemy_list.add(enemy)
        if lvl == 2:
            print("Level " + str(lvl))

        return enemy_list

    # x location, y location, img width, img height, img file
    def platform(lvl, tx, ty):
        plat_list = pygame.sprite.Group()
        ploc = []
        i = 0
        if lvl == 1:
            ploc.append((0, ScreenY - ty - 280, 10))
            ploc.append((0, ScreenY - ty - 96, 2))
            ploc.append((120, ScreenY - ty - 96, 18))
            ploc.append((120, ScreenY - ty - 192, 18))
            while i < len(ploc):
                j = 0
                while j <= ploc[i][2]:
                    plat = Platform((ploc[i][0] + (j * tx)), ploc[i][1], tx, ty, 'Assets\Level\RebarPlatformBasic28x28.png')
                    plat_list.add(plat)
                    j = j + 1
                print('run' + str(i) + str(ploc[i]))
                i = i + 1

        if lvl == 2:
            print("Level " + str(lvl))

        return plat_list


class Platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, imgw, imgh, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img).convert()
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc
        
'''SETUP'''
clock = pygame.time.Clock()
pygame.init()
Screen = pygame.display.set_mode([ScreenX,ScreenY])
background = pygame.Surface(Screen.get_size())
backdropbox = Screen.get_rect()
#Player Set Up Code
player = Player()  #Spawn Player
player.rect.x = 591  #Player Spawn Location X
player.rect.y = 401  #Player Spawn Location Y
player_list = pygame.sprite.Group()
player_list.add(player)
steps = 8
#Decor Set Up Code
Communist = Decor(32,100, 'Assets\Extras\Enemy.png', 96, 69)
decor_list = pygame.sprite.Group()
decor_list.add(Communist)
Damsel = Decor(130,120, 'Assets\Extras\Vault_Girl.png', 28, 52)
decor_list.add(Damsel)
Stack = Decor(170, 120, 'Assets\Extras/Nuke_Stack.png', 100, 50)
decor_list.add(Stack)
#Enemy Set Up Code
enemy_list = pygame.sprite.Group()
nuke_Throw = Enemy_throwable(32, 100, 'Assets\Extras/Nuke_Throw.png')
enemy_list.add(nuke_Throw)
#Level Set Up Code
gloc = []
ty = 28
tx = 28
i = 0
while i <= (ScreenX/tx)+28:
    gloc.append(i*tx)
    i += 1
ground_list = Level.ground(1, gloc, tx,ty)
Plat_list = Level.platform(1, tx, ty)
lvl = 1




'''MAIN LOOP'''
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(-steps,0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(steps, 0)
            if event.key == pygame.K_SPACE:
                player.jump()
            if event.key == pygame.K_UP or event.key == ord('w'):
                print('Climb')

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                player.control(steps, 0)
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                player.control(-steps, 0)

        #Gets Mouse Position for placing sprites during Dev.
        #if event.type == pygame.MOUSEMOTION:
        #    x,y = pygame.mouse.get_pos()
        #    print(x,y)

    #Draw to the Screen 
    player.update()
    Screen.fill([0,0,0])          
    Screen.blit(background, backdropbox)
    player.gravity()
   # player.update()
    ground_list.draw(Screen) # refresh ground
    Plat_list.draw(Screen)
    decor_list.draw(Screen)
    enemy_list.draw(Screen)
    player_list.draw(Screen)
    pygame.display.flip()
    clock.tick(40)


