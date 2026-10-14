import sys
import random

import pygame 
from constants import POINTS_PER_ASTEROID, SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from particle import Particle


def main():
    print(f"Starting Asteroids Game with Pygame version {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH} \n Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0.0
    running = True
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    particles = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (updatable, drawable, asteroids)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)
    Particle.containers = (updatable, drawable, particles)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    player1 = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    field = AsteroidField()

    while running:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((125, 125, 125))
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player1):
                log_event("player_hit")
                player1.reset()
                if player1.get_lives() <= 0:
                    print("Game over!")
                    print(f"Final score: {player1.get_score()}")
                    sys.exit()
                for a in asteroids:
                    a.kill()
                break

            for shot in shots:
                if asteroid.collides_with(shot):
                    for _ in range(10):
                        new_particle = Particle(asteroid.position.x, asteroid.position.y, 2)
                        new_particle.velocity = pygame.Vector2(0, 1).rotate(random.uniform(0, 360)) * random.uniform(50, 150)
                    log_event("asteroid_shot")
                    asteroide_type = asteroid.split()
                    player1.add_score(POINTS_PER_ASTEROID*asteroide_type.value)
                    shot.kill()
                    break
        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()
        dt = clock.tick(60) / 1000.0  # Convert milliseconds to seconds




if __name__ == "__main__":
    main()
