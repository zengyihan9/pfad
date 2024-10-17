import pygame
import sys
import numpy as np
import wave
import colorsys
import random

# Generate sine wave audio at different frequencies
def generate_sine_wave(filename, frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    y = 0.5 * np.sin(2 * np.pi * frequency * t)
    y = (y * 32767).astype(np.int16)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(y.tobytes())

# Generate more audio files
generate_sine_wave("sound1.wav", 440, 2)    # A4
generate_sine_wave("sound2.wav", 554.37, 2) # C#5
generate_sine_wave("sound3.wav", 659.25, 2) # E5
generate_sine_wave("sound4.wav", 740, 2)    # F#5
generate_sine_wave("sound5.wav", 830, 2)    # G#5

print("声音文件生成完成！")

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("点击播放声音")

# Load audio effects
sounds = {
    "sound1": pygame.mixer.Sound("sound1.wav"),
    "sound2": pygame.mixer.Sound("sound2.wav"),
    "sound3": pygame.mixer.Sound("sound3.wav"),
    "sound4": pygame.mixer.Sound("sound4.wav"),
    "sound5": pygame.mixer.Sound("sound5.wav"),
}

# Define the area
regions = [
    {"rect": pygame.Rect(0, 0, screen_width // 5, screen_height), "sound": sounds["sound1"]},
    {"rect": pygame.Rect(screen_width // 5, 0, screen_width // 5, screen_height), "sound": sounds["sound2"]},
    {"rect": pygame.Rect(2 * screen_width // 5, 0, screen_width // 5, screen_height), "sound": sounds["sound3"]},
    {"rect": pygame.Rect(3 * screen_width // 5, 0, screen_width // 5, screen_height), "sound": sounds["sound4"]},
    {"rect": pygame.Rect(4 * screen_width // 5, 0, screen_width // 5, screen_height), "sound": sounds["sound5"]},
]

def get_rainbow_color(position, max_position):
    """根据位置返回渐变的彩虹颜色"""
    ratio = position / max_position
    hue = ratio * 360  # Convert to a 0-360 degree hue
    color = colorsys.hsv_to_rgb(hue / 360, 1.0, 1.0)
    return (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))

# Initialize the data for tracking mouse trails
trail_length = 30
trail = []

# Define a star effect class
class Star:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 25)  # Increase the initial size
        self.lifetime = 240  # The lifespan of the star is 240 frames (4 seconds)

    def update(self):
        if self.lifetime < 60:  # Gradually decrease in size during the last second
            self.size -= 0.5
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            pygame.draw.polygon(surface, (255, 255, 0), [
                (self.x, self.y - self.size),
                (self.x + self.size * 0.5, self.y - self.size * 0.5),
                (self.x + self.size, self.y),
                (self.x + self.size * 0.5, self.y + self.size * 0.5),
                (self.x, self.y + self.size),
                (self.x - self.size * 0.5, self.y + self.size * 0.5),
                (self.x - self.size, self.y),
                (self.x - self.size * 0.5, self.y - self.size * 0.5),
            ])

# Store the star effect
stars = []

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse click
                mouse_pos = event.pos
                for region in regions:
                    if region["rect"].collidepoint(mouse_pos):
                        region["sound"].play()
                        stars.append(Star(mouse_pos[0], mouse_pos[1]))
        elif event.type == pygame.MOUSEMOTION:
            trail.append(event.pos)
            if len(trail) > trail_length:
                trail.pop(0)

    screen.fill((255, 255, 255))

    for region in regions:
        for y in range(region["rect"].top, region["rect"].bottom):
            color = get_rainbow_color(y - region["rect"].top, region["rect"].height)
            pygame.draw.line(screen, color, (region["rect"].left, y), (region["rect"].right, y))

    # Draw mouse trails
    for i in range(len(trail)):
        pos = trail[i]
        color = get_rainbow_color(i, len(trail))
        alpha = int(255 * (i + 1) / len(trail))
        radius = 15
        surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, color + (alpha,), (radius, radius), radius)
        screen.blit(surface, (pos[0] - radius, pos[1] - radius))

    # 绘Draw and update the star effect
    for star in stars[:]:
        star.draw(screen)
        star.update()
        if star.lifetime <= 0:
            stars.remove(star)

    pygame.display.flip()