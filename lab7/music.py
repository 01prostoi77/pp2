import pygame
import os


pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Keyboard Music Player")


music_folder = r'C:\Users\Farkhat\Desktop\PP2\labworks\musicpapka'
playlist = [os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith('.mp3')]

if not playlist:
    print("No music files found in", music_folder)
    pygame.quit()
    exit()


current_track = 0
playing = True

def play_track(index):
    pygame.mixer.music.load(playlist[index])
    pygame.mixer.music.play()
    print("Now playing:", os.path.basename(playlist[index]))

def stop_track():
    pygame.mixer.music.stop()
    print("Music stopped.")

def next_track():
    global current_track
    current_track = (current_track + 1) % len(playlist)
    play_track(current_track)

def previous_track():
    global current_track
    current_track = (current_track - 1) % len(playlist)
    play_track(current_track)


play_track(current_track)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  
                if pygame.mixer.music.get_busy():
                    stop_track()
                    playing = False
                else:
                    play_track(current_track)
                    playing = True
            elif event.key == pygame.K_RIGHT:  
                next_track()
            elif event.key == pygame.K_LEFT:  
                previous_track()

pygame.quit()
