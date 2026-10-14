import pygame
from circleshape import CircleShape
from constants import PLAYER_BRAKE_POWER, PLAYER_LIVES, PLAYER_MAX_SPEED, PLAYER_RADIUS, LINE_WIDTH, PLAYER_SHOOT_COOLDOWN, PLAYER_SHOOT_SPEED, PLAYER_SPEED, PLAYER_THRUST, PLAYER_TURN_SPEED, SCREEN_HEIGHT, SCREEN_WIDTH
from shot import Shot


class Player(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0.0  # in degrees
        self.shot_cooldown = 0.0  # in seconds
        self.score = 0  # Initialize score to zero
        self.score_text = pygame.font.Font(None, 36)
        self.lives = PLAYER_LIVES  # Initialize lives to 3

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
        score_text = self.score_text.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_text = self.score_text.render(f"Lives: {self.lives}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))


    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_DOWN]:
            self.brake(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        self.shot_cooldown -= dt
        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)
        

    def move(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * dt * PLAYER_THRUST
        self.velocity = self.velocity.clamp_magnitude(PLAYER_MAX_SPEED)

    def brake(self, dt: float) -> None:
        self.velocity = self.velocity.move_towards(pygame.Vector2(0, 0), PLAYER_BRAKE_POWER * dt)

    def shoot(self) -> "Shot":
        if self.shot_cooldown > 0:
            return None
        else:
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN  # half a second cooldown
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = forward * PLAYER_SHOOT_SPEED
            return shot

    def add_score(self, points: int) -> None:
        self.score += points

    def get_score(self) -> int:
        return self.score
    def get_lives(self) -> int:
        return self.lives

    def reset(self) -> None:
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.rotation = 0.0
        self.shot_cooldown = 0.0
        self.lives -= 1