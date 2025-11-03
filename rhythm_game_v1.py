import pygame
import sys
import random

window_resolution = (1280, 720)
fps_cap = 60

music_volume = 0.07

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (215, 215, 215)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode(window_resolution)
pygame.display.set_caption("PyRhythm v1")

# Load song data
pygame.mixer.init()
pygame.mixer.music.load('rhythm_game_v1_data/AcTuGmAtU3M.mp3')
print(f"vol: {pygame.mixer.music.get_volume()} * mult: {music_volume} =")
pygame.mixer.music.set_volume(pygame.mixer.music.get_volume() * music_volume)
print(f"volume: {pygame.mixer.music.get_volume()}")

try:
    with open('rhythm_game_v1_data/AcTuGmAtU3M.txt', 'r') as f:
        song_data = f.read()
except Exception as e:
    print(f"Error reading file: {e}")

print(song_data)
song_data = song_data.replace('(', '').replace(')', '').replace(' ', '').strip()
print(song_data)
song_data = song_data.split(",")
print(song_data)
song_data_ms = []
for i in song_data:
    ms = 0
    i = i.split(".")
    print(i, end=": ")
    ms += int(i[0]) * 60000
    ms += int(i[1]) * 1000
    ms += int(i[2])
    i = ms
    song_data_ms.append(i)
    print(i, end=", ")
print()
print(song_data_ms)


pygame.font.init()
title_font = pygame.font.SysFont('Comic Sans MS', 90)
score_font = pygame.font.SysFont('Comic Sans MS', 30)

current_game_state = 0
score = 0
current_note = 0
last_rad = 0
current_rad = 0
song_playing = False
beat_time = 0
last_beat_time = 0
music_elapsed = 0
new_beat = True
draw_red = False
game_hit = False
note_spawn_time = 0
rr = 235

# Game Loop Control
clock = pygame.time.Clock()
running = True

# Main Game Loop
while running:
    # Get HUD Input ---
    key_input = pygame.key.get_pressed()

    game_hit = False

    # Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # Clean up code would go here

        # Hit Logic
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # LMB
                game_hit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                game_hit = True


    # Escape To Menu                  MIGRATE?
    if key_input[pygame.K_ESCAPE]:
        current_game_state = 0

    # Main control ---                MIGRATE?
    if current_game_state == 0:
        if key_input[pygame.K_SPACE] or pygame.mouse.get_pressed()[0]:
            score = 0
            current_note = 0
            current_game_state = 1
            last_rad = 0
            current_rad = 0
            beat_time = 0
            last_beat_time = 0
            music_elapsed = 0
            new_beat = True
            draw_red = False
            game_hit = False
            note_spawn_time = 0
            rr = 235

    # # Call each sprite's update
    # all_sprites.update()

    # Drawing ---
    screen.fill(BLACK)  # Clear the screen with black
    # all_sprites.draw(screen)  # Draw all sprites

    # Menu ---
    if current_game_state == 0:
        # Draw texts
        text_surface_1 = title_font.render('Py', False, (255, 222, 87))
        text_surface_1_2 = title_font.render('Rhythm', False, (69, 132, 182))
        text_surface_1_3 = title_font.render('v1', False, (220, 220, 220))
        text_surface_2 = score_font.render('Controls: Space or Left Mouse Button & Escape', False, (220, 220, 220))
        text_surface_3 = score_font.render(f'Previous Score: {score}', False, (230, 230, 230))
        text_surface_4 = score_font.render('Made with love by Roadbobek <3', False, (rr, random.randint(90, 130), random.randint(90, 130)))
        text_surface_5 = score_font.render(f'DEMO BUILD  o.0', False, (220, 220, 220))
        if random.choice(('y', 'n', 'n', 'n', 'n')) == 'y':
            rr += 1
            if rr == 255:
                rr = 205
        screen.blit(text_surface_1, (150, 200))
        screen.blit(text_surface_1_2, (250, 200))
        screen.blit(text_surface_1_3, (610, 200))
        screen.blit(text_surface_2, (170, 340))
        screen.blit(text_surface_3, (170, 380))
        screen.blit(text_surface_4, (740, 620))
        screen.blit(text_surface_5, (200, 550))

    # Playing ---
    elif current_game_state == 1:
        # Play song
        if not song_playing:
            pygame.mixer.music.play(-1)
            song_playing = True

        # Draw beat circles
        if new_beat:
            note_spawn_time = music_elapsed
            current_note += 1
            new_beat = False

        music_elapsed = pygame.mixer.music.get_pos()
        beat_time = song_data_ms[current_note]
        last_beat_time = song_data_ms[current_note - 1] if current_note > 0 else 0
        time_gap_ms = beat_time - note_spawn_time
        if time_gap_ms <= 0: time_gap_ms = 1.0  # Safety check
        # time_gap_ms = beat_time - last_beat_time
        time_since_spawn = music_elapsed - note_spawn_time
        time_remaining_ms = beat_time - music_elapsed

        # if current_rad >= 430:
        #     last_rad = 0
        #     current_rad = 0

        if time_since_spawn >= 0: # v3
            # The core calculation: (Time Elapsed / Total Travel Time) * Final Size
            current_rad = (420 * (time_since_spawn / time_gap_ms))
        else:
            current_rad = 0.0

        # current_rad = 420 * ((time_gap_ms - time_remaining_ms) / time_gap_ms) # v2
        # last_rad = current_rad # v1

        print(f"time_remaining_ms {time_remaining_ms}")
        print(f"current_rad (before cap): {current_rad}")


        if current_rad > 420:
            current_rad = 420
            draw_red = True
            pygame.draw.circle(screen, RED, (window_resolution[0] // 2, window_resolution[1] // 2), current_rad, 0)
        if current_rad == 420:
            score *= 0.75
            new_beat = True
        elif current_rad != 420:
            pygame.draw.circle(screen, WHITE, (window_resolution[0] // 2, window_resolution[1] // 2), current_rad, 0)

        # Hit Logic
        if game_hit:
            if time_remaining_ms <= 200:
                score += 200 - time_remaining_ms
                new_beat = True
            elif 200 < time_remaining_ms <= 333:
                score *= 0.75
                new_beat = True

        print("score: ", score)

        # Draw stupid circle
        if draw_red:
            pygame.draw.circle(screen, WHITE, (window_resolution[0] // 2, window_resolution[1] // 2), 420, 4)
            pygame.draw.circle(screen, RED, (window_resolution[0] // 2, window_resolution[1] // 2), 458, 12)
            draw_red = False
        else:
            pygame.draw.circle(screen, WHITE, (window_resolution[0] // 2, window_resolution[1] // 2), 420, 4)
        draw_red = False

        # Draw Score
        text_surface = score_font.render(f'Score: {int(score)}', False, (220, 220, 220))
        screen.blit(text_surface, (100, 50))


    # Display Update
    pygame.display.flip()

    # Control the frame rate (for example 60 frames per second)
    clock.tick(fps_cap)

# Quit Pygame and exit the program
pygame.quit()
sys.exit()
