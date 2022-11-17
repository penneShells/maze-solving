# raycasting time
#spawning the rays is the easy part, i need to position them around the point accurately for proper vision

import pygame
from random import randint
import random
import os
import time
import neat
import visualize
import pickle


#read pygame docs about creating sprites as "subsprites" of one parent sprite, don't know if that would work but it sure sounds nice huh

pygame.init()

#just basic variable declaration so i wanted them seperate up here
#important ones

size = (700, 500)
screen = pygame.display.set_mode(size)

black = [0, 0, 0]
white = [255, 255, 255]
yellow = [255, 255, 0]
green = [0, 255, 0]

coords = [100, 0, 150, 200, 100, 300, 150, 500, 250, 0, 300, 400, 400, 100, 500, 500]

clock = pygame.time.Clock()

##walls = []
##Points = []
##greatlist = []
##all_sprites_list = pygame.sprite.Group()

#spawns in walls based on the list of coords
def blockFromCoords(inx, iny, finx, finy):
    walls.append(wall(green, finx - inx, finy - iny))
    all_sprites_list.add(walls[len(walls) - 1])
    walls[len(walls) - 1].rect.x = inx
    walls[len(walls) - 1].rect.y = iny
    coords.pop(3)
    coords.pop(2)
    coords.pop(1)
    coords.pop(0)

#gets the position of the mouse for drawing walls
def pos():
    screen.fill(black)
    x, y = pygame.mouse.get_pos()
    return x, y

#reuseable collision logic
def block(a, b):
    if pygame.sprite.collide_mask(a, b):
        if a.rect.x < b.rect.x and a.rect.y >= b.rect.y and a.rect.y < b.rect.y + b.rect.height:
            a.rect.x = b.rect.x - 10
            
        if a.rect.x >= b.rect.x + b.rect.width - 10 and a.rect.y >= b.rect.y and a.rect.y < b.rect.y + b.rect.height:
            a.rect.x = b.rect.x + b.rect.width
  
        if a.rect.y >= b.rect.y + b.rect.height - 10 and a.rect.x >= b.rect.x and a.rect.x < b.rect.x + b.rect.width:   
            a.rect.y = b.rect.y + b.rect.height
            
        if a.rect.y <= b.rect.y and a.rect.x >= b.rect.x and a.rect.x < b.rect.x + b.rect.width:
            a.rect.y = b.rect.y - 10
            
#creates the wall class just to save a little time instead of writing it out every time
class wall(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        
        self.image = pygame.Surface([width, height])
        self.image.fill(black)
        self.image.set_colorkey(black)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()
        
#"player" class with movement logic
class Point(pygame.sprite.Sprite):
    
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(black)
        self.image.set_colorkey(black)
 
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()


    def moveUp(self, pixels):
        self.rect.y -= pixels
        #Check that you are not going too far (off the screen)
        if self.rect.y < 0:
          self.rect.y = 0
      
    def moveDown(self, pixels):
        self.rect.y += pixels
        #Check that you are not going too far (off the screen)
        if self.rect.y > 490:
          self.rect.y = 490

    def moveRight(self, pixels):
        self.rect.x += pixels

        if self.rect.x > 690:
            self.rect.x = 690
            
    def moveLeft(self, pixels):
        self.rect.x -= pixels

        if self.rect.x < 0:
            self.rect.x = 0

class Ray(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(black)
        self.image.set_colorkey(black)
 
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()
    def position(self, x, y):
        self.rect.x = x + 4
        self.rect.y = y + 4
        


#same deal as the walls but with the objective
class Goal(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(black)
        self.image.set_colorkey(black)
 
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()


#other variable declaration but i like having them closer to the while loop for reasons later down the line
#doesn't really make a difference but it's worth it for peace of mind

def main(genomes, config):
    movin = []
    goals = []
    points = []
    ge = []
    nets = []
    counter = []
    greatlist = []
    all_sprites_list = pygame.sprite.Group()

    for genome_id, g in genomes:
        g.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        gratlist.append(pygame.sprite.Group())
        #points.append(Point(white, 10, 10))
        ge.append(g)
        
    # a lot of this is redundant but humour me
    for lesserlist in greatlist:
        lesserlist.append(Point(white, 10, 10))
        
        

    goal = Goal(yellow, 20, 20)
    goal.rect.x = 600
    goal.rect.y = 400
    all_sprites_list.add(goal)
        
        
        
    mainloop = True

    while mainloop == True:

        while len(coords) != 0:
            blockFromCoords(coords[0], coords[1], coords[2], coords[3])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x: #Pressing the x Key will quit the game
                         mainloop=False
                         #dont think this actually does anything but it looks
                         #nice huh
        for x, point in enumerate(points):
            
            if pygame.sprite.collide_mask(point, goal):
                print("COLLISION")
                ge[x].fitness += 10000

        for wall in walls:
            all_sprites_list.add(wall)
        

        #another for loop woo
        #checkin for if moving towards

        for x, point in enumerate(points):
            output = nets[x].activate((point.rect.x, point.rect.y, goal.rect.x, goal.rect.y))
            if output[0] > 0.5:
                ge[x].fitness += 0.5
                if point.rect.x > goal.rect.x:
              #      print(0)
                    point.moveLeft(8)              
            if output[1] > 0.5:
                ge[x].fitness += 0.5
                if point.rect.x < goal.rect.x:
                 #   print(1)
                    point.moveRight(8)
            if output[2] > 0.5:
                ge[x].fitness += 0.5
                if point.rect.y > goal.rect.y:
                   # print(2)
                    point.moveUp(8)        
            if output[3] > 0.5:    
                ge[x].fitness += 0.5
                if point.rect.y < goal.rect.y:
                   # print(3)
                    point.moveDown(8)
            else:
                ge[x].fitness -= 100

        for wall in walls:
            for point in points:
                block(point, wall)
            
        screen.fill(black)
        all_sprites_list.draw(screen)

        #update screen
        pygame.display.flip()

        #60 fps
        clock.tick(60)
        for lesserlist in greaterlist:
            lesserlist.update()

        
def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    p = neat.Population(config)
    #gives info about gen
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    winner = p.run(main, 50)
    
    with open("winner2.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close
   
    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)

    
