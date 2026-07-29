import pygame
import random
import sys
import os

# Pre-initialize Pygame mixer for optimized sound playback
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# Screen settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 50
FPS = 60  # Frames per second

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Set up display with double buffering to reduce stuttering
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Flappy Bird Game!")

# Game settings
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PIPE_WIDTH = 70  # Increased pipe width for better visibility
PIPE_GAP = 150
GRAVITY = 0.5
BIRD_FLAP_STRENGTH = -10

# Obstacle settings
OBSTACLE_FREQUENCY = 1500  # Milliseconds between each obstacle spawn
OBSTACLE_WIDTH = 40
OBSTACLE_HEIGHT = 30
OBSTACLE_SPEED = 6

# Load images with alpha for transparency and transformations
def load_image(path, width=None, height=None, alpha=False):
    try:
        image = pygame.image.load(path)
        if alpha:
            image = image.convert_alpha()  # Enable transparency if alpha is True
        else:
            image = image.convert()
        if width and height:
            image = pygame.transform.scale(image, (width, height))  # Scale image
        return image
    except pygame.error as e:
        print(f"Error loading image '{path}': {e}")
        pygame.quit()
        sys.exit()

# Load images only once to reduce redundancy
bird_image = load_image('pngkey.com-flappy-bird-png-8781424.png', BIRD_WIDTH, BIRD_HEIGHT, alpha=True)
pipe_image = load_image('pngkey.com-flappy-bird-pipe-png-1831473.png', PIPE_WIDTH, SCREEN_HEIGHT, alpha=True)
background_image = load_image('Flappy Bird Background.png', SCREEN_WIDTH, SCREEN_HEIGHT)
menu_background_image = load_image('Flappy Bird Background.png', SCREEN_WIDTH, SCREEN_HEIGHT)
obstacle_image = load_image('NicePng_angry-birds-png_539817.png', OBSTACLE_WIDTH, OBSTACLE_HEIGHT, alpha=True)

# Load sounds with error handling
def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"Error loading sound '{path}': {e}")
        return None

# Load sounds
flap_sound = load_sound('244981__ani_music__wing-flap-flag-flapping-6a.wav')
hit_sound = load_sound('406272__anthousai__hit-wooden-02.wav')

# Font for score display and menu text
font = pygame.font.SysFont(None, 36)

# Initialize high score
high_score = 0
if os.path.exists("high_score.txt"):
    with open("high_score.txt", "r") as f:
        high_score = int(f.read())

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.rect = bird_image.get_rect(topleft=(self.x, self.y))

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y

    def flap(self):
        self.velocity = BIRD_FLAP_STRENGTH
        if flap_sound:
            flap_sound.play()

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(150, SCREEN_HEIGHT - PIPE_GAP - 150)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (self.height + PIPE_GAP))
        self.scored = False

    def update(self):
        self.x -= 5
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        screen.blit(pipe_image, self.top_rect, pygame.Rect(0, 0, PIPE_WIDTH, self.height))
        screen.blit(pipe_image, self.bottom_rect, pygame.Rect(0, SCREEN_HEIGHT - (SCREEN_HEIGHT - self.bottom_rect.y), PIPE_WIDTH, SCREEN_HEIGHT - self.bottom_rect.y))

    def off_screen(self):
        return self.x < -PIPE_WIDTH

# Obstacle class
class Obstacle:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = random.randint(50, SCREEN_HEIGHT - GROUND_HEIGHT - OBSTACLE_HEIGHT)
        self.rect = pygame.Rect(self.x, self.y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

    def update(self):
        self.x -= OBSTACLE_SPEED
        self.rect.x = self.x

    def draw(self):
        if obstacle_image:
            screen.blit(obstacle_image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, BLUE, self.rect)

    def off_screen(self):
        return self.x < -OBSTACLE_WIDTH

# Show high score screen
def show_high_score():
    screen.fill(WHITE)
    screen.blit(menu_background_image, (0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
    back_text = font.render("Press 'R' to return", True, BLACK)
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))
    screen.blit(back_text, (100, SCREEN_HEIGHT - 50))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return

# Show credits screen
def show_credits():
    screen.fill(WHITE)
    screen.blit(menu_background_image, (0, 0))
    credits_text_lines = [
        "Credits:",
        "Game created by: Owen Olien, Ignacio, and Kevin",
        "Design and Programming: Owen and Ignacio",
        "Special Thanks to ChatGPT"
    ]
    y_offset = SCREEN_HEIGHT // 2 - 60
    for line in credits_text_lines:
        text_surface = font.render(line, True, BLACK)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += 30
    back_text = font.render("Press 'R' to return", True, BLACK)
    screen.blit(back_text, (100, SCREEN_HEIGHT - 50))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return

# Show instructions screen
def show_instructions():
    screen.fill(WHITE)
    screen.blit(menu_background_image, (0, 0))
    instructions_text_lines = [
        "Instructions:",
        "1. Press the SPACEBAR to make the bird flap its wings.",
        "2. The goal is to fly through the pipes without hitting them.",
        "3. Avoid hitting the top and bottom of the screen as well.",
        "4. Each pipe you pass increases your score by 1.",
        "5. Try to beat your high score!",
        "",
        "Press 'R' to return to the main menu."
    ]
    y_offset = SCREEN_HEIGHT // 2 - 100
    for line in instructions_text_lines:
        text_surface = font.render(line, True, BLACK)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += 30
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return

# Main game function
def main_game():
    global high_score
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    obstacles = []
    score = 0
    running = True

    # Set up an obstacle timer
    pygame.time.set_timer(pygame.USEREVENT + 1, OBSTACLE_FREQUENCY)

    while running:
        clock.tick(FPS)
        screen.blit(background_image, (0, 0))

        # Event handling for quitting, bird flapping, and spawning obstacles
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.flap()
            elif event.type == pygame.USEREVENT + 1:  # Custom event for spawning obstacles
                obstacles.append(Obstacle())

        # Update bird and check if it hits the ground
        bird.update()
        if bird.y > SCREEN_HEIGHT - GROUND_HEIGHT - BIRD_HEIGHT:
            if hit_sound:
                hit_sound.play()
            running = False

        # Update pipes and check for collisions
        for pipe in pipes:
            pipe.update()
            pipe.draw()
            if not pipe.scored and pipe.x + PIPE_WIDTH < bird.x:
                score += 1
                pipe.scored = True
            if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                if hit_sound:
                    hit_sound.play()
                running = False

        # Remove off-screen pipes and add new ones
        if pipes[0].off_screen():
            pipes.pop(0)
            pipes.append(Pipe())

        # Update obstacles
        for obstacle in obstacles[:]:
            obstacle.update()
            obstacle.draw()
            if bird.rect.colliderect(obstacle.rect):
                if hit_sound:
                    hit_sound.play()
                running = False
            if obstacle.off_screen():
                obstacles.remove(obstacle)

        # Draw bird, score, and update display
        bird.draw()
        score_surface = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_surface, (10, 10))
        pygame.display.update()

    # Update high score if the current score is higher
    if score > high_score:
        high_score = score
        with open("high_score.txt", "w") as f:
            f.write(str(high_score))

# Main menu function with added Instructions button
def main_menu():
    play_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 160, 200, 50)
    high_score_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 80, 200, 50)
    credits_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 0, 200, 50)
    instructions_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80, 200, 50)
    quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 160, 200, 50)

    while True:
        screen.blit(menu_background_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, YELLOW if play_button_rect.collidepoint(mouse_pos) else WHITE, play_button_rect)
        pygame.draw.rect(screen, YELLOW if high_score_button_rect.collidepoint(mouse_pos) else WHITE, high_score_button_rect)
        pygame.draw.rect(screen, YELLOW if credits_button_rect.collidepoint(mouse_pos) else WHITE, credits_button_rect)
        pygame.draw.rect(screen, YELLOW if instructions_button_rect.collidepoint(mouse_pos) else WHITE, instructions_button_rect)
        pygame.draw.rect(screen, YELLOW if quit_button_rect.collidepoint(mouse_pos) else WHITE, quit_button_rect)

        play_text = font.render("Play", True, BLACK)
        high_score_text = font.render("High Score", True, BLACK)
        credits_text = font.render("Credits", True, BLACK)
        instructions_text = font.render("Instructions", True, BLACK)
        quit_text = font.render("Quit", True, BLACK)

        screen.blit(play_text, play_text.get_rect(center=play_button_rect.center))
        screen.blit(high_score_text, high_score_text.get_rect(center=high_score_button_rect.center))
        screen.blit(credits_text, credits_text.get_rect(center=credits_button_rect.center))
        screen.blit(instructions_text, instructions_text.get_rect(center=instructions_button_rect.center))
        screen.blit(quit_text, quit_text.get_rect(center=quit_button_rect.center))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    main_game()
                elif high_score_button_rect.collidepoint(event.pos):
                    show_high_score()
                elif credits_button_rect.collidepoint(event.pos):
                    show_credits()
                elif instructions_button_rect.collidepoint(event.pos):
                    show_instructions()
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main_menu()
