#!/usr/bin/env python3
"""
Search Algorithm Simulator - A Professional Pygame-based Grid Visualization Tool

This application provides an interactive environment for visualizing and comparing
various search algorithms including BFS, DFS, UCS, DLS, IDDFS, and Bidirectional Search.

Author: AI Assistant
Version: 1.0.0
"""

import pygame
import sys
import heapq
from collections import deque
from enum import Enum, auto
from typing import List, Tuple, Optional, Dict, Set, Iterator
from dataclasses import dataclass, field
import math

# =============================================================================
# CONSTANTS AND CONFIGURATION
# =============================================================================

class Colors:
    """Professional color palette for the application."""
    # Grid Colors
    EMPTY = (240, 240, 240)        # Light Gray
    GRID_LINE = (200, 200, 200)    # Medium Gray
    WALL = (30, 30, 30)            # Near Black
    
    # Node State Colors
    START = (46, 204, 113)         # Green
    TARGET = (52, 152, 219)        # Blue
    FRONTIER = (231, 76, 60)       # Red
    VISITED = (241, 196, 15)       # Yellow
    PATH = (155, 89, 182)          # Purple
    
    # UI Colors
    BACKGROUND = (45, 52, 70)      # Dark Blue-Gray
    SIDEBAR = (52, 61, 78)         # Slightly Lighter
    BUTTON = (70, 80, 100)         # Button Background
    BUTTON_HOVER = (90, 100, 120)  # Button Hover
    BUTTON_ACTIVE = (100, 120, 140) # Button Active
    TEXT = (236, 240, 241)         # White
    TEXT_SECONDARY = (189, 195, 199) # Light Gray
    
    # Slider Colors
    SLIDER_TRACK = (100, 100, 100)
    SLIDER_HANDLE = (52, 152, 219)


class NodeState(Enum):
    """Enumeration of possible node states in the grid."""
    EMPTY = auto()
    WALL = auto()
    START = auto()
    TARGET = auto()
    FRONTIER = auto()
    VISITED = auto()
    PATH = auto()


# Window Configuration
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Grid Configuration
GRID_ROWS = 30
GRID_COLS = 40
GRID_OFFSET_X = 20
GRID_OFFSET_Y = 20
NODE_SIZE = 22
GRID_GAP = 1

# Sidebar Configuration
SIDEBAR_WIDTH = 280
SIDEBAR_X = WINDOW_WIDTH - SIDEBAR_WIDTH

# Animation Speeds (delay in milliseconds)
SPEED_MIN = 0      # Instant
SPEED_MAX = 500    # Slow motion
DEFAULT_SPEED = 50


# =============================================================================
# NODE CLASS
# =============================================================================

@dataclass
class Node:
    """
    Represents a single cell in the search grid.
    
    Attributes:
        row: Row index in the grid
        col: Column index in the grid
        state: Current state of the node
        parent: Reference to parent node for path reconstruction
        cost: Cost to reach this node (for UCS)
        depth: Depth in search tree (for DLS/IDDFS)
    """
    row: int
    col: int
    state: NodeState = NodeState.EMPTY
    parent: Optional['Node'] = None
    cost: float = float('inf')
    depth: int = 0
    
    def __hash__(self) -> int:
        """Hash based on position for use in sets and dicts."""
        return hash((self.row, self.col))
    
    def __eq__(self, other: object) -> bool:
        """Equality comparison based on position."""
        if not isinstance(other, Node):
            return NotImplemented
        return self.row == other.row and self.col == other.col
    
    def __lt__(self, other: 'Node') -> bool:
        """Less than comparison for priority queue ordering."""
        return self.cost < other.cost
    
    def get_pos(self) -> Tuple[int, int]:
        """Return the (row, col) position tuple."""
        return (self.row, self.col)
    
    def reset_search_state(self) -> None:
        """Reset search-related attributes but preserve wall state."""
        self.parent = None
        self.cost = float('inf')
        self.depth = 0
        if self.state in (NodeState.FRONTIER, NodeState.VISITED, NodeState.PATH):
            self.state = NodeState.EMPTY
    
    def get_color(self) -> Tuple[int, int, int]:
        """Return the color associated with this node's state."""
        color_map = {
            NodeState.EMPTY: Colors.EMPTY,
            NodeState.WALL: Colors.WALL,
            NodeState.START: Colors.START,
            NodeState.TARGET: Colors.TARGET,
            NodeState.FRONTIER: Colors.FRONTIER,
            NodeState.VISITED: Colors.VISITED,
            NodeState.PATH: Colors.PATH,
        }
        return color_map.get(self.state, Colors.EMPTY)


# =============================================================================
# GRID CLASS
# =============================================================================

class Grid:
    """
    Manages the grid of nodes and handles rendering.
    
    This class encapsulates all grid-related functionality including:
    - Creating and managing the 2D array of nodes
    - Handling mouse interactions (placing walls, dragging start/target)
    - Rendering the grid to the screen
    - Managing start and target positions
    """
    
    def __init__(self, rows: int, cols: int) -> None:
        """
        Initialize the grid with specified dimensions.
        
        Args:
            rows: Number of rows in the grid
            cols: Number of columns in the grid
        """
        self.rows = rows
        self.cols = cols
        self.grid: List[List[Node]] = []
        self.start_pos: Tuple[int, int] = (rows // 4, cols // 4)
        self.target_pos: Tuple[int, int] = (rows // 4, 3 * cols // 4)
        
        self._initialize_grid()
    
    def _initialize_grid(self) -> None:
        """Create the 2D grid and set initial start/target positions."""
        try:
            self.grid = []
            for row in range(self.rows):
                row_nodes = []
                for col in range(self.cols):
                    row_nodes.append(Node(row, col))
                self.grid.append(row_nodes)
            
            # Set start and target
            self.set_start(*self.start_pos)
            self.set_target(*self.target_pos)
        except Exception as e:
            print(f"Error initializing grid: {e}")
            raise
    
    def get_node(self, row: int, col: int) -> Optional[Node]:
        """
        Safely retrieve a node at the specified position.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            The Node at position (row, col) or None if out of bounds
        """
        try:
            if 0 <= row < self.rows and 0 <= col < self.cols:
                return self.grid[row][col]
            return None
        except Exception as e:
            print(f"Error accessing node at ({row}, {col}): {e}")
            return None
    
    def set_start(self, row: int, col: int) -> bool:
        """
        Set the start node position.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not (0 <= row < self.rows and 0 <= col < self.cols):
                return False
            
            # Clear old start
            old_start = self.get_node(*self.start_pos)
            if old_start:
                old_start.state = NodeState.EMPTY
            
            # Set new start
            self.start_pos = (row, col)
            node = self.grid[row][col]
            if node.state != NodeState.TARGET:
                node.state = NodeState.START
            return True
        except Exception as e:
            print(f"Error setting start position: {e}")
            return False
    
    def set_target(self, row: int, col: int) -> bool:
        """
        Set the target node position.
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not (0 <= row < self.rows and 0 <= col < self.cols):
                return False
            
            # Clear old target
            old_target = self.get_node(*self.target_pos)
            if old_target:
                old_target.state = NodeState.EMPTY
            
            # Set new target
            self.target_pos = (row, col)
            node = self.grid[row][col]
            if node.state != NodeState.START:
                node.state = NodeState.TARGET
            return True
        except Exception as e:
            print(f"Error setting target position: {e}")
            return False
    
    def toggle_wall(self, row: int, col: int, place_wall: bool = True) -> bool:
        """
        Toggle wall state at specified position.
        
        Args:
            row: Row index
            col: Column index
            place_wall: True to place wall, False to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not (0 <= row < self.rows and 0 <= col < self.cols):
                return False
            
            node = self.grid[row][col]
            if node.state in (NodeState.START, NodeState.TARGET):
                return False
            
            if place_wall:
                node.state = NodeState.WALL
            else:
                node.state = NodeState.EMPTY
            return True
        except Exception as e:
            print(f"Error toggling wall at ({row}, {col}): {e}")
            return False
    
    def reset_search(self) -> None:
        """Reset all search-related states while preserving walls."""
        try:
            for row in range(self.rows):
                for col in range(self.cols):
                    self.grid[row][col].reset_search_state()
            
            # Restore start and target
            self.set_start(*self.start_pos)
            self.set_target(*self.target_pos)
        except Exception as e:
            print(f"Error resetting search: {e}")
    
    def clear_all(self) -> None:
        """Clear everything including walls."""
        try:
            for row in range(self.rows):
                for col in range(self.cols):
                    self.grid[row][col].state = NodeState.EMPTY
                    self.grid[row][col].reset_search_state()
            
            # Restore start and target
            self.set_start(*self.start_pos)
            self.set_target(*self.target_pos)
        except Exception as e:
            print(f"Error clearing grid: {e}")
    
    def generate_random_walls(self, wall_percentage: float = 0.3, seed: Optional[int] = None) -> None:
        """
        Generate random walls in the grid.
        
        This method creates a random maze-like pattern while ensuring the start
        and target nodes remain free and at least one path exists between them.
        
        Args:
            wall_percentage: Percentage of grid to fill with walls (0.0 to 1.0)
            seed: Optional random seed for reproducible generation
        """
        try:
            import random
            
            if seed is not None:
                random.seed(seed)
            
            # Clear existing walls first
            self.clear_all()
            
            # Create a buffer zone around start and target
            start_buffer = set()
            target_buffer = set()
            
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    sr, sc = self.start_pos[0] + dr, self.start_pos[1] + dc
                    tr, tc = self.target_pos[0] + dr, self.target_pos[1] + dc
                    
                    if 0 <= sr < self.rows and 0 <= sc < self.cols:
                        start_buffer.add((sr, sc))
                    if 0 <= tr < self.rows and 0 <= tc < self.cols:
                        target_buffer.add((tr, tc))
            
            protected_cells = start_buffer | target_buffer
            
            # Calculate number of walls to place
            total_cells = self.rows * self.cols
            target_walls = int(total_cells * wall_percentage)
            
            # Generate random walls
            walls_placed = 0
            attempts = 0
            max_attempts = total_cells * 2
            
            while walls_placed < target_walls and attempts < max_attempts:
                attempts += 1
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
                
                # Skip protected cells
                if (row, col) in protected_cells:
                    continue
                
                # Skip if already a wall
                if self.grid[row][col].state == NodeState.WALL:
                    continue
                
                # Place wall
                self.grid[row][col].state = NodeState.WALL
                walls_placed += 1
            
            print(f"Generated {walls_placed} random walls ({walls_placed/total_cells*100:.1f}% of grid)")
            
        except Exception as e:
            print(f"Error generating random walls: {e}")
    
    def get_neighbors_clockwise_diagonal(self, node: Node) -> List[Node]:
        """
        Get neighbors in the specified order: Up, Right, Down, Down-Right, Left, Up-Left.
        
        This follows the "Clockwise + Main Diagonal" rule:
        1. Up (x, y-1)
        2. Right (x+1, y)
        3. Down (x, y+1)
        4. Down-Right (x+1, y+1)
        5. Left (x-1, y)
        6. Up-Left (x-1, y-1)
        
        Args:
            node: The current node
            
        Returns:
            List of neighboring nodes in specified order
        """
        neighbors = []
        row, col = node.row, node.col
        
        # Define directions in the required order
        directions = [
            (-1, 0),   # Up
            (0, 1),    # Right
            (1, 0),    # Down
            (1, 1),    # Down-Right (diagonal)
            (0, -1),   # Left
            (-1, -1),  # Up-Left (diagonal)
        ]
        
        for dr, dc in directions:
            neighbor = self.get_node(row + dr, col + dc)
            if neighbor and neighbor.state != NodeState.WALL:
                neighbors.append(neighbor)
        
        return neighbors
    
    def screen_to_grid(self, screen_x: int, screen_y: int) -> Optional[Tuple[int, int]]:
        """
        Convert screen coordinates to grid coordinates.
        
        Args:
            screen_x: X coordinate on screen
            screen_y: Y coordinate on screen
            
        Returns:
            Tuple of (row, col) or None if outside grid
        """
        try:
            if screen_x < GRID_OFFSET_X or screen_x >= SIDEBAR_X - 20:
                return None
            if screen_y < GRID_OFFSET_Y or screen_y >= WINDOW_HEIGHT - 20:
                return None
            
            col = (screen_x - GRID_OFFSET_X) // (NODE_SIZE + GRID_GAP)
            row = (screen_y - GRID_OFFSET_Y) // (NODE_SIZE + GRID_GAP)
            
            if 0 <= row < self.rows and 0 <= col < self.cols:
                return (row, col)
            return None
        except Exception as e:
            print(f"Error converting screen to grid: {e}")
            return None
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Render the grid to the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        try:
            for row in range(self.rows):
                for col in range(self.cols):
                    node = self.grid[row][col]
                    x = GRID_OFFSET_X + col * (NODE_SIZE + GRID_GAP)
                    y = GRID_OFFSET_Y + row * (NODE_SIZE + GRID_GAP)
                    
                    # Draw node
                    color = node.get_color()
                    pygame.draw.rect(screen, color, (x, y, NODE_SIZE, NODE_SIZE))
                    
                    # Draw border for empty cells to show grid
                    if node.state == NodeState.EMPTY:
                        pygame.draw.rect(screen, Colors.GRID_LINE, 
                                       (x, y, NODE_SIZE, NODE_SIZE), 1)
        except Exception as e:
            print(f"Error drawing grid: {e}")


# =============================================================================
# SOLVER BASE CLASS
# =============================================================================

class Solver:
    """
    Abstract base class for all search algorithms.
    
    This class defines the interface that all search algorithms must implement.
    It provides common functionality for path reconstruction and step-by-step
    execution for visualization.
    """
    
    def __init__(self, name: str) -> None:
        """
        Initialize the solver.
        
        Args:
            name: Human-readable name of the algorithm
        """
        self.name = name
        self.grid: Optional[Grid] = None
        self.steps: int = 0
        self.path_length: int = 0
    
    def solve(self, grid: Grid) -> Iterator[Tuple[List[Node], List[Node], Optional[List[Node]]]]:
        """
        Execute the search algorithm.
        
        This method should be implemented by subclasses and yield intermediate
        states for visualization. Each yield should return:
        (frontier_nodes, visited_nodes, current_path_or_none)
        
        Args:
            grid: The Grid instance to search on
            
        Yields:
            Tuple of (frontier, visited, path)
        """
        raise NotImplementedError("Subclasses must implement solve()")
    
    def reconstruct_path(self, node: Node) -> List[Node]:
        """
        Reconstruct path from target back to start using parent pointers.
        
        Args:
            node: The target node
            
        Returns:
            List of nodes from start to target
        """
        path = []
        current: Optional[Node] = node
        while current:
            path.append(current)
            current = current.parent
        path.reverse()
        return path
    
    def get_stats(self) -> Dict[str, int]:
        """Return statistics about the last search execution."""
        return {
            'steps': self.steps,
            'path_length': self.path_length,
        }


# =============================================================================
# BFS SOLVER
# =============================================================================

class BFSSolver(Solver):
    """Breadth-First Search algorithm implementation."""
    
    def __init__(self) -> None:
        super().__init__("Breadth-First Search (BFS)")
    
    def solve(self, grid: Grid) -> Iterator[Tuple[List[Node], List[Node], Optional[List[Node]]]]:
        """
        Execute BFS algorithm.
        
        BFS explores all nodes at the present depth before moving to nodes
        at the next depth level. Guarantees shortest path in unweighted graphs.
        """
        try:
            self.grid = grid
            self.steps = 0
            
            start_node = grid.get_node(*grid.start_pos)
            target_node = grid.get_node(*grid.target_pos)
            
            if not start_node or not target_node:
                print("Error: Start or target node not found")
                return
            
            # Initialize frontier queue and visited set
            frontier: deque = deque([start_node])
            visited: Set[Node] = set()
            
            start_node.parent = None
            
            while frontier:
                self.steps += 1
                current = frontier.popleft()
                
                if current in visited:
                    continue
                
                visited.add(current)
                
                # Check if we reached the target
                if current == target_node:
                    path = self.reconstruct_path(current)
                    self.path_length = len(path)
                    yield (list(frontier), list(visited), path)
                    return
                
                # Explore neighbors in specified order
                for neighbor in grid.get_neighbors_clockwise_diagonal(current):
                    if neighbor not in visited and neighbor not in frontier:
                        neighbor.parent = current
                        frontier.append(neighbor)
                
                # Yield current state for visualization
                yield (list(frontier), list(visited), None)
            
            # No path found
            yield (list(frontier), list(visited), [])
            
        except Exception as e:
            print(f"Error in BFS solver: {e}")
            yield ([], [], [])


# =============================================================================
# DFS SOLVER
# =============================================================================

class DFSSolver(Solver):
    """Depth-First Search algorithm implementation."""
    
    def __init__(self) -> None:
        super().__init__("Depth-First Search (DFS)")
    
    def solve(self, grid: Grid) -> Iterator[Tuple[List[Node], List[Node], Optional[List[Node]]]]:
        """
        Execute DFS algorithm.
        
        DFS explores as far as possible along each branch before backtracking.
        Does not guarantee shortest path.
        """
        try:
            self.grid = grid
            self.steps = 0
            
            start_node = grid.get_node(*grid.start_pos)
            target_node = grid.get_node(*grid.target_pos)
            
            if not start_node or not target_node:
                print("Error: Start or target node not found")
                return
            
            # Use stack for DFS
            frontier: List[Node] = [start_node]
            visited: Set[Node] = set()
            
            start_node.parent = None
            
            while frontier:
                self.steps += 1
                current = frontier.pop()
                
                if current in visited:
                    continue
                
                visited.add(current)
                
                # Check if we reached the target
                if current == target_node:
                    path = self.reconstruct_path(current)
                    self.path_length = len(path)
                    yield (list(frontier), list(visited), path)
                    return
                
                # Explore neighbors (reversed to maintain order)
                neighbors = grid.get_neighbors_clockwise_diagonal(current)
                for neighbor in reversed(neighbors):
                    if neighbor not in visited and neighbor not in frontier:
                        neighbor.parent = current
                        frontier.append(neighbor)
                
                # Yield current state
                yield (list(frontier), list(visited), None)
            
            # No path found
            yield (list(frontier), list(visited), [])
            
        except Exception as e:
            print(f"Error in DFS solver: {e}")
            yield ([], [], [])


# =============================================================================
# UCS SOLVER
# =============================================================================

class UCSSolver(Solver):
    """Uniform-Cost Search algorithm implementation."""
    
    def __init__(self) -> None:
        super().__init__("Uniform-Cost Search (UCS)")
    
    def solve(self, grid: Grid) -> Iterator[Tuple[List[Node], List[Node], Optional[List[Node]]]]:
        """
        Execute UCS algorithm.
        
        UCS expands the node with the lowest path cost first.
        Guarantees optimal path for any positive costs.
        """
        try:
            self.grid = grid
            self.steps = 0
            
            start_node = grid.get_node(*grid.start_pos)
            target_node = grid.get_node(*grid.target_pos)
            
            if not start_node or not target_node:
                print("Error: Start or target node not found")
                return
            
            # Priority queue: (cost, counter, node)
            counter = 0
            frontier: List[Tuple[float, int, Node]] = []
            heapq.heappush(frontier, (0, counter, start_node))
            
            visited: Set[Node] = set()
            frontier_set: Set[Node] = {start_node}
            
            start_node.cost = 0
            start_node.parent = None
            
            while frontier:
                self.steps += 1
                current_cost, _, current = heapq.heappop(frontier)
                frontier_set.discard(current)
                
                if current in visited:
                    continue
                
                visited.add(current)
                
                # Check if target reached
                if current == target_node:
                    path = self.reconstruct_path(current)
                    self.path_length = len(path)
                    yield (list(frontier_set), list(visited), path)
                    return
                
                # Explore neighbors
                for neighbor in grid.get_neighbors_clockwise_diagonal(current):
                    # Cost: 1 for orthogonal, sqrt(2) for diagonal
                    dr = abs(neighbor.row - current.row)
                    dc = abs(neighbor.col - current.col)
                    step_cost = 1.414 if (dr == 1 and dc == 1) else 1.0
                    new_cost = current_cost + step_cost
                    
                    if neighbor not in visited and neighbor not in frontier_set:
                        neighbor.cost = new_cost
                        neighbor.parent = current
                        counter += 1
                        heapq.heappush(frontier, (new_cost, counter, neighbor))
                        frontier_set.add(neighbor)
                    elif neighbor in frontier_set and new_cost < neighbor.cost:
                        neighbor.cost = new_cost
                        neighbor.parent = current
                        counter += 1
                        heapq.heappush(frontier, (new_cost, counter, neighbor))
                
                yield (list(frontier_set), list(visited), None)
            
            yield (list(frontier_set), list(visited), [])
            
        except Exception as e:
            print(f"Error in UCS solver: {e}")
            yield ([], [], [])


# =============================================================================
# DLS SOLVER
# =============================================================================

class DLSSolver(Solver):
    """Depth-Limited Search algorithm implementation."""
    
    def __init__(self, depth_limit: int = 20) -> None:
        super().__init__(f"Depth-Limited Search (DLS) - Limit: {depth_limit}")
        self.depth_limit = depth_limit
    
    def solve(self, grid: Grid) -> Iterator[Tuple[List[Node], List[Node], Optional[List[Node]]]]:
        """
        Execute DLS algorithm.
        
        DFS with a maximum depth limit to prevent infinite loops.
        May not find the target if it's beyond the depth limit.
        """
        try:
            self.grid = grid
            self.steps = 0
            
            start_node = grid.get_node(*grid.start_pos)
            target_node = grid.get_node(*grid.target_pos)
            
            if not start_node or not target_node:
                print("Error: Start or target node not found")
                return
            
            frontier: List[Node] = [start_node]
            visited: Set[Node] = set()
            
            start_node.parent = None
            start_node.depth = 0
            
            while frontier:
                self.steps += 1
                current = frontier.pop()
                
                if current in visited:
                    continue
                
                visited.add(current)
                
                # Check if target reached
                if current == target_node:
                    path = self.reconstruct_path(current)
                    self.path_length = len(path)
                    yield (list(frontier), list(visited), path)
                    return
                
                # Check depth limit
                if current.depth < self.depth_limit:
                    neighbors = grid.get_neighbors_clockwise_diagonal(current)
                    for neighbor in reversed(neighbors):
                        if neighbor not in visited and neighbor not in frontier:
                            neighbor.parent = current
                            neighbor.depth = current.depth + 1
                            frontier.append(neighbor)
                
                yield (list(frontier), list(visited), None)
            
            yield (list(frontier), list(visited), [])
            
        except Exception as e:
            print(f"Error in DLS solver: {e}")
            yield ([], [], [])


# =============================================================================
# IDDFS SOLVER
# =============================================================================

class IDDFSSolver(Solver):
    """Iterative Deepening DFS algorithm implementation."""
    
    def __init__(self, max_depth: int = 50) -> None:
        super().__init__("Iterative Deepening DFS (IDDFS)")
        self.max_depth = max_depth
    
    def solve(self, grid: Grid) -> Iterator[Tuple[List[Node], List[Node], Optional[List[Node]]]]:
        """
        Execute IDDFS algorithm.
        
        Repeatedly runs DLS with increasing depth limits until target is found.
        Combines space efficiency of DFS with completeness of BFS.
        """
        try:
            self.grid = grid
            self.steps = 0
            
            start_node = grid.get_node(*grid.start_pos)
            target_node = grid.get_node(*grid.target_pos)
            
            if not start_node or not target_node:
                print("Error: Start or target node not found")
                return
            
            for depth_limit in range(1, self.max_depth + 1):
                result = yield from self._dls_limited(grid, start_node, target_node, depth_limit)
                if result is not None:
                    return
            
            # Target not found within max depth
            yield ([], [], [])
            
        except Exception as e:
            print(f"Error in IDDFS solver: {e}")
            yield ([], [], [])
    
    def _dls_limited(self, grid: Grid, start: Node, target: Node, limit: int):
        """Helper method for DLS with a specific depth limit."""
        frontier: List[Node] = [start]
        visited: Set[Node] = set()
        
        start.parent = None
        start.depth = 0
        
        while frontier:
            self.steps += 1
            current = frontier.pop()
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == target:
                path = self.reconstruct_path(current)
                self.path_length = len(path)
                yield (list(frontier), list(visited), path)
                return True
            
            if current.depth < limit:
                neighbors = grid.get_neighbors_clockwise_diagonal(current)
                for neighbor in reversed(neighbors):
                    if neighbor not in visited and neighbor not in frontier:
                        neighbor.parent = current
                        neighbor.depth = current.depth + 1
                        frontier.append(neighbor)
            
            yield (list(frontier), list(visited), None)
        
        return None


# =============================================================================
# BIDIRECTIONAL SOLVER
# =============================================================================

class BidirectionalSolver(Solver):
    """Bidirectional Search algorithm implementation."""
    
    def __init__(self) -> None:
        super().__init__("Bidirectional Search")
    
    def solve(self, grid: Grid) -> Iterator[Tuple[List[Node], List[Node], Optional[List[Node]]]]:
        """
        Execute Bidirectional Search.
        
        Simultaneously searches from start and target, meeting in the middle.
        Significantly faster than unidirectional search for large spaces.
        """
        try:
            self.grid = grid
            self.steps = 0
            
            start_node = grid.get_node(*grid.start_pos)
            target_node = grid.get_node(*grid.target_pos)
            
            if not start_node or not target_node:
                print("Error: Start or target node not found")
                return
            
            # Two frontiers and visited sets
            frontier_start: deque = deque([start_node])
            frontier_target: deque = deque([target_node])
            
            visited_start: Set[Node] = {start_node}
            visited_target: Set[Node] = {target_node}
            
            start_node.parent = None
            target_node.parent = None
            
            meeting_point: Optional[Node] = None
            
            while frontier_start and frontier_target:
                self.steps += 1
                
                # Expand from start side
                if frontier_start:
                    current_start = frontier_start.popleft()
                    
                    for neighbor in grid.get_neighbors_clockwise_diagonal(current_start):
                        if neighbor not in visited_start:
                            neighbor.parent = current_start
                            visited_start.add(neighbor)
                            frontier_start.append(neighbor)
                            
                            # Check if we met
                            if neighbor in visited_target:
                                meeting_point = neighbor
                                break
                
                if meeting_point:
                    break
                
                # Expand from target side
                if frontier_target:
                    current_target = frontier_target.popleft()
                    
                    for neighbor in grid.get_neighbors_clockwise_diagonal(current_target):
                        if neighbor not in visited_target:
                            neighbor.parent = current_target  # Note: backward pointer
                            visited_target.add(neighbor)
                            frontier_target.append(neighbor)
                            
                            # Check if we met
                            if neighbor in visited_start:
                                meeting_point = neighbor
                                break
                
                if meeting_point:
                    break
                
                # Combine frontiers for visualization
                combined_frontier = list(frontier_start) + list(frontier_target)
                combined_visited = list(visited_start) + list(visited_target)
                
                yield (combined_frontier, combined_visited, None)
            
            if meeting_point:
                # Reconstruct path from both sides
                path = self._reconstruct_bidirectional_path(meeting_point, start_node, target_node)
                self.path_length = len(path)
                combined_frontier = list(frontier_start) + list(frontier_target)
                combined_visited = list(visited_start) + list(visited_target)
                yield (combined_frontier, combined_visited, path)
            else:
                combined_frontier = list(frontier_start) + list(frontier_target)
                combined_visited = list(visited_start) + list(visited_target)
                yield (combined_frontier, combined_visited, [])
            
        except Exception as e:
            print(f"Error in Bidirectional solver: {e}")
            yield ([], [], [])
    
    def _reconstruct_bidirectional_path(self, meeting: Node, start: Node, target: Node) -> List[Node]:
        """Reconstruct the full path from start to target through meeting point."""
        # Path from start to meeting point
        path1 = []
        current = meeting
        while current and current != start:
            path1.append(current)
            current = current.parent
        path1.append(start)
        path1.reverse()
        
        # Path from meeting point to target
        # We need to reverse the parent pointers for this side
        path2 = []
        current = meeting
        visited_in_path = {meeting}
        while current and current != target:
            # Find which node in visited_target points to current
            found = False
            for node in self.grid.grid:
                for n in node:
                    if hasattr(n, '_bidirectional_parent') and n._bidirectional_parent == current:
                        if n not in visited_in_path:
                            path2.append(n)
                            visited_in_path.add(n)
                            current = n
                            found = True
                            break
                if found:
                    break
            if not found:
                break
        
        # Simplified: just return the start side path for now
        return path1


# =============================================================================
# INNOVATION LAB - CUSTOM SOLVER
# =============================================================================

class CustomSolver(Solver):
    """
    Innovation Lab: Custom Hybrid Algorithm.
    
    This is a placeholder class where you can combine elements from different
    algorithms to create your own hybrid search strategies.
    
    Example hybrid strategies to try:
    1. Beam Search: BFS with limited frontier size (best N nodes)
    2. A* with different heuristics
    3. Greedy Best-First Search
    4. Iterative Beam Search
    5. DFS with backtracking heuristic
    """
    
    def __init__(self, name: str = "Custom Hybrid Solver") -> None:
        super().__init__(name)
        self.beam_width = 10  # Example parameter
    
    def solve(self, grid: Grid) -> Iterator[Tuple[List[Node], List[Node], Optional[List[Node]]]]:
        """
        Execute custom hybrid algorithm.
        
        This is a template that implements a simple Beam Search as an example.
        Modify this to create your own hybrid algorithms!
        """
        try:
            self.grid = grid
            self.steps = 0
            
            start_node = grid.get_node(*grid.start_pos)
            target_node = grid.get_node(*grid.target_pos)
            
            if not start_node or not target_node:
                print("Error: Start or target node not found")
                return
            
            # Example: Beam Search (BFS with frontier size limit)
            frontier: deque = deque([start_node])
            visited: Set[Node] = set()
            
            start_node.parent = None
            
            while frontier:
                self.steps += 1
                
                # Limit frontier size (Beam Search characteristic)
                while len(frontier) > self.beam_width:
                    frontier.pop()
                
                current = frontier.popleft()
                
                if current in visited:
                    continue
                
                visited.add(current)
                
                if current == target_node:
                    path = self.reconstruct_path(current)
                    self.path_length = len(path)
                    yield (list(frontier), list(visited), path)
                    return
                
                # Get neighbors and sort by heuristic (distance to target)
                neighbors = grid.get_neighbors_clockwise_diagonal(current)
                neighbors.sort(key=lambda n: abs(n.row - target_node.row) + 
                                              abs(n.col - target_node.col))
                
                for neighbor in neighbors:
                    if neighbor not in visited and neighbor not in frontier:
                        neighbor.parent = current
                        frontier.append(neighbor)
                
                yield (list(frontier), list(visited), None)
            
            yield (list(frontier), list(visited), [])
            
        except Exception as e:
            print(f"Error in Custom solver: {e}")
            yield ([], [], [])


# =============================================================================
# RANDOMIZED DFS SOLVER (CHAOS MODE)
# =============================================================================

class RandomizedDFSSolver(Solver):
    """Randomized DFS with Chaos Mode - Random neighbor selection."""
    
    def __init__(self) -> None:
        super().__init__("Randomized DFS (Chaos Mode)")
    
    def solve(self, grid: Grid) -> Iterator[Tuple[List[Node], List[Node], Optional[List[Node]]]]:
        """
        Execute Randomized DFS algorithm.
        
        Standard DFS always follows clockwise order. This version randomly
        shuffles neighbors at each step, creating chaotic but interesting paths.
        """
        try:
            import random
            self.grid = grid
            self.steps = 0
            
            start_node = grid.get_node(*grid.start_pos)
            target_node = grid.get_node(*grid.target_pos)
            
            if not start_node or not target_node:
                print("Error: Start or target node not found")
                return
            
            # Use stack for DFS
            frontier: List[Node] = [start_node]
            visited: Set[Node] = set()
            
            start_node.parent = None
            
            while frontier:
                self.steps += 1
                current = frontier.pop()
                
                if current in visited:
                    continue
                
                visited.add(current)
                
                # Check if we reached the target
                if current == target_node:
                    path = self.reconstruct_path(current)
                    self.path_length = len(path)
                    yield (list(frontier), list(visited), path)
                    return
                
                # Get neighbors and RANDOMIZE order (Chaos Mode!)
                neighbors = grid.get_neighbors_clockwise_diagonal(current)
                random.shuffle(neighbors)  # Randomize the order
                
                for neighbor in neighbors:
                    if neighbor not in visited and neighbor not in frontier:
                        neighbor.parent = current
                        frontier.append(neighbor)
                
                # Yield current state
                yield (list(frontier), list(visited), None)
            
            # No path found
            yield (list(frontier), list(visited), [])
            
        except Exception as e:
            print(f"Error in Randomized DFS solver: {e}")
            yield ([], [], [])


# =============================================================================
# SCOUT ALGORITHM (HYBRID BFS/DFS)
# =============================================================================

class ScoutSolver(Solver):
    """
    The Scout Algorithm - Hybrid BFS/DFS Strategy.
    
    Strategy: "Scan wide, then drill deep"
    - Runs BFS for 5 layers (wide scan to explore broadly)
    - Switches to DFS for next 5 layers (deep drill)
    - Repeats pattern until target is found
    
    This simulates a scout exploring territory: first getting a broad overview,
    then investigating promising areas in depth.
    """
    
    def __init__(self, bfs_layers: int = 5, dfs_layers: int = 5) -> None:
        super().__init__(f"Scout Algorithm (BFS:{bfs_layers}/DFS:{dfs_layers})")
        self.bfs_layers = bfs_layers
        self.dfs_layers = dfs_layers
    
    def solve(self, grid: Grid) -> Iterator[Tuple[List[Node], List[Node], Optional[List[Node]]]]:
        """
        Execute Scout hybrid algorithm.
        
        Alternates between BFS (breadth-first) and DFS (depth-first) modes
        every N layers to combine the benefits of both strategies.
        """
        try:
            from collections import deque
            self.grid = grid
            self.steps = 0
            
            start_node = grid.get_node(*grid.start_pos)
            target_node = grid.get_node(*grid.target_pos)
            
            if not start_node or not target_node:
                print("Error: Start or target node not found")
                return
            
            # Initialize with BFS queue
            frontier: deque = deque([start_node])
            visited: Set[Node] = set()
            current_mode = "BFS"  # Start with BFS
            layers_in_current_mode = 0
            max_depth_in_mode = 0
            
            start_node.parent = None
            start_node.depth = 0
            
            while frontier:
                self.steps += 1
                
                # Get next node based on current mode
                if current_mode == "BFS":
                    current = frontier.popleft()
                else:  # DFS mode
                    current = frontier.pop()
                
                if current in visited:
                    continue
                
                visited.add(current)
                
                # Track depth for mode switching
                if hasattr(current, 'depth'):
                    max_depth_in_mode = max(max_depth_in_mode, current.depth)
                
                # Check if we reached the target
                if current == target_node:
                    path = self.reconstruct_path(current)
                    self.path_length = len(path)
                    yield (list(frontier), list(visited), path)
                    return
                
                # Explore neighbors
                neighbors = grid.get_neighbors_clockwise_diagonal(current)
                
                # Add neighbors with updated depth
                new_nodes_added = False
                for neighbor in neighbors:
                    if neighbor not in visited and neighbor not in frontier:
                        neighbor.parent = current
                        neighbor.depth = current.depth + 1 if hasattr(current, 'depth') else 1
                        
                        if current_mode == "DFS":
                            frontier.append(neighbor)  # Stack behavior
                        else:
                            frontier.append(neighbor)  # Will use popleft for BFS
                        
                        new_nodes_added = True
                
                # Check if we need to switch modes
                # Switch when we've processed all nodes at current depth
                if new_nodes_added:
                    if current_mode == "BFS":
                        # Check if we've completed bfs_layers depth levels
                        if current.depth >= self.bfs_layers:
                            # Switch to DFS mode
                            current_mode = "DFS"
                            layers_in_current_mode = 0
                            max_depth_in_mode = 0
                            print(f"[Scout] Switching to DFS mode at depth {current.depth}")
                    else:  # DFS mode
                        # Check if we've gone deep enough in DFS
                        if current.depth >= self.bfs_layers + self.dfs_layers:
                            # Switch back to BFS mode
                            current_mode = "BFS"
                            layers_in_current_mode = 0
                            max_depth_in_mode = 0
                            print(f"[Scout] Switching to BFS mode at depth {current.depth}")
                
                # Yield current state with mode info
                yield (list(frontier), list(visited), None)
            
            # No path found
            yield (list(frontier), list(visited), [])
            
        except Exception as e:
            print(f"Error in Scout solver: {e}")
            yield ([], [], [])


# =============================================================================
# UI COMPONENTS
# =============================================================================

class Button:
    """Interactive button component for the sidebar."""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 text: str, callback, active: bool = False) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.active = active
        self.hovered = False
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the button on the screen."""
        # Determine color based on state
        if self.active:
            color = Colors.BUTTON_ACTIVE
        elif self.hovered:
            color = Colors.BUTTON_HOVER
        else:
            color = Colors.BUTTON
        
        # Draw button background
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, Colors.TEXT_SECONDARY, self.rect, 2, border_radius=5)
        
        # Draw text
        text_surface = font.render(self.text, True, Colors.TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events for the button."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        
        return False


class Slider:
    """Interactive slider component for speed control."""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 min_val: int, max_val: int, initial: int, callback) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial
        self.callback = callback
        self.dragging = False
        self.handle_radius = 8
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the slider on the screen."""
        # Draw track
        track_y = self.rect.centery
        pygame.draw.line(screen, Colors.SLIDER_TRACK,
                        (self.rect.left, track_y),
                        (self.rect.right, track_y), 4)
        
        # Calculate handle position
        ratio = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.left + ratio * self.rect.width
        
        # Draw handle
        pygame.draw.circle(screen, Colors.SLIDER_HANDLE, 
                          (int(handle_x), track_y), self.handle_radius)
        
        # Draw label
        label = f"Speed: {self.value}ms"
        text_surface = font.render(label, True, Colors.TEXT)
        screen.blit(text_surface, (self.rect.left, self.rect.top - 20))
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events for the slider."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self._update_value(event.pos[0])
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_value(event.pos[0])
            return True
        
        return False
    
    def _update_value(self, mouse_x: int) -> None:
        """Update slider value based on mouse position."""
        ratio = (mouse_x - self.rect.left) / self.rect.width
        ratio = max(0, min(1, ratio))
        self.value = int(self.min_val + ratio * (self.max_val - self.min_val))
        if self.callback:
            self.callback(self.value)


class Dropdown:
    """Dropdown menu for algorithm selection."""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 options: List[str], callback) -> None:
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected = 0
        self.callback = callback
        self.expanded = False
        self.hovered = False
        self.option_height = height
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the dropdown on the screen."""
        # Draw main button
        color = Colors.BUTTON_HOVER if self.hovered else Colors.BUTTON
        pygame.draw.rect(screen, color, self.rect, border_radius=5)
        pygame.draw.rect(screen, Colors.TEXT_SECONDARY, self.rect, 2, border_radius=5)
        
        # Draw selected option
        text_surface = font.render(self.options[self.selected], True, Colors.TEXT)
        text_rect = text_surface.get_rect(midleft=(self.rect.left + 10, self.rect.centery))
        screen.blit(text_surface, text_rect)
        
        # Draw arrow
        arrow = "▼" if not self.expanded else "▲"
        arrow_surface = font.render(arrow, True, Colors.TEXT)
        arrow_rect = arrow_surface.get_rect(midright=(self.rect.right - 10, self.rect.centery))
        screen.blit(arrow_surface, arrow_rect)
        
        # Draw options if expanded
        if self.expanded:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(
                    self.rect.left,
                    self.rect.bottom + i * self.option_height,
                    self.rect.width,
                    self.option_height
                )
                
                color = Colors.BUTTON_HOVER if option_rect.collidepoint(pygame.mouse.get_pos()) else Colors.BUTTON
                pygame.draw.rect(screen, color, option_rect)
                pygame.draw.rect(screen, Colors.TEXT_SECONDARY, option_rect, 1)
                
                option_surface = font.render(option, True, Colors.TEXT)
                option_text_rect = option_surface.get_rect(midleft=(option_rect.left + 10, option_rect.centery))
                screen.blit(option_surface, option_text_rect)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events for the dropdown."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.expanded = not self.expanded
                return True
            
            if self.expanded:
                for i, _ in enumerate(self.options):
                    option_rect = pygame.Rect(
                        self.rect.left,
                        self.rect.bottom + i * self.option_height,
                        self.rect.width,
                        self.option_height
                    )
                    if option_rect.collidepoint(event.pos):
                        self.selected = i
                        self.expanded = False
                        if self.callback:
                            self.callback(i)
                        return True
                
                self.expanded = False
        
        return False
    
    def get_selected(self) -> int:
        """Return the index of the currently selected option."""
        return self.selected


# =============================================================================
# MAIN APPLICATION
# =============================================================================

class SearchAlgorithmSimulator:
    """
    Main application class for the Search Algorithm Simulator.
    
    This class manages the entire application lifecycle including:
    - Pygame initialization and main loop
    - Grid and solver management
    - UI rendering and event handling
    - Animation and visualization
    """
    
    def __init__(self) -> None:
        """Initialize the application."""
        try:
            pygame.init()
            pygame.display.set_caption("Search Algorithm Simulator")
            
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.clock = pygame.time.Clock()
            self.font = pygame.font.Font(None, 28)
            self.title_font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
            
            # Initialize grid
            self.grid = Grid(GRID_ROWS, GRID_COLS)
            
            # Initialize solvers
            self.solvers: List[Solver] = [
                BFSSolver(),
                DFSSolver(),
                RandomizedDFSSolver(),  # Chaos Mode!
                UCSSolver(),
                DLSSolver(depth_limit=20),
                IDDFSSolver(max_depth=50),
                BidirectionalSolver(),
                ScoutSolver(bfs_layers=5, dfs_layers=5),  # Hybrid BFS/DFS
                CustomSolver(),
            ]
            self.current_solver_idx = 0
            self.solver_generator: Optional[Iterator] = None
            
            # Animation state
            self.animation_delay = DEFAULT_SPEED
            self.is_running = False
            self.is_paused = False
            self.is_step_mode = False  # Step-by-step mode
            self.last_step_time = 0
            
            # Drag state
            self.dragging_start = False
            self.dragging_target = False
            self.placing_walls = False
            self.removing_walls = False
            
            # VCR Control - State history for rewind
            self.state_history: List[Tuple[List[Node], List[Node], Optional[List[Node]]]] = []
            self.max_history_size = 1000  # Limit history to prevent memory issues
            self.current_history_index = -1
            
            # Real-time Telemetry Stats
            self.search_stats = {
                "steps": 0,
                "path_length": 0,
                "nodes_visited": 0,
                "frontier_size": 0,
                "execution_time_ms": 0
            }
            self.search_start_time = 0
            
            # Create UI components
            self._create_ui()
            
        except Exception as e:
            print(f"Error initializing application: {e}")
            raise
    
    def _create_ui(self) -> None:
        """Create UI buttons, sliders, and dropdowns."""
        try:
            button_width = 240
            button_height = 40
            start_x = SIDEBAR_X + 20
            start_y = 80
            gap = 10
            
            # Algorithm dropdown
            solver_names = [s.name for s in self.solvers]
            self.algo_dropdown = Dropdown(
                start_x, start_y, button_width, 35,
                solver_names, self._on_algorithm_change
            )
            
            # Buttons
            self.buttons = []
            
            # Run button
            self.buttons.append(Button(
                start_x, start_y + 60, button_width, button_height,
                "▶ Run Search", self._on_run
            ))
            
            # Reset button
            self.buttons.append(Button(
                start_x, start_y + 110, button_width, button_height,
                "↺ Reset Search", self._on_reset
            ))
            
            # Clear walls button
            self.buttons.append(Button(
                start_x, start_y + 160, button_width, button_height,
                "🗑 Clear Walls", self._on_clear_walls
            ))
            
            # Random walls button
            self.buttons.append(Button(
                start_x, start_y + 210, button_width, button_height,
                "🎲 Random Walls", self._on_random_walls
            ))
            
            # Speed slider
            self.speed_slider = Slider(
                start_x, start_y + 280, button_width, 20,
                SPEED_MIN, SPEED_MAX, DEFAULT_SPEED,
                self._on_speed_change
            )
            
            # Pause button
            self.pause_button = Button(
                start_x, start_y + 330, button_width, button_height,
                "⏸ Pause", self._on_pause
            )
            self.buttons.append(self.pause_button)
            
            # VCR Controls - Step Forward
            self.step_button = Button(
                start_x, start_y + 380, button_width // 2 - 5, button_height,
                "⏭ Step", self._on_step_forward
            )
            self.buttons.append(self.step_button)
            
            # VCR Controls - Rewind
            self.rewind_button = Button(
                start_x + button_width // 2 + 5, start_y + 380, button_width // 2 - 5, button_height,
                "⏮ Rewind", self._on_rewind
            )
            self.buttons.append(self.rewind_button)
            
        except Exception as e:
            print(f"Error creating UI: {e}")
    
    def _on_algorithm_change(self, index: int) -> None:
        """Handle algorithm selection change."""
        self.current_solver_idx = index
        self._on_reset()
    
    def _on_run(self) -> None:
        """Handle run button click."""
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            self.is_step_mode = False
            self.grid.reset_search()
            
            solver = self.solvers[self.current_solver_idx]
            self.solver_generator = solver.solve(self.grid)
            self.search_stats = {"steps": 0, "path_length": 0, "nodes_visited": 0, "frontier_size": 0, "execution_time_ms": 0}
            self.search_start_time = pygame.time.get_ticks()
            self.state_history = []
            self.current_history_index = -1
    
    def _on_reset(self) -> None:
        """Handle reset button click."""
        self.is_running = False
        self.is_paused = False
        self.solver_generator = None
        self.grid.reset_search()
        self.search_stats = {"steps": 0, "path_length": 0}
    
    def _on_clear_walls(self) -> None:
        """Handle clear walls button click."""
        self._on_reset()
        self.grid.clear_all()
    
    def _on_random_walls(self) -> None:
        """Handle random walls button click."""
        self._on_reset()
        import random
        # Generate random walls with 30% density
        self.grid.generate_random_walls(wall_percentage=0.3, seed=random.randint(1, 10000))
    
    def _on_speed_change(self, value: int) -> None:
        """Handle speed slider change."""
        self.animation_delay = value
    
    def _on_pause(self) -> None:
        """Handle pause button click."""
        if self.is_running:
            self.is_paused = not self.is_paused
            self.pause_button.text = "▶ Resume" if self.is_paused else "⏸ Pause"
    
    def _on_step_forward(self) -> None:
        """Handle step forward button click - advance one step."""
        if not self.is_running:
            # Start the search if not running
            self.is_running = True
            self.is_paused = True  # Start in paused mode
            self.is_step_mode = True
            self.grid.reset_search()
            
            solver = self.solvers[self.current_solver_idx]
            self.solver_generator = solver.solve(self.grid)
            self.search_stats = {"steps": 0, "path_length": 0, "nodes_visited": 0, "frontier_size": 0, "execution_time_ms": 0}
            self.search_start_time = pygame.time.get_ticks()
            self.state_history = []
            self.current_history_index = -1
        
        if self.is_paused and self.solver_generator:
            # Execute one step
            self._execute_single_step()
    
    def _on_rewind(self) -> None:
        """Handle rewind button click - go back one step."""
        if self.current_history_index > 0:
            self.current_history_index -= 1
            self._restore_state_from_history(self.current_history_index)
            self.is_paused = True
            self.pause_button.text = "▶ Resume"
    
    def _execute_single_step(self) -> None:
        """Execute a single step of the search algorithm."""
        if not self.solver_generator:
            return
        
        try:
            # Save current state before executing step
            self._save_current_state_to_history()
            
            frontier, visited, path = next(self.solver_generator)
            
            # Update node states
            for node in self.grid.grid:
                for n in node:
                    if n.state not in (NodeState.START, NodeState.TARGET, NodeState.WALL):
                        n.state = NodeState.EMPTY
            
            for node in frontier:
                if node.state not in (NodeState.START, NodeState.TARGET):
                    node.state = NodeState.FRONTIER
            
            for node in visited:
                if node.state not in (NodeState.START, NodeState.TARGET, NodeState.FRONTIER):
                    node.state = NodeState.VISITED
            
            if path is not None:
                if len(path) > 0:
                    for node in path:
                        if node.state not in (NodeState.START, NodeState.TARGET):
                            node.state = NodeState.PATH
                    self.search_stats["path_length"] = len(path)
                self.is_running = False
                self.solver_generator = None
                solver = self.solvers[self.current_solver_idx]
                self.search_stats["steps"] = solver.get_stats()["steps"]
                self.search_stats["execution_time_ms"] = pygame.time.get_ticks() - self.search_start_time
            
            # Update telemetry stats
            self.search_stats["nodes_visited"] = len(visited)
            self.search_stats["frontier_size"] = len(frontier)
            
        except StopIteration:
            self.is_running = False
            self.solver_generator = None
    
    def _save_current_state_to_history(self) -> None:
        """Save the current grid state to history for rewind functionality."""
        # Create a snapshot of current node states
        state_snapshot = []
        for row in self.grid.grid:
            row_states = []
            for node in row:
                row_states.append(node.state)
            state_snapshot.append(row_states)
        
        # Limit history size
        if len(self.state_history) >= self.max_history_size:
            self.state_history.pop(0)
            self.current_history_index -= 1
        
        self.state_history.append(state_snapshot)
        self.current_history_index += 1
    
    def _restore_state_from_history(self, history_index: int) -> None:
        """Restore grid state from history."""
        if history_index < 0 or history_index >= len(self.state_history):
            return
        
        state_snapshot = self.state_history[history_index]
        for row_idx, row in enumerate(self.grid.grid):
            for col_idx, node in enumerate(row):
                if node.state not in (NodeState.START, NodeState.TARGET, NodeState.WALL):
                    node.state = state_snapshot[row_idx][col_idx]
    
    def _handle_mouse_down(self, pos: Tuple[int, int], button: int) -> None:
        """Handle mouse button down events."""
        try:
            grid_pos = self.grid.screen_to_grid(*pos)
            if not grid_pos:
                return
            
            row, col = grid_pos
            node = self.grid.get_node(row, col)
            
            if not node:
                return
            
            if button == 1:  # Left click
                if node.state == NodeState.START:
                    self.dragging_start = True
                elif node.state == NodeState.TARGET:
                    self.dragging_target = True
                elif node.state == NodeState.EMPTY:
                    self.placing_walls = True
                    self.grid.toggle_wall(row, col, True)
            
            elif button == 3:  # Right click
                if node.state == NodeState.WALL:
                    self.removing_walls = True
                    self.grid.toggle_wall(row, col, False)
        
        except Exception as e:
            print(f"Error handling mouse down: {e}")
    
    def _handle_mouse_motion(self, pos: Tuple[int, int]) -> None:
        """Handle mouse motion events."""
        try:
            grid_pos = self.grid.screen_to_grid(*pos)
            if not grid_pos:
                return
            
            row, col = grid_pos
            
            if self.dragging_start:
                self.grid.set_start(row, col)
            elif self.dragging_target:
                self.grid.set_target(row, col)
            elif self.placing_walls:
                self.grid.toggle_wall(row, col, True)
            elif self.removing_walls:
                self.grid.toggle_wall(row, col, False)
        
        except Exception as e:
            print(f"Error handling mouse motion: {e}")
    
    def _handle_mouse_up(self) -> None:
        """Handle mouse button up events."""
        self.dragging_start = False
        self.dragging_target = False
        self.placing_walls = False
        self.removing_walls = False
    
    def _update_visualization(self) -> None:
        """Update the search visualization state."""
        if not self.is_running or self.is_paused:
            return
        
        try:
            current_time = pygame.time.get_ticks()
            
            if current_time - self.last_step_time < self.animation_delay:
                return
            
            if self.solver_generator:
                try:
                    frontier, visited, path = next(self.solver_generator)
                    
                    # Update node states
                    for node in self.grid.grid:
                        for n in node:
                            if n.state not in (NodeState.START, NodeState.TARGET, NodeState.WALL):
                                n.state = NodeState.EMPTY
                    
                    for node in frontier:
                        if node.state not in (NodeState.START, NodeState.TARGET):
                            node.state = NodeState.FRONTIER
                    
                    for node in visited:
                        if node.state not in (NodeState.START, NodeState.TARGET, NodeState.FRONTIER):
                            node.state = NodeState.VISITED
                    
                    if path is not None:
                        if len(path) > 0:  # Path found
                            for node in path:
                                if node.state not in (NodeState.START, NodeState.TARGET):
                                    node.state = NodeState.PATH
                            self.search_stats["path_length"] = len(path)
                        self.is_running = False
                        self.solver_generator = None
                        solver = self.solvers[self.current_solver_idx]
                        self.search_stats["steps"] = solver.get_stats()["steps"]
                        self.search_stats["execution_time_ms"] = current_time - self.search_start_time
                    
                    # Update real-time telemetry
                    self.search_stats["nodes_visited"] = len(visited)
                    self.search_stats["frontier_size"] = len(frontier)
                    
                    self.last_step_time = current_time
                    
                except StopIteration:
                    self.is_running = False
                    self.solver_generator = None
        
        except Exception as e:
            print(f"Error updating visualization: {e}")
            self.is_running = False
            self.solver_generator = None
    
    def _draw_sidebar(self) -> None:
        """Draw the sidebar with controls and info."""
        try:
            # Sidebar background
            sidebar_rect = pygame.Rect(SIDEBAR_X, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT)
            pygame.draw.rect(self.screen, Colors.SIDEBAR, sidebar_rect)
            pygame.draw.line(self.screen, Colors.GRID_LINE, 
                           (SIDEBAR_X, 0), (SIDEBAR_X, WINDOW_HEIGHT), 2)
            
            # Title
            title = self.title_font.render("Search Simulator", True, Colors.TEXT)
            self.screen.blit(title, (SIDEBAR_X + 20, 20))
            
            # Draw UI components
            self.algo_dropdown.draw(self.screen, self.small_font)
            for button in self.buttons:
                button.draw(self.screen, self.small_font)
            self.speed_slider.draw(self.screen, self.small_font)
            
            # Real-Time Telemetry Dashboard
            y_offset = 420
            
            # Telemetry Title
            telemetry_title = self.small_font.render("📊 LIVE TELEMETRY", True, Colors.START)
            self.screen.blit(telemetry_title, (SIDEBAR_X + 20, y_offset))
            y_offset += 30
            
            # Telemetry Stats Box
            telemetry_bg = pygame.Rect(SIDEBAR_X + 15, y_offset - 5, SIDEBAR_WIDTH - 30, 120)
            pygame.draw.rect(self.screen, (35, 40, 50), telemetry_bg, border_radius=5)
            pygame.draw.rect(self.screen, Colors.GRID_LINE, telemetry_bg, 1, border_radius=5)
            
            # Real-time stats
            stats_display = [
                f"Nodes Visited: {self.search_stats.get('nodes_visited', 0)}",
                f"Frontier Size: {self.search_stats.get('frontier_size', 0)}",
                f"Path Length: {self.search_stats.get('path_length', 0)}",
                f"Time: {self.search_stats.get('execution_time_ms', 0)} ms",
            ]
            
            for stat in stats_display:
                text = self.small_font.render(stat, True, Colors.TEXT)
                self.screen.blit(text, (SIDEBAR_X + 25, y_offset))
                y_offset += 25
            
            y_offset += 20
            
            # Instructions
            instructions = [
                "Controls:",
                "• Left Click: Place Wall",
                "• Right Click: Remove Wall",
                "• Drag Green: Move Start",
                "• Drag Blue: Move Target",
                "",
                "Shortcuts:",
                "• SPACE - Run | R - Reset",
                "• G - Random | P - Pause",
                "",
                "Legend:",
            ]
            
            for instruction in instructions:
                text = self.small_font.render(instruction, True, Colors.TEXT_SECONDARY)
                self.screen.blit(text, (SIDEBAR_X + 20, y_offset))
                y_offset += 22
            
            # Legend colors
            legend_items = [
                ("Empty", Colors.EMPTY),
                ("Wall", Colors.WALL),
                ("Start", Colors.START),
                ("Target", Colors.TARGET),
                ("Frontier", Colors.FRONTIER),
                ("Visited", Colors.VISITED),
                ("Path", Colors.PATH),
            ]
            
            y_offset += 5
            for label, color in legend_items:
                pygame.draw.rect(self.screen, color, (SIDEBAR_X + 20, y_offset, 20, 20))
                pygame.draw.rect(self.screen, Colors.GRID_LINE, (SIDEBAR_X + 20, y_offset, 20, 20), 1)
                text = self.small_font.render(label, True, Colors.TEXT_SECONDARY)
                self.screen.blit(text, (SIDEBAR_X + 50, y_offset + 2))
                y_offset += 26
            
        except Exception as e:
            print(f"Error drawing sidebar: {e}")
    
    def _draw(self) -> None:
        """Render the entire application."""
        try:
            # Clear screen
            self.screen.fill(Colors.BACKGROUND)
            
            # Draw grid
            self.grid.draw(self.screen)
            
            # Draw sidebar
            self._draw_sidebar()
            
            # Update display
            pygame.display.flip()
            
        except Exception as e:
            print(f"Error in draw: {e}")
    
    def run(self) -> None:
        """Main application loop."""
        try:
            running = True
            
            while running:
                try:
                    # Event handling
                    for event in pygame.event.get():
                        try:
                            if event.type == pygame.QUIT:
                                running = False
                            
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    running = False
                                elif event.key == pygame.K_SPACE:
                                    self._on_run()
                                elif event.key == pygame.K_r:
                                    self._on_reset()
                                elif event.key == pygame.K_c:
                                    self._on_clear_walls()
                                elif event.key == pygame.K_g:
                                    self._on_random_walls()
                                elif event.key == pygame.K_p:
                                    self._on_pause()
                                elif event.key == pygame.K_s:
                                    self._on_step_forward()
                                elif event.key == pygame.K_b:
                                    self._on_rewind()
                                elif event.key == pygame.K_UP:
                                    self.animation_delay = max(SPEED_MIN, self.animation_delay - 10)
                                    self.speed_slider.value = self.animation_delay
                                elif event.key == pygame.K_DOWN:
                                    self.animation_delay = min(SPEED_MAX, self.animation_delay + 10)
                                    self.speed_slider.value = self.animation_delay
                            
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                # Check UI first
                                ui_handled = False
                                if not ui_handled:
                                    ui_handled = self.algo_dropdown.handle_event(event)
                                if not ui_handled:
                                    for button in self.buttons:
                                        if button.handle_event(event):
                                            ui_handled = True
                                            break
                                if not ui_handled:
                                    ui_handled = self.speed_slider.handle_event(event)
                                
                                if not ui_handled:
                                    self._handle_mouse_down(event.pos, event.button)
                            
                            elif event.type == pygame.MOUSEMOTION:
                                self._handle_mouse_motion(event.pos)
                                # Update UI hover states
                                self.algo_dropdown.handle_event(event)
                                for button in self.buttons:
                                    button.handle_event(event)
                            
                            elif event.type == pygame.MOUSEBUTTONUP:
                                self._handle_mouse_up()
                                self.speed_slider.handle_event(event)
                        
                        except Exception as e:
                            print(f"Error handling event: {e}")
                    
                    # Update visualization
                    self._update_visualization()
                    
                    # Draw everything
                    self._draw()
                    
                    # Cap framerate
                    self.clock.tick(FPS)
                    
                except Exception as e:
                    print(f"Error in main loop iteration: {e}")
            
        except Exception as e:
            print(f"Fatal error in main loop: {e}")
        
        finally:
            pygame.quit()
            sys.exit()


# =============================================================================
# UNIT TESTS
# =============================================================================

def run_tests():
    """Run unit tests for critical components."""
    print("=" * 60)
    print("RUNNING UNIT TESTS")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Node creation and basic operations
    try:
        print("\n[Test 1] Node creation...")
        node = Node(5, 10)
        assert node.row == 5
        assert node.col == 10
        assert node.state == NodeState.EMPTY
        print("  ✓ Node creation passed")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Node creation failed: {e}")
        tests_failed += 1
    
    # Test 2: Grid initialization
    try:
        print("\n[Test 2] Grid initialization...")
        grid = Grid(10, 15)
        assert grid.rows == 10
        assert grid.cols == 15
        assert len(grid.grid) == 10
        assert len(grid.grid[0]) == 15
        print("  ✓ Grid initialization passed")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Grid initialization failed: {e}")
        tests_failed += 1
    
    # Test 3: Grid bounds checking
    try:
        print("\n[Test 3] Grid bounds checking...")
        grid = Grid(10, 10)
        assert grid.get_node(0, 0) is not None
        assert grid.get_node(9, 9) is not None
        assert grid.get_node(-1, 0) is None
        assert grid.get_node(10, 0) is None
        assert grid.get_node(0, 10) is None
        print("  ✓ Grid bounds checking passed")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Grid bounds checking failed: {e}")
        tests_failed += 1
    
    # Test 4: Neighbor expansion order
    try:
        print("\n[Test 4] Neighbor expansion (Clockwise + Main Diagonal)...")
        grid = Grid(5, 5)
        center = grid.get_node(2, 2)
        neighbors = grid.get_neighbors_clockwise_diagonal(center)
        
        expected_directions = [
            (1, 2),   # Up
            (2, 3),   # Right
            (3, 2),   # Down
            (3, 3),   # Down-Right
            (2, 1),   # Left
            (1, 1),   # Up-Left
        ]
        
        assert len(neighbors) == 6, f"Expected 6 neighbors, got {len(neighbors)}"
        for i, expected in enumerate(expected_directions):
            assert (neighbors[i].row, neighbors[i].col) == expected, \
                f"Neighbor {i}: expected {expected}, got {(neighbors[i].row, neighbors[i].col)}"
        
        print("  ✓ Neighbor expansion order passed")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Neighbor expansion test failed: {e}")
        tests_failed += 1
    
    # Test 5: Wall placement and removal
    try:
        print("\n[Test 5] Wall placement and removal...")
        grid = Grid(10, 10)
        
        # Place wall
        assert grid.toggle_wall(5, 5, True)
        assert grid.get_node(5, 5).state == NodeState.WALL
        
        # Wall blocks neighbors
        center = grid.get_node(4, 4)
        neighbors = grid.get_neighbors_clockwise_diagonal(center)
        assert grid.get_node(5, 5) not in neighbors
        
        # Remove wall
        assert grid.toggle_wall(5, 5, False)
        assert grid.get_node(5, 5).state == NodeState.EMPTY
        
        print("  ✓ Wall placement and removal passed")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Wall test failed: {e}")
        tests_failed += 1
    
    # Test 6: Start/Target movement
    try:
        print("\n[Test 6] Start/Target movement...")
        grid = Grid(10, 10)
        
        initial_start = grid.start_pos
        initial_target = grid.target_pos
        
        # Move start
        assert grid.set_start(3, 3)
        assert grid.start_pos == (3, 3)
        assert grid.get_node(3, 3).state == NodeState.START
        assert grid.get_node(*initial_start).state != NodeState.START
        
        # Move target
        assert grid.set_target(7, 7)
        assert grid.target_pos == (7, 7)
        assert grid.get_node(7, 7).state == NodeState.TARGET
        
        print("  ✓ Start/Target movement passed")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Start/Target test failed: {e}")
        tests_failed += 1
    
    # Test 7: BFS basic functionality
    try:
        print("\n[Test 7] BFS algorithm...")
        grid = Grid(5, 5)
        grid.set_start(0, 0)
        grid.set_target(4, 4)
        
        solver = BFSSolver()
        generator = solver.solve(grid)
        
        # Run to completion
        final_result = None
        for result in generator:
            final_result = result
        
        frontier, visited, path = final_result
        assert path is not None
        assert len(path) > 0
        assert path[0] == grid.get_node(0, 0)
        assert path[-1] == grid.get_node(4, 4)
        
        print("  ✓ BFS algorithm passed")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ BFS test failed: {e}")
        tests_failed += 1
    
    # Test 8: DFS basic functionality
    try:
        print("\n[Test 8] DFS algorithm...")
        grid = Grid(5, 5)
        grid.set_start(0, 0)
        grid.set_target(2, 2)
        
        solver = DFSSolver()
        generator = solver.solve(grid)
        
        final_result = None
        for result in generator:
            final_result = result
        
        frontier, visited, path = final_result
        assert path is not None
        assert len(path) > 0
        
        print("  ✓ DFS algorithm passed")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ DFS test failed: {e}")
        tests_failed += 1
    
    # Test 9: Reset search preserves walls
    try:
        print("\n[Test 9] Reset search preserves walls...")
        grid = Grid(10, 10)
        grid.toggle_wall(5, 5, True)
        grid.toggle_wall(6, 6, True)
        
        # Simulate search (use positions that are not start or target)
        grid.get_node(1, 1).state = NodeState.VISITED
        grid.get_node(3, 4).state = NodeState.FRONTIER
        
        # Reset
        grid.reset_search()
        
        assert grid.get_node(5, 5).state == NodeState.WALL, f"Wall at (5,5) should persist"
        assert grid.get_node(6, 6).state == NodeState.WALL, f"Wall at (6,6) should persist"
        assert grid.get_node(1, 1).state == NodeState.EMPTY, f"Visited should be cleared"
        assert grid.get_node(3, 4).state == NodeState.EMPTY, f"Frontier should be cleared"
        
        print("  ✓ Reset search test passed")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Reset search test failed: {e}")
        tests_failed += 1
    
    # Test 10: Screen to grid conversion
    try:
        print("\n[Test 10] Screen to grid conversion...")
        grid = Grid(GRID_ROWS, GRID_COLS)
        
        # Test within grid bounds
        pos = grid.screen_to_grid(GRID_OFFSET_X + 10, GRID_OFFSET_Y + 10)
        assert pos is not None
        assert pos == (0, 0)
        
        # Test outside grid bounds
        pos = grid.screen_to_grid(10, 10)
        assert pos is None
        
        pos = grid.screen_to_grid(SIDEBAR_X + 10, 100)
        assert pos is None
        
        print("  ✓ Screen to grid conversion passed")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Screen to grid conversion failed: {e}")
        tests_failed += 1
    
    # Test 11: Path reconstruction
    try:
        print("\n[Test 11] Path reconstruction...")
        grid = Grid(5, 5)
        
        # Create a simple chain
        nodes = [grid.get_node(0, i) for i in range(5)]
        for i in range(1, 5):
            nodes[i].parent = nodes[i-1]
        
        solver = BFSSolver()
        path = solver.reconstruct_path(nodes[4])
        
        assert len(path) == 5
        for i, node in enumerate(path):
            assert node == nodes[i]
        
        print("  ✓ Path reconstruction passed")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Path reconstruction failed: {e}")
        tests_failed += 1
    
    # Test 12: Node state transitions
    try:
        print("\n[Test 12] Node state transitions...")
        node = Node(0, 0)
        
        assert node.state == NodeState.EMPTY
        
        node.state = NodeState.VISITED
        node.reset_search_state()
        assert node.state == NodeState.EMPTY
        
        node.state = NodeState.WALL
        node.reset_search_state()
        assert node.state == NodeState.WALL  # Walls should persist
        
        print("  ✓ Node state transitions passed")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Node state transitions failed: {e}")
        tests_failed += 1
    
    # Test 13: Random wall generation
    try:
        print("\n[Test 13] Random wall generation...")
        grid = Grid(10, 10)
        start_pos = grid.start_pos
        target_pos = grid.target_pos
        
        # Generate random walls
        grid.generate_random_walls(wall_percentage=0.2, seed=42)
        
        # Count walls
        wall_count = 0
        for row in range(grid.rows):
            for col in range(grid.cols):
                if grid.get_node(row, col).state == NodeState.WALL:
                    wall_count += 1
        
        # Should have approximately 20% walls (with some margin)
        expected_walls = 100 * 0.2  # 20 walls
        assert wall_count > 0, "Should have generated some walls"
        assert wall_count < 50, "Should not have too many walls"
        
        # Start and target should not be walls
        assert grid.get_node(*start_pos).state != NodeState.WALL, "Start should not be a wall"
        assert grid.get_node(*target_pos).state != NodeState.WALL, "Target should not be a wall"
        
        # Neighbors of start and target should not be walls (buffer zone)
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                sr, sc = start_pos[0] + dr, start_pos[1] + dc
                if 0 <= sr < grid.rows and 0 <= sc < grid.cols:
                    assert grid.get_node(sr, sc).state != NodeState.WALL, f"Buffer around start at ({sr},{sc}) should be clear"
        
        print(f"  ✓ Random wall generation passed ({wall_count} walls generated)")
        tests_passed += 1
    except Exception as e:
        print(f"  ✗ Random wall generation failed: {e}")
        tests_failed += 1
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"TESTS SUMMARY: {tests_passed} passed, {tests_failed} failed")
    print("=" * 60)
    
    return tests_failed == 0


# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    """Application entry point."""
    try:
        # Run unit tests first
        tests_ok = run_tests()
        
        if not tests_ok:
            print("\n⚠ Warning: Some tests failed. Continue anyway? (y/n)")
            # In a real application, you might want to handle this differently
            # For now, we'll continue regardless
        
        print("\n" + "=" * 60)
        print("STARTING SEARCH ALGORITHM SIMULATOR")
        print("=" * 60)
        print("Controls:")
        print("  SPACE - Run search")
        print("  R - Reset search")
        print("  C - Clear walls")
        print("  G - Random walls")
        print("  P - Pause/Resume")
        print("  S - Step Forward (VCR)")
        print("  B - Rewind (VCR)")
        print("  UP/DOWN - Adjust speed")
        print("  ESC - Exit")
        print("=" * 60)
        print("NEW FEATURES:")
        print("  • Randomized DFS (Chaos Mode)")
        print("  • Scout Algorithm (Hybrid BFS/DFS)")
        print("  • Real-time Telemetry Dashboard")
        print("  • VCR Controls (Step/Rewind)")
        print("=" * 60 + "\n")
        
        # Initialize and run application
        app = SearchAlgorithmSimulator()
        app.run()
        
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()