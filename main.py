import cv2
import pygame
import numpy as np
import asyncio
import websockets

pygame.init()
cap = cv2.VideoCapture(0)

window_size = (640, 480)
screen = pygame.display.set_mode(window_size)

heading = 0

async def receive_heading():
    global heading
    async with websockets.connect("ws://localhost:8765") as websocket:
        while True:
            message = await websocket.recv()
            heading = float(message.split(":")[1].strip())

def draw_compass(screen, heading):
    center = (window_size[0] // 2, window_size[1] // 2)
    length = 100
    end_pos = (
        center[0] + int(length * np.cos(np.radians(heading))),
        center[1] - int(length * np.sin(np.radians(heading)))
    )
    pygame.draw.line(screen, (255, 0, 0), center, end_pos, 5)

async def main():
    global heading

    # Start receiving heading in the background
    asyncio.create_task(receive_heading())

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        scale_factor = 0.5  # Adjust this value as needed
        frame = cv2.resize(frame, None, fx=scale_factor, fy=scale_factor)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame_surface = pygame.surfarray.make_surface(frame)

        frame_rect = frame_surface.get_rect(center=(window_size[0] // 2, window_size[1] // 2))

        screen.fill((255, 255, 255))
        screen.blit(frame_surface, frame_rect.topleft)

        draw_compass(screen, heading)

        pygame.display.flip()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.quit()

asyncio.run(main())