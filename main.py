import cv2
import pygame
import numpy as np

pygame.init()
cap = cv2.VideoCapture(0)

window_size = (640, 480)
screen = pygame.display.set_mode(window_size)

def draw_compass(screen, heading):
    center = (window_size[0] // 2, window_size[1] // 2)
    length = 100
    end_pos = (
        center[0] + int(length * np.cos(np.radians(heading))),
        center[1] - int(length * np.sin(np.radians(heading)))
    )

    pygame.draw.line(screen, (255, 0, 0), center, end_pos, 5)

heading = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    scale_factor = 0.5
    frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame_surface = pygame.surfarray.make_surface(frame)
    frame_rect = frame_surface.get_rect(center=(window_size[0] // 2, window_size[1] // 2))

    screen.fill((255, 255, 255))
    screen.blit(frame_surface, frame_rect.topleft)

    draw_compass(screen, heading)
    heading += 1

    pygame.display.flip()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()