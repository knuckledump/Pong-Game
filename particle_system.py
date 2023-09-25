import pygame as p
import random 
from config import *
from pygame.locals import *

class particle:
    def __init__(self,g,x,y):
        
        self.game = g
        self.game.effects.append(self)
        
        self.width = 200
        self.height = 200
        self.image = p.Surface((self.width,self.height))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x - self.width//2
        self.rect.y = y - self.height//2

        self.particle_list = []
        self.color = (255,255,255)
        
        self.light_color = (80,20,10)
        self.life_time = 15
    
    def update(self):
        self.life_time -= 1
        if self.life_time <= 0:
            self.kill()
        
        particle = [[self.rect.x + self.width//2 ,self.rect.y + self.height//2] , [random.randint(-50,50)/3,random.randint(-50,50)/3] , random.randint(5,10)]
        self.particle_list.append(particle)
        for par in self.particle_list:
            par[0][0] += par[1][0]
            par[0][1] += par[1][1]
            par[2] -= 0.4
            if par[2] <=0:
                self.particle_list.remove(par)
        
            p.draw.circle(self.game.screen, self.color, [int(par[0][0]), int(par[0][1])], int(par[2]))
            radius = particle[2] * 1.5
            self.game.screen.blit(self.circle_surf(radius, self.light_color), (int(par[0][0] - radius), int(par[0][1] - radius)), special_flags=BLEND_RGB_ADD)
        
    def circle_surf(self,radius, color):
        
        surf = p.Surface((radius * 2, radius * 2))
        p.draw.circle(surf, color, (radius, radius), radius)
        surf.set_colorkey((0, 0, 0))
        return surf

    def kill(self):
        self.game.effects.remove(self)
