import os
import numpy as np
import keyboard
import time
from typing import Tuple

class MinecraftConsole:
    def __init__(self, world_size: Tuple[int, int, int] = (10, 10, 10)):
        self.world_size = world_size
        # Initialize world with air (0), some ground blocks (1), and random trees (2)
        self.world = np.zeros(world_size, dtype=int)
        
        # Create ground
        self.world[:, :, 0] = 1
        
        # Add some random trees
        for _ in range(5):
            x = np.random.randint(1, world_size[0]-1)
            y = np.random.randint(1, world_size[1]-1)
            height = np.random.randint(3, 6)
            self.world[x, y, 1:height] = 2
        
        # Player position (start in middle of map, on top of ground)
        self.player_pos = [world_size[0]//2, world_size[1]//2, 1]
        self.block_types = {
            0: ' ',  # Air
            1: '▓',  # Ground
            2: '♠',  # Tree
            3: '☺'   # Player
        }

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_view_slice(self):
        # Get a 2D slice of the world at player's level
        return self.world[:, :, self.player_pos[2]]

    def draw(self):
        self.clear_screen()
        view = self.get_view_slice()
        
        # Create a copy of the view to add player
        display = view.copy()
        display[self.player_pos[0], self.player_pos[1]] = 3
        
        # Draw the world
        print(f"Position: x={self.player_pos[0]} y={self.player_pos[1]} z={self.player_pos[2]}")
        print("Use WASD to move, Q/E to move up/down, X to exit")
        print("─" * (self.world_size[1] * 2 + 2))
        
        for row in display:
            print("│", end="")
            for cell in row:
                print(self.block_types[cell] * 2, end="")
            print("│")
        
        print("─" * (self.world_size[1] * 2 + 2))

    def move_player(self, dx=0, dy=0, dz=0):
        new_pos = [
            self.player_pos[0] + dx,
            self.player_pos[1] + dy,
            self.player_pos[2] + dz
        ]
        
        # Check boundaries
        if (0 <= new_pos[0] < self.world_size[0] and
            0 <= new_pos[1] < self.world_size[1] and
            0 <= new_pos[2] < self.world_size[2]):
            
            # Check if new position is not occupied by a block
            if self.world[new_pos[0], new_pos[1], new_pos[2]] == 0:
                self.player_pos = new_pos

    def run(self):
        print("Welcome to Console Minecraft!")
        print("Loading world...")
        time.sleep(1)
        
        while True:
            self.draw()
            
            if keyboard.is_pressed('w'):
                self.move_player(dx=-1)
            elif keyboard.is_pressed('s'):
                self.move_player(dx=1)
            elif keyboard.is_pressed('a'):
                self.move_player(dy=-1)
            elif keyboard.is_pressed('d'):
                self.move_player(dy=1)
            elif keyboard.is_pressed('q'):
                self.move_player(dz=1)
            elif keyboard.is_pressed('e'):
                self.move_player(dz=-1)
            elif keyboard.is_pressed('x'):
                print("Thanks for playing!")
                break
            
            time.sleep(0.1)

if __name__ == "__main__":
    game = MinecraftConsole()
    game.run()