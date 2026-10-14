from circleshape import CircleShape
import pygame
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT
import logger
import random
import enum
import random

class AsteroidKind(enum.Enum):
    SMALL = 4
    MEDIUM = 2
    LARGE = 1


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.num_sides = random.randint(8, 12)
        self.offsets = []
        for _ in range(self.num_sides):
            #Loop through that number of edges. For each edge, calculate its angle. If you have 10 edges, they should be roughly 36 degrees apart (360 / 10)
            angle = 360 / self.num_sides * _
            #Then, For each angle, create a pygame.Vector2(0, 1). Rotate it by the angle.
            self.offsets.append(pygame.Vector2(0, 1).rotate(angle))
            # multiply that vector by a random number between 0.8 and 1.2, and multiply it by the radius of the asteroid. This will give you a point that is somewhere around the edge of the asteroid, but not exactly on the edge.
            self.offsets[-1] *= random.uniform(0.8, 1.2) * self.radius  

    def draw(self, screen: pygame.Surface) -> None:
        points = [self.position + offset for offset in self.offsets]
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)

    def split(self) -> None:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return AsteroidKind.SMALL
        elif self.radius <= ASTEROID_MIN_RADIUS * 2:
            logger.log_event("asteroid_split")
            angle = random.uniform(20,50)
            new_velocity1 = self.velocity.rotate(angle)
            new_velocity2 = self.velocity.rotate(-angle)
            new_radius = self.radius / 2
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = new_velocity1 * 1.2
            asteroid2.velocity = new_velocity2 * 1.2
            return AsteroidKind.MEDIUM
        else:
            logger.log_event("asteroid_split")
            angle = random.uniform(20,50)
            new_velocity1 = self.velocity.rotate(angle)
            new_velocity2 = self.velocity.rotate(-angle)
            new_radius = self.radius / 2
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = new_velocity1 * 1.2
            asteroid2.velocity = new_velocity2 * 1.2
            return AsteroidKind.LARGE
        