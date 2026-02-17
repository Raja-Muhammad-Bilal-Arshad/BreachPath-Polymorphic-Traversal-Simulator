# Search Algorithm Simulator

A professional, interactive Pygame-based visualization tool for exploring and comparing various search algorithms on a 2D grid. Built for AI/CS education and algorithm analysis.

![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)
![Pygame Version](https://img.shields.io/badge/pygame-2.6+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Implemented Algorithms](#implemented-algorithms)
- [Innovation Lab](#innovation-lab)
- [Controls](#controls)
- [Architecture](#architecture)
- [Testing](#testing)
- [Technical Details](#technical-details)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Search Algorithm Simulator provides an interactive environment for visualizing how different search algorithms explore a grid to find paths from a start node to a target node. It features real-time visualization, VCR-style controls, comprehensive statistics, and innovative hybrid algorithms.

**Key Capabilities:**
- 9 different search algorithms
- Real-time telemetry dashboard
- Step-by-step execution with rewind
- Random maze generation
- Interactive wall placement
- Custom hybrid algorithms

## Features

### Core Features
- **Interactive Grid**: 30×40 grid with click-and-drag interface
- **Multiple Algorithms**: 9 built-in search algorithms
- **Real-time Visualization**: Watch algorithms explore in real-time
- **VCR Controls**: Play, pause, step forward, and rewind
- **Telemetry Dashboard**: Live statistics during search
- **Random Maze Generation**: Auto-generate obstacles

### Visual Elements

#### Grid Elements
- 🟢 **Green**: Start node (can be dragged)
- 🔵 **Blue**: Target node (can be dragged)
- 🔴 **Red**: Frontier nodes (to be explored)
- 🟡 **Yellow**: Visited nodes (already explored)
- 🟣 **Purple**: Final path
- ⬛ **Dark Gray**: Walls (obstacles)
- ⬜ **Light Gray**: Empty cells

#### UI Theme (Professional Dark)
- **Sidebar Background**: Dark Slate Grey (#2d2d2d)
- **Buttons**: Gunmetal Grey with Cyan hover accents
- **Text**: White, anti-aliased
- **ComboBox**: Professional dropdown with shadow effects
- **Telemetry Panel**: Semi-transparent with cyan border
- **Accent Color**: Bright Cyan (#00c8ff)

### Advanced Features
- **Neighbor Expansion Order**: Clockwise + Main Diagonal (Up → Right → Down → Down-Right → Left → Up-Left)
- **State History**: Rewind to any previous step
- **Speed Control**: Adjustable animation delay (0-500ms)
- **Algorithm Comparison**: Side-by-side performance metrics

## Installation

### Prerequisites
- Python 3.13 or higher
- Pygame 2.6 or higher

### Install Dependencies

```bash
pip install pygame
```

### Clone and Run

```bash
cd "/home/bhai/Desktop/4th Semester/AI/Solved Assignments/ProjectAssignment1"
python search_simulator.py
```

## Usage

### Basic Usage

1. **Run the simulator**:
   ```bash
   python search_simulator.py
   ```

2. **Select an algorithm** from the dropdown menu

3. **Create obstacles**:
   - Left-click to place walls
   - Right-click to remove walls
   - Click "Random Walls" for auto-generation

4. **Run the search**:
   - Click "▶ Run Search" or press `SPACE`
   - Watch the visualization in real-time

5. **Control playback**:
   - `P` or Pause button: Pause/Resume
   - `S` or Step button: Advance one step
   - `B` or Rewind button: Go back one step

### Moving Start and Target

- **Drag the green node** to move the start position
- **Drag the blue node** to move the target position
- The algorithm will automatically re-run when positions change

## Implemented Algorithms

### 1. Breadth-First Search (BFS)
- **Type**: Uninformed, Complete, Optimal
- **Strategy**: Explores all nodes at current depth before next level
- **Time Complexity**: O(b^d)
- **Space Complexity**: O(b^d)
- **Characteristics**: Guarantees shortest path in unweighted graphs

### 2. Depth-First Search (DFS)
- **Type**: Uninformed, Complete (finite spaces)
- **Strategy**: Explores as far as possible along each branch
- **Time Complexity**: O(b^m)
- **Space Complexity**: O(bm)
- **Characteristics**: Memory efficient, may not find optimal path

### 3. Randomized DFS (Chaos Mode) ⭐ NEW
- **Type**: Uninformed, Variant
- **Strategy**: DFS with randomized neighbor selection
- **Characteristics**: Creates chaotic, unpredictable paths
- **Use Case**: Interesting for visualization, shows impact of ordering

### 4. Uniform-Cost Search (UCS)
- **Type**: Uninformed, Complete, Optimal
- **Strategy**: Expands lowest path cost first
- **Time Complexity**: O(b^(1+⌊C*/ε⌋))
- **Characteristics**: Handles different step costs (1 for orthogonal, √2 for diagonal)

### 5. Depth-Limited Search (DLS)
- **Type**: Uninformed, Not Complete
- **Strategy**: DFS with maximum depth limit
- **Characteristics**: Prevents infinite loops in infinite spaces
- **Limit**: Configurable (default: 20)

### 6. Iterative Deepening DFS (IDDFS)
- **Type**: Uninformed, Complete, Optimal
- **Strategy**: Repeated DLS with increasing limits
- **Time Complexity**: O(b^d)
- **Space Complexity**: O(bd)
- **Characteristics**: Best of BFS and DFS combined

### 7. Bidirectional Search
- **Type**: Uninformed, Complete, Optimal
- **Strategy**: Simultaneous search from start and target
- **Time Complexity**: O(b^(d/2))
- **Characteristics**: Much faster for large search spaces

### 8. Scout Algorithm (Hybrid BFS/DFS) ⭐ NEW
- **Type**: Hybrid, Innovation Lab
- **Strategy**: Alternates between BFS (5 layers) and DFS (5 layers)
- **Tactic**: "Scan wide, then drill deep"
- **Characteristics**: Combines broad exploration with deep investigation
- **Use Case**: Simulates scout behavior - overview first, then detailed exploration

### 9. Custom Solver (Beam Search)
- **Type**: Informed, Hybrid
- **Strategy**: BFS with frontier size limit
- **Characteristics**: Memory-bounded, uses heuristic sorting
- **Beam Width**: Configurable (default: 10)

## Innovation Lab

### The Scout Algorithm

A novel hybrid approach that mimics how a scout might explore unknown territory:

```
Pattern: BFS → DFS → BFS → DFS → ...
Layers:  [5]    [5]    [5]    [5]
         ^      ^      ^      ^
         └──────┴──────┴──────┘
         "Scan wide, then drill deep"
```

**Why it works:**
- **BFS Phase**: Gets a broad overview of the landscape
- **DFS Phase**: Investigates promising areas in depth
- **Alternation**: Prevents getting stuck in either mode

### Randomized DFS (Chaos Mode)

Standard DFS always follows a fixed order. Chaos Mode randomizes neighbor selection at each step:

```python
# Standard DFS
neighbors = [Up, Right, Down, Down-Right, Left, Up-Left]

# Randomized DFS
neighbors = [Right, Up-Left, Down, Up, Down-Right, Left]  # Random!
```

**Visual Effect**: Creates beautiful, chaotic exploration patterns that are never the same twice.

## Controls

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `SPACE` | Run search |
| `R` | Reset search |
| `C` | Clear all walls |
| `G` | Generate random walls |
| `P` | Pause/Resume |
| `S` | Step forward (VCR) |
| `B` | Rewind (VCR) |
| `↑` | Increase speed |
| `↓` | Decrease speed |
| `ESC` | Exit |

### Mouse Controls

| Action | Effect |
|--------|--------|
| Left Click (empty) | Place wall |
| Left Click (wall) | Remove wall |
| Left Drag (green) | Move start position |
| Left Drag (blue) | Move target position |
| Right Click (wall) | Remove wall |

### UI Controls (Professional Dark Theme)

The UI has been completely redesigned with a **dynamic vertical layout** that prevents overlapping elements:

#### Algorithm Selection (Top)
- **Professional ComboBox**: Single dropdown widget showing current algorithm
  - **Closed**: Displays selected algorithm with dropdown arrow
  - **Open**: Full list with hover effects and click-to-select
  - **Scroll Support**: Mouse wheel for long lists

#### Control Buttons (Grouped in Rows)
All buttons use **Gunmetal Grey** with **Cyan hover accents**:

**Primary Controls** (Horizontal Row):
- **▶ Run**: Start visualization
- **⏸ Pause**: Pause/Resume execution
- **🗑 Clear**: Remove all walls

**VCR Controls** (Horizontal Row):
- **⏭ Step**: Advance one iteration
- **⏮ Rewind**: Go back one iteration

**Actions** (Horizontal Row):
- **↺ Reset**: Clear search state
- **🎲 Random**: Generate random walls

#### Speed Control
- **Slider**: Adjust animation delay (0-500ms)
- **Visual Feedback**: Filled track with cyan handle
- **Value Display**: Shows current delay in milliseconds

#### Live Telemetry Panel (Bottom - Fixed Position)
- **Semi-transparent Background**: Dark overlay with cyan border
- **Position**: Always anchored to bottom of sidebar
- **Real-time Updates**:
  - Nodes Visited: Counter
  - Frontier Size: Nodes waiting to be explored
  - Path Length: Final path count
  - Execution Time: Milliseconds elapsed

**Layout Benefits:**
- ✅ No overlapping elements
- ✅ Dynamic Y-positioning with 15px padding
- ✅ Consistent 10px gaps between all elements
- ✅ Telemetry always visible at bottom
- ✅ Professional dark theme throughout
- **⏸ Pause**: Pause/resume execution
- **⏭ Step**: Advance one iteration
- **⏮ Rewind**: Go back one iteration

## Architecture

### Class Hierarchy

```
SearchAlgorithmSimulator (Main Application)
├── Grid
│   ├── Node[][] (2D array)
│   └── Methods for wall placement, coordinate conversion
├── Solver (Abstract Base)
│   ├── BFSSolver
│   ├── DFSSolver
│   ├── RandomizedDFSSolver
│   ├── UCSSolver
│   ├── DLSSolver
│   ├── IDDFSSolver
│   ├── BidirectionalSolver
│   ├── ScoutSolver
│   └── CustomSolver
└── UI Components (Professional Dark Theme)
    ├── Sidebar (Dynamic Layout Manager)
    │   ├── ComboBox (Professional Dropdown)
    │   ├── Button (Cyan Hover Accents)
    │   ├── Slider (Cyan Handle)
    │   └── Telemetry Panel (Fixed Bottom)
    └── Layout System
        ├── Dynamic Y-positioning
        ├── 15px Element Padding
        └── Z-index Management
```

### Node State Machine

```
┌─────────┐    Place Wall     ┌─────────┐
│  EMPTY  │ ─────────────────→│  WALL   │
└─────────┘                   └─────────┘
     │                             │
     │ Search Visits               │ Remove Wall
     ↓                             ↓
┌─────────┐    Search Done    ┌─────────┐
│ VISITED │ ←─────────────────│ FRONTIER│
└─────────┘                   └─────────┘
     │
     │ Path Found
     ↓
┌─────────┐
│  PATH   │
└─────────┘
```

### Algorithm Interface

All solvers implement:

```python
class Solver:
    def solve(self, grid: Grid) -> Iterator[Tuple[List[Node], List[Node], Optional[List[Node]]]]:
        """
        Yields: (frontier, visited, path)
        - frontier: Nodes to be explored
        - visited: Nodes already explored
        - path: Final path (None if not done, [] if no path found)
        """
        pass
```

## Testing

### Running Tests

```bash
# Run built-in tests
python search_simulator.py

# Run comprehensive test suite
python test_search_simulator.py
```

### Test Coverage

The comprehensive test suite includes:

1. **Node Tests** (6 tests)
   - Creation, hashing, equality
   - State transitions
   - Color mapping

2. **Grid Tests** (14 tests)
   - Initialization and bounds
   - Start/target movement
   - Wall placement/removal
   - Neighbor expansion
   - Coordinate conversion

3. **Algorithm Tests** (18 tests)
   - BFS, DFS, Randomized DFS
   - UCS, DLS, IDDFS
   - Bidirectional, Scout
   - Path finding verification
   - Statistics validation

4. **Integration Tests** (2 tests)
   - Full workflow testing
   - Complex maze solving

**Total: 48 tests, all passing ✓**

### Manual Testing Checklist

- [ ] All 9 algorithms complete successfully
- [ ] Start/target dragging works
- [ ] Wall placement/removal works
- [ ] Random wall generation works
- [ ] Step forward/rewind work correctly
- [ ] Speed adjustment works
- [ ] Pause/resume works
- [ ] Telemetry updates in real-time
- [ ] No crashes on edge cases

## Technical Details

### Constants

```python
WINDOW_WIDTH = 1200      # Total window width
WINDOW_HEIGHT = 800      # Total window height
GRID_ROWS = 30           # Grid rows
GRID_COLS = 40           # Grid columns
NODE_SIZE = 22           # Pixel size of each cell
GRID_GAP = 1             # Gap between cells
SIDEBAR_WIDTH = 280      # Right panel width
DEFAULT_SPEED = 50       # Animation delay (ms)
```

### Neighbor Expansion Order

```
    [0,-1]  Up
       ↑
[-1,-1]←●→[0,+1]   Up-Left ← ● → Right
  Up-Left   ↓        ↑     ↓    [+1,+1]
       [+1,0]      Down-Right Down-Right
       Down
       
[+1,+1]  Down-Right (Diagonal)
[-1,-1]  Up-Left (Diagonal)
```

Order: **Up → Right → Down → Down-Right → Left → Up-Left**

### Color Scheme (Professional Dark Theme)

#### Grid Colors
| Element | RGB Value | Hex |
|---------|-----------|-----|
| Empty | (240, 240, 240) | #F0F0F0 |
| Wall | (30, 30, 30) | #1E1E1E |
| Start | (46, 204, 113) | #2ECC71 |
| Target | (52, 152, 219) | #3498DB |
| Frontier | (231, 76, 60) | #E74C3C |
| Visited | (241, 196, 15) | #F1C40F |
| Path | (155, 89, 182) | #9B59B6 |
| Background | (30, 30, 35) | #1E1E23 |

#### Professional UI Colors (Dark Theme)
| Element | RGB Value | Hex | Usage |
|---------|-----------|-----|-------|
| Sidebar | (45, 45, 50) | #2d2d2d | Background |
| Button Normal | (70, 70, 75) | #46464b | Gunmetal Grey |
| Button Hover | (0, 200, 255) | #00c8ff | Cyan Accent |
| Button Active | (0, 150, 200) | #0096c8 | Darker Cyan |
| Text | (255, 255, 255) | #FFFFFF | White |
| Text Secondary | (180, 180, 180) | #b4b4b4 | Light Grey |
| Section Header | (0, 200, 255) | #00c8ff | Cyan |
| Slider Handle | (0, 200, 255) | #00c8ff | Cyan |
| Dropdown BG | (60, 60, 65) | #3c3c41 | Dark |
| Telemetry BG | (35, 35, 40, 220) | #232328dc | Semi-transparent |
| Telemetry Border | (0, 200, 255, 100) | #00c8ff64 | Cyan tint |

## Screenshots

### Main Interface (Professional Dark Theme)
```
┌──────────────────────────────────────────────────────────────────┐
│  Grid Area (30×40)                      │ Sidebar (Dark Slate)  │
│                                         │ ┌───────────────────┐ │
│  🟢 → 🔵                                │ │  Search Simulator │ │
│                                         │ └───────────────────┘ │
│  ⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜                      │ ┌───────────────────┐ │
│  ⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜                      │ │ Algorithm     [▼] │ │
│  ⬜⬜🟡🟡🟡⬜⬜⬜⬜⬜                      │ └───────────────────┘ │
│  ⬜⬜🟡🔴🔴⬜⬜⬜⬜⬜                      │ ┌───┬───┬───┐       │ │
│  ⬜⬜🟡⬜⬜⬜⬜⬜⬜⬜                      │ │▶Run│⏸Pse│🗑Clr│       │ │
│  ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜                      │ └───┴───┴───┘       │ │
│                                         │ ┌─────┬─────┐       │ │
│  🟢=Start  🔵=Target  🟡=Visited        │ │⏭Step│⏮Re wd│       │ │
│  🔴=Frontier  ⬛=Wall  🟣=Path          │ └─────┴─────┘       │ │
│                                         │ ┌─────┬─────┐       │ │
│                                         │ │↺Rst│🎲Rnd│       │ │
│                                         │ └─────┴─────┘       │ │
│                                         │ Speed: [━━━●━━] 50ms│ │
│                                         │                       │ │
│                                         │ ╔═══════════════════╗ │
│                                         │ ║  📊 LIVE TELEMETRY║ │
│                                         │ ║  ─────────────────║ │
│                                         │ ║  Nodes Visited: 42║ │
│                                         │ ║  Frontier Size:  8║ │
│                                         │ ║  Path Length:   15║ │
│                                         │ ║  Time:       1250ms║ │
│                                         │ ╚═══════════════════╝ │
└──────────────────────────────────────────────────────────────────┘
```

### UI Components Breakdown

#### 1. Algorithm ComboBox (Professional Dropdown)
```
┌─────────────────────┐
│ Algorithm     [▼]   │  ← Closed State (shows selection)
└─────────────────────┘

┌─────────────────────┐
│ ▼ Algorithm         │
├─────────────────────┤
│ ○ Breadth-First     │  ← Open State (overlay with z-index)
│ ○ Depth-First       │
│ ○ Randomized DFS    │
│ ○ Uniform-Cost      │
│ ● Scout Algorithm   │  ← Current selection (cyan highlight)
│ ○ ...               │
└─────────────────────┘
```

#### 2. Button Layout (Horizontal Grouping)
```
Primary Controls:    VCR Controls:       Actions:
┌───┬───┬───┐       ┌─────┬─────┐       ┌─────┬─────┐
│▶Run│⏸Pse│🗑Clr│       │⏭Step│⏮Re wd│       │↺Rst│🎲Rnd│
└───┴───┴───┘       └─────┴─────┘       └─────┴─────┘
   Gunmetal Grey        Cyan on Hover        10px gap
```

#### 3. Telemetry Panel (Fixed Bottom)
```
╭─────────────────────╮
│  📊 LIVE TELEMETRY  │  ← Semi-transparent background
│  ─────────────────  │
│  Nodes Visited:  42 │  ← Label : Value (right-aligned)
│  Frontier Size:   8 │
│  Path Length:    15 │
│  Time:        1250ms│
╰─────────────────────╯
      Cyan Border
```

## UI Architecture (New in v2.0)

### Dynamic Layout System

The UI uses a professional **Sidebar class** with dynamic vertical positioning to ensure no elements ever overlap:

```python
class Sidebar:
    def __init__(self, x, width, height, fonts...):
        self.current_y = 20  # Start position
        self.padding = 15    # 15px between elements
        
    def advance_y(self, height, padding=None):
        """Move Y position down and return old value"""
        old_y = self.current_y
        self.current_y += height + (padding or self.padding)
        return old_y
```

**Layout Flow:**
1. Title (fixed at top)
2. ComboBox (Algorithm selection)
3. Primary Controls (Run/Pause/Clear) - Horizontal row
4. VCR Controls (Step/Rewind) - Horizontal row
5. Action Buttons (Reset/Random) - Horizontal row
6. Speed Slider
7. Telemetry Panel (Fixed to bottom)

### Professional ComboBox Widget

The new ComboBox replaces the old dropdown with:
- **Z-index management**: Draws overlay last for highest priority
- **Semi-transparent backdrop**: Darkens rest of UI when open
- **Smooth hover effects**: Cyan highlight on selection
- **Scroll wheel support**: For long algorithm lists
- **Click-outside-to-close**: Intuitive interaction

```python
class ComboBox:
    def draw(self, screen, font):
        # Closed state shows current selection
        if self.expanded:
            # Draw overlay backdrop
            # Draw dropdown list on top
            # Handle mouse clicks
```

### Visual Style System

All UI components follow the **Professional Dark Theme**:

```python
class Colors:
    SIDEBAR = (45, 45, 50)        # #2d2d2d - Dark Slate
    BUTTON = (70, 70, 75)         # Gunmetal Grey
    BUTTON_HOVER = (0, 200, 255)  # Cyan accent
    TEXT = (255, 255, 255)        # White
```

**Design Principles:**
- ✅ Consistent 15px padding between elements
- ✅ 10px gaps between horizontal buttons
- ✅ Shadows for depth (2px offset)
- ✅ Rounded corners (6px radius)
- ✅ Cyan (#00c8ff) as accent color
- ✅ Gunmetal grey for neutral elements

### Telemetry Panel (Fixed Bottom)

```python
def _draw_telemetry(self, screen, stats):
    # Calculate position - always at bottom
    telemetry_y = sidebar_height - panel_height - 20
    
    # Semi-transparent background
    s = pygame.Surface((width, height), pygame.SRCALPHA)
    s.fill((35, 35, 40, 220))  # RGBA with alpha
    
    # Cyan border
    pygame.draw.rect(screen, (0, 200, 255, 100), rect, 2)
```

**Benefits:**
- Always visible, never scrolls away
- Separated from controls (no accidental clicks)
- Semi-transparent so grid is still visible
- Real-time updates during search

## Contributing

### Adding New Algorithms

1. Create a new class inheriting from `Solver`:

```python
class MyNewSolver(Solver):
    def __init__(self):
        super().__init__("My New Algorithm")
    
    def solve(self, grid: Grid):
        # Initialize
        start_node = grid.get_node(*grid.start_pos)
        target_node = grid.get_node(*grid.target_pos)
        
        # Your algorithm logic
        while frontier:
            # Process node
            
            # Yield state for visualization
            yield (frontier_list, visited_list, current_path)
```

2. Add to solver list in `SearchAlgorithmSimulator.__init__()`

### Code Style

- Follow PEP 8
- Use type hints
- Document all methods
- Add unit tests

## Performance Comparison

| Algorithm | Time (avg) | Path Quality | Memory |
|-----------|------------|--------------|---------|
| BFS | Medium | Optimal | High |
| DFS | Fast | Suboptimal | Low |
| Randomized DFS | Variable | Variable | Low |
| UCS | Slow | Optimal | High |
| DLS | Fast* | May Fail | Low |
| IDDFS | Medium | Optimal | Low |
| Bidirectional | Fast | Optimal | Medium |
| Scout | Medium | Good | Medium |

*When target within limit

## Troubleshooting

### Common Issues

**Issue**: Window doesn't open
- **Solution**: Ensure Pygame is installed: `pip install pygame`

**Issue**: Slow performance
- **Solution**: Reduce animation delay or use smaller grid

**Issue**: Algorithm doesn't find path
- **Solution**: Check that start and target aren't blocked by walls

**Issue**: Rewind doesn't work
- **Solution**: Rewind is only available during active search

## Future Enhancements

- [ ] A* Search with heuristics
- [ ] Greedy Best-First Search
- [ ] Save/load maze configurations
- [ ] Export path as image
- [ ] Multi-threading for large grids
- [ ] 3D visualization
- [ ] Mobile support

## Credits

Developed for AI/CS Education
- Author: Raja Muhammad Bilal Arshad
- Version: 1.0.0
- Created: 2026

## License

This project is licensed under the MIT License.

---

**Happy Searching! 🚀**

For questions or issues, please refer to the documentation or contact the development team.
