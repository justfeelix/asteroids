import pygame 
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state

def main():
    print(f"Starting Asteroids Game with Pygame version {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH} \n Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    while running:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((125, 125, 125))
        pygame.display.flip()
        clock.tick(60)




if __name__ == "__main__":
    main()
