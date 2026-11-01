import math
import random
import sys
from dataclasses import dataclass

import pygame


WIDTH, HEIGHT = 960, 640
FPS = 60

BLACK = (8, 12, 22)
GREEN = (67, 226, 160)
DARK_GREEN = (18, 91, 75)
RED = (255, 92, 122)
DARK_RED = (130, 35, 72)
BROWN = (255, 184, 107)
DARK_BROWN = (105, 62, 60)
CYAN = (82, 213, 255)
VIOLET = (156, 118, 255)
PANEL = (16, 24, 39)
PANEL_LIGHT = (26, 37, 58)
WHITE = (238, 247, 255)
MUTED = (135, 155, 180)


def draw_glow(screen: pygame.Surface, color: tuple[int, int, int], center: tuple[int, int], radius: int, alpha: int = 70) -> None:
    glow = pygame.Surface((radius * 2 + 8, radius * 2 + 8), pygame.SRCALPHA)
    pygame.draw.circle(glow, (*color, alpha), (radius + 4, radius + 4), radius)
    screen.blit(glow, (center[0] - radius - 4, center[1] - radius - 4), special_flags=pygame.BLEND_PREMULTIPLIED)


def draw_field(screen: pygame.Surface, time_ms: int = 0) -> None:
    horizon_y = 105
    sway_time = time_ms / 1000.0
    frame_sway = math.sin(sway_time * 1.35) * 6
    gentle_sway = math.sin(sway_time * 0.9) * 4
    jungle_dark = (7, 31, 27)
    jungle_mid = (12, 58, 43)
    jungle_light = (28, 96, 65)

    screen.fill(jungle_dark)
    for y in range(horizon_y, HEIGHT):
        depth = (y - horizon_y) / (HEIGHT - horizon_y)
        color = (
            int(18 - depth * 6),
            int(58 + depth * 25),
            int(43 + depth * 12),
        )
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    # Explore-jungle expedition: ancient temple silhouettes beyond the canopy.
    light = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for x, width in ((330, 130), (520, 170), (710, 110)):
        pygame.draw.polygon(light, (255, 236, 158, 18), [(x, 90), (x + width, 90), (x + width + 150, HEIGHT), (x - 30, HEIGHT)])
    screen.blit(light, (0, 0))
    pygame.draw.rect(screen, (4, 24, 23), (0, 0, WIDTH, horizon_y))
    pygame.draw.ellipse(screen, (31, 104, 67), (345, 47, 270, 82))
    pygame.draw.ellipse(screen, (43, 126, 78), (395, 35, 170, 70))
    pygame.draw.polygon(screen, (77, 90, 65), [(390, 72), (480, 34), (570, 72), (570, 105), (390, 105)])
    pygame.draw.polygon(screen, (105, 108, 77), [(480, 27), (590, 73), (370, 73)])
    pygame.draw.rect(screen, (58, 71, 52), (405, 69, 150, 36))
    pygame.draw.rect(screen, (22, 48, 40), (446, 82, 68, 23))
    for x in (404, 428, 532, 556):
        pygame.draw.rect(screen, (121, 122, 85), (x, 66, 14, 39))
    pygame.draw.circle(screen, (190, 168, 91), (480, 82), 7)

    # Perspective paths and ground cracks give the clearing depth.
    vanishing_x = WIDTH // 2
    pygame.draw.polygon(screen, (42, 83, 59), [(340, horizon_y), (620, horizon_y), (720, HEIGHT), (240, HEIGHT)])
    pygame.draw.polygon(screen, (55, 104, 68), [(390, horizon_y), (570, horizon_y), (625, HEIGHT), (335, HEIGHT)])

    ground_lines = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for offset in range(-5, 6):
        bottom_x = vanishing_x + offset * 92
        pygame.draw.line(ground_lines, (91, 145, 100, 52), (vanishing_x + offset * 18, horizon_y), (bottom_x, HEIGHT), 1)
    for y in (150, 205, 275, 360, 470, 570):
        half_width = int((y - horizon_y) * 1.05)
        pygame.draw.line(ground_lines, (91, 145, 100, 45), (vanishing_x - half_width, y), (vanishing_x + half_width, y), 1)
    screen.blit(ground_lines, (0, 0))

    # Massive trees frame the battlefield and recede toward the horizon.
    for index, (x, trunk_width, top_y) in enumerate(((42, 48, 58), (918, 52, 42))):
        tree_sway = frame_sway * (1 if index == 0 else -1)
        canopy_x = x + tree_sway
        pygame.draw.polygon(screen, (43, 31, 28), [(x - trunk_width + tree_sway * 0.15, top_y), (x + trunk_width + tree_sway * 0.15, top_y), (x + trunk_width // 2, HEIGHT), (x - trunk_width // 2, HEIGHT)])
        pygame.draw.line(screen, (77, 58, 42), (x + tree_sway * 0.15, top_y + 20), (x, HEIGHT), 8)
        pygame.draw.ellipse(screen, jungle_dark, (canopy_x - 76, top_y - 46 + int(abs(tree_sway)), 152, 95))
        pygame.draw.ellipse(screen, jungle_light, (canopy_x - 52, top_y - 52 - int(abs(tree_sway) * 0.4), 105, 88))

    # Mid-ground trunks sway slightly more slowly than the foreground trees.
    for index, (x, height, width) in enumerate(((155, 205, 22), (805, 225, 24), (270, 150, 15), (690, 160, 16))):
        trunk_sway = gentle_sway * (1 if index % 2 == 0 else -1)
        top_x = x + trunk_sway
        pygame.draw.polygon(screen, (51, 39, 31), [(x - width, horizon_y + height - 75), (x + width, horizon_y + height - 75), (top_x + width // 2, horizon_y + height), (top_x - width // 2, horizon_y + height)])
        pygame.draw.ellipse(screen, (13, 72, 48), (top_x - width - 18, horizon_y + height - 105 + int(abs(trunk_sway) * 0.5), width * 4 + 36, 46))

    # Hanging vines and foreground leaves add depth around the arena.
    vines = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for index, (x, length) in enumerate(((100, 145), (860, 170), (190, 105), (770, 120))):
        vine_sway = math.sin(sway_time * 1.8 + index) * 8
        pygame.draw.line(vines, (26, 91, 52, 220), (x, 0), (x + 12 + vine_sway, length), 3)
        for y in range(35, length, 28):
            leaf_x = x + (0 if y % 56 == 35 else 8) + vine_sway * (y / length)
            pygame.draw.ellipse(vines, (43, 128, 70, 230), (leaf_x, y, 18, 8))
    screen.blit(vines, (0, 0))

    fern_positions = ((25, 590), (95, 625), (865, 625), (935, 570), (180, 540), (780, 540))
    for fx, fy in fern_positions:
        direction = -1 if fx < WIDTH / 2 else 1
        for angle in range(-5, 6):
            end_x = fx + direction * (18 + abs(angle) * 7)
            end_y = fy - 15 - (6 - abs(angle)) * 5
            pygame.draw.line(screen, (20, 82, 48), (fx, fy), (end_x, end_y), 5)
            pygame.draw.ellipse(screen, jungle_light, (end_x - 8 * direction, end_y - 5, 16, 9))

    # Explorer camp markers frame the battlefield.
    for x, y, direction in ((115, 530, 1), (845, 530, -1)):
        pygame.draw.line(screen, (91, 56, 35), (x, y + 5), (x, y - 62), 8)
        pygame.draw.polygon(screen, (231, 191, 92), [(x + direction * 4, y - 58), (x + direction * 46, y - 50), (x + direction * 4, y - 33)])
        pygame.draw.line(screen, (93, 61, 38), (x + direction * 40, y + 15), (x + direction * 40, y + 49), 7)
        flame_y = y + 15
        pygame.draw.polygon(screen, (255, 177, 67), [(x + direction * 40, flame_y), (x + direction * 33, flame_y + 18), (x + direction * 47, flame_y + 18)])
        pygame.draw.circle(screen, (255, 220, 116), (x + direction * 40, flame_y + 5), 5)

    # Exploration compass ring for the player's perimeter.
    pygame.draw.circle(screen, (220, 200, 126), (WIDTH // 2, 390), 170, 1)
    pygame.draw.circle(screen, (82, 213, 255), (WIDTH // 2, 390), 280, 1)

    # Naturalistic, animated wildlife silhouettes in the jungle scenery.
    wildlife_time = time_ms / 1000.0
    bird_x = int(120 + ((wildlife_time * 35) % (WIDTH - 240)))
    bird_y = 145 + int(math.sin(wildlife_time * 2.2) * 12)
    wing_lift = int(math.sin(wildlife_time * 5.0) * 8)
    pygame.draw.ellipse(screen, (35, 42, 43), (bird_x - 7, bird_y - 4, 14, 8))
    pygame.draw.polygon(screen, (42, 50, 51), [(bird_x - 4, bird_y), (bird_x - 23, bird_y - 10 + wing_lift), (bird_x - 17, bird_y + 4)])
    pygame.draw.polygon(screen, (42, 50, 51), [(bird_x + 4, bird_y), (bird_x + 23, bird_y - 10 - wing_lift), (bird_x + 17, bird_y + 4)])
    pygame.draw.polygon(screen, (44, 47, 45), [(bird_x + 6, bird_y - 1), (bird_x + 14, bird_y + 1), (bird_x + 6, bird_y + 2)])

    monkey_x = 710 + int(math.sin(wildlife_time * 1.3) * 22)
    monkey_y = 205 + int(math.cos(wildlife_time * 1.3) * 8)
    pygame.draw.line(screen, (53, 34, 27), (monkey_x - 7, monkey_y + 3), (monkey_x - 18, monkey_y + 15 + int(math.sin(wildlife_time * 2) * 3)), 5)
    pygame.draw.line(screen, (53, 34, 27), (monkey_x + 7, monkey_y + 3), (monkey_x + 18, monkey_y + 15 - int(math.sin(wildlife_time * 2) * 3)), 5)
    pygame.draw.ellipse(screen, (79, 49, 34), (monkey_x - 10, monkey_y - 2, 20, 18))
    pygame.draw.circle(screen, (108, 68, 43), (monkey_x, monkey_y - 8), 9)
    pygame.draw.circle(screen, (143, 108, 73), (monkey_x, monkey_y - 6), 5)
    pygame.draw.circle(screen, (79, 49, 34), (monkey_x - 9, monkey_y - 8), 4)
    pygame.draw.circle(screen, (79, 49, 34), (monkey_x + 9, monkey_y - 8), 4)
    pygame.draw.arc(screen, (62, 39, 30), (monkey_x - 5, monkey_y - 7, 10, 10), 0.3, math.pi - 0.3, 1)

    frog_x = 255 + int(math.sin(wildlife_time * 0.8) * 18)
    frog_y = 535 + int(abs(math.sin(wildlife_time * 2)) * 3)
    pygame.draw.ellipse(screen, (48, 104, 52), (frog_x - 13, frog_y - 4, 26, 14))
    pygame.draw.ellipse(screen, (69, 132, 67), (frog_x - 9, frog_y - 9, 18, 12))
    pygame.draw.circle(screen, (75, 145, 72), (frog_x - 7, frog_y - 11), 5)
    pygame.draw.circle(screen, (75, 145, 72), (frog_x + 7, frog_y - 11), 5)
    pygame.draw.circle(screen, (222, 226, 180), (frog_x - 7, frog_y - 11), 2)
    pygame.draw.circle(screen, (222, 226, 180), (frog_x + 7, frog_y - 11), 2)
    pygame.draw.circle(screen, (20, 32, 26), (frog_x - 7, frog_y - 11), 1)
    pygame.draw.circle(screen, (20, 32, 26), (frog_x + 7, frog_y - 11), 1)

    snake_x = 700 + int(math.sin(wildlife_time * 1.1) * 25)
    snake_curve = int(math.sin(wildlife_time * 2.2) * 3)
    pygame.draw.arc(screen, (30, 87, 49), (snake_x - 21, 500 + snake_curve, 42, 17), 0.1, math.pi * 1.75, 5)
    pygame.draw.arc(screen, (86, 139, 60), (snake_x - 13, 502 + snake_curve, 28, 12), 0.1, math.pi * 1.75, 2)
    pygame.draw.ellipse(screen, (30, 87, 49), (snake_x + 13, 497 + snake_curve, 11, 7))
    pygame.draw.circle(screen, (210, 205, 115), (snake_x + 20, 499 + snake_curve), 1)
    pygame.draw.circle(screen, (210, 205, 115), (snake_x + 21, 502 + snake_curve), 1)


@dataclass
class Bullet:
    x: float
    y: float
    vx: float
    vy: float
    radius: int = 5

    def update(self) -> None:
        self.x += self.vx
        self.y += self.vy

    def draw(self, screen: pygame.Surface) -> None:
        x, y = int(self.x), int(self.y)
        draw_glow(screen, RED, (x, y), 14, 55)
        pygame.draw.circle(screen, WHITE, (x, y), self.radius, 2)
        pygame.draw.circle(screen, RED, (x, y), max(2, self.radius - 5))
        pygame.draw.circle(screen, (255, 220, 230), (x - 2, y - 2), 2)


@dataclass
class PowerStar:
    x: float
    y: float
    radius: int = 18

    def draw(self, screen: pygame.Surface, time_ms: int) -> None:
        cx, cy = int(self.x), int(self.y)
        pulse = math.sin(time_ms / 180.0) * 3
        draw_glow(screen, (255, 224, 102), (cx, cy), 28, 55)
        points = []
        for index in range(10):
            angle = -math.pi / 2 + index * math.pi / 5
            radius = 16 + pulse if index % 2 == 0 else 7 + pulse * 0.4
            points.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))
        pygame.draw.polygon(screen, (255, 215, 74), points)
        pygame.draw.polygon(screen, (255, 246, 170), points, 2)


@dataclass
class Enemy:
    x: float
    y: float
    speed: float
    phase: float
    radius: int = 22
    kind: str = "red"
    hits: int = 0
    hp: int = 1

    def update(self, target_x: float, target_y: float) -> None:
        angle = math.atan2(target_y - self.y, target_x - self.x)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed
        self.phase += 0.12

    def hit(self) -> bool:
        if self.kind == "blue":
            self.hp -= 1
            return self.hp <= 0
        if self.kind != "green":
            return True
        self.hits += 1
        self.speed += 0.35
        return self.hits >= 3

    def draw(self, screen: pygame.Surface) -> None:
        bob = math.sin(self.phase) * 3
        cx, cy = int(self.x), int(self.y + bob)
        if self.kind == "green":
            draw_glow(screen, GREEN, (cx, cy), 29, 38)
            pygame.draw.circle(screen, (12, 58, 50), (cx, cy), 22)
            pygame.draw.circle(screen, DARK_GREEN, (cx, cy), 19)
            eye_color = GREEN
        elif self.kind == "blue":
            draw_glow(screen, CYAN, (cx, cy), 32, 45)
            pygame.draw.circle(screen, (18, 55, 92), (cx, cy), 23)
            pygame.draw.circle(screen, (28, 96, 150), (cx, cy), 20)
            eye_color = CYAN
        else:
            draw_glow(screen, RED, (cx, cy), 29, 38)
            pygame.draw.circle(screen, (66, 18, 44), (cx, cy), 22)
            pygame.draw.circle(screen, DARK_RED, (cx, cy), 19)
            eye_color = RED
        pygame.draw.circle(screen, eye_color, (cx - 7, cy - 5), 4)
        pygame.draw.circle(screen, eye_color, (cx + 7, cy - 5), 4)
        pygame.draw.circle(screen, WHITE, (cx - 6, cy - 6), 1)
        pygame.draw.circle(screen, WHITE, (cx + 8, cy - 6), 1)
        pygame.draw.arc(screen, eye_color, (cx - 9, cy - 4, 18, 12), math.pi * 0.15, math.pi * 0.85, 2)
        swing = math.sin(self.phase * 0.9) * 4
        pygame.draw.line(screen, eye_color, (cx - 14, cy + 2), (cx - 25, cy + 13 + swing), 6)
        pygame.draw.line(screen, eye_color, (cx + 14, cy + 2), (cx + 25, cy + 13 - swing), 6)
        if self.kind == "blue":
            bar_width = 46
            pygame.draw.rect(screen, (10, 20, 35), (cx - bar_width // 2, cy - 31, bar_width, 5), border_radius=2)
            pygame.draw.rect(screen, CYAN, (cx - bar_width // 2, cy - 31, int(bar_width * self.hp / 25), 5), border_radius=2)
            hp_font = pygame.font.Font(None, 18)
            hp_text = hp_font.render(str(self.hp), True, WHITE)
            screen.blit(hp_text, hp_text.get_rect(center=(cx, cy - 39)))


@dataclass
class ExperienceOrb:
    x: float
    y: float
    phase: float = 0.0

    def update(self, target_x: float, target_y: float) -> None:
        self.phase += 0.12
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.hypot(dx, dy)
        if distance and distance < 170:
            speed = min(9, 2 + (170 - distance) / 18)
            self.x += dx / distance * speed
            self.y += dy / distance * speed

    def draw(self, screen: pygame.Surface) -> None:
        bob_y = math.sin(self.phase) * 3
        draw_glow(screen, BROWN, (int(self.x), int(self.y + bob_y)), 14, 55)
        pygame.draw.circle(screen, BROWN, (int(self.x), int(self.y + bob_y)), 7)
        pygame.draw.circle(screen, WHITE, (int(self.x - 2), int(self.y + bob_y - 2)), 2)


class Giant:
    def __init__(self) -> None:
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.speed = 5
        self.angle = 0.0
        self.four_guns = False
        self.four_gun_timer = 0

    def move(self, keys: pygame.key.ScancodeWrapper) -> None:
        dx = int(keys[pygame.K_d] or keys[pygame.K_RIGHT]) - int(keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = int(keys[pygame.K_s] or keys[pygame.K_DOWN]) - int(keys[pygame.K_w] or keys[pygame.K_UP])
        length = math.hypot(dx, dy)
        if length:
            self.x += dx / length * self.speed
            self.y += dy / length * self.speed
        self.x = max(70, min(WIDTH - 70, self.x))
        self.y = max(125, min(HEIGHT - 80, self.y))

    def aim_at(self, position: tuple[int, int]) -> None:
        self.angle = math.atan2(position[1] - self.y, position[0] - self.x)

    def shoot(self) -> Bullet:
        return Bullet(
            self.x + math.cos(self.angle) * 48,
            self.y + math.sin(self.angle) * 48,
            math.cos(self.angle) * 12,
            math.sin(self.angle) * 12,
        )

    def shoot_all(self) -> list[Bullet]:
        angles = (-0.24, -0.08, 0.08, 0.24) if getattr(self, "four_guns", False) else (0.0,)
        bullets = []
        for offset in angles:
            angle = self.angle + offset
            bullets.append(Bullet(
                self.x + math.cos(angle) * 48,
                self.y + math.sin(angle) * 48,
                math.cos(angle) * 12,
                math.sin(angle) * 12,
            ))
        return bullets

    def collides_with(self, enemy: Enemy) -> bool:
        nearest_x = max(self.x - 66, min(enemy.x, self.x + 66))
        nearest_y = max(self.y - 70, min(enemy.y, self.y + 92))
        return math.hypot(enemy.x - nearest_x, enemy.y - nearest_y) < enemy.radius

    def draw(self, screen: pygame.Surface) -> None:
        cx, cy = int(self.x), int(self.y)
        draw_glow(screen, GREEN, (cx, cy), 82, 28)
        pygame.draw.circle(screen, (9, 32, 42), (cx, cy - 48), 27)
        pygame.draw.circle(screen, BROWN, (cx, cy - 48), 23)
        pygame.draw.arc(screen, DARK_BROWN, (cx - 19, cy - 66, 38, 38), 3.35, 6.05, 4)
        pygame.draw.circle(screen, (35, 18, 25), (cx - 8, cy - 52), 3)
        pygame.draw.circle(screen, (35, 18, 25), (cx + 8, cy - 52), 3)
        pygame.draw.rect(screen, (7, 44, 48), (cx - 30, cy - 25, 60, 70), border_radius=18)
        pygame.draw.rect(screen, DARK_GREEN, (cx - 27, cy - 22, 54, 64), border_radius=16)
        pygame.draw.line(screen, GREEN, (cx - 22, cy - 8), (cx - 66, cy + 26), 16)
        pygame.draw.line(screen, CYAN, (cx + 22, cy - 8), (cx + 66, cy + 26), 16)
        pygame.draw.line(screen, DARK_GREEN, (cx - 17, cy + 39), (cx - 33, cy + 92), 20)
        pygame.draw.line(screen, GREEN, (cx + 17, cy + 39), (cx + 33, cy + 92), 20)
        gun_end = (cx + int(math.cos(self.angle) * 78), cy + int(math.sin(self.angle) * 78))
        pygame.draw.line(screen, (20, 31, 46), (cx, cy), gun_end, 15)
        pygame.draw.line(screen, CYAN, (cx, cy), gun_end, 7)
        pygame.draw.circle(screen, WHITE, gun_end, 7)
        pygame.draw.circle(screen, CYAN, gun_end, 4)
        if self.four_guns:
            seconds_left = max(1, math.ceil(self.four_gun_timer / FPS))
            timer_text = pygame.font.Font(None, 24).render(f"4 GUNS  {seconds_left}s", True, (255, 224, 102))
            screen.blit(timer_text, timer_text.get_rect(center=(cx, cy - 105)))


def spawn_enemy() -> Enemy:
    side = random.randrange(4)
    if side == 0:
        x, y = random.randint(-30, WIDTH + 30), -40
    elif side == 1:
        x, y = WIDTH + 40, random.randint(100, HEIGHT)
    elif side == 2:
        x, y = random.randint(-30, WIDTH + 30), HEIGHT + 40
    else:
        x, y = -40, random.randint(100, HEIGHT)
    roll = random.random()
    if roll < 0.15:
        kind, hp, speed_range = "blue", 25, (0.55, 1.05)
    elif roll < 0.40:
        kind, hp, speed_range = "green", 3, (0.65, 1.15)
    else:
        kind, hp, speed_range = "red", 1, (0.8, 1.45)
    speed = random.uniform(*speed_range)
    return Enemy(x, y, speed, random.random() * math.tau, kind=kind, hp=hp)


def draw_ui(screen: pygame.Surface, font: pygame.font.Font, score: int, wave: int, xp: int) -> None:
    header = pygame.Rect(16, 14, WIDTH - 32, 72)
    pygame.draw.rect(screen, PANEL, header, border_radius=16)
    pygame.draw.rect(screen, PANEL_LIGHT, header, width=1, border_radius=16)

    accent = pygame.Rect(16, 14, 5, 72)
    pygame.draw.rect(screen, GREEN, accent, border_radius=16)
    title_font = pygame.font.Font(None, 34)
    title = title_font.render("GIANT MAN  //  LAST STAND", True, WHITE)
    screen.blit(title, (36, 25))
    controls = font.render("WASD  MOVE    •    MOUSE  AIM    •    CLICK / SPACE  FIRE", True, MUTED)
    screen.blit(controls, (38, 58))

    xp_panel = pygame.Rect(WIDTH - 406, 21, 120, 58)
    score_panel = pygame.Rect(WIDTH - 276, 21, 120, 58)
    wave_panel = pygame.Rect(WIDTH - 146, 21, 114, 58)
    for panel, color in ((xp_panel, BROWN), (score_panel, CYAN), (wave_panel, VIOLET)):
        pygame.draw.rect(screen, (9, 15, 28), panel, border_radius=12)
        pygame.draw.rect(screen, (*color, 180), panel, width=1, border_radius=12)
    xp_value = title_font.render(f"{xp:03d}", True, BROWN)
    score_value = title_font.render(f"{score:03d}", True, CYAN)
    wave_value = title_font.render(f"{wave:02d}", True, VIOLET)
    screen.blit(xp_value, xp_value.get_rect(center=(xp_panel.centerx, xp_panel.top + 20)))
    screen.blit(score_value, score_value.get_rect(center=(score_panel.centerx, score_panel.top + 20)))
    screen.blit(wave_value, wave_value.get_rect(center=(wave_panel.centerx, wave_panel.top + 20)))
    xp_label = pygame.font.Font(None, 18).render("XP", True, MUTED)
    score_label = pygame.font.Font(None, 18).render("ELIMINATED", True, MUTED)
    wave_label = pygame.font.Font(None, 18).render("WAVE", True, MUTED)
    screen.blit(xp_label, xp_label.get_rect(center=(xp_panel.centerx, xp_panel.bottom - 13)))
    screen.blit(score_label, score_label.get_rect(center=(score_panel.centerx, score_panel.bottom - 13)))
    screen.blit(wave_label, wave_label.get_rect(center=(wave_panel.centerx, wave_panel.bottom - 13)))

    status = pygame.Rect(16, HEIGHT - 45, 190, 29)
    pygame.draw.rect(screen, PANEL, status, border_radius=14)
    pygame.draw.circle(screen, RED, (status.left + 16, status.centery), 5)
    status_text = pygame.font.Font(None, 20).render("PERIMETER CRITICAL", True, WHITE)
    screen.blit(status_text, (status.left + 28, status.top + 7))


def draw_menu(screen: pygame.Surface, menu_font: pygame.font.Font, buttons: tuple[pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect]) -> None:
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((3, 8, 16, 205))
    screen.blit(overlay, (0, 0))

    panel = pygame.Rect(WIDTH // 2 - 190, HEIGHT // 2 - 205, 380, 410)
    pygame.draw.rect(screen, PANEL, panel, border_radius=24)
    pygame.draw.rect(screen, PANEL_LIGHT, panel, width=2, border_radius=24)

    title = pygame.font.Font(None, 52).render("GAME MENU", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, panel.top + 52)))

    labels = ("RESUME", "MINIMIZE", "FULLSCREEN", "CLICKER WORLD")
    for button, label in zip(buttons, labels):
        pygame.draw.rect(screen, PANEL_LIGHT, button, border_radius=12)
        pygame.draw.rect(screen, CYAN, button, width=1, border_radius=12)
        text = menu_font.render(label, True, WHITE)
        screen.blit(text, text.get_rect(center=button.center))

    hint = pygame.font.Font(None, 20).render("Press ESC to close", True, MUTED)
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, panel.bottom - 28)))


def draw_clicker_world(screen: pygame.Surface, font: pygame.font.Font, click_button: pygame.Rect, transport_button: pygame.Rect, clicks: int, xp: int) -> None:
    screen.fill((8, 18, 28))

    glow = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    for x, y, radius, color in ((180, 180, 150, GREEN), (780, 190, 130, CYAN), (480, 520, 180, VIOLET)):
        pygame.draw.circle(glow, (*color, 24), (x, y), radius)
    screen.blit(glow, (0, 0))

    title = pygame.font.Font(None, 64).render("CLICKER WORLD", True, WHITE)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 58)))

    score_text = pygame.font.Font(None, 42).render(f"Clicks: {clicks}", True, CYAN)
    screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, 125)))

    pygame.draw.circle(screen, PANEL_LIGHT, click_button.center, click_button.width // 2 + 18)
    pygame.draw.circle(screen, CYAN, click_button.center, click_button.width // 2 + 18, 4)
    pygame.draw.circle(screen, GREEN, click_button.center, click_button.width // 2)
    pygame.draw.circle(screen, WHITE, click_button.center, click_button.width // 2, 6)
    button_text = pygame.font.Font(None, 38).render("CLICK!", True, BLACK)
    screen.blit(button_text, button_text.get_rect(center=click_button.center))

    pygame.draw.rect(screen, PANEL_LIGHT, transport_button, border_radius=14)
    pygame.draw.rect(screen, BROWN, transport_button, width=2, border_radius=14)
    transport_text = pygame.font.Font(None, 28).render(f"TRANSPORT CLICKS TO XP  (1:1)", True, WHITE)
    screen.blit(transport_text, transport_text.get_rect(center=transport_button.center))

    xp_text = font.render(f"Game XP: {xp}", True, BROWN)
    screen.blit(xp_text, xp_text.get_rect(center=(WIDTH // 2, transport_button.bottom + 20)))

    hint = font.render("ESC  RETURN TO GAME", True, MUTED)
    screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT - 14)))


def main() -> None:
    pygame.init()
    fullscreen = False
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Giant Man: Last Stand - F11 Fullscreen")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    giant = Giant()
    bullets: list[Bullet] = []
    enemies: list[Enemy] = []
    stars: list[PowerStar] = []
    xp_orbs: list[ExperienceOrb] = []
    score = 0
    xp = 0
    spawn_timer = 0
    star_spawn_timer = FPS * 10
    fire_cooldown = 0
    game_over = False
    menu_open = False
    clicker_world = False
    clicker_clicks = 0
    running = True
    replay_button = pygame.Rect(WIDTH // 2 - 110, HEIGHT // 2 + 75, 220, 48)
    click_button = pygame.Rect(WIDTH // 2 - 105, HEIGHT // 2 - 65, 210, 210)
    transport_button = pygame.Rect(WIDTH // 2 - 175, HEIGHT - 115, 350, 54)
    replay_font = pygame.font.Font(None, 32)
    menu_font = pygame.font.Font(None, 30)
    menu_buttons = (
        pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 - 125, 240, 54),
        pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 - 55, 240, 54),
        pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 15, 240, 54),
        pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 85, 240, 54),
    )

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key in (pygame.K_F11, pygame.K_RETURN) and (event.key == pygame.K_F11 or event.mod & pygame.KMOD_ALT):
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
            elif event.type == pygame.MOUSEMOTION:
                giant.aim_at(event.pos)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not game_over:
                if clicker_world:
                    clicker_world = False
                else:
                    menu_open = not menu_open
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if clicker_world:
                    if click_button.collidepoint(event.pos):
                        clicker_clicks += 1
                    elif transport_button.collidepoint(event.pos) and clicker_clicks > 0:
                        xp += clicker_clicks
                        clicker_clicks = 0
                elif menu_open:
                    if menu_buttons[0].collidepoint(event.pos):
                        menu_open = False
                    elif menu_buttons[1].collidepoint(event.pos):
                        pygame.display.iconify()
                    elif menu_buttons[2].collidepoint(event.pos):
                        fullscreen = not fullscreen
                        if fullscreen:
                            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
                        else:
                            screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    elif menu_buttons[3].collidepoint(event.pos):
                        clicker_world = True
                        menu_open = False
                elif game_over and replay_button.collidepoint(event.pos):
                    giant = Giant()
                    bullets.clear()
                    enemies.clear()
                    stars.clear()
                    xp_orbs.clear()
                    giant.four_guns = False
                    giant.four_gun_timer = 0
                    score = 0
                    xp = 0
                    spawn_timer = 0
                    star_spawn_timer = FPS * 10
                    fire_cooldown = 0
                    game_over = False
                elif not game_over and not menu_open and fire_cooldown <= 0:
                    bullets.extend(giant.shoot_all())
                    fire_cooldown = 8
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if not game_over and not menu_open and not clicker_world and fire_cooldown <= 0:
                    bullets.extend(giant.shoot_all())
                    fire_cooldown = 8

        if not game_over and not menu_open and not clicker_world:
            keys = pygame.key.get_pressed()
            giant.move(keys)
            if pygame.mouse.get_focused():
                giant.aim_at(pygame.mouse.get_pos())
            if keys[pygame.K_SPACE] and not clicker_world and fire_cooldown <= 0:
                bullets.extend(giant.shoot_all())
                fire_cooldown = 8
            fire_cooldown = max(0, fire_cooldown - 1)

            spawn_timer -= 1
            wave = score // 10 + 1
            if spawn_timer <= 0:
                enemies.append(spawn_enemy())
                spawn_timer = max(18, 58 - wave * 3)

            star_spawn_timer -= 1
            if star_spawn_timer <= 0:
                stars.append(PowerStar(
                    random.randint(100, WIDTH - 100),
                    random.randint(150, HEIGHT - 90),
                ))
                star_spawn_timer = FPS * 10

            collected_stars = []
            for star in stars:
                if math.hypot(giant.x - star.x, giant.y - star.y) < 55:
                    giant.four_guns = True
                    giant.four_gun_timer = FPS * 5
                    collected_stars.append(star)
            stars = [star for star in stars if star not in collected_stars]

            if giant.four_guns:
                giant.four_gun_timer -= 1
                if giant.four_gun_timer <= 0:
                    giant.four_gun_timer = 0
                    giant.four_guns = False

            for orb in xp_orbs:
                orb.update(giant.x, giant.y)
            collected_orbs = []
            for orb in xp_orbs:
                if math.hypot(giant.x - orb.x, giant.y - orb.y) < 28:
                    xp += 1
                    collected_orbs.append(orb)
            xp_orbs = [orb for orb in xp_orbs if orb not in collected_orbs]

            for bullet in bullets:
                bullet.update()
            bullets = [bullet for bullet in bullets if -20 < bullet.x < WIDTH + 20 and -20 < bullet.y < HEIGHT + 20]

            for enemy in enemies:
                enemy.update(giant.x, giant.y)
                if giant.collides_with(enemy):
                    game_over = True

            surviving_bullets: list[Bullet] = []
            for bullet in bullets:
                hit = False
                for enemy in enemies[:]:
                    if math.hypot(bullet.x - enemy.x, bullet.y - enemy.y) < enemy.radius + bullet.radius:
                        if enemy.hit():
                            enemies.remove(enemy)
                            score += 1
                            xp_orbs.append(ExperienceOrb(enemy.x, enemy.y, random.random() * math.tau))
                        hit = True
                        break
                if not hit:
                    surviving_bullets.append(bullet)
            bullets = surviving_bullets

        if clicker_world:
            draw_clicker_world(screen, font, click_button, transport_button, clicker_clicks, xp)
            pygame.display.flip()
            continue

        draw_field(screen, pygame.time.get_ticks())
        wave = score // 10 + 1
        draw_ui(screen, font, score, wave, xp)
        pygame.draw.circle(screen, (82, 213, 255, 80), (int(giant.x), int(giant.y)), 125, 2)
        pygame.draw.circle(screen, (82, 213, 255, 45), (int(giant.x), int(giant.y)), 112, 1)
        for bullet in bullets:
            bullet.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for star in stars:
            star.draw(screen, pygame.time.get_ticks())
        for orb in xp_orbs:
            orb.draw(screen)
        giant.draw(screen)
        if menu_open:
            draw_menu(screen, menu_font, menu_buttons)
        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((3, 6, 14, 205))
            screen.blit(overlay, (0, 0))
            modal = pygame.Rect(WIDTH // 2 - 250, HEIGHT // 2 - 145, 500, 260)
            pygame.draw.rect(screen, PANEL, modal, border_radius=24)
            pygame.draw.rect(screen, PANEL_LIGHT, modal, width=2, border_radius=24)
            pygame.draw.line(screen, RED, (modal.left + 35, modal.top + 13), (modal.right - 35, modal.top + 13), 3)
            message = pygame.font.Font(None, 72).render("SIGNAL LOST", True, WHITE)
            prompt = pygame.font.Font(None, 24).render("The perimeter has been breached", True, MUTED)
            screen.blit(message, message.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 52)))
            screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 5)))
            replay_button.y = HEIGHT // 2 + 48
            pygame.draw.rect(screen, GREEN, replay_button, border_radius=12)
            replay_text = replay_font.render("REDEPLOY", True, BLACK)
            screen.blit(replay_text, replay_text.get_rect(center=replay_button.center))
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
