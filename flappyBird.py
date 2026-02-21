# ---------------------------------------------------------
# Project: Flappy Abeer (Flappy Bird Clone)
# Author: Abeer (FAST University)
# Tech: Python & Pygame
# © 2026 Abeer - All Rights Reserved
# ---------------------------------------------------------
import pygame
import random
import math

# --- SETUP ---
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Abeer")
clock = pygame.time.Clock()

# Load fonts
try:
    font_title = pygame.font.Font(None, 48)
    font_score = pygame.font.Font(None, 36)
    font_gameover = pygame.font.Font(None, 64)
    font_instruction = pygame.font.Font(None, 28)
except:
    font_title = pygame.font.SysFont("Arial", 48, bold=True)
    font_score = pygame.font.SysFont("Arial", 36, bold=True)
    font_gameover = pygame.font.SysFont("Arial", 64, bold=True)
    font_instruction = pygame.font.SysFont("Arial", 28)

# --- VARIABLES ---
GRAVITY = 0.25
BIRD_JUMP = -6
PIPE_SPEED = 3
PIPE_GAP = 180
PIPE_FREQUENCY = 1800

# Colors
SKY_BLUE = (135, 206, 235)
WHITE = (255, 255, 255)
BLACK = (30, 30, 40)
GREEN = (76, 175, 80)
DARK_GREEN = (56, 142, 60)
RED = (231, 76, 60)
YELLOW = (241, 196, 15)
ORANGE = (230, 126, 34)
BROWN = (139, 69, 19)
CLOUD_COLOR = (255, 255, 255, 180)

class Bird:
    def __init__(self):
        self.x = 80
        self.y = HEIGHT // 2
        self.vel = 0
        self.radius = 15
        self.angle = 0
        self.eye_radius = 5
        self.eye_offset_x = 5
        self.eye_offset_y = -3
        self.wing_flap = 0
        self.wing_speed = 0.3
        self.trail = []
        self.max_trail = 8
        self.color = YELLOW
        self.eye_color = BLACK
        self.beak_color = ORANGE
        
    def jump(self):
        self.vel = BIRD_JUMP
        self.wing_flap = 10  # Wing flap effect on jump
        
    def move(self):
        self.vel += GRAVITY
        self.y += self.vel
        
        # Rotate bird based on velocity
        self.angle = max(-30, min(30, -self.vel * 4))
        
        # Wing flapping animation
        self.wing_flap += self.wing_speed
        if self.wing_flap > 20:
            self.wing_flap = 0
            
        # Add trail effect
        self.trail.append((self.x, self.y + 2))
        if len(self.trail) > self.max_trail:
            self.trail.pop(0)
            
    def draw(self):
        # Draw trail
        for i, (tx, ty) in enumerate(self.trail):
            alpha = int(255 * (i / len(self.trail)) * 0.3)
            pygame.draw.circle(screen, (self.color[0], self.color[1], self.color[2], alpha), 
                             (int(tx), int(ty)), int(self.radius * (i / len(self.trail))))
        
        # Draw bird body
        bird_pos = (int(self.x), int(self.y))
        
        # Rotated drawing
        angle_rad = math.radians(self.angle)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        
        # Draw body
        pygame.draw.circle(screen, self.color, bird_pos, self.radius)
        
        # Draw wing
        wing_y_offset = math.sin(self.wing_flap) * 3
        wing_points = [
            (self.x - 10 * cos_a - 5 * sin_a, self.y - 10 * sin_a + 5 * cos_a + wing_y_offset),
            (self.x - 15 * cos_a, self.y - 15 * sin_a),
            (self.x - 10 * cos_a + 5 * sin_a, self.y - 10 * sin_a - 5 * cos_a + wing_y_offset)
        ]
        pygame.draw.polygon(screen, (self.color[0]*0.8, self.color[1]*0.8, self.color[2]*0.8), wing_points)
        
        # Draw eye
        eye_x = self.x + self.eye_offset_x * cos_a - self.eye_offset_y * sin_a
        eye_y = self.y + self.eye_offset_x * sin_a + self.eye_offset_y * cos_a
        pygame.draw.circle(screen, self.eye_color, (int(eye_x), int(eye_y)), self.eye_radius)
        pygame.draw.circle(screen, WHITE, (int(eye_x + 2), int(eye_y - 2)), 2)
        
        # Draw beak
        beak_points = [
            (self.x + 10 * cos_a - 3 * sin_a, self.y + 10 * sin_a + 3 * cos_a),
            (self.x + 20 * cos_a, self.y + 20 * sin_a),
            (self.x + 10 * cos_a + 3 * sin_a, self.y + 10 * sin_a - 3 * cos_a)
        ]
        pygame.draw.polygon(screen, self.beak_color, beak_points)

class Pipe:
    def __init__(self, x, height):
        self.x = x
        self.height = height
        self.width = 60
        self.color = GREEN
        self.top_cap_color = DARK_GREEN
        self.passed = False
        self.cap_height = 20
        
    def move(self):
        self.x -= PIPE_SPEED
        
    def draw(self):
        # Draw top pipe
        top_rect = pygame.Rect(self.x, 0, self.width, self.height)
        pygame.draw.rect(screen, self.color, top_rect)
        pygame.draw.rect(screen, self.top_cap_color, 
                        pygame.Rect(self.x - 5, self.height - self.cap_height, self.width + 10, self.cap_height))
        
        # Draw bottom pipe
        bottom_y = self.height + PIPE_GAP
        bottom_rect = pygame.Rect(self.x, bottom_y, self.width, HEIGHT - bottom_y)
        pygame.draw.rect(screen, self.color, bottom_rect)
        pygame.draw.rect(screen, self.top_cap_color, 
                        pygame.Rect(self.x - 5, bottom_y, self.width + 10, self.cap_height))
        
        # Draw pipe pattern
        pattern_color = (self.color[0]*0.9, self.color[1]*0.9, self.color[2]*0.9)
        for i in range(0, self.height, 20):
            pattern_rect = pygame.Rect(self.x + 10, i, self.width - 20, 10)
            pygame.draw.rect(screen, pattern_color, pattern_rect)
            
        for i in range(bottom_y + 20, HEIGHT, 20):
            pattern_rect = pygame.Rect(self.x + 10, i, self.width - 20, 10)
            pygame.draw.rect(screen, pattern_color, pattern_rect)

class Cloud:
    def __init__(self):
        self.x = random.randint(-100, WIDTH)
        self.y = random.randint(50, 200)
        self.speed = random.uniform(0.2, 0.8)
        self.size = random.randint(30, 60)
        
    def move(self):
        self.x += self.speed
        if self.x > WIDTH + 100:
            self.x = -100
            self.y = random.randint(50, 200)
            
    def draw(self):
        # Create cloud with overlapping circles
        for i in range(3):
            offset_x = i * self.size * 0.6
            radius = self.size * (0.8 + i * 0.1)
            pygame.draw.circle(screen, CLOUD_COLOR, 
                             (int(self.x + offset_x), int(self.y)), int(radius))
        for i in range(2):
            offset_x = i * self.size * 0.6 + self.size * 0.3
            radius = self.size * (0.7 + i * 0.1)
            pygame.draw.circle(screen, CLOUD_COLOR, 
                             (int(self.x + offset_x), int(self.y - self.size * 0.3)), int(radius))

def draw_background():
    # Gradient sky
    for y in range(HEIGHT):
        color_value = int(135 + (y / HEIGHT) * 100)
        color = (color_value, 206 - (y / HEIGHT) * 50, 235)
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))
    
    # Sun
    sun_x, sun_y = WIDTH - 80, 80
    pygame.draw.circle(screen, YELLOW, (sun_x, sun_y), 40)
    pygame.draw.circle(screen, ORANGE, (sun_x, sun_y), 35)
    
    # Sun rays
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        start_x = sun_x + 40 * math.cos(rad)
        start_y = sun_y + 40 * math.sin(rad)
        end_x = sun_x + 55 * math.cos(rad)
        end_y = sun_y + 55 * math.sin(rad)
        pygame.draw.line(screen, YELLOW, (start_x, start_y), (end_x, end_y), 3)

def draw_ground():
    # Ground with texture
    ground_y = HEIGHT - 50
    pygame.draw.rect(screen, BROWN, (0, ground_y, WIDTH, 50))
    
    # Grass on top
    grass_height = 10
    pygame.draw.rect(screen, DARK_GREEN, (0, ground_y, WIDTH, grass_height))
    
    # Grass blades
    for x in range(0, WIDTH, 5):
        blade_height = random.randint(5, 15)
        blade_points = [
            (x, ground_y),
            (x + 2, ground_y - blade_height),
            (x + 4, ground_y)
        ]
        pygame.draw.polygon(screen, GREEN, blade_points)

def draw_particle_effect(x, y, color, count=20):
    particles = []
    for _ in range(count):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 8)
        size = random.uniform(2, 6)
        lifetime = random.uniform(20, 40)
        particles.append({
            'x': x, 'y': y,
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed,
            'size': size,
            'lifetime': lifetime,
            'color': color
        })
    return particles

def update_particles(particles):
    new_particles = []
    for p in particles:
        p['x'] += p['vx']
        p['y'] += p['vy']
        p['vy'] += 0.1  # Gravity
        p['lifetime'] -= 1
        if p['lifetime'] > 0:
            new_particles.append(p)
    return new_particles

def draw_particles(particles):
    for p in particles:
        alpha = int(255 * (p['lifetime'] / 40))
        color_with_alpha = (p['color'][0], p['color'][1], p['color'][2], alpha)
        pygame.draw.circle(screen, color_with_alpha, (int(p['x']), int(p['y'])), int(p['size']))

# --- MAIN GAME LOOP ---
def main():
    bird = Bird()
    pipes = []
    clouds = [Cloud() for _ in range(5)]
    score = 0
    high_score = 0
    last_pipe_time = pygame.time.get_ticks()
    running = True
    game_over = False
    game_started = False
    particles = []
    shake_intensity = 0
    score_flash = 0
    
    while running:
        # Screen shake effect
        shake_x = random.randint(-shake_intensity, shake_intensity) if shake_intensity > 0 else 0
        shake_y = random.randint(-shake_intensity, shake_intensity) if shake_intensity > 0 else 0
        shake_intensity = max(0, shake_intensity - 1)
        
        # Draw background
        screen.fill(SKY_BLUE)
        draw_background()
        
        # Draw clouds
        for cloud in clouds:
            cloud.draw()
            if game_started and not game_over:
                cloud.move()
        
        # Draw ground
        draw_ground()
        
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_started:
                        game_started = True
                    if not game_over:
                        bird.jump()
                        # Add jump particles
                        particles.extend(draw_particle_effect(bird.x - 10, bird.y, WHITE, 10))
                    else:
                        # Reset game
                        bird = Bird()
                        pipes.clear()
                        score = 0
                        game_over = False
                        game_started = True
                        last_pipe_time = pygame.time.get_ticks()
                        shake_intensity = 0
        
        if game_started and not game_over:
            # 2. Bird Movement
            bird.move()
            
            # 3. Pipe Generation
            current_time = pygame.time.get_ticks()
            if current_time - last_pipe_time > PIPE_FREQUENCY:
                pipe_height = random.randint(100, 400)
                pipes.append(Pipe(WIDTH, pipe_height))
                last_pipe_time = current_time
            
            # 4. Pipe Movement & Collision
            for pipe in pipes[:]:
                pipe.move()
                pipe.draw()
                
                # Collision Check
                bird_circle_x = bird.x + bird.radius * 0.7
                bird_circle_y = bird.y
                bird_radius = bird.radius * 0.9
                
                # Check collision with top pipe
                if (bird_circle_x + bird_radius > pipe.x and 
                    bird_circle_x - bird_radius < pipe.x + pipe.width and
                    bird_circle_y - bird_radius < pipe.height):
                    game_over = True
                    shake_intensity = 10
                    particles.extend(draw_particle_effect(bird.x, bird.y, RED, 30))
                
                # Check collision with bottom pipe
                bottom_pipe_top = pipe.height + PIPE_GAP
                if (bird_circle_x + bird_radius > pipe.x and 
                    bird_circle_x - bird_radius < pipe.x + pipe.width and
                    bird_circle_y + bird_radius > bottom_pipe_top):
                    game_over = True
                    shake_intensity = 10
                    particles.extend(draw_particle_effect(bird.x, bird.y, RED, 30))
                
                # Score Check
                if not pipe.passed and pipe.x + pipe.width < bird.x:
                    pipe.passed = True
                    score += 1
                    score_flash = 10
                    particles.extend(draw_particle_effect(pipe.x + pipe.width//2, 
                                                         pipe.height + PIPE_GAP//2, 
                                                         YELLOW, 15))
                    high_score = max(high_score, score)
                
                # Remove off-screen pipes
                if pipe.x < -pipe.width:
                    pipes.remove(pipe)
            
            # Floor/Ceiling Collision
            if bird.y >= HEIGHT - 50 - bird.radius or bird.y < bird.radius:
                game_over = True
                shake_intensity = 10
                particles.extend(draw_particle_effect(bird.x, bird.y, RED, 30))
        
        # Update and draw particles
        particles = update_particles(particles)
        draw_particles(particles)
        
        # Draw bird
        if game_started:
            bird.draw()
        
        # Draw Score with flash effect
        if score_flash > 0:
            score_color = (min(255, 255 + score_flash * 10), 255, min(255, 255 + score_flash * 10))
            score_flash -= 1
        else:
            score_color = WHITE
            
        score_text = font_score.render(f"Score: {score}", True, score_color)
        high_score_text = font_score.render(f"High: {high_score}", True, WHITE)
        
        # Draw scores with background
        pygame.draw.rect(screen, (0, 0, 0, 100), (5, 5, 150, 70), 0, 10)
        screen.blit(score_text, (15, 15))
        screen.blit(high_score_text, (15, 45))
        
        if not game_started:
            # Start screen
            title_text = font_title.render("Flappy Abeer", True, WHITE)
            instruction_text = font_instruction.render("Press SPACE to Start", True, WHITE)
            hint_text = font_instruction.render("Press SPACE to Flap", True, WHITE)
            
            # Draw semi-transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2 + shake_x, 150 + shake_y))
            screen.blit(instruction_text, (WIDTH//2 - instruction_text.get_width()//2 + shake_x, 250 + shake_y))
            screen.blit(hint_text, (WIDTH//2 - hint_text.get_width()//2 + shake_x, 300 + shake_y))
            
            # Draw example bird in center
            example_bird = Bird()
            example_bird.x = WIDTH // 2
            example_bird.y = 400
            example_bird.wing_flap = math.sin(pygame.time.get_ticks() * 0.005) * 10
            example_bird.draw()
            
        elif game_over:
            # Game Over Screen
            game_over_text = font_gameover.render("GAME OVER", True, RED)
            restart_text = font_instruction.render("Press SPACE to Restart", True, WHITE)
            final_score = font_score.render(f"Final Score: {score}", True, YELLOW)
            
            # Draw semi-transparent overlay
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2 + shake_x, 200 + shake_y))
            screen.blit(final_score, (WIDTH//2 - final_score.get_width()//2 + shake_x, 280 + shake_y))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2 + shake_x, 350 + shake_y))
        
        pygame.display.update()
        clock.tick(60) # Limit to 60 FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()