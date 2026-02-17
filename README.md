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
- 🟢 **Green**: Start node (can be dragged)
- 🔵 **Blue**: Target node (can be dragged)
- 🔴 **Red**: Frontier nodes (to be explored)
- 🟡 **Yellow**: Visited nodes (already explored)
- 🟣 **Purple**: Final path
- ⬛ **Dark Gray**: Walls (obstacles)
- ⬜ **Light Gray**: Empty cells

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

### UI Controls

- **Algorithm Dropdown**: Select from 9 algorithms
- **▶ Run Search**: Start visualization
- **↺ Reset Search**: Clear search state
- **🗑 Clear Walls**: Remove all walls
- **🎲 Random Walls**: Generate random obstacles
- **Speed Slider**: Adjust animation delay (0-500ms)
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
└── UI Components
    ├── Button
    ├── Slider
    └── Dropdown
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

### Color Scheme

| Element | RGB Value | Hex |
|---------|-----------|-----|
| Empty | (240, 240, 240) | #F0F0F0 |
| Wall | (30, 30, 30) | #1E1E1E |
| Start | (46, 204, 113) | #2ECC71 |
| Target | (52, 152, 219) | #3498DB |
| Frontier | (231, 76, 60) | #E74C3C |
| Visited | (241, 196, 15) | #F1C40F |
| Path | (155, 89, 182) | #9B59B6 |
| Background | (45, 52, 70) | #2D3446 |

## Screenshots

### Main Interface
```
┌────────────────────────────────────────────────────────────────┐
│  Grid Area (30×40)                        │ Sidebar (280px)   │
│                                           │                   │
│  🟢 → 🔵                                  │ Algorithm: [▼]    │
│                                           │                   │
│  ⬛⬛⬛⬜⬜⬜⬜⬜⬜⬜                        │ [▶ Run Search]   │
│  ⬛⬜⬜⬜⬜⬜⬜⬜⬜⬜                        │ [↺ Reset]        │
│  ⬜⬜🟡🟡🟡⬜⬜⬜⬜⬜                        │ [🗑 Clear Walls] │
│  ⬜⬜🟡🔴🔴⬜⬜⬜⬜⬜                        │ [🎲 Random]      │
│  ⬜⬜🟡⬜⬜⬜⬜⬜⬜⬜                        │                   │
│  ⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜                        │ Speed: [━━━●━━]  │
│                                           │                   │
│  🟢=Start  🔵=Target  🟡=Visited          │ [⏸ Pause]        │
│  🔴=Frontier  ⬛=Wall  🟣=Path            │ [⏭ Step] [⏮ Rew]│
│                                           │                   │
│                                           │ 📊 LIVE TELEMETRY │
│                                           │ ┌──────────────┐  │
│                                           │ │ Nodes: 42    │  │
│                                           │ │ Frontier: 8  │  │
│                                           │ │ Path: 15     │  │
│                                           │ │ Time: 1250ms │  │
│                                           │ └──────────────┘  │
└────────────────────────────────────────────────────────────────┘
```

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
