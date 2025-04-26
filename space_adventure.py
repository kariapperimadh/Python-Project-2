import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Asset loading function
import pygame
import random
import sys
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Asset loading function
def load_image(name):
    # Construct the full image path
    image_path = os.path.join('assets', 'images', name)

    # Check if the file exists before attempting to load it
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' not found!")
        return None  # Return None to signal that the image failed to load

    try:
        # Load the image and convert it for faster rendering with transparency
        image = pygame.image.load(image_path).convert_alpha()
        return image
    except pygame.error as e:
        # Log error with more details
        print(f"Cannot load image: {image_path}")
        print(f"Error: {e}")
        return None  # Returning None instead of a blank surface

# Game settings
FPS = 60

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Adventure - Debug Challenge")

# Clock for controlling game speed
clock = pygame.time.Clock()

# Load game images
player_img = load_image('player.png')
player_mini_img = load_image('player_mini.png')
bullet_img = load_image('bullet.png')
enemy_imgs = [load_image(f'enemy{i}.png') for i in range(1, 4)]
powerup_imgs = {
    'shield': load_image('powerup_shield.png'),
    'power': load_image('powerup_power.png')
}
explosion_imgs = [load_image(f'explosion{i}.png') for i in range(1, 6)]

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Ensure player_img is loaded successfully
        if player_img is None:
            raise FileNotFoundError("Player image not loaded. Check 'assets/images/player.png'")
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.shield = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = 0
        self.power_level = 1
        self.power_timer = 0
        self.max_power_level = 3  # Define maximum power level here

    def update(self):
        # Handle the player's movement if not hidden
        if not self.hidden:
            self.speed_x = 0
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_LEFT]:
                self.speed_x = -8
            if keystate[pygame.K_RIGHT]:
                self.speed_x = 8
            self.rect.x += self.speed_x

            # Ensure the player stays on the screen
            if self.rect.right > SCREEN_WIDTH:
                self.rect.right = SCREEN_WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

        # Unhide the player after being hidden for a certain time (1 second)
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = SCREEN_WIDTH // 2
            self.rect.bottom = SCREEN_HEIGHT - 10

        # Handle power-up timeout (decrease power level after 5 seconds)
        if self.power_level > 1 and pygame.time.get_ticks() - self.power_timer > 5000:  # 5 seconds power-up duration
            self.power_level -= 1
            self.power_timer = pygame.time.get_ticks()

    def shoot(self):
        if not self.hidden:
            if self.power_level == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif self.power_level >= 2:
                # Double shot (slightly to the left and right)
                bullet1 = Bullet(self.rect.left + 10, self.rect.top)
                bullet2 = Bullet(self.rect.right - 10, self.rect.top)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT + 200)  # Moves the player off-screen

    def powerup(self):
        if self.power_level < self.max_power_level:  # Prevent power level from exceeding max
            self.power_level += 1
            self.power_timer = pygame.time.get_ticks()  # Reset the timer when the power-up is collected

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_orig = random.choice(enemy_imgs)
        self.image = self.image_orig.copy()  # Create a copy to avoid modifying the original
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # Wrap around screen horizontally
        if self.rect.left < -25:
            self.rect.right = SCREEN_WIDTH + 25
        if self.rect.right > SCREEN_WIDTH + 25:
            self.rect.left = -25

        # Reset position if goes off the bottom
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            self.speedx = random.randrange(-3, 3)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        if bullet_img is None:
            raise FileNotFoundError("Bullet image not loaded. Check 'assets/images/bullet.png'")
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10  # Move upwards

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Powerup class
class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(['shield', 'power'])
        if self.type not in powerup_imgs or powerup_imgs[self.type] is None:
            raise FileNotFoundError(f"Powerup image for '{self.type}' not loaded.")
        self.image = powerup_imgs[self.type]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Explosion animation class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.images = explosion_imgs
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images):
                self.kill()
            else:
                old_center = self.rect.center
                self.image = self.images[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = old_center

# Function to draw text
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("arial", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Function to draw shield bar
def draw_shield_bar(surface, x, y, percentage):
    if percentage < 0:
        percentage = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percentage / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

# Function to draw lives
def draw_lives(surface, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(img, img_rect)

# Game loop
def main_game():
    global all_sprites, bullets, enemies, powerups

    game_over = False
    running = True

    # Sprite groups
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    # Create player
    player = Player()
    all_sprites.add(player)

    # Create enemies
    for _ in range(8):
        new_enemy = Enemy()
        all_sprites.add(new_enemy)
        enemies.add(new_enemy)

    # Score
    score = 0

    # Main game loop
    while running:
        # Keep loop running at the right speed
        clock.tick(FPS)

        # Process input (events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Update
        all_sprites.update()

        # Check bullet-enemy collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)  # Enemies disappear on hit
        for hit in hits:
            score += 10
            # Create explosion
            explosion = Explosion(hit.rect.center, 30)
            all_sprites.add(explosion)
            # Random chance for power-up
            if random.random() > 0.7:  # Adjusted probability for balance
                powerup = Powerup()
                all_sprites.add(powerup)
                powerups.add(powerup)
            # Spawn new enemy
            new_enemy = Enemy()
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)

        # Check player-enemy collisions
        hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle) # Using circle collision for better feel
        for hit in hits:
            player.shield -= 20
            explosion = Explosion(hit.rect.center, 50) # Larger explosion for impact
            all_sprites.add(explosion)
            new_enemy = Enemy()
            all_sprites.add(new_enemy)
            enemies.add(new_enemy)
            if player.shield <= 0:
                player.lives -= 1
                player.shield = 100
                player.hide()
                if player.lives < 0:  # Corrected game over condition
                    game_over = True

        # Check player-powerup collisions
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += 25  # Slightly increased shield boost
                if player.shield > 100:
                    player.shield = 100
            if hit.type == 'power':
                player.powerup()

        # Game Over condition
        if game_over:
            running = False # Set running to False to exit the main loop
            # You might want to implement a game over screen here

        # Draw / render
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Draw UI
        draw_text(screen, str(score), 18, SCREEN_WIDTH / 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, SCREEN_WIDTH - 100, 5, player.lives, player_mini_img)

        # Flip the display
        pygame.display.flip()

    pygame.quit()
    sys.exit() # Ensure proper exit

if __name__ == "__main__":
    main_game()

# Game settings
FPS = 60

# Create the screen
import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Adventure - Debug Challenge")

# Clock for controlling game speed
clock = pygame.time.Clock()

# Load game images
import pygame
import os
import sys  # Import sys if you plan to exit

def load_image(name):
    image_path = os.path.join('assets', 'images', name)
    if not os.path.exists(image_path):
        print(f"Error: File not found at '{image_path}'")
        return None
    try:
        image = pygame.image.load(image_path).convert_alpha()
        return image
    except pygame.error as e:
        print(f"Error loading image '{image_path}': {e}")
        return None

player_img = load_image('player.png')
if player_img is None:
    print("Failed to load player image. Exiting.")
    pygame.quit()
    sys.exit()

player_mini_img = load_image('player_mini.png')
if player_mini_img is None:
    print("Failed to load player mini image. Continuing without.")
    player_mini_img = pygame.Surface((16, 16)) # Provide a fallback

bullet_img = load_image('bullet.png')
if bullet_img is None:
    print("Failed to load bullet image. Using a default.")
    bullet_img = pygame.Surface((10, 20))
    bullet_img.fill((255, 255, 0)) # Example default color

enemy_imgs = [load_image(f'enemy{i}.png') for i in range(1, 4)]
# Filter out any None values from the list
enemy_imgs = [img for img in enemy_imgs if img is not None]
if not enemy_imgs:
    print("Failed to load any enemy images. The game might not have enemies.")

powerup_imgs = {
    'shield': load_image('powerup_shield.png'),
    'power': load_image('powerup_power.png')
}
# Filter out any None values from the dictionary
powerup_imgs = {key: img for key, img in powerup_imgs.items() if img is not None}
if not powerup_imgs:
    print("Failed to load any powerup images. No powerups will appear.")
elif None in powerup_imgs.values():
    print("Warning: Some powerup images failed to load.")

explosion_imgs = [load_image(f'explosion{i}.png') for i in range(1, 6)]
# Filter out any None values from the list
explosion_imgs = [img for img in explosion_imgs if img is not None]
if not explosion_imgs:
    print("Failed to load any explosion images. No explosions will be shown.")

# Now you can safely use these image variables, knowing they are either
# valid Pygame surfaces or you've handled the loading failure.


# Player class
player_img = load_image('player.png')
if player_img is None:
    print("Failed to load player image. Exiting.")
    pygame.quit()
    sys.exit()

# Now you can safely create the Player instance
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        # ... rest of the __init__ method ...

    def update(self):
        # ... your update method ...
        
        # Power up timeout
        def update(self):
        # ... other update logic ...

        if self.power_level > 1 and pygame.time.get_ticks() - self.power_timer > 5000:
            self.power_level -= 1
            self.power_timer = pygame.time.get_ticks()

        # ... rest of the update logic ...
       
        
        # Movement
        self.speed_x = 0
keystate = pygame.key.get_pressed()
if keystate[pygame.K_LEFT]:
    self.speed_x = -8  # Corrected direction
elif keystate[pygame.K_RIGHT]:
    self.speed_x = 8
else:
    self.speed_x = 0  # Stop movement if no keys are pressed


# Enemy class
import pygame
import random

# Assuming SCREEN_WIDTH is defined elsewhere in your code
# Assuming enemy_imgs is a list of Pygame Surface objects

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(enemy_imgs)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        # Reset enemy when it goes off the bottom of the screen
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)
            # Optionally reset horizontal speed as well
            # self.speedx = random.randrange(-3, 3)

        # Handle enemies going off the sides (optional: make them disappear)
        if self.rect.left < -25 or self.rect.right > SCREEN_WIDTH + 25:
            self.kill() # Remove the sprite from all sprite groups
            # Alternatively, to reset from the top with a new horizontal position:
            # self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            # self.rect.y = random.randrange(-100, -40)
            # self.speedy = random.randrange(1, 8)
            # # Optionally reset horizontal speed
            # self.speedx = random.randrange(-3, 3)


# Bullet class
import pygame

# Assuming bullet_img is defined elsewhere

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10  # Changed to a negative value for upward movement

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Powerup class
import pygame
import random

# Assuming SCREEN_WIDTH is defined elsewhere in your code
# Assuming powerup_imgs is a dictionary of Pygame Surface objects like:
# powerup_imgs = {'shield': shield_image, 'power': power_image}

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(['shield', 'power'])
        self.image = powerup_imgs[self.type]
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = 2  # Adjusted to a slightly slower speed (you can change this)
        self.speedx = random.randrange(-1, 2) # Added slight horizontal drift

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # Optional: Add boundary checking for horizontal movement
        if self.rect.left < 0:
            self.rect.left = 0
            self.speedx *= -1
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.speedx *= -1

# Explosion animation class
import pygame

# Assuming explosion_imgs is a list of Pygame Surface objects

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.images = explosion_imgs
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame]
                old_center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = old_center



# Function to draw text
import pygame

def draw_text(surface, text, size, x, y, color=(255, 255, 255), font_name="arial", bold=False, italic=False, align="midtop"):
    """
    Draws text onto a Pygame surface with customizable font, color, style, and alignment.

    Args:
        surface: The Pygame Surface to draw on.
        text: The string of text to draw.
        size: The font size (integer).
        x: The horizontal coordinate for the text's position.
        y: The vertical coordinate for the text's position.
        color: The color of the text (RGB tuple, default is white).
        font_name: The name of the system font to use (default is "arial").
        bold: Boolean indicating if the font should be bold (default is False).
        italic: Boolean indicating if the font should be italic (default is False).
        align: A string indicating the alignment point for (x, y).
               Possible values: "topleft", "topmid", "topright",
                                "midleft", "midtop", "midright",
                                "bottomleft", "bottommid", "bottomright",
                                "center". Default is "midtop".
    """
    font = pygame.font.SysFont(font_name, size, bold, italic)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if align == "topleft":
        text_rect.topleft = (x, y)
    elif align == "topmid":
        text_rect.midtop = (x, y)
    elif align == "topright":
        text_rect.topright = (x, y)
    elif align == "midleft":
        text_rect.midleft = (x, y)
    elif align == "midtop":
        text_rect.midtop = (x, y)
    elif align == "midright":
        text_rect.midright = (x, y)
    elif align == "bottomleft":
        text_rect.bottomleft = (x, y)
    elif align == "bottommid":
        text_rect.midbottom = (x, y)
    elif align == "bottomright":
        text_rect.bottomright = (x, y)
    elif align == "center":
        text_rect.center = (x, y)
    else:
        print(f"Warning: Unknown alignment '{align}', defaulting to midtop.")
        text_rect.midtop = (x, y)

    surface.blit(text_surface, text_rect)

# Example usage (assuming you have a Pygame screen initialized):
if __name__ == '__main__':
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Text Drawing Example")
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    black = (0, 0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(black)

        draw_text(screen, "Top Left", 24, 10, 10, white, align="topleft")
        draw_text(screen, "Top Mid", 24, screen_width // 2, 10, white, align="topmid")
        draw_text(screen, "Top Right", 24, screen_width - 10, 10, white, align="topright")

        draw_text(screen, "Mid Left", 24, 10, screen_height // 2, white, align="midleft")
        draw_text(screen, "Center", 36, screen_width // 2, screen_height // 2, red, bold=True, align="center")
        draw_text(screen, "Mid Right", 24, screen_width - 10, screen_height // 2, white, align="midright")

        draw_text(screen, "Bottom Left", 24, 10, screen_height - 10, white, align="bottomleft")
        draw_text(screen, "Bottom Mid", 24, screen_width // 2, screen_height - 10, white, align="bottommid")
        draw_text(screen, "Bottom Right", 24, screen_width - 10, screen_height - 10, white, align="bottomright")

        draw_text(screen, "Italic Text", 20, 50, 550, green, italic=True)
        draw_text(screen, "Bold Italic", 20, 200, 550, white, bold=True, italic=True)

        pygame.display.flip()

    pygame.quit()


# Function to draw shield bar
import pygame

def draw_shield_bar(surface, x, y, percentage, bar_length=100, bar_height=10, good_color=(0, 255, 0), warning_color=(255, 255, 0), danger_color=(255, 0, 0), outline_color=(255, 255, 255), outline_thickness=2):
    """
    Draws a customizable shield/health bar onto a Pygame surface.

    Args:
        surface: The Pygame Surface to draw on.
        x: The horizontal coordinate for the top-left corner of the bar.
        y: The vertical coordinate for the top-left corner of the bar.
        percentage: A numerical value (0-100) representing the current level.
        bar_length: The total length of the bar in pixels (default is 100).
        bar_height: The height of the bar in pixels (default is 10).
        good_color: The color of the bar when the percentage is high (default is green).
        warning_color: The color of the bar when the percentage is medium (default is yellow).
        danger_color: The color of the bar when the percentage is low (default is red).
        outline_color: The color of the bar's outline (default is white).
        outline_thickness: The thickness of the bar's outline in pixels (default is 2).
    """
    if percentage < 0:
        percentage = 0
    if percentage > 100:
        percentage = 100

    fill = (percentage / 100) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    color = good_color

    if percentage > 60:
        color = good_color
    elif percentage > 30:
        color = warning_color
    else:
        color = danger_color

    pygame.draw.rect(surface, color, fill_rect)
    pygame.draw.rect(surface, outline_color, outline_rect, outline_thickness)

# Example usage (assuming you have a Pygame screen initialized):
if __name__ == '__main__':
    pygame.init()
    screen_width = 400
    screen_height = 200
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Customizable Shield Bar Example")
    black = (0, 0, 0)
    green = (0, 255, 0)
    yellow = (255, 255, 0)
    red = (255, 0, 0)
    white = (255, 255, 255)

    shield_level = 100
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    shield_level -= 10
                if event.key == pygame.K_RIGHT:
                    shield_level += 10
                shield_level = max(0, min(100, shield_level))

        screen.fill(black)
        draw_shield_bar(screen, 50, 50, shield_level)
        draw_shield_bar(screen, 50, 80, shield_level, bar_length=150, bar_height=15, good_color=yellow, warning_color=red, danger_color=white, outline_color=green, outline_thickness=3)
        pygame.display.flip()

    pygame.quit()



# Function to draw lives
import pygame

def draw_lives(surface, x, y, lives, img, spacing=30, alignment="topleft"):
    """
    Draws life icons onto a Pygame surface with customizable spacing and alignment.

    Args:
        surface: The Pygame Surface to draw on.
        x: The horizontal starting position for the first life icon.
        y: The vertical starting position for the first life icon.
        lives: An integer representing the current number of lives.
        img: The Pygame Surface object representing the image to use for each life icon.
        spacing: The horizontal space (in pixels) between each life icon (default is 30).
        alignment: A string indicating the alignment point for the starting (x, y) coordinates
                   relative to the group of life icons.
                   Possible values: "topleft" (default), "topright", "bottomleft", "bottomright".
    """
    img_rect = img.get_rect()
    img_width = img_rect.width
    total_width = lives * img_width + (lives - 1) * spacing
    start_x = x
    start_y = y

    if alignment == "topright":
        start_x = x - total_width
    elif alignment == "bottomleft":
        start_y = y - img_rect.height
    elif alignment == "bottomright":
        start_x = x - total_width
        start_y = y - img_rect.height

    for i in range(lives):
        draw_x = start_x + (img_width + spacing) * i
        draw_y = start_y
        surface.blit(img, (draw_x, draw_y))

# Example usage (assuming you have a Pygame screen and a life image loaded):
if __name__ == '__main__':
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Drawing Lives with Customization")
    black = (0, 0, 0)

    # Load the life image (replace 'player_mini.png' with your image file)
    try:
        player_mini_img = pygame.image.load('player_mini.png').convert_alpha()
    except pygame.error as e:
        print(f"Error loading image: {e}")
        pygame.quit()
        exit()

    lives_count = 5
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(black)

        draw_lives(screen, 10, 10, lives_count, player_mini_img)
        draw_lives(screen, screen_width - 10, 10, lives_count - 2, player_mini_img, alignment="topright")
        draw_lives(screen, 10, screen_height - 10, lives_count - 3, player_mini_img, spacing=40, alignment="bottomleft")
        draw_lives(screen, screen_width - 10, screen_height - 10, lives_count - 4, player_mini_img, spacing=20, alignment="bottomright")

        pygame.display.flip()

    pygame.quit()


# Game loop
import pygame
import random

# Import your game settings and assets
from settings import * # Assuming you have a settings.py file
from sprites import Player, Enemy, Bullet, Powerup, Explosion  # Assuming your sprite classes are in sprites.py
from os import path

def main_game():
    global all_sprites, bullets, enemies, powerups, player

    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()  # Initialize sound module
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Load game assets
    img_dir = path.join(path.dirname(__file__), 'img')
    snd_dir = path.join(path.dirname(__file__), 'snd')
    explosion_anim = {}
    for size in ['lg', 'sm']:
        explosion_anim[size] = []
        for i in range(9):
            filename = f'regularExplosion0{i}.png'
            img = pygame.image.load(path.join(img_dir, filename)).convert()
            img.set_colorkey(BLACK)
            img_scaled = pygame.transform.scale(img, (75, 75) if size == 'lg' else (32, 32))
            explosion_anim[size].append(img_scaled)
    player_img = pygame.image.load(path.join(img_dir, PLAYER_IMG)).convert_alpha()
    player_mini_img = pygame.transform.scale(player_img, (25, 19))
    player_mini_img.set_colorkey(BLACK)
    bullet_img = pygame.image.load(path.join(img_dir, BULLET_IMG)).convert_alpha()
    enemy_images = []
    enemy_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png']
    for img_name in enemy_list:
        enemy_images.append(pygame.image.load(path.join(img_dir, img_name)).convert_alpha())
    powerup_images = {}
    powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield_gold.png')).convert_alpha()
    powerup_images['power'] = pygame.image.load(path.join(img_dir, 'bolt_gold.png')).convert_alpha()

    # Load sounds
    shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'Laser_09.wav'))
    expl_sounds = [pygame.mixer.Sound(path.join(snd_dir, f'Explosion_{i}.wav')) for i in [0, 1]]
    pygame.mixer.music.load(path.join(snd_dir, BG_MUSIC))
    pygame.mixer.music.set_volume(0.4)

    # Initialize sprite groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

    for _ in range(8):
        new_enemy()

    score = 0
    pygame.mixer.music.play(loops=-1)
    game_over = False
    running = True

    # Game loop
    while running:
        if game_over:
            show_game_over_screen(screen) # Assuming you have this function
            running = False
            continue

        # Keep loop running at the right speed
        clock.tick(FPS)

        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Update
        all_sprites.update()

        # Check for bullet-enemy collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 50 - hit.radius # Example scoring based on enemy size
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            if random.random() > 0.9:
                pow = Powerup(hit.rect.center)
                all_sprites.add(pow)
                powerups.add(pow)
            new_enemy()

        # Check for player-enemy collisions
        hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
        for hit in hits:
            player.shield -= hit.radius * 2 # Example damage based on enemy size
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            new_enemy()
            if player.shield <= 0:
                death_explosion = Explosion(player.rect.center, 'lg')
                all_sprites.add(death_explosion)
                player.hide()
                player.lives -= 1
                player.shield = 100
                if player.lives == 0 and not death_explosion.alive():
                    game_over = True

        # Check for player-powerup collisions
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                player.shield += random.randrange(10, 30)
                if player.shield >= 100:
                    player.shield = 100
            if hit.type == 'power':
                player.powerup()

        # Draw / render
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_text(screen, str(score), 18, WIDTH // 2, 10)
        draw_shield_bar(screen, 5, 5, player.shield)
        draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

        # After drawing everything, flip the display
        pygame.display.flip()

    pygame.quit()

def new_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

def show_game_over_screen(screen):
    # Your game over screen logic here
    pass

if __name__ == '__main__':
    main_game()
    
    
    # Sprite groups
    import pygame

# Initialize sprite groups (it's good practice to do this at the top level of your script
# or within the main game initialization function)
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# You would then proceed to create your game objects (player, enemies, etc.)
# and add them to these groups. For example:

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 500)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(100, 700), random.randrange(50, 200))

import random

# Create instances of your sprites
player = Player()
all_sprites.add(player)

for _ in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Example of shooting (you'd integrate this into your player's control)
def player_shoot():
    bullet = Bullet(player.rect.centerx, player.rect.top)
    all_sprites.add(bullet)
    bullets.add(bullet)

class Powerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randrange(100, 700), random.randrange(50, 200))

powerup = Powerup()
all_sprites.add(powerup)
powerups.add(powerup)

# In your main game loop, you would then update and draw these groups:
def game_loop(screen):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_shoot()

        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sprite Group Example")
    game_loop(screen)

    
    # Create player
    player = Player()
all_sprites.add(player)

    
    # Create enemies
    for i in range(8):
        new_enemy = Enemy()
        all_sprites.add(new_enemy)
        enemies.add(new_enemy)
    
  

# Scoreimport pygame
import sys  # Ensure sys is imported

# Initialize Pygame (you might have this elsewhere, but it's crucial)
pygame.init()

# Game settings (you'll likely have more of these)
WIDTH = 800
HEIGHT = 600
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Awesome Game")
clock = pygame.time.Clock()

# Player sprite (assuming you have a Player class)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)

    def shoot(self):
        print("Player shooting!") # Placeholder for actual shooting logic

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

score = 0
running = True

# Main game loop
while running:
    # Keep loop running at the right speed
    clock.tick(FPS)

    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update game elements (you'll have more here)
    all_sprites.update()

    # Draw / render
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)

    # *after* drawing everything, flip the display
    pygame.display.flip()

# Uninitialize Pygame after the loop
pygame.quit()
sys.exit()
     
       

# Update
import pygame
import random

# Assume these are defined elsewhere in your code
# SCREEN_WIDTH, BLACK, Enemy, Explosion, Powerup, Player, draw_text, draw_shield_bar, draw_lives
# all_sprites, enemies, bullets, powerups, player, score, player_mini_img, screen

def main_game():
    pygame.init()
    SCREEN_WIDTH = 800  # Example value
    SCREEN_HEIGHT = 600 # Example value
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("My Awesome Game")
    clock = pygame.time.Clock()
    FPS = 60
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Example sprite groups (assuming they are initialized elsewhere)
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    # Example player and enemy (assuming their classes are defined elsewhere)
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((50, 50))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
            self.rect.centerx = SCREEN_WIDTH // 2
            self.rect.bottom = SCREEN_HEIGHT - 10
            self.shield = 100
            self.lives = 3
            self.hidden = False
            self.hide_timer = pygame.time.get_ticks()

        def update(self):
            if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000: # 1 second invulnerability
                self.hidden = False
                self.rect.centerx = SCREEN_WIDTH // 2
                self.rect.bottom = SCREEN_HEIGHT - 10

        def hide(self):
            self.hidden = True
            self.hide_timer = pygame.time.get_ticks()
            self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT + 1000) # Move off screen

        def powerup(self):
            # Implement power-up logic here
            pass

    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((30, 30))
            self.image.fill(RED)
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)

        def update(self):
            self.rect.y += self.speedy
            if self.rect.top > SCREEN_HEIGHT + 10:
                self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
                self.rect.y = random.randrange(-100, -40)
                self.speedy = random.randrange(1, 5)

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface((10, 20))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = -10

        def update(self):
            self.rect.y += self.speedy
            if self.rect.bottom < 0:
                self.kill()

    class Explosion(pygame.sprite.Sprite):
        def __init__(self, center, size):
            super().__init__()
            # For simplicity, let's just have a white square for explosion
            self.image = pygame.Surface((size, size))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.frame = 0
            self.last_update = pygame.time.get_ticks()
            self.frame_rate = 50 # milliseconds per frame

        def update(self):
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                if self.frame == 2: # Simple 2-frame "explosion"
                    self.kill()

    class Powerup(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.type = random.choice(['shield', 'power'])
            self.image = pygame.Surface((20, 20))
            self.image.fill((0, 255, 0) if self.type == 'shield' else (255, 255, 0))
            self.rect = self.image.get_rect()
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = 3

        def update(self):
            self.rect.y += self.speedy
            if self.rect.top > SCREEN_HEIGHT + 10:
                self.kill()

    def draw_text(surf, text, size, x, y):
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(midtop=(x, y))
        surf.blit(text_surface, text_rect)

    def draw_shield_bar(surf, x, y, pct):
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(surf, (0, 255, 0), fill_rect)
        pygame.draw.rect(surf, WHITE, outline_rect, 2
