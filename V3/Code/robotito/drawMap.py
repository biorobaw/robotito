import sys
import pygame
import math
from pygame.locals import *

def main():
    (x,y) = (500,500)   
    deg = 0             
    pygame.init()       
    pygame.display.set_mode((x, y), 0, 32) 
    screen = pygame.display.get_surface()

    while (1):
        pygame.draw.rect(screen, (0, 200, 0), (0,0,int(x/2),int(y/2)))
        pygame.draw.line(screen, (0, 200, 0), (0, y/2), (x, int(y/2)))
        pygame.draw.line(screen, (0, 200, 0), (int(x/2), 0), (int(x/2), y))
        for i in range(1, 30):
            dx = x/2 + x/2 * math.cos(math.radians(deg-i))
            dy = y/2 + x/2 * math.sin(math.radians(deg-i))
            pygame.draw.aaline(screen, (0, 255/i, 0), (int(x/2), int(y/2)), (int(dx), int(dy)),5)

        pygame.display.update()     
        pygame.time.wait(30)        
        screen.fill((0, 20, 0, 0))  

        for event in pygame.event.get():
            if event.type == QUIT:      
                pygame.quit()           
                sys.exit()
if __name__ == "__main__":
        main()