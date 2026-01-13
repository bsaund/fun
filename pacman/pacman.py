import pygame
import random
import sys
import math
from typing import List, Tuple, Optional, Union, Deque
from collections import deque

# Initialize Pygame
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Type aliases
Maze = List[List[int]]
Direction = Tuple[int, int]
Color = Tuple[int, int, int]
Position = Tuple[int, int]

# Constants
CELL_SIZE: int = 30
GRID_WIDTH: int = 19
GRID_HEIGHT: int = 21
WINDOW_WIDTH: int = CELL_SIZE * GRID_WIDTH
WINDOW_HEIGHT: int = CELL_SIZE * GRID_HEIGHT

# Colors
BLACK: Color = (0, 0, 0)
BLUE: Color = (0, 0, 255)
YELLOW: Color = (255, 255, 0)
WHITE: Color = (255, 255, 255)
RED: Color = (255, 0, 0)
GREEN: Color = (0, 255, 0)

# Game speed
FPS: int = 10
MIN_FPS: int = 3
MAX_FPS: int = 15
MOVE_SPEED: int = 5  # Pixels per frame for smooth movement

# Maze layout (1 = wall, 0 = path with dot, 2 = empty path, 3 = power pellet)
MAZE: Maze = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,3,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,3,1],
    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
    [1,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,0,1,1,1,2,1,2,1,1,1,0,1,1,1,1],
    [2,2,2,1,0,1,2,2,2,2,2,2,2,1,0,1,2,2,2],
    [1,1,1,1,0,1,2,1,1,2,1,1,2,1,0,1,1,1,1],
    [2,2,2,2,0,2,2,1,2,2,2,1,2,2,0,2,2,2,2],
    [1,1,1,1,0,1,2,1,1,1,1,1,2,1,0,1,1,1,1],
    [2,2,2,1,0,1,2,2,2,2,2,2,2,1,0,1,2,2,2],
    [1,1,1,1,0,1,2,1,1,1,1,1,2,1,0,1,1,1,1],
    [1,3,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,3,1],
    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
    [1,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,0,1,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,0,1,0,1,1,1,1,1,1,0,1],
    [1,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class Pacman:
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x  # Grid position
        self.y: int = y  # Grid position
        self.px: float = x * CELL_SIZE + CELL_SIZE // 2  # Pixel position
        self.py: float = y * CELL_SIZE + CELL_SIZE // 2  # Pixel position
        self.direction: Direction = (0, 0)
        self.next_direction: Direction = (0, 0)
        self.mouth_open: bool = True
        self.mouth_angle: int = 0
        
    def is_at_cell_center(self) -> bool:
        """Check if pacman is aligned with a cell center"""
        cell_center_x: float = self.x * CELL_SIZE + CELL_SIZE // 2
        cell_center_y: float = self.y * CELL_SIZE + CELL_SIZE // 2
        return abs(self.px - cell_center_x) < MOVE_SPEED and abs(self.py - cell_center_y) < MOVE_SPEED
        
    def update(self, maze: Maze) -> None:
        # Snap to cell center if close enough
        cell_center_x: float = self.x * CELL_SIZE + CELL_SIZE // 2
        cell_center_y: float = self.y * CELL_SIZE + CELL_SIZE // 2
        if abs(self.px - cell_center_x) < MOVE_SPEED:
            self.px = cell_center_x
        if abs(self.py - cell_center_y) < MOVE_SPEED:
            self.py = cell_center_y
        
        # Try to change direction if at cell center
        if self.is_at_cell_center():
            if self.can_move(self.next_direction, maze):
                self.direction = self.next_direction
        
        # Move in current direction if possible
        if self.direction != (0, 0) and self.can_move(self.direction, maze):
            # Move by pixels
            self.px += self.direction[0] * MOVE_SPEED
            self.py += self.direction[1] * MOVE_SPEED
            
            # Update grid position when crossing cell boundaries
            new_x: int = int(self.px // CELL_SIZE)
            new_y: int = int(self.py // CELL_SIZE)
            
            # Handle wrapping
            if new_x < 0:
                new_x = GRID_WIDTH - 1
                self.px = new_x * CELL_SIZE + CELL_SIZE // 2
            elif new_x >= GRID_WIDTH:
                new_x = 0
                self.px = new_x * CELL_SIZE + CELL_SIZE // 2
            if new_y < 0:
                new_y = GRID_HEIGHT - 1
                self.py = new_y * CELL_SIZE + CELL_SIZE // 2
            elif new_y >= GRID_HEIGHT:
                new_y = 0
                self.py = new_y * CELL_SIZE + CELL_SIZE // 2
            
            if new_x != self.x or new_y != self.y:
                self.x = new_x
                self.y = new_y
                # Snap to center of new cell
                self.px = self.x * CELL_SIZE + CELL_SIZE // 2
                self.py = self.y * CELL_SIZE + CELL_SIZE // 2
            
        # Animate mouth
        self.mouth_angle = (self.mouth_angle + 10) % 360
        
    def can_move(self, direction: Direction, maze: Maze) -> bool:
        if direction == (0, 0):
            return True
        new_x: int = self.x + direction[0]
        new_y: int = self.y + direction[1]
        
        # Wrap around screen edges
        if new_x < 0:
            new_x = GRID_WIDTH - 1
        if new_x >= GRID_WIDTH:
            new_x = 0
        if new_y < 0:
            new_y = GRID_HEIGHT - 1
        if new_y >= GRID_HEIGHT:
            new_y = 0
            
        # Check if it's a wall
        if maze[new_y][new_x] == 1:
            return False
        return True
    
    def draw(self, screen: pygame.Surface) -> None:
        center_x: int = int(self.px)
        center_y: int = int(self.py)
        radius: int = CELL_SIZE // 2 - 2
        
        # Draw pacman circle with mouth
        if self.direction == (0, 0) or self.mouth_angle % 60 < 30:
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius)
        else:
            # Calculate mouth opening based on direction
            start_angle: int = 0
            if self.direction == (1, 0):  # Right
                start_angle = 0
            elif self.direction == (-1, 0):  # Left
                start_angle = 180
            elif self.direction == (0, -1):  # Up
                start_angle = 90
            elif self.direction == (0, 1):  # Down
                start_angle = 270
                
            pygame.draw.circle(screen, YELLOW, (center_x, center_y), radius)
            # Draw mouth by drawing a triangle
            points: List[Tuple[int, int]] = [(center_x, center_y)]
            if self.direction == (1, 0):  # Right
                points.append((center_x + radius, center_y - radius // 2))
                points.append((center_x + radius, center_y + radius // 2))
            elif self.direction == (-1, 0):  # Left
                points.append((center_x - radius, center_y - radius // 2))
                points.append((center_x - radius, center_y + radius // 2))
            elif self.direction == (0, -1):  # Up
                points.append((center_x - radius // 2, center_y - radius))
                points.append((center_x + radius // 2, center_y - radius))
            elif self.direction == (0, 1):  # Down
                points.append((center_x - radius // 2, center_y + radius))
                points.append((center_x + radius // 2, center_y + radius))
            
            pygame.draw.polygon(screen, BLACK, points)

class Ghost:
    def __init__(self, x: int, y: int, color: Color, maze: Maze) -> None:
        self.x: int = x  # Grid position
        self.y: int = y  # Grid position
        self.px: float = x * CELL_SIZE + CELL_SIZE // 2  # Pixel position
        self.py: float = y * CELL_SIZE + CELL_SIZE // 2  # Pixel position
        self.start_x: int = x
        self.start_y: int = y
        self.color: Color = color
        self.original_color: Color = color
        # Initialize with a valid direction (one that can actually move)
        valid_dirs: List[Direction] = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        valid_dirs = [d for d in valid_dirs if self._can_move_direction(d, maze, x, y)]
        if valid_dirs:
            self.direction: Direction = random.choice(valid_dirs)
        else:
            self.direction = (0, 0)  # No valid direction, will be set on first update
        self.vulnerable: bool = False
        self.dead: bool = False
        self.path_to_start: List[Direction] = []  # Path to follow when dead
    
    def _can_move_direction(self, direction: Direction, maze: Maze, x: int, y: int) -> bool:
        """Helper to check if a direction is valid from a given position"""
        if direction == (0, 0):
            return True
        new_x: int = x + direction[0]
        new_y: int = y + direction[1]
        
        # Handle wrapping
        if new_x < 0:
            new_x = GRID_WIDTH - 1
        elif new_x >= GRID_WIDTH:
            new_x = 0
        if new_y < 0:
            new_y = GRID_HEIGHT - 1
        elif new_y >= GRID_HEIGHT:
            new_y = 0
            
        # Check if it's a wall
        if maze[new_y][new_x] == 1:
            return False
        return True
        
    def is_at_cell_center(self) -> bool:
        """Check if ghost is aligned with a cell center"""
        cell_center_x: float = self.x * CELL_SIZE + CELL_SIZE // 2
        cell_center_y: float = self.y * CELL_SIZE + CELL_SIZE // 2
        return abs(self.px - cell_center_x) < MOVE_SPEED and abs(self.py - cell_center_y) < MOVE_SPEED
    
    def find_path_to_start(self, maze: Maze) -> List[Direction]:
        """Use BFS to find the shortest path from current position to start position"""
        # BFS to find shortest path
        queue: Deque[Tuple[int, int, List[Direction]]] = deque([(self.x, self.y, [])])
        visited: set[Position] = {(self.x, self.y)}
        
        directions: List[Direction] = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        while queue:
            x, y, path = queue.popleft()
            
            # Check if we reached the start
            if x == self.start_x and y == self.start_y:
                return path
            
            # Try all four directions
            for dx, dy in directions:
                new_x: int = x + dx
                new_y: int = y + dy
                
                # Handle wrapping
                if new_x < 0:
                    new_x = GRID_WIDTH - 1
                elif new_x >= GRID_WIDTH:
                    new_x = 0
                if new_y < 0:
                    new_y = GRID_HEIGHT - 1
                elif new_y >= GRID_HEIGHT:
                    new_y = 0
                
                # Check if valid move (not a wall and not visited)
                if maze[new_y][new_x] != 1 and (new_x, new_y) not in visited:
                    visited.add((new_x, new_y))
                    new_path: List[Direction] = path + [(dx, dy)]
                    queue.append((new_x, new_y, new_path))
        
        # If no path found, return empty list
        return []
        
    def update(self, maze: Maze, vulnerable: bool = False) -> None:
        self.vulnerable = vulnerable
        
        # Snap to cell center if close enough
        cell_center_x: float = self.x * CELL_SIZE + CELL_SIZE // 2
        cell_center_y: float = self.y * CELL_SIZE + CELL_SIZE // 2
        if abs(self.px - cell_center_x) < MOVE_SPEED:
            self.px = cell_center_x
        if abs(self.py - cell_center_y) < MOVE_SPEED:
            self.py = cell_center_y
        
        # Check if we can move in current direction - if not, change direction immediately
        can_move_current: bool = self.can_move(self.direction, maze)
        
        # Only change direction when at cell center OR if current direction is blocked
        # For non-dead ghosts, also allow direction change more frequently to help them escape
        can_change_direction: bool = (
            self.is_at_cell_center() or 
            not can_move_current or 
            (not self.dead and self.direction == (0, 0))
        )
        
        if can_change_direction:
            if self.dead:
                # Return to starting position using pathfinding
                if self.x == self.start_x and self.y == self.start_y:
                    self.dead = False
                    self.path_to_start = []
                else:
                    # Recalculate path if we don't have one
                    if not self.path_to_start:
                        self.path_to_start = self.find_path_to_start(maze)
                    
                    # Follow the path
                    if self.path_to_start:
                        # Get the next direction from the path
                        next_direction: Direction = self.path_to_start[0]
                        if self.can_move(next_direction, maze):
                            self.direction = next_direction
                            # Remove the first step from the path since we're taking it
                            self.path_to_start.pop(0)
                    else:
                        # If pathfinding failed, fall back to simple approach
                        preferred_dirs: List[Direction] = []
                        if self.x < self.start_x:
                            preferred_dirs.append((1, 0))
                        elif self.x > self.start_x:
                            preferred_dirs.append((-1, 0))
                        if self.y < self.start_y:
                            preferred_dirs.append((0, 1))
                        elif self.y > self.start_y:
                            preferred_dirs.append((0, -1))
                        
                        # Try preferred directions first
                        moved: bool = False
                        for dir in preferred_dirs:
                            if self.can_move(dir, maze):
                                self.direction = dir
                                moved = True
                                break
                        
                        # If can't move in preferred direction, pick any valid direction
                        if not moved:
                            valid_dirs: List[Direction] = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                            valid_dirs = [d for d in valid_dirs if self.can_move(d, maze)]
                            if valid_dirs:
                                self.direction = random.choice(valid_dirs)
                            else:
                                # If truly stuck, try to snap to center and continue
                                self.px = self.x * CELL_SIZE + CELL_SIZE // 2
                                self.py = self.y * CELL_SIZE + CELL_SIZE // 2
                                return
            else:
                # Improved AI: at every path split (intersection), choose a random direction
                # but never go back the way you came
                # Get all valid directions from current position
                all_valid_dirs: List[Direction] = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                all_valid_dirs = [d for d in all_valid_dirs if self.can_move(d, maze)]
                
                if not all_valid_dirs:
                    # If truly stuck, snap to center
                    self.px = self.x * CELL_SIZE + CELL_SIZE // 2
                    self.py = self.y * CELL_SIZE + CELL_SIZE // 2
                    return
                
                # Calculate the "back" direction (opposite of current direction)
                back_direction: Direction = (-self.direction[0], -self.direction[1])
                
                # If at a cell center (path split), choose randomly from valid directions
                # but exclude going back the way we came
                if self.is_at_cell_center():
                    # At an intersection - choose random direction, but not back
                    forward_dirs: List[Direction] = [d for d in all_valid_dirs if d != back_direction]
                    # If we have forward options, use them; otherwise use all valid (dead end)
                    if forward_dirs:
                        self.direction = random.choice(forward_dirs)
                    else:
                        # Dead end - must go back
                        self.direction = random.choice(all_valid_dirs)
                elif not can_move_current or self.direction == (0, 0):
                    # Current direction blocked or no direction set - pick random valid direction
                    # but avoid going back if possible
                    forward_dirs = [d for d in all_valid_dirs if d != back_direction]
                    if forward_dirs:
                        self.direction = random.choice(forward_dirs)
                    else:
                        self.direction = random.choice(all_valid_dirs)
                # Otherwise, continue in current direction (ghost is between intersections)
                
        # Move in current direction if possible
        if self.can_move(self.direction, maze):
            # Move by pixels
            self.px += self.direction[0] * MOVE_SPEED
            self.py += self.direction[1] * MOVE_SPEED
            
            # Update grid position when crossing cell boundaries
            new_x: int = int(self.px // CELL_SIZE)
            new_y: int = int(self.py // CELL_SIZE)
            
            # Handle wrapping
            if new_x < 0:
                new_x = GRID_WIDTH - 1
                self.px = new_x * CELL_SIZE + CELL_SIZE // 2
            elif new_x >= GRID_WIDTH:
                new_x = 0
                self.px = new_x * CELL_SIZE + CELL_SIZE // 2
            if new_y < 0:
                new_y = GRID_HEIGHT - 1
                self.py = new_y * CELL_SIZE + CELL_SIZE // 2
            elif new_y >= GRID_HEIGHT:
                new_y = 0
                self.py = new_y * CELL_SIZE + CELL_SIZE // 2
            
            if new_x != self.x or new_y != self.y:
                self.x = new_x
                self.y = new_y
                # Snap to center of new cell
                self.px = self.x * CELL_SIZE + CELL_SIZE // 2
                self.py = self.y * CELL_SIZE + CELL_SIZE // 2
                
                # If dead and following a path, check if we need to recalculate
                if self.dead and self.path_to_start:
                    # If we've reached the start, clear the path
                    if self.x == self.start_x and self.y == self.start_y:
                        self.path_to_start = []
                    # Otherwise, if path seems wrong, recalculate
                    elif len(self.path_to_start) > 0:
                        # Verify the path is still valid by checking if next step makes sense
                        next_dir: Direction = self.path_to_start[0]
                        expected_x: int = self.x + next_dir[0]
                        expected_y: int = self.y + next_dir[1]
                        # Handle wrapping
                        if expected_x < 0:
                            expected_x = GRID_WIDTH - 1
                        elif expected_x >= GRID_WIDTH:
                            expected_x = 0
                        if expected_y < 0:
                            expected_y = GRID_HEIGHT - 1
                        elif expected_y >= GRID_HEIGHT:
                            expected_y = 0
                        
                        # If the next step would hit a wall, recalculate
                        if maze[expected_y][expected_x] == 1:
                            self.path_to_start = self.find_path_to_start(maze)
    
    def can_move(self, direction: Direction, maze: Maze) -> bool:
        new_x: int = self.x + direction[0]
        new_y: int = self.y + direction[1]
        
        # Wrap around screen edges
        if new_x < 0:
            new_x = GRID_WIDTH - 1
        if new_x >= GRID_WIDTH:
            new_x = 0
        if new_y < 0:
            new_y = GRID_HEIGHT - 1
        if new_y >= GRID_HEIGHT:
            new_y = 0
            
        # Check if it's a wall
        if maze[new_y][new_x] == 1:
            return False
        return True
    
    def draw(self, screen: pygame.Surface, power_pellet_timer: int = 0) -> None:
        center_x: int = int(self.px)
        center_y: int = int(self.py)
        width: int = CELL_SIZE - 4
        height: int = CELL_SIZE - 4
        
        # Choose color based on state
        color: Color
        if self.dead:
            color = (50, 50, 50)  # Dark gray when dead
        elif self.vulnerable:
            # Flash white when power pellet is about to expire (last 30 frames)
            FLASH_THRESHOLD: int = 30
            if power_pellet_timer > 0 and power_pellet_timer <= FLASH_THRESHOLD:
                # Flash between blue and white (every 5 frames)
                if (power_pellet_timer // 5) % 2 == 0:
                    color = (255, 255, 255)  # White when flashing
                else:
                    color = (100, 100, 255)  # Blue when vulnerable
            else:
                color = (100, 100, 255)  # Blue when vulnerable
        else:
            color = self.color
        
        # Draw ghost shape: rounded top with wavy bottom
        left: int = center_x - width // 2
        right: int = center_x + width // 2
        top: int = center_y - height // 2
        bottom: int = center_y + height // 2
        
        # Draw rounded head (top half)
        head_rect: pygame.Rect = pygame.Rect(left, top, width, height // 2 + 3)
        pygame.draw.ellipse(screen, color, head_rect)
        
        # Draw body rectangle (will be modified with wavy bottom)
        body_top: int = center_y
        body_bottom: int = bottom
        body_rect: pygame.Rect = pygame.Rect(left, body_top, width, height // 2)
        pygame.draw.rect(screen, color, body_rect)
        
        # Draw wavy bottom by drawing black rectangles to "cut out" waves
        wave_width: int = width // 3
        wave_height: int = 6
        wave_bottom: int = body_bottom
        
        # Cut out 3 waves from the bottom
        for i in range(3):
            wave_x: int = left + i * wave_width + wave_width // 4
            # Draw black rectangle to create wave indentation
            wave_cut: pygame.Rect = pygame.Rect(wave_x, wave_bottom - wave_height, wave_width // 2, wave_height + 1)
            pygame.draw.rect(screen, BLACK, wave_cut)
        
        # Redraw the rounded parts of waves
        for i in range(3):
            wave_x = left + i * wave_width + wave_width // 4
            # Draw small rounded tops for each wave
            wave_top_rect: pygame.Rect = pygame.Rect(wave_x, wave_bottom - wave_height - 2, wave_width // 2, wave_height + 2)
            pygame.draw.ellipse(screen, color, wave_top_rect)
        
        if not self.dead:
            # Draw eyes (two white circles with black pupils)
            eye_size: int = 4
            eye_y: int = center_y - height // 4
            left_eye_x: int = center_x - width // 4
            right_eye_x: int = center_x + width // 4
            
            # White part of eyes
            pygame.draw.circle(screen, WHITE, (left_eye_x, eye_y), eye_size)
            pygame.draw.circle(screen, WHITE, (right_eye_x, eye_y), eye_size)
            
            # Black pupils (look in direction of movement)
            pupil_size: int = 2
            pupil_offset_x: int = 0
            pupil_offset_y: int = 0
            if self.direction == (1, 0):  # Right
                pupil_offset_x = 1
            elif self.direction == (-1, 0):  # Left
                pupil_offset_x = -1
            elif self.direction == (0, -1):  # Up
                pupil_offset_y = -1
            elif self.direction == (0, 1):  # Down
                pupil_offset_y = 1
            
            pygame.draw.circle(screen, BLACK, (left_eye_x + pupil_offset_x, eye_y + pupil_offset_y), pupil_size)
            pygame.draw.circle(screen, BLACK, (right_eye_x + pupil_offset_x, eye_y + pupil_offset_y), pupil_size)

def draw_maze(screen: pygame.Surface, maze: Maze) -> None:
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect: pygame.Rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLUE, rect)
            elif maze[y][x] == 0:
                # Draw small dot
                center_x: int = x * CELL_SIZE + CELL_SIZE // 2
                center_y: int = y * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, WHITE, (center_x, center_y), 2)
            elif maze[y][x] == 3:
                # Draw power pellet (large dot)
                center_x = x * CELL_SIZE + CELL_SIZE // 2
                center_y = y * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, WHITE, (center_x, center_y), 6)

def count_dots(maze: Maze) -> int:
    count: int = 0
    for row in maze:
        count += row.count(0) + row.count(3)  # Count both regular dots and power pellets
    return count

class SpeedSlider:
    """A slider to control game speed"""
    def __init__(self, x: int, y: int, width: int, min_val: int, max_val: int, initial_val: int) -> None:
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = 20
        self.min_val: int = min_val
        self.max_val: int = max_val
        self.value: float = float(initial_val)
        self.dragging: bool = False
        self.handle_width: int = 15
        self.handle_height: int = 20
    
    def get_handle_x(self) -> int:
        """Get the x position of the slider handle"""
        ratio: float = (self.value - self.min_val) / (self.max_val - self.min_val)
        return int(self.x + ratio * (self.width - self.handle_width))
    
    def set_value_from_pos(self, mouse_x: int) -> None:
        """Set slider value based on mouse x position"""
        mouse_x = max(self.x, min(self.x + self.width - self.handle_width, mouse_x))
        ratio: float = (mouse_x - self.x) / (self.width - self.handle_width)
        self.value = self.min_val + ratio * (self.max_val - self.min_val)
        self.value = max(self.min_val, min(self.max_val, self.value))
    
    def is_clicked(self, mouse_x: int, mouse_y: int) -> bool:
        """Check if the slider handle is clicked"""
        handle_x: int = self.get_handle_x()
        return (handle_x <= mouse_x <= handle_x + self.handle_width and
                self.y <= mouse_y <= self.y + self.handle_height)
    
    def is_in_slider_area(self, mouse_x: int, mouse_y: int) -> bool:
        """Check if mouse is in the slider area"""
        return (self.x <= mouse_x <= self.x + self.width and
                self.y <= mouse_y <= self.y + self.height)
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the slider"""
        # Draw slider track
        track_rect: pygame.Rect = pygame.Rect(self.x, self.y + self.height // 2 - 2, self.width, 4)
        pygame.draw.rect(screen, WHITE, track_rect)
        
        # Draw slider handle
        handle_x: int = self.get_handle_x()
        handle_rect: pygame.Rect = pygame.Rect(handle_x, self.y, self.handle_width, self.handle_height)
        pygame.draw.rect(screen, YELLOW, handle_rect)
        pygame.draw.rect(screen, WHITE, handle_rect, 2)
        
        # Draw value label
        font: pygame.font.Font = pygame.font.Font(None, 24)
        value_text: pygame.Surface = font.render(f"Speed: {int(self.value)}", True, WHITE)
        screen.blit(value_text, (self.x, self.y - 25))

def create_waka_sound() -> Optional[pygame.mixer.Sound]:
    """Create a simple 'waka waka' sound effect"""
    try:
        import numpy as np
        sample_rate: int = 22050
        duration: float = 0.08  # seconds
        frames: int = int(sample_rate * duration)
        
        # Create a simple beep sound (sine wave)
        arr = np.zeros((frames, 2), dtype=np.int16)
        for i in range(frames):
            # Frequency modulation for "waka" effect
            t: float = float(i) / sample_rate
            freq: float = 440 + 150 * math.sin(t * 30)  # Varying frequency
            wave: float = 3000 * math.sin(freq * 2 * math.pi * t)
            # Add envelope to make it sound better
            envelope: float = 1.0 - (t / duration) * 0.3
            wave *= envelope
            wave_val: int = max(-32768, min(32767, int(wave)))  # Clamp to int16 range
            arr[i] = [wave_val, wave_val]
        
        sound: pygame.mixer.Sound = pygame.sndarray.make_sound(arr)
        return sound
    except ImportError:
        # If numpy not available, return None (sound will be skipped)
        return None

def main() -> None:
    screen: pygame.Surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pacman")
    clock: pygame.time.Clock = pygame.time.Clock()
    
    # Create a mutable copy of the maze
    maze: Maze = [row[:] for row in MAZE]
    
    # Initialize pacman
    pacman: Pacman = Pacman(9, 15)
    
    # Initialize ghosts (start them in accessible positions)
    ghosts: List[Ghost] = [
        Ghost(9, 9, RED, maze),
        Ghost(8, 9, (255, 184, 255), maze),  # Pink
        Ghost(10, 9, (0, 255, 255), maze),   # Cyan
        Ghost(9, 8, (255, 184, 82), maze),   # Orange
    ]
    
    score: int = 0
    total_dots: int = count_dots(maze)
    game_over: bool = False
    won: bool = False
    power_pellet_timer: int = 0
    POWER_PELLET_DURATION: int = 120  # frames (about 20 seconds at 6 FPS)
    
    font: pygame.font.Font = pygame.font.Font(None, 36)
    
    # Create sound effects
    waka_sound: Optional[pygame.mixer.Sound] = create_waka_sound()
    last_dot_collected: bool = False
    
    # Create speed slider
    slider: SpeedSlider = SpeedSlider(10, WINDOW_HEIGHT - 40, 200, MIN_FPS, MAX_FPS, FPS)
    current_fps: int = FPS
    
    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if slider.is_clicked(event.pos[0], event.pos[1]):
                        slider.dragging = True
                    elif slider.is_in_slider_area(event.pos[0], event.pos[1]):
                        # Clicked on slider track, move handle there
                        slider.set_value_from_pos(event.pos[0])
                        current_fps = int(slider.value)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    slider.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if slider.dragging:
                    slider.set_value_from_pos(event.pos[0])
                    current_fps = int(slider.value)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.next_direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    pacman.next_direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    pacman.next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    pacman.next_direction = (1, 0)
                elif event.key == pygame.K_r and game_over:
                    # Restart game
                    maze = [row[:] for row in MAZE]
                    pacman = Pacman(9, 15)
                    ghosts = [
                        Ghost(9, 9, RED, maze),
                        Ghost(8, 9, (255, 184, 255), maze),
                        Ghost(10, 9, (0, 255, 255), maze),
                        Ghost(9, 8, (255, 184, 82), maze),
                    ]
                    score = 0
                    total_dots = count_dots(maze)
                    game_over = False
                    won = False
                    power_pellet_timer = 0
        
        if not game_over:
            # Update power pellet timer
            if power_pellet_timer > 0:
                power_pellet_timer -= 1
            
            # Update game state
            pacman.update(maze)
            
            # Check if pacman collected a dot
            dot_collected: bool = False
            if maze[pacman.y][pacman.x] == 0:
                maze[pacman.y][pacman.x] = 2
                score += 10
                total_dots -= 1
                dot_collected = True
            elif maze[pacman.y][pacman.x] == 3:
                # Power pellet collected
                maze[pacman.y][pacman.x] = 2
                score += 50
                total_dots -= 1
                power_pellet_timer = POWER_PELLET_DURATION
                dot_collected = True
            
            # Play waka sound when collecting dots
            if dot_collected and not last_dot_collected and waka_sound:
                waka_sound.play()
            last_dot_collected = dot_collected
            
            # Update ghosts
            is_vulnerable: bool = power_pellet_timer > 0
            for ghost in ghosts:
                ghost.update(maze, vulnerable=is_vulnerable)
            
            # Check collision with ghosts (using pixel distance for smooth collision)
            collision_distance: float = CELL_SIZE // 2
            for ghost in ghosts:
                dx: float = pacman.px - ghost.px
                dy: float = pacman.py - ghost.py
                distance: float = (dx * dx + dy * dy) ** 0.5
                if distance < collision_distance:
                    if ghost.vulnerable and not ghost.dead:
                        # Eat the ghost
                        ghost.dead = True
                        # Calculate path back to start
                        ghost.path_to_start = ghost.find_path_to_start(maze)
                        score += 200
                    elif not ghost.dead:
                        # Pacman caught by ghost
                        game_over = True
                        won = False
                        break
                
            # Check if all dots collected
            if total_dots == 0:
                game_over = True
                won = True
        
        # Draw everything
        screen.fill(BLACK)
        draw_maze(screen, maze)
        
        if not game_over:
            pacman.draw(screen)
            for ghost in ghosts:
                ghost.draw(screen, power_pellet_timer)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw speed slider
        slider.draw(screen)
        
        # Draw game over message
        if game_over:
            if won:
                game_over_text = font.render("You Win! Press R to restart", True, GREEN)
            else:
                game_over_text = font.render("Game Over! Press R to restart", True, RED)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()
        clock.tick(current_fps)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
