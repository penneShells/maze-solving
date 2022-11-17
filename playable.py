import pygame
from random import randint

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
class point(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(black)
        self.image.set_colorkey(black)
 
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        self.rect.y -= pixels
        if self.rect.y < 0:
          self.rect.y = 0
      
    def moveDown(self, pixels):
        self.rect.y += pixels
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

#same deal as the walls but with the objective
class goal(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(black)
        self.image.set_colorkey(black)
 
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()


#other variable declaration but i like having them closer to the while loop for reasons later down the line
#doesn't really make a difference but it's worth it for peace of mind
all_sprites_list = pygame.sprite.Group()

Point = point(white, 10, 10)
Goal = goal(yellow, 20, 20)

all_sprites_list.add(Point)
all_sprites_list.add(Goal)

walls = []
initxs = []
initys = []
finxs = []
finys = []

mainLoop = True

#game loop
while mainLoop == True:
    #spawn in maze walls without pressing a button
    while len(coords) != 0:
        blockFromCoords(coords[0], coords[1], coords[2], coords[3])
    

    #check for user inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False

        #gets inital coords of the nouse
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print(callable(wall))
            initx, inity = pos()
            initxs.append(initx)
            initys.append(inity)
            print(initx, inity)

        #gets final coords of the mouse
        elif event.type == pygame.MOUSEBUTTONUP:
            print(callable(wall))
            finx, finy = pos()
            finxs.append(finx)
            finys.append(finy)
            print(finx, finy)

        #registers keystrokes
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_x: 
                mainLoop=False
                
            #kills all walls, might only work for one now but i'll get around to it
            #if event.key==pygame.K_c:
            #    if len(walls)  != 0:
            #        pygame.sprite.Sprite.kill(Wall)
            #        walls.pop(0)
            #        update screen
            #        pygame.display.flip()

            #creates walls based on coords collected by mouse
            if event.key==pygame.K_o and callable(wall) != False:
                for x, initx in enumerate(initxs):
                    walls.append(wall(green, finxs[x] - initxs[x], finys[x] - initys[x]))
                    all_sprites_list.add(walls[x])
                    walls[x].rect.x = initxs[x]
                    walls[x].rect.y = initys[x]

            #creates walls based on coords array
            if event.key==pygame.K_m and callable(wall) != False:
                while len(coords) != 0:
                    blockFromCoords(coords[0], coords[1], coords[2], coords[3])

    #stops the goal from spawning inside of a wall
    for wall in walls:
        block(Point, wall)
        if pygame.sprite.collide_mask(wall, Goal):
            Goal.rect.x = randint(10, 689)
            Goal.rect.y = randint(10, 489)
    
    #user based movement           
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and Point.rect.y != 0:
        Point.moveUp(5)
    if keys[pygame.K_s]:
        Point.moveDown(5)
    if keys[pygame.K_a]:
        Point.moveLeft(5)
    if keys[pygame.K_d]:
        Point.moveRight(5)

    #goal point collision
    if pygame.sprite.collide_mask(Point, Goal):
        Goal.rect.x = randint(10, 689)
        Goal.rect.y = randint(10, 489)
        
    #draws sprites and makes screen black
    screen.fill(black)
    all_sprites_list.draw(screen)

    #update screen
    pygame.display.flip()

    #60 fps
    clock.tick(60)

pygame.quit()
