import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_SHOOT_COOLDOWN, PLAYER_SHOOT_SPEED, PLAYER_SPEED, PLAYER_TURN_SPEED
from shot import Shot


class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0.0  # in degrees
        self.shot_cooldown = 0.0  # in seconds

    def triangle(self) -> list[pygame.Vector2]:

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius /1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius / 2 + right
        c = self.position - forward * self.radius / 2 - right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        points = self.triangle()
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_DOWN]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        self.shot_cooldown -= dt
        

    def move(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * dt * PLAYER_SPEED

    def shoot(self) -> "Shot":
        if self.shot_cooldown > 0:
            return None
        else:
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN  # half a second cooldown
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = forward * PLAYER_SHOOT_SPEED
            return shot