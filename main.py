import pygame
import numpy as np
import asyncio
import websockets

pygame.init()

# Set up the display
window_size = (640, 480)
screen = pygame.display.set_mode(window_size)

heading = 0  # Initialize heading variable

async def receive_heading():
    global heading
    try:
        async with websockets.connect("ws://172.20.10.10:8765") as websocket:
            print("WebSocket connection established.")
            while True:
                message = await websocket.recv()
                print(f"Received message: {message}")
                heading = float(message.split(":")[1].strip())
    except Exception as e:
        print(f"WebSocket connection error: {e}")

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
        screen.fill((255, 255, 255))  # Clear the screen

        draw_compass(screen, heading)  # Draw the compass with the updated heading

        pygame.display.flip()

        if pygame.key.get_pressed()[pygame.K_q]:
            break

        await asyncio.sleep(0.01)  # To prevent the loop from consuming too much CPU

    pygame.quit()

asyncio.run(main())