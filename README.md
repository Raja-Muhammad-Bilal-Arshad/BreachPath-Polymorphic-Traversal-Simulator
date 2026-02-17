# Search Algorithm Simulator v6.0

A professional, interactive Pygame-based visualization tool for exploring and comparing various search algorithms on a 2D grid. Built for AI/CS Research and algorithm analysis.

**👻 New in v6.0**: Stealth Search (Minimum Memory) - Revolutionary "Ghost Mode" algorithm that operates with O(depth) memory instead of O(nodes)!

**Previously in v5.0**: KWS (Kinetic Wavefront Search) - High-speed experimental algorithm that "slides" in cardinal directions with laser-like beam visualization!

**Previously in v4.0**: DABPS (Density-Adaptive Bi-Phase Search) - Revolutionary topology-aware algorithm with perimeter building and density-based strategy switching!

**Previously in v3.0**: Westra Adaptive Search Research Module with memory-adaptive algorithm and real-time color visualization!

**Previously in v2.0**: Fullscreen support, dynamic window resizing, and completely refactored UI with professional dark theme!

![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)
![Pygame Version](https://img.shields.io/badge/pygame-2.6+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Version](https://img.shields.io/badge/version-2.0.0-brightgreen.svg)

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
- 13 different search algorithms (including 5 research algorithms)
- Real-time telemetry dashboard
- Step-by-step execution with rewind
- Random maze generation
- Interactive wall placement
- Custom hybrid algorithms
- **Fullscreen & Maximize mode** (NEW v2.0)
- **Dynamic window resizing with auto-scaling grid** (NEW v2.0)
- **Professional dark UI theme with header bar** (NEW v2.0)
- **DABPS topology-aware algorithm** (NEW v4.0)
- **KWS high-speed kinetic algorithm** (NEW v5.0)
- **Stealth Search minimum memory algorithm** (NEW v6.0)
- **Research modules with visual color transitions**

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
- 🔵 **Blue**: Research BFS phase (Westra Algorithm)
- 🟠 **Orange**: Research DFS phase (Westra Algorithm)
- 🟡 **Gold**: Research Mode indicator
- 🟠 **Orange**: DABPS Perimeter phase (The Net)
- 🔵 **Cyan**: DABPS Adaptive phase (The Scout)
- 🔵 **Transparent Blue**: KWS Beam phase (Scan rays)
- 🟡 **Bright Yellow**: KWS Stop phase (Stopping points)
- 🔵 **Cyan**: Stealth Path (Ghost Mode current thread)
- 🔴 **Red**: Stealth Head (Ghost Mode current node)

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

### 10. Westra Adaptive Search (Research Module) 🔬 NEW
- **Type**: Research, Adaptive
- **Strategy**: Dynamic BFS/DFS switching based on memory usage
- **Innovation**: Automatically adapts to map complexity in real-time
- **Panic Threshold**: 100 nodes (triggers DFS when exceeded)
- **Check Interval**: Every 50 steps
- **Visualization**: Blue (BFS) → Orange (DFS) color transition
- **Use Case**: Research into memory-adaptive search algorithms

### 11. DABPS - Density-Adaptive Bi-Phase Search 🆕 NEWEST
- **Type**: Research, Bi-Phase, Density-Adaptive
- **Strategy**: Two-phase approach with perimeter building + density-based switching
- **Phase 1**: Reverse Perimeter BFS (builds "The Net" around target)
- **Phase 2**: Adaptive forward search (switches BFS/DFS based on neighbor density)
- **Innovation**: Uses corridor detection (≤1 neighbor = DFS, >1 neighbor = BFS)
- **Visualization**: Orange (Perimeter/Net) → Cyan (Adaptive/Scout)
- **Use Case**: Research into topology-aware pathfinding algorithms

### 12. Kinetic Wavefront Search (KWS) ⚡ HIGH-SPEED
- **Type**: Experimental, High-Speed, Kinetic
- **Strategy**: "Slides" in cardinal directions until hitting obstacles (not step-by-step crawling)
- **Movement**: Kinetic sliding (Up, Right, Down, Left) until wall/edge/target
- **Innovation**: Stopping points create wavefront corners; beams show laser-like scan paths
- **Visualization**: Transparent Blue (Beams/Scan Rays) + Bright Yellow (Stopping Points/Corners)
- **Effect**: Looks like laser scanning the map, not flood fill
- **Use Case**: High-speed open space exploration, corridor detection, visual demonstration of kinetic movement

### 13. Stealth Search (Minimum Memory) 👻 GHOST MODE
- **Type**: Research, Memory-Optimized, Stealth
- **Strategy**: IDDFS with path-checking only (NO global visited set)
- **Memory Model**: O(depth) instead of O(nodes) - only tracks current recursion stack
- **Innovation**: "Ghost Mode" - algorithm "forgets" where it's been to save memory
- **Cycle Prevention**: Only checks if neighbor is in current path stack
- **Visualization**: Cyan (Current Path) + Red (Head) - NO visited nodes (yellow) drawn
- **Effect**: Visualizes a "ghost" moving through the grid
- **Use Case**: Extreme memory-constrained environments, embedded systems, demonstrating memory vs. time tradeoffs

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

### Westra Adaptive Search (Research Module) 🔬

A cutting-edge research algorithm that demonstrates **memory-adaptive search behavior**:

```
Algorithm Behavior:
╔════════════════════════════════════════════════════════════╗
║  1. Start with Bidirectional BFS                           ║
║     → Explores efficiently from both start and target      ║
║                                                            ║
║  2. Every 50 steps: Check memory usage                     ║
║     → If queue_size > 100: MEMORY PANIC!                   ║
║     → Switch to DFS to reduce queue size                   ║
║                                                            ║
║  3. DFS Phase: Drill deep to reduce memory                 ║
║     → Orange nodes show DFS exploration                    ║
║     → If dead end: Revert to BFS                           ║
║                                                            ║
║  4. Visual Color Shift: Blue → Orange → Blue               ║
║     → Shows real-time adaptation to complexity             ║
╚════════════════════════════════════════════════════════════╝
```

**Key Research Contributions:**
- **Dynamic Strategy Switching**: Automatically adapts based on runtime conditions
- **Memory-Aware**: Monitors queue size to prevent memory overflow
- **Visual Demonstration**: Color changes show adaptation in real-time
- **Bidirectional Start**: Uses bidirectional BFS for optimal initial exploration

**Color Coding:**
- 🔵 **Blue Nodes (RESEARCH_BFS)**: BFS exploration phase
- 🟠 **Orange Nodes (RESEARCH_DFS)**: DFS exploration phase  
- 🟡 **Gold Button**: Research Mode indicator

**Research Applications:**
- Memory-constrained search environments
- Dynamic algorithm selection
- Real-time complexity adaptation
- Visual demonstration of algorithm behavior

### DABPS - Density-Adaptive Bi-Phase Search 🆕

A revolutionary **topology-aware search algorithm** that adapts to map structure:

```
DABPS Algorithm - Two Phase Approach:
╔════════════════════════════════════════════════════════════╗
║  PHASE 1: REVERSE PERIMETER BFS (The Net)                  ║
║  ─────────────────────────────────────────                 ║
║  • Start from TARGET, expand outward                       ║
║  • Build a perimeter of nodes around target                ║
║  • Limit: 50 nodes (configurable)                          ║
║  • Color: Orange (The Net)                                 ║
║                                                            ║
║  PHASE 2: ADAPTIVE FORWARD SEARCH (The Scout)              ║
║  ─────────────────────────────────────────                 ║
║  • Start from START, move toward perimeter                 ║
║  • Density Detection at each step:                         ║
║                                                            ║
║    CORRIDOR (≤1 unvisited neighbor):                       ║
║    → Use DFS (Fast, linear traversal)                      ║
║    → "We're in a tunnel, move fast!"                       ║
║                                                            ║
║    OPEN ROOM (>1 unvisited neighbor):                      ║
║    → Use BFS (Optimal, broad exploration)                  ║
║    → "We're in open space, explore carefully!"             ║
║                                                            ║
║  • Color: Cyan (The Scout)                                 ║
║                                                            ║
║  INTERCEPTION: When Scout meets Net                        ║
║  → Path reconstructed through meeting point                ║
╚════════════════════════════════════════════════════════════╝
```

**Why DABPS is Revolutionary:**

1. **Topology Awareness**: Actually "sees" the map structure (corridors vs rooms)
2. **Optimal Strategy Selection**: Chooses right algorithm for right situation
3. **Two-Phase Approach**: Perimeter acts as a "net" to catch the forward search
4. **Visual Storytelling**: Orange net + Cyan scout creates clear visual narrative

**Color Coding:**
- 🟠 **Orange (DABPS_PERIMETER)**: Perimeter building phase (The Net)
- 🔵 **Cyan (DABPS_ADAPTIVE)**: Adaptive search phase (The Scout)
- 🟢 **Green**: Start node
- 🔴 **Red**: Target node

**Research Applications:**
- Topology-aware pathfinding
- Game AI navigation (corridor vs room detection)
- Robotics path planning
- Maze-solving optimization
- Algorithmic efficiency research

**Console Output Example:**
```
[DABPS] Starting Density-Adaptive Bi-Phase Search...
[DABPS] Perimeter limit: 50 nodes
[DABPS] Perimeter built (50 nodes). Starting adaptive search...
[DABPS] ✓ Found intersection with perimeter!
[DABPS] ✓ Path found!
[DABPS] Total steps: 245
[DABPS] Perimeter nodes: 50
[DABPS] Corridors (DFS): 89, Rooms (BFS): 34
[DABPS] Density switches: 123
```

### Kinetic Wavefront Search (KWS) ⚡ HIGH-SPEED EXPERIMENTAL

A revolutionary **high-speed kinetic algorithm** that "slides" rather than crawls:

```
KWS Algorithm - Kinetic Sliding Approach:
╔════════════════════════════════════════════════════════════╗
║  THE CONCEPT: "Don't crawl, SLIDE!"                       ║
║                                                            ║
║  Traditional algorithms: Step 1 → Step 2 → Step 3...      ║
║  KWS: SLIDE until obstacle!                               ║
║                                                            ║
║  PHASE 1: KINETIC SLIDING                                  ║
║  ─────────────────────────                                 ║
║  • From stopping point, slide in 4 directions:            ║
║    → UP: Slide until wall/edge/target                     ║
║    → RIGHT: Slide until wall/edge/target                  ║
║    → DOWN: Slide until wall/edge/target                   ║
║    → LEFT: Slide until wall/edge/target                   ║
║                                                            ║
║  • Each slide creates a "beam" (laser-like path)          ║
║  • End of slide = New "stopping point" (corner)           ║
║                                                            ║
║  PHASE 2: WAVEFRONT EXPANSION                              ║
║  ─────────────────────────────                             ║
║  • Each stopping point becomes new source                 ║
║  • Wavefront expands from corners                         ║
║  • Like ripples in a pond, but kinetic!                   ║
║                                                            ║
║  STOP CONDITION: Hit target or exhaust all paths          ║
╚════════════════════════════════════════════════════════════╝
```

**Why KWS is Revolutionary:**

1. **Kinetic Movement**: Doesn't step cell-by-cell; slides rapidly across open space
2. **Laser-Scan Effect**: Visual beams show exploration like laser scanning
3. **Corner Detection**: Automatically finds strategic stopping points
4. **High-Speed**: Much faster in open areas compared to traditional algorithms
5. **Visual Drama**: Transparent blue beams + bright yellow corners = stunning visualization

**Color Coding:**
- 🔵 **Transparent Blue (KWS_BEAM)**: Slide beams / scan rays
- 🟡 **Bright Yellow (KWS_STOP)**: Stopping points / corners
- 🟢 **Green**: Start node
- 🔴 **Red**: Target node

**Visual Effect:**
```
Traditional BFS (Flood Fill):
▓▓▓▓▓
▓▓▓▓▓  ← Gradual expansion
▓▓▓▓▓

KWS (Laser Scan):
──────→  ← Instant slide
  │
  ↓
──────→  ← Another slide
```

**Research Applications:**
- High-speed open space exploration
- Corridor and corner detection
- Visual demonstration of kinetic algorithms
- Game AI for fast pathfinding
- Laser scanning simulation
- Robotics rapid exploration

**Console Output Example:**
```
[KWS] Starting Kinetic Wavefront Search...
[KWS] Sliding in cardinal directions until obstacles...
[KWS] ✓ Target reached!
[KWS] Total steps: 15
[KWS] Stopping points: 8
[KWS] Beam nodes: 127
```

### Stealth Search (Minimum Memory) 👻 GHOST MODE

A revolutionary **memory-optimized algorithm** that operates in "Ghost Mode":

```
Stealth Search - Extreme Memory Optimization:
╔════════════════════════════════════════════════════════════╗
║  THE PROBLEM: Traditional Algorithms Use Too Much Memory  ║
║                                                            ║
║  Traditional BFS/DFS: Store ALL visited nodes             ║
║  → Memory: O(nodes) - Grows with grid size                ║
║  → Example: 1000x1000 grid = 1,000,000 nodes stored!      ║
║                                                            ║
║  STEALTH SOLUTION: Only Store Current Path                ║
║  → Memory: O(depth) - Grows with path length only         ║
║  → Example: Same grid, but only 50 nodes in memory!       ║
║                                                            ║
║  THE GHOST MODE VISUALIZATION:                            ║
║  ─────────────────────────────                            ║
║                                                            ║
║  Traditional Algorithm (With Visited Set):                ║
║  ▓▓▓▓▓▓▓▓                                                ║
║  ▓VISITED▓  ← Yellow shows everywhere it's been           ║
║  ▓▓▓▓▓▓▓▓                                                ║
║                                                            ║
║  Stealth Search (Ghost Mode):                             ║
║        ╱                                                 ║
║       ╱   ← Only shows CURRENT path (Cyan)               ║
║      ●     ← Current head (Red)                          ║
║                                                            ║
║  The algorithm "forgets" where it's been!                 ║
║                                                            ║
║  CYCLE PREVENTION (The Memory Trick):                     ║
║  ───────────────────────────────────                      ║
║  Instead of checking global 'visited' set:                ║
║  → Check if neighbor is in current path stack ONLY        ║
║  → This prevents loops without storing history            ║
║                                                            ║
║  ALGORITHM STRUCTURE:                                     ║
║  ─────────────────────                                    ║
║  1. Iterative Deepening DFS (IDDFS)                       ║
║  2. Start with depth limit = 1                            ║
║  3. Increase depth until target found                     ║
║  4. Path-checking prevents cycles (no visited set!)       ║
║  5. Backtracking removes nodes from stack instantly       ║
╚════════════════════════════════════════════════════════════╝
```

**Why Stealth Search is Revolutionary:**

1. **O(depth) Memory**: Only stores current path, not entire grid
2. **Ghost Mode**: Visual shows only active path (cyan) + head (red)
3. **No Yellow Visited Nodes**: Demonstrates "forgetting" for memory savings
4. **Complete Algorithm**: Still finds optimal path (IDDFS property)
5. **Visual Drama**: Eerie ghost-like movement through the grid

**Color Coding:**
- 🔵 **Cyan (STEALTH_PATH)**: Current path stack (the active thread)
- 🔴 **Red (STEALTH_HEAD)**: Current head/node being explored
- ❌ **NO Yellow Visited Nodes**: The algorithm forgets where it's been!
- 🟢 **Green**: Start node
- 🟣 **Purple**: Target node

**Memory Comparison:**
```
Grid Size: 100x100 = 10,000 cells

Algorithm          Memory Usage      Visual
─────────────────────────────────────────────
BFS                O(10,000)         Yellow everywhere
DFS                O(10,000)         Yellow everywhere  
Stealth Search     O(path length)    Cyan path only
                   ~O(20-50)         Ghost Mode!
```

**Research Applications:**
- Extreme memory-constrained environments
- Embedded systems with limited RAM
- Demonstrating memory vs. time tradeoffs
- Visual proof of concept for minimal-memory pathfinding
- Teaching algorithmic memory complexity
- Robotics with limited onboard memory

**Console Output Example:**
```
[Stealth] Initializing Ghost Mode Search...
[Stealth] Memory optimization: NO global visited set
[Stealth] Only tracking current path stack (O(depth) memory)
[Stealth] Starting depth limit: 1
[Stealth] Increasing depth limit to 2
[Stealth] Increasing depth limit to 3
...
[Stealth] ✓ Target found!
[Stealth] Total steps: 847
[Stealth] Final depth: 15
[Stealth] Path length: 15
[Stealth] Memory used: O(15) (only path stack)
```

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
| `ESC` | Exit fullscreen / Quit (if windowed) |
| `F11` | Toggle fullscreen mode |
| `□` (Button) | Maximize/Restore window |

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

**Research Mode** 🔬 (Golden Accent Button):
- **🔬 Research Mode**: Instantly switch to Westra Adaptive Search
- **Gold Color**: Distinctive golden accent for research mode
- **One-Click**: Automatically selects the Westra algorithm
- **Visual Feedback**: Console logs show mode switch confirmation

---

## Fullscreen & Window Management ⭐ NEW

### Dynamic Window Resizing

The application now supports **fullscreen mode** and **dynamic window resizing**:

#### Fullscreen Features
- **Maximize Button**: Click the `□` / `⛶` button in the sidebar header to toggle fullscreen
- **F11 Key**: Alternative keyboard shortcut to toggle fullscreen
- **ESC Key**: Exit fullscreen mode (or quit if already windowed)
- **Smooth Transitions**: Seamless switch between windowed and fullscreen modes

#### Dynamic Grid Scaling
When the window is resized or maximized:

1. **Auto-Detection**: New screen dimensions are automatically detected
2. **Grid Recalculation**: 
   - Grid columns and rows are recalculated based on available space
   - Node size is optimized (15px - 40px range) to maximize grid coverage
   - Grid expands to fill available space minus sidebar
3. **State Preservation**:
   - Current search is paused and reset
   - Start and target positions are reinitialized
   - Walls are cleared (re-mapping complex walls to new grid is not supported)
4. **UI Adaptation**: Sidebar and all UI elements resize to fit new dimensions

#### Example Resolutions
| Mode | Window Size | Grid Size | Node Size |
|------|-------------|-----------|-----------|
| Default | 1200x800 | 40x30 | 22px |
| Maximized | 1920x1080 | ~70x45 | ~25px |
| Fullscreen | Display native | Calculated | Optimized |

**Note**: On window resize, the grid is recreated with new dimensions. This provides a fresh canvas while maintaining the professional layout and all functionality.

### Resize Event Handling

The application handles several window events:
- **VIDEORESIZE**: User drags window corner to resize
- **FULLSCREEN toggle**: Via button, F11 key, or maximize
- **Minimize/Restore**: Window state changes
- **Multi-monitor**: Works across different display configurations

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
- ✅ Fullscreen/maximize support
- ✅ Dynamic window resizing

#### Header Bar (Top of Sidebar)
- **Sleek Dark Header**: Darker background bar at top of sidebar
- **Application Title**: "Search Simulator" text
- **Maximize/Fullscreen Button**: Toggle button (□ / ⛶) in top-right corner
- **Visual Separation**: Border line separates header from controls

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
    │   ├── Header Bar (Title + Maximize Button)
    │   ├── ComboBox (Professional Dropdown)
    │   ├── Button (Cyan Hover Accents)
    │   ├── Slider (Cyan Handle)
    │   └── Telemetry Panel (Fixed Bottom)
    └── Layout System
        ├── Dynamic Y-positioning
        ├── 15px Element Padding
        ├── Z-index Management
        └── Window Resize Handling

### Window & Display System

```
Window Management
├── Fullscreen Toggle (_toggle_fullscreen)
│   ├── F11 Key Binding
│   ├── Maximize Button
│   └── ESC to Exit
├── Dynamic Grid Scaling (_on_window_resize)
│   ├── Calculate new dimensions
│   ├── Recalculate node size
│   ├── Update grid rows/cols
│   └── Recreate UI elements
└── VIDEORESIZE Event Handler
    ├── Update display surface
    ├── Recalculate all positions
    └── Refresh grid and UI
```
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

#### Core Functionality
- [ ] All 9 algorithms complete successfully
- [ ] Start/target dragging works
- [ ] Wall placement/removal works
- [ ] Random wall generation works
- [ ] Step forward/rewind work correctly
- [ ] Speed adjustment works
- [ ] Pause/resume works
- [ ] Telemetry updates in real-time
- [ ] No crashes on edge cases

#### Window Management & Fullscreen
- [ ] Fullscreen toggle via F11 key works
- [ ] Fullscreen toggle via maximize button works
- [ ] ESC key exits fullscreen mode
- [ ] Window can be resized by dragging corners
- [ ] Grid scales properly on window resize
- [ ] Grid is cleared on resize (expected behavior)
- [ ] UI elements reposition correctly on resize
- [ ] Telemetry panel stays anchored to bottom
- [ ] Sidebar maintains proper width during resize
- [ ] Application works on different screen resolutions
- [ ] Multi-monitor setup handling works

#### Research Module (Westra Adaptive Search)
- [ ] Research Mode button switches to Westra algorithm
- [ ] Blue nodes appear during BFS phase
- [ ] Orange nodes appear during DFS phase
- [ ] Color shift occurs when algorithm adapts
- [ ] Console logs show mode switches and panic events
- [ ] Algorithm handles memory panic correctly (queue > 100)
- [ ] Algorithm reverts from DFS on dead end
- [ ] Statistics show mode switch count
- [ ] Bidirectional search works correctly
- [ ] Path is found and displayed properly

#### Research Module (DABPS - Density-Adaptive Bi-Phase Search)
- [ ] DABPS algorithm appears in dropdown menu
- [ ] Orange nodes appear during perimeter building phase (The Net)
- [ ] Cyan nodes appear during adaptive search phase (The Scout)
- [ ] Perimeter is built around target (up to 50 nodes)
- [ ] Density detection works (corridor vs room)
- [ ] DFS used in corridors (≤1 neighbor)
- [ ] BFS used in open rooms (>1 neighbor)
- [ ] Interception occurs when scout meets perimeter
- [ ] Path is reconstructed correctly
- [ ] Console logs show perimeter size and density statistics
- [ ] Statistics show corridor count and room count

#### Research Module (KWS - Kinetic Wavefront Search)
- [ ] KWS algorithm appears in dropdown menu
- [ ] Transparent blue beams appear during sliding
- [ ] Bright yellow stopping points appear at corners
- [ ] Algorithm slides in 4 cardinal directions (Up, Right, Down, Left)
- [ ] Sliding stops at walls, edges, or target
- [ ] Each stopping point becomes new wavefront source
- [ ] Visual effect looks like laser scanning (not flood fill)
- [ ] Path is found by connecting stopping points
- [ ] Console logs show stopping points and beam node counts
- [ ] Statistics show beam nodes and path segments

#### Research Module (Stealth Search - Minimum Memory)
- [ ] Stealth Search algorithm appears in dropdown menu
- [ ] Cyan path shows current thread (Ghost Mode)
- [ ] Red head shows current node being explored
- [ ] NO yellow visited nodes drawn (algorithm "forgets")
- [ ] Iterative deepening increases depth limit progressively
- [ ] Path-checking only (no global visited set)
- [ ] Memory usage is O(depth) not O(nodes)
- [ ] Backtracking removes nodes from stack immediately
- [ ] Target is found using IDDFS approach
- [ ] Console logs show depth limit increases
- [ ] Statistics show memory optimization flag

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
| Header Bar | (35, 35, 40) | #232328 | Top header |
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

#### Research Module Colors
| Element | RGB Value | Hex | Usage |
|---------|-----------|-----|-------|
| Research BFS | (0, 100, 255) | #0064FF | Blue - BFS phase |
| Research DFS | (255, 140, 0) | #FF8C00 | Orange - DFS phase |
| Mode Research | (255, 215, 0) | #FFD700 | Gold - Research Mode button |
| DABPS Perimeter | (255, 140, 0) | #FF8C00 | Orange - The Net |
| DABPS Adaptive | (0, 255, 255) | #00FFFF | Cyan - The Scout |
| KWS Beam | (100, 150, 255, 120) | #6496FF78 | Transparent Blue - Scan rays |
| KWS Stop | (255, 255, 0) | #FFFF00 | Bright Yellow - Stopping points |
| Stealth Path | (0, 200, 255) | #00C8FF | Cyan - Current path stack |
| Stealth Head | (255, 50, 50) | #FF3232 | Red - Current head node |

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
│                                         │ [🔬 Research Mode]   │ │
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

## 🛡️ Comparative Analysis of Search Strategies

The following table contrasts standard uninformed search algorithms with the **Novel Westra Research Algorithms** implemented in this simulator.

| **Algorithm** | **Time Complexity** | **Space Complexity** | **Complete?** | **Optimal?** | **Westra Tactical Use Case** |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Breadth-First Search (BFS)** | $O(b^d)$ | $O(b^d)$ | Yes | Yes | **Standard Mapping:** Best for guarantees in small, unknown areas. |
| **Depth-First Search (DFS)** | $O(b^m)$ | $O(bm)$ | No | No | **Deep Penetration:** Good for finding *any* path in massive mazes where memory is tight. |
| **Uniform-Cost Search (UCS)** | $O(b^{1+ \lfloor C^*/\epsilon \rfloor})$ | $O(b^{1+ \lfloor C^*/\epsilon \rfloor})$ | Yes | Yes | **Terrain Analysis:** Essential when "mud" or "hills" (weights) are involved. |
| **Depth-Limited Search (DLS)** | $O(b^l)$ | $O(bl)$ | No | No | **Safety Perimeter:** Used when you only care about targets within $l$ clicks. |
| **Iterative Deepening (IDDFS)** | $O(b^d)$ | $O(bd)$ | Yes | Yes | **The Gold Standard:** Best balance of speed and memory for standard CPUs. |
| **Bidirectional Search** | $O(b^{d/2})$ | $O(b^{d/2})$ | Yes | Yes | **Pincer Movement:** The fastest standard algorithm, but requires knowing the Target location. |
| **Randomized DFS (Chaos)** | $O(b^m)$ | $O(bm)$ | No | No | **Evasion:** Unpredictable pathing useful for confusing adversarial AI. |
| **Scout Algorithm (Hybrid)** | Variable | Variable | Yes | No | **Reconnaissance:** Scans the perimeter (BFS) before diving deep (DFS). |
| **Westra DABPS (Research)** | **$O(b_{eff}^d)$** | **Adaptive** | Yes | Near | **Intelligent Switch:** Optimizes for "Corridors" vs "Rooms" dynamically. |
| **Kinetic Wavefront (KWS)** | **$O(k)$** | **$O(k)$** | Yes | No | **Hyperspeed:** The fastest possible traversal for open spaces (sliding). |
| **Westra Stealth Search** | $O(b^d)$ | **$O(d)$** | Yes | Yes | **Ghost Protocol:** Minimum theoretical memory usage. Zero footprint. |
| **Random Walk (Baseline)** | $O(\infty)$ | $O(1)$ | No | No | **Desperation:** The baseline "blind" movement. Used as a control variable. |

---
* **Legend:**
  * $b$: Branching factor
  * $d$: Depth of shallowest goal
  * $m$: Maximum path length
  * $k$: Number of corners (turns) in path
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

Developed for AI/CS Research
- Author: Raja Muhammad Bilal Arshad
- Version: 1.0.0
- Created: 2026

## License

This project is licensed under the MIT License.

---

**Happy Searching! 🚀**

For questions or issues, please refer to the documentation or contact the development team.
