import pygame as p
import random
from config import *
from particle_system import *

#SIMPLE SPRITESHEET MANIPULATION CLASS.....................................................................
class spritesheet:
    def __init__(self,file):
        self.sheet = p.image.load(file)
        
    def get_sprite(self,x,y,width,height):
        sprite = p.Surface([width,height])
        sprite.blit(self.sheet,(0,0),(x,y,width,height))
        sprite.set_colorkey(BLACK)
        return(sprite)



class left_player(p.sprite.Sprite):
    def __init__(self,g):
        #MAIN GAME CLASS ATTRIBUTES.......................................................
        self.game = g
        self._layer = 2
        self.groups = self.game.all_sprites , self.game.players
        p.sprite.Sprite.__init__(self,self.groups)

        #OBJECT DIMENSIONS ATTRIBUTES.......................................................
        self.width = 20
        self.height = 100

        #OBJECT IMAGE ATTRIBUES.............................................................
        self.img_spritesheet = spritesheet("images/player.png")
        self.image = self.img_spritesheet.get_sprite(0,0,self.width,self.height)

        #OBJECT RECTANGLE AND POSITION ATTRIBUTES............................................
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = HEIGHT//2 - self.height//2

        #OBJECT GAMEPLAY ATTRIBUTES.........................................................
        self.speed = 0

    def update(self):
        #MAIN UPDATE FUNCTION (runs each frame in the main game loop)........................
        self.keys()
        self.mouvement()

    def keys(self):
        #GETTING KEYBOARD INPUTS..............................................................
        keys = p.key.get_pressed()
        if keys[p.K_z] and self.rect.y > 0:
            self.speed = -PLAYER_SPEED
        if keys[p.K_s] and self.rect.y < HEIGHT - self.height:
            self.speed = PLAYER_SPEED

    def mouvement(self):
        #MOVING THE PLAYER EACH FRAME............................................................
        self.rect.y += self.speed
        self.speed = 0

class right_player(left_player):
    def __init__(self,g):
        left_player.__init__(self,g)
        self.image = self.img_spritesheet.get_sprite(0,20,self.width,self.height)
        self.rect.x = WIDTH - self.width - 10

    def keys(self):
        keys = p.key.get_pressed()
        if keys[p.K_p] and self.rect.y > 0:
            self.speed = -PLAYER_SPEED
        if keys[p.K_m] and self.rect.y < HEIGHT - self.height:
            self.speed = PLAYER_SPEED


class ball(p.sprite.Sprite):
    def __init__(self,g):
        self.game = g
        self._layer = 2
        self.groups = self.game.all_sprites
        p.sprite.Sprite.__init__(self,self.groups)

        self.width = 20
        self.height = 20

        self.img_spritesheet = spritesheet("images/ball.png")
        self.image = self.img_spritesheet.get_sprite(0,0,self.width,self.height)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH//2 - self.width//2
        self.rect.y = HEIGHT //2 - self.height//2

        self.x_speed = 0
        self.y_speed = 0
        self.speed_add = 0.5

        self.is_launched = False

    def update(self):
        #MAIN UPDATE FUNCTION....................................................................
        self.keys()
        self.mouvement()
        self.collide()

        #SCORE CHANGEMENTS.......................................................................
        if self.rect.x <= -20:
            self.game.score["right_player"] +=1
            self.reset()
        elif self.rect.x >= WIDTH + 20:
            self.game.score["left_player"] +=1
            self.reset()


    def keys(self):
        keys = p.key.get_pressed()
        if keys[p.K_SPACE] and not self.is_launched:
            self.launch()

    def launch(self):
        self.is_launched = True
        self.game.playing = True

        #GIVING THE BALL A RANDOM LAUNCH DIRECTION.......................................................
        self.x_speed = random.choice([-1,1]) * BALL_SPEED
        self.y_speed = random.choice([-1,1]) * BALL_SPEED

    def collide(self):
        #DETECTING PLAYER COLLISION/ args = (Object, other_group, Do_Kill)................
        player_hits = p.sprite.spritecollide(self,self.game.players,False)
        if player_hits:
            self.x_speed = -self.x_speed     #INVERTING X_SPEED
            self.game.change_background()    #CHANGING BACKGROUND COLOR EACH PLAYER HIT

            #ADDING BALL SPEED EACH PLAYER HIT.............................................
            if self.x_speed <0:
                self.x_speed -=self.speed_add
            else:
                self.x_speed +=self.speed_add

            if self.y_speed <0:
                self.y_speed -=self.speed_add
            else:
                self.y_speed +=self.speed_add
        
        #DETECTING BORDER COLLISION..................................................................
        if self.rect.y <= 0 or self.rect.y >= HEIGHT - self.height:
            self.y_speed = -self.y_speed    #INVERTING Y_SPEED EACH BORDER HIT
            particle(self.game, self.rect.x - self.width//2, self.rect.y - self.height//2) #ADDING PARTICLES EACH BORDER HIT
    
    def mouvement(self):
        #MOVING THE BALL EACH FRAME...............................................................................
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

    def reset(self):
        #RESETTING BALL POSITION AND SPEED..........................................................................
        self.rect.x = WIDTH//2 - self.width//2
        self.rect.y = HEIGHT //2 - self.height//2
        self.x_speed = 0
        self.y_speed = 0
        self.is_launched = False
        self.game.playing = False

