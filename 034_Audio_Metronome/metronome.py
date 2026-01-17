import pygame
import time
import numpy as np
import collections

# Settings
WIDTH, HEIGHT = 600, 400
FPS = 60
SAMPLE_RATE = 44100

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
ACCENT = (0, 255, 200)
RED = (255, 50, 50)

def generate_beep(frequency=1000, duration=0.1):
    """Generate a square wave beep."""
    n_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n_samples, endpoint=False)
    
    # Square wave
    waveform = np.sign(np.sin(2 * np.pi * frequency * t))
    
    # Convert to 16-bit signed integer
    waveform = (waveform * 32767).astype(np.int16)
    
    # Stereo
    stereo_waveform = np.column_stack((waveform, waveform))
    return pygame.sndarray.make_sound(stereo_waveform)

def main():
    pygame.init()
    pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Day 34: Metronome & Tap BPM")
    clock = pygame.time.Clock()
    font_big = pygame.font.SysFont("Consolas", 80, bold=True)
    font_small = pygame.font.SysFont("Consolas", 24)

    # Audio
    low_beep = generate_beep(800, 0.05)
    high_beep = generate_beep(1200, 0.05)

    # State
    bpm = 120.0
    is_running = False
    last_tick_time = time.time()
    next_tick_time = time.time()
    
    # Tap Tempo
    tap_times = collections.deque(maxlen=5)
    last_tap_time = 0
    
    # Visual
    flash_alpha = 0

    running = True
    while running:
        current_time = time.time()
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Tap Logic
                    now = time.time()
                    if now - last_tap_time > 2.0:
                        tap_times.clear() # Reset if too long
                    
                    tap_times.append(now)
                    last_tap_time = now
                    
                    if len(tap_times) > 1:
                        intervals = [tap_times[i] - tap_times[i-1] for i in range(1, len(tap_times))]
                        avg_interval = sum(intervals) / len(intervals)
                        if avg_interval > 0:
                            bpm = 60.0 / avg_interval
                            # Restart metronome sync
                            if is_running:
                                next_tick_time = now + avg_interval
                            
                    flash_alpha = 255 # Flash on tap too
                    
                elif event.key == pygame.K_RETURN:
                    is_running = not is_running
                    if is_running:
                        next_tick_time = time.time()
                elif event.key == pygame.K_UP:
                    bpm += 1
                elif event.key == pygame.K_DOWN:
                    bpm = max(1, bpm - 1)
                elif event.key == pygame.K_RIGHT:
                    bpm += 5
                elif event.key == pygame.K_LEFT:
                    bpm = max(1, bpm - 5)

        # Metronome Logic
        if is_running:
            interval = 60.0 / bpm
            if current_time >= next_tick_time:
                high_beep.play()
                flash_alpha = 255
                # Drift correction: aim for the next expected slot strictly
                next_tick_time += interval
                # If we lag too much, just reset (unlikely in normal loop)
                if current_time > next_tick_time + 0.1:
                    next_tick_time = current_time + interval

        # Drawing
        screen.fill(BLACK)

        # Flash Effect
        if flash_alpha > 0:
            flash_surface = pygame.Surface((WIDTH, HEIGHT))
            flash_surface.fill(ACCENT)
            flash_surface.set_alpha(flash_alpha)
            screen.blit(flash_surface, (0, 0))
            flash_alpha = max(0, flash_alpha - 15)

        # Text
        status_text = "RUNNING" if is_running else "PAUSED"
        color = ACCENT if is_running else RED
        
        bpm_text = font_big.render(f"{int(bpm)} BPM", True, WHITE)
        status_render = font_small.render(f"[{status_text}]", True, color)
        info_text = font_small.render("SPACE: Tap | ENTER: Start/Stop | Arrows: Adjust", True, (150, 150, 150))

        screen.blit(bpm_text, (WIDTH//2 - bpm_text.get_width()//2, HEIGHT//2 - 50))
        screen.blit(status_render, (WIDTH//2 - status_render.get_width()//2, HEIGHT//2 + 30))
        screen.blit(info_text, (WIDTH//2 - info_text.get_width()//2, HEIGHT - 40))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
