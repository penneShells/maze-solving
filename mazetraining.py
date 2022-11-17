import pygame
from random import randint
import random
import os
import time
import neat
import visualize
import pickle

pygame.init()


size = (700, 500)
screen = pygame.display.set_mode(size)

black = [0, 0, 0]
white = [255, 255, 255]
yellow = [255, 255, 0]


clock = pygame.time.Clock()

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
            

class Goal(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(black)
        self.image.set_colorkey(black)
 
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()
    
def main(genomes, config):
    movin = []
    goals = []
    points = []
    ge = []
    nets = []
    counter = []
    all_sprites_list = pygame.sprite.Group()

    for genome_id, g in genomes:
        g.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        points.append(Point(white, 10, 10))
        ge.append(g)
    # a lot of this is redundant but humour me
    for point in points:
        all_sprites_list.add(point)
        count = 0
        counter.append(count)
        moving = 5
        movin.append(moving)
        goal = Goal(yellow, 20, 20)
        goals.append(goal)
        goal.rect.x = 400
        goal.rect.y = 200
        all_sprites_list.add(goal)
        
        
        
    mainloop = True

    while mainloop == True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mainloop = False
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_x: #Pressing the x Key will quit the game
                         mainloop=False
                         #dont think this actually does anything but it looks
                         #nice huh
        for x, point in enumerate(points):
            if pygame.sprite.collide_mask(point, goals[x]):
                print("COLLISION")
                ge[x].fitness += 10000
                goals[x].rect.x = randint(10, 689)
                goals[x].rect.y = randint(10, 489)
        

        #another for loop woo
        #checkin for if moving towards

        for x, point in enumerate(points):
            output = nets[x].activate((point.rect.x, point.rect.y, goals[x].rect.x, goals[x].rect.y))
            if output[0] > 0.5:
                ge[x].fitness += 0.5
                if point.rect.x > goals[x].rect.x:
              #      print(0)
                    point.moveLeft(8)              
            if output[1] > 0.5:
                ge[x].fitness += 0.5
                if point.rect.x < goals[x].rect.x:
                 #   print(1)
                    point.moveRight(8)
            if output[2] > 0.5:
                ge[x].fitness += 0.5
                if point.rect.y > goals[x].rect.y:
                   # print(2)
                    point.moveUp(8)        
            if output[3] > 0.5:    
                ge[x].fitness += 0.5
                if point.rect.y < goals[x].rect.y:
                   # print(3)
                    point.moveDown(8)
            else:
                ge[x].fitness -= 100
            
        screen.fill(black)
        all_sprites_list.draw(screen)

        #update screen
        pygame.display.flip()

        #60 fps
        clock.tick(60)
        all_sprites_list.update()

        
#loads in config file and such
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

    
