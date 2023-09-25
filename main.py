import pygame as p
from sprites import *
from config import *
import sys


class game:
    def __init__(self):
        p.init()
        self.screen = p.display.set_mode((WIDTH,HEIGHT))
        p.display.set_caption("Pong Game")
        self.clock = p.time.Clock()
        self.running = True
        self.playing = False
        
    
    def new(self):

        #GAMEPLAY SPRITES HOLDERS..........................................................
        self.all_sprites = p.sprite.LayeredUpdates()
        self.players = p.sprite.LayeredUpdates()
        self.effects = []

        #GAMEPLAY ASSETS....................................................................
        self.ball = ball(self)
        self.l_player = left_player(self)        
        self.r_player = right_player(self)

        #POLISH ASSETS......................................................................
        self.score = {"left_player":0, "right_player":0}
        self.font = p.font.Font('Retro Gaming.ttf', 32)
        self.background_color = [50,50,50]
        
    
    def events(self):
        for event in p.event.get():
        #CLOSING THE GAME...................................................................
            if event.type == p.QUIT:
                self.running = False
                p.quit()
                sys.exit()

        
    def update(self):
        #UPDATING ALL SPRITES EACH FRAME.....................................................
        self.all_sprites.update()

    def draw_score(self):
        #RENDERING TEXT /args = (Text, Antialias(generally True), Color)......................
        l_player_score_text = self.font.render(str(self.score["left_player"]), True, WHITE)
        r_player_score_text = self.font.render(str(self.score["right_player"]), True, WHITE)

        #BLITTING THE RENDERED TEXT ON THE SCREEN /args = (rendered_text, coords)
        self.screen.blit(l_player_score_text,(WIDTH//2 - 50 , 20))
        self.screen.blit(r_player_score_text,(WIDTH//2 + 50 - 16, 20))

    def change_background(self):
        #CHANGING RGB VALUES OF THE BACKGROUND................................................
        self.background_color[0] += random.randint(-30,30)
        if self.background_color[0]> 255:
            self.background_color[0] = 255
        elif self.background_color[0]< 0:
            self.background_color[0] = 0

        self.background_color[1] += random.randint(-30,30)
        if self.background_color[1]> 255:
            self.background_color[1] = 255
        elif self.background_color[1]< 0:
            self.background_color[1] = 0

        self.background_color[2] += random.randint(-30,30)
        if self.background_color[2]> 255:
            self.background_color[2] = 255
        elif self.background_color[2]< 0:
            self.background_color[2] = 0


    def draw_starter_text(self):
        l_player_input_text = self.font.render("Z/S TO MOVE", True, WHITE)
        r_player_input_text = self.font.render("P/M TO MOVE", True, WHITE)
        ball_input_text = self.font.render("SPACE TO START", True, WHITE)

        self.screen.blit(l_player_input_text, (175//2,HEIGHT*3//4))
        self.screen.blit(r_player_input_text, (WIDTH - 325 ,HEIGHT*3//4))
        self.screen.blit(ball_input_text, (WIDTH//2 - 160 ,HEIGHT//4))

    def draw(self):
        #DRAWING ALL GAME ASSETS...............................................................
        self.screen.fill(self.background_color)
        self.all_sprites.draw(self.screen)

        for effect in self.effects:
            effect.update()
        
        self.draw_score()

        if not self.playing:
            self.draw_starter_text()

        self.clock.tick(FPS) 
        p.display.update()
        
    def main(self):
        #MAIN GAME LOOP.........................................................................
        while self.running:
            self.events()
            self.update()
            self.draw()
            
    
#MAIN PROGRAM....................................................................................
g = game()
g.new()

g.main()

p.quit()
sys.exit()