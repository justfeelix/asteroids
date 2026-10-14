
import pygame
from circleshape import CircleShape
from constants import LIFE_TIME


class Particle(CircleShape):
    def __init__(self, x: float, y: float, radius: float, lifetime: float=LIFE_TIME) -> None:
        super().__init__(x, y, radius)
        self.lifetime = lifetime

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "white", self.position, self.radius)
