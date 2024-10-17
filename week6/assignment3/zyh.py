import pygame
import sys
import numpy as np
import wave

# 生成不同频率的正弦波音效
def generate_sine_wave(filename, frequency, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    y = 0.5 * np.sin(2 * np.pi * frequency * t)
    y = (y * 32767).astype(np.int16)
    with wave.open(filename, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(y.tobytes())

# 生成更多的音效文件
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

# 加载音效
sounds = {
    "sound1": pygame.mixer.Sound("sound1.wav"),
    "sound2": pygame.mixer.Sound("sound2.wav"),
    "sound3": pygame.mixer.Sound("sound3.wav"),
    "sound4": pygame.mixer.Sound("sound4.wav"),
    "sound5": pygame.mixer.Sound("sound5.wav"),
}

# 定义区域
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
    r = int(255 * (1 - ratio) if ratio < 0.5 else 0)
    g = int(255 * ratio if ratio < 0.5 else 255 * (1 - ratio))
    b = int(255 * (ratio - 0.5) * 2 if ratio > 0.5 else 0)
    return (r, g, b)

# 主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                mouse_pos = event.pos
                for region in regions:
                    if region["rect"].collidepoint(mouse_pos):
                        region["sound"].play()

    screen.fill((255, 255, 255))

    for region in regions:
        for y in range(region["rect"].top, region["rect"].bottom):
            color = get_rainbow_color(y - region["rect"].top, region["rect"].height)
            pygame.draw.line(screen, color, (region["rect"].left, y), (region["rect"].right, y))

    pygame.display.flip()