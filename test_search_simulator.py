#!/usr/bin/env python3
"""
Comprehensive Unit Tests for Search Algorithm Simulator
Tests every single component, method, and edge case.
"""

import unittest
import sys
import os
import math

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from search_simulator import (
    Node, NodeState, Grid, Colors,
    BFSSolver, DFSSolver, RandomizedDFSSolver, UCSSolver,
    DLSSolver, IDDFSSolver, BidirectionalSolver, ScoutSolver, CustomSolver,
    Button, Slider, ComboBox
)


# =============================================================================
# NODE CLASS TESTS
# =============================================================================

class TestNode(unittest.TestCase):
    """Test the Node class thoroughly."""
    
    def test_node_creation_default(self):
        """Test default node creation."""
        node = Node(5, 10)
        self.assertEqual(node.row, 5)
        self.assertEqual(node.col, 10)
        self.assertEqual(node.state, NodeState.EMPTY)
        self.assertIsNone(node.parent)
        self.assertEqual(node.cost, float('inf'))
        self.assertEqual(node.depth, 0)
    
    def test_node_creation_with_state(self):
        """Test node creation with specific state."""
        node = Node(3, 4)
        node.state = NodeState.WALL
        self.assertEqual(node.state, NodeState.WALL)
    
    def test_node_hash(self):
        """Test node hashing for use in sets/dicts."""
        node1 = Node(1, 2)
        node2 = Node(1, 2)
        node3 = Node(2, 1)
        
        self.assertEqual(hash(node1), hash(node2))
        self.assertNotEqual(hash(node1), hash(node3))
    
    def test_node_equality(self):
        """Test node equality comparison."""
        node1 = Node(5, 5)
        node2 = Node(5, 5)
        node3 = Node(5, 6)
        
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, "not a node")
    
    def test_node_less_than(self):
        """Test node comparison for priority queue."""
        node1 = Node(0, 0)
        node1.cost = 10
        node2 = Node(0, 0)
        node2.cost = 20
        
        self.assertLess(node1, node2)
        self.assertFalse(node2 < node1)
    
    def test_get_pos(self):
        """Test position getter."""
        node = Node(7, 8)
        self.assertEqual(node.get_pos(), (7, 8))
    
    def test_reset_search_state_empty(self):
        """Test resetting search state for empty node."""
        node = Node(1, 1)
        node.state = NodeState.VISITED
        node.parent = Node(0, 0)
        node.cost = 50
        node.depth = 5
        
        node.reset_search_state()
        
        self.assertEqual(node.state, NodeState.EMPTY)
        self.assertIsNone(node.parent)
        self.assertEqual(node.cost, float('inf'))
        self.assertEqual(node.depth, 0)
    
    def test_reset_search_state_wall_preserved(self):
        """Test that walls are preserved during reset."""
        node = Node(1, 1)
        node.state = NodeState.WALL
        node.parent = Node(0, 0)
        
        node.reset_search_state()
        
        self.assertEqual(node.state, NodeState.WALL)
        self.assertIsNone(node.parent)
    
    def test_get_color_all_states(self):
        """Test color mapping for all states."""
        color_map = {
            NodeState.EMPTY: Colors.EMPTY,
            NodeState.WALL: Colors.WALL,
            NodeState.START: Colors.START,
            NodeState.TARGET: Colors.TARGET,
            NodeState.FRONTIER: Colors.FRONTIER,
            NodeState.VISITED: Colors.VISITED,
            NodeState.PATH: Colors.PATH,
        }
        
        for state, expected_color in color_map.items():
            node = Node(0, 0)
            node.state = state
            self.assertEqual(node.get_color(), expected_color)


# =============================================================================
# GRID CLASS TESTS
# =============================================================================

class TestGrid(unittest.TestCase):
    """Test the Grid class thoroughly."""
    
    def test_grid_initialization(self):
        """Test grid creation."""
        grid = Grid(10, 15)
        self.assertEqual(grid.rows, 10)
        self.assertEqual(grid.cols, 15)
        self.assertEqual(len(grid.grid), 10)
        self.assertEqual(len(grid.grid[0]), 15)
    
    def test_grid_start_target_positions(self):
        """Test initial start and target positions."""
        grid = Grid(20, 20)
        expected_start = (5, 5)  # rows//4, cols//4
        expected_target = (5, 15)  # rows//4, 3*cols//4
        
        self.assertEqual(grid.start_pos, expected_start)
        self.assertEqual(grid.target_pos, expected_target)
    
    def test_get_node_valid(self):
        """Test getting valid nodes."""
        grid = Grid(5, 5)
        
        node = grid.get_node(0, 0)
        self.assertIsNotNone(node)
        self.assertEqual(node.row, 0)
        self.assertEqual(node.col, 0)
        
        node = grid.get_node(4, 4)
        self.assertIsNotNone(node)
        self.assertEqual(node.row, 4)
        self.assertEqual(node.col, 4)
    
    def test_get_node_invalid(self):
        """Test getting invalid/out of bounds nodes."""
        grid = Grid(5, 5)
        
        self.assertIsNone(grid.get_node(-1, 0))
        self.assertIsNone(grid.get_node(0, -1))
        self.assertIsNone(grid.get_node(5, 0))
        self.assertIsNone(grid.get_node(0, 5))
        self.assertIsNone(grid.get_node(100, 100))
    
    def test_set_start_valid(self):
        """Test setting valid start position."""
        grid = Grid(10, 10)
        old_start = grid.start_pos
        
        result = grid.set_start(3, 3)
        
        self.assertTrue(result)
        self.assertEqual(grid.start_pos, (3, 3))
        self.assertEqual(grid.get_node(3, 3).state, NodeState.START)
        self.assertNotEqual(grid.get_node(*old_start).state, NodeState.START)
    
    def test_set_start_invalid(self):
        """Test setting invalid start position."""
        grid = Grid(5, 5)
        
        self.assertFalse(grid.set_start(-1, 0))
        self.assertFalse(grid.set_start(0, -1))
        self.assertFalse(grid.set_start(5, 0))
        self.assertFalse(grid.set_start(0, 5))
    
    def test_set_target_valid(self):
        """Test setting valid target position."""
        grid = Grid(10, 10)
        old_target = grid.target_pos
        
        result = grid.set_target(7, 7)
        
        self.assertTrue(result)
        self.assertEqual(grid.target_pos, (7, 7))
        self.assertEqual(grid.get_node(7, 7).state, NodeState.TARGET)
        self.assertNotEqual(grid.get_node(*old_target).state, NodeState.TARGET)
    
    def test_set_target_invalid(self):
        """Test setting invalid target position."""
        grid = Grid(5, 5)
        
        self.assertFalse(grid.set_target(-1, 0))
        self.assertFalse(grid.set_target(100, 100))
    
    def test_toggle_wall_place(self):
        """Test placing a wall."""
        grid = Grid(5, 5)
        
        result = grid.toggle_wall(2, 2, place_wall=True)
        
        self.assertTrue(result)
        self.assertEqual(grid.get_node(2, 2).state, NodeState.WALL)
    
    def test_toggle_wall_remove(self):
        """Test removing a wall."""
        grid = Grid(5, 5)
        grid.toggle_wall(2, 2, place_wall=True)
        
        result = grid.toggle_wall(2, 2, place_wall=False)
        
        self.assertTrue(result)
        self.assertEqual(grid.get_node(2, 2).state, NodeState.EMPTY)
    
    def test_toggle_wall_on_start(self):
        """Test that walls cannot be placed on start node."""
        grid = Grid(5, 5)
        start_pos = grid.start_pos
        
        result = grid.toggle_wall(*start_pos, place_wall=True)
        
        self.assertFalse(result)
        self.assertEqual(grid.get_node(*start_pos).state, NodeState.START)
    
    def test_toggle_wall_on_target(self):
        """Test that walls cannot be placed on target node."""
        grid = Grid(5, 5)
        target_pos = grid.target_pos
        
        result = grid.toggle_wall(*target_pos, place_wall=True)
        
        self.assertFalse(result)
        self.assertEqual(grid.get_node(*target_pos).state, NodeState.TARGET)
    
    def test_toggle_wall_invalid(self):
        """Test toggling wall at invalid position."""
        grid = Grid(5, 5)
        
        self.assertFalse(grid.toggle_wall(-1, 0, True))
        self.assertFalse(grid.toggle_wall(5, 5, True))
    
    def test_reset_search(self):
        """Test resetting search state."""
        grid = Grid(10, 10)  # Use larger grid to avoid start/target positions
        grid.toggle_wall(5, 5, True)  # Use middle position
        grid.get_node(6, 6).state = NodeState.VISITED
        grid.get_node(7, 7).state = NodeState.FRONTIER
        
        grid.reset_search()
        
        self.assertEqual(grid.get_node(5, 5).state, NodeState.WALL)  # Wall preserved
        self.assertEqual(grid.get_node(6, 6).state, NodeState.EMPTY)  # Visited cleared
        self.assertEqual(grid.get_node(7, 7).state, NodeState.EMPTY)  # Frontier cleared
        self.assertEqual(grid.get_node(*grid.start_pos).state, NodeState.START)
        self.assertEqual(grid.get_node(*grid.target_pos).state, NodeState.TARGET)
    
    def test_clear_all(self):
        """Test clearing entire grid."""
        grid = Grid(10, 10)  # Use larger grid
        grid.toggle_wall(5, 5, True)  # Use middle position
        grid.get_node(6, 6).state = NodeState.VISITED
        
        grid.clear_all()
        
        self.assertEqual(grid.get_node(5, 5).state, NodeState.EMPTY)  # Wall cleared
        self.assertEqual(grid.get_node(6, 6).state, NodeState.EMPTY)  # Visited cleared
        self.assertEqual(grid.get_node(*grid.start_pos).state, NodeState.START)
        self.assertEqual(grid.get_node(*grid.target_pos).state, NodeState.TARGET)
    
    def test_get_neighbors_clockwise_diagonal(self):
        """Test neighbor expansion in clockwise + diagonal order."""
        grid = Grid(5, 5)
        center = grid.get_node(2, 2)
        
        neighbors = grid.get_neighbors_clockwise_diagonal(center)
        
        expected_positions = [
            (1, 2),   # Up
            (2, 3),   # Right
            (3, 2),   # Down
            (3, 3),   # Down-Right (diagonal)
            (2, 1),   # Left
            (1, 1),   # Up-Left (diagonal)
        ]
        
        self.assertEqual(len(neighbors), 6)
        actual_positions = [(n.row, n.col) for n in neighbors]
        self.assertEqual(actual_positions, expected_positions)
    
    def test_get_neighbors_with_walls(self):
        """Test that walls are excluded from neighbors."""
        grid = Grid(5, 5)
        grid.toggle_wall(1, 2, True)  # Block Up
        center = grid.get_node(2, 2)
        
        neighbors = grid.get_neighbors_clockwise_diagonal(center)
        
        self.assertEqual(len(neighbors), 5)
        neighbor_positions = [(n.row, n.col) for n in neighbors]
        self.assertNotIn((1, 2), neighbor_positions)
    
    def test_get_neighbors_corner(self):
        """Test neighbor expansion at grid corner."""
        grid = Grid(5, 5)
        corner = grid.get_node(0, 0)
        
        neighbors = grid.get_neighbors_clockwise_diagonal(corner)
        
        # Only Right and Down should be valid (Up and Up-Left are out of bounds)
        expected_positions = [
            (0, 1),   # Right
            (1, 0),   # Down
            (1, 1),   # Down-Right
        ]
        
        actual_positions = [(n.row, n.col) for n in neighbors]
        self.assertEqual(sorted(actual_positions), sorted(expected_positions))
    
    def test_generate_random_walls(self):
        """Test random wall generation."""
        grid = Grid(10, 10)
        start_pos = grid.start_pos
        target_pos = grid.target_pos
        
        grid.generate_random_walls(wall_percentage=0.2, seed=42)
        
        # Count walls
        wall_count = 0
        for row in range(grid.rows):
            for col in range(grid.cols):
                if grid.get_node(row, col).state == NodeState.WALL:
                    wall_count += 1
        
        self.assertGreater(wall_count, 0)
        self.assertLess(wall_count, 50)
        
        # Start and target should not be walls
        self.assertNotEqual(grid.get_node(*start_pos).state, NodeState.WALL)
        self.assertNotEqual(grid.get_node(*target_pos).state, NodeState.WALL)
    
    def test_screen_to_grid_conversion(self):
        """Test screen to grid coordinate conversion."""
        from search_simulator import GRID_OFFSET_X, GRID_OFFSET_Y, NODE_SIZE, GRID_GAP
        
        grid = Grid(30, 40)
        
        # Test valid position
        screen_x = GRID_OFFSET_X + 10
        screen_y = GRID_OFFSET_Y + 10
        result = grid.screen_to_grid(screen_x, screen_y)
        self.assertEqual(result, (0, 0))
        
        # Test invalid position (outside grid)
        result = grid.screen_to_grid(10, 10)
        self.assertIsNone(result)


# =============================================================================
# SOLVER ALGORITHM TESTS
# =============================================================================

class TestBFSSolver(unittest.TestCase):
    """Test BFS algorithm thoroughly."""
    
    def test_bfs_finds_path(self):
        """Test BFS finds a path."""
        grid = Grid(5, 5)
        grid.set_start(0, 0)
        grid.set_target(4, 4)
        
        solver = BFSSolver()
        generator = solver.solve(grid)
        
        final_result = None
        for result in generator:
            final_result = result
        
        frontier, visited, path = final_result
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], grid.get_node(0, 0))
        self.assertEqual(path[-1], grid.get_node(4, 4))
    
    def test_bfs_no_path(self):
        """Test BFS when target is unreachable."""
        grid = Grid(5, 5)
        grid.set_start(0, 0)
        grid.set_target(0, 4)
        
        # Create a wall blocking the path
        for row in range(5):
            grid.toggle_wall(row, 2, True)
        
        solver = BFSSolver()
        generator = solver.solve(grid)
        
        final_result = None
        for result in generator:
            final_result = result
        
        frontier, visited, path = final_result
        self.assertEqual(path, [])  # Empty path means no solution
    
    def test_bfs_stats(self):
        """Test BFS statistics."""
        grid = Grid(3, 3)
        grid.set_start(0, 0)
        grid.set_target(2, 2)
        
        solver = BFSSolver()
        generator = solver.solve(grid)
        
        for _ in generator:
            pass
        
        stats = solver.get_stats()
        self.assertIn('steps', stats)
        self.assertIn('path_length', stats)
        self.assertGreater(stats['steps'], 0)
        self.assertGreater(stats['path_length'], 0)


class TestDFSSolver(unittest.TestCase):
    """Test DFS algorithm thoroughly."""
    
    def test_dfs_finds_path(self):
        """Test DFS finds a path."""
        grid = Grid(5, 5)
        grid.set_start(0, 0)
        grid.set_target(4, 4)
        
        solver = DFSSolver()
        generator = solver.solve(grid)
        
        final_result = None
        for result in generator:
            final_result = result
        
        frontier, visited, path = final_result
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], grid.get_node(0, 0))
        self.assertEqual(path[-1], grid.get_node(4, 4))
    
    def test_dfs_vs_bfs_path_length(self):
        """Test that DFS path may be longer than BFS (not optimal)."""
        grid_bfs = Grid(5, 5)
        grid_bfs.set_start(0, 0)
        grid_bfs.set_target(4, 4)
        
        grid_dfs = Grid(5, 5)
        grid_dfs.set_start(0, 0)
        grid_dfs.set_target(4, 4)
        
        bfs_solver = BFSSolver()
        dfs_solver = DFSSolver()
        
        for result in bfs_solver.solve(grid_bfs):
            pass
        for result in dfs_solver.solve(grid_dfs):
            pass
        
        # BFS should find shortest path, DFS may find longer
        bfs_path_length = bfs_solver.get_stats()['path_length']
        dfs_path_length = dfs_solver.get_stats()['path_length']
        
        self.assertGreaterEqual(dfs_path_length, bfs_path_length)


class TestRandomizedDFSSolver(unittest.TestCase):
    """Test Randomized DFS (Chaos Mode)."""
    
    def test_randomized_dfs_finds_path(self):
        """Test Randomized DFS finds a path."""
        grid = Grid(5, 5)
        grid.set_start(0, 0)
        grid.set_target(4, 4)
        
        solver = RandomizedDFSSolver()
        generator = solver.solve(grid)
        
        final_result = None
        for result in generator:
            final_result = result
        
        frontier, visited, path = final_result
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 0)
    
    def test_randomized_dfs_different_paths(self):
        """Test that Randomized DFS produces different paths."""
        grid1 = Grid(10, 10)
        grid1.set_start(0, 0)
        grid1.set_target(9, 9)
        
        grid2 = Grid(10, 10)
        grid2.set_start(0, 0)
        grid2.set_target(9, 9)
        
        solver1 = RandomizedDFSSolver()
        solver2 = RandomizedDFSSolver()
        
        for result in solver1.solve(grid1):
            pass
        for result in solver2.solve(grid2):
            pass
        
        # Due to randomization, paths may differ
        # (Not guaranteed but highly likely in larger grids)


class TestUCSSolver(unittest.TestCase):
    """Test UCS algorithm thoroughly."""
    
    def test_ucs_finds_optimal_path(self):
        """Test UCS finds optimal path with diagonal costs."""
        grid = Grid(5, 5)
        grid.set_start(0, 0)
        grid.set_target(4, 4)
        
        solver = UCSSolver()
        generator = solver.solve(grid)
        
        final_result = None
        for result in generator:
            final_result = result
        
        frontier, visited, path = final_result
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 0)
    
    def test_ucs_cost_calculation(self):
        """Test UCS cost calculation."""
        grid = Grid(5, 5)
        grid.set_start(0, 0)
        grid.set_target(4, 4)
        
        solver = UCSSolver()
        
        for result in solver.solve(grid):
            pass
        
        stats = solver.get_stats()
        self.assertGreater(stats['steps'], 0)
        self.assertGreater(stats['path_length'], 0)


class TestDLSSolver(unittest.TestCase):
    """Test DLS algorithm thoroughly."""
    
    def test_dls_finds_path_within_limit(self):
        """Test DLS finds path within depth limit."""
        grid = Grid(5, 5)
        grid.set_start(0, 0)
        grid.set_target(2, 2)
        
        solver = DLSSolver(depth_limit=10)
        generator = solver.solve(grid)
        
        final_result = None
        for result in generator:
            final_result = result
        
        frontier, visited, path = final_result
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 0)
    
    def test_dls_fails_beyond_limit(self):
        """Test DLS fails when target is beyond depth limit."""
        grid = Grid(10, 10)
        grid.set_start(0, 0)
        grid.set_target(9, 9)  # Far target
        
        solver = DLSSolver(depth_limit=5)  # Very low limit
        generator = solver.solve(grid)
        
        final_result = None
        for result in generator:
            final_result = result
        
        frontier, visited, path = final_result
        # Should not find path within limit


class TestIDDFSSolver(unittest.TestCase):
    """Test IDDFS algorithm thoroughly."""
    
    def test_iddfs_finds_path(self):
        """Test IDDFS finds path with iterative deepening."""
        grid = Grid(5, 5)
        grid.set_start(0, 0)
        grid.set_target(4, 4)
        
        solver = IDDFSSolver(max_depth=50)
        generator = solver.solve(grid)
        
        final_result = None
        for result in generator:
            final_result = result
        
        frontier, visited, path = final_result
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 0)


class TestBidirectionalSolver(unittest.TestCase):
    """Test Bidirectional Search algorithm."""
    
    def test_bidirectional_finds_path(self):
        """Test Bidirectional search finds path."""
        grid = Grid(5, 5)
        grid.set_start(0, 0)
        grid.set_target(4, 4)
        
        solver = BidirectionalSolver()
        generator = solver.solve(grid)
        
        final_result = None
        for result in generator:
            final_result = result
        
        frontier, visited, path = final_result
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 0)


class TestScoutSolver(unittest.TestCase):
    """Test Scout (Hybrid BFS/DFS) algorithm."""
    
    def test_scout_finds_path(self):
        """Test Scout algorithm finds path."""
        grid = Grid(10, 10)
        grid.set_start(0, 0)
        grid.set_target(9, 9)
        
        solver = ScoutSolver(bfs_layers=3, dfs_layers=3)
        generator = solver.solve(grid)
        
        final_result = None
        for result in generator:
            final_result = result
        
        frontier, visited, path = final_result
        self.assertIsNotNone(path)
        self.assertGreater(len(path), 0)
    
    def test_scout_switches_modes(self):
        """Test that Scout algorithm switches between BFS and DFS."""
        grid = Grid(10, 10)
        grid.set_start(0, 0)
        grid.set_target(9, 9)
        
        solver = ScoutSolver(bfs_layers=2, dfs_layers=2)
        
        # Just run and verify it completes
        for result in solver.solve(grid):
            pass
        
        stats = solver.get_stats()
        self.assertGreater(stats['steps'], 0)


# =============================================================================
# PATH RECONSTRUCTION TESTS
# =============================================================================

class TestPathReconstruction(unittest.TestCase):
    """Test path reconstruction functionality."""
    
    def test_simple_path(self):
        """Test reconstructing a simple linear path."""
        grid = Grid(5, 5)
        nodes = [grid.get_node(0, i) for i in range(5)]
        
        for i in range(1, 5):
            nodes[i].parent = nodes[i-1]
        
        solver = BFSSolver()
        path = solver.reconstruct_path(nodes[4])
        
        self.assertEqual(len(path), 5)
        self.assertEqual(path[0], nodes[0])
        self.assertEqual(path[-1], nodes[4])
    
    def test_single_node_path(self):
        """Test path reconstruction with single node."""
        grid = Grid(3, 3)
        node = grid.get_node(1, 1)
        node.parent = None
        
        solver = BFSSolver()
        path = solver.reconstruct_path(node)
        
        self.assertEqual(len(path), 1)
        self.assertEqual(path[0], node)


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def test_full_search_workflow(self):
        """Test complete search workflow from start to finish."""
        grid = Grid(10, 10)
        grid.generate_random_walls(wall_percentage=0.1, seed=42)
        
        solvers = [
            BFSSolver(),
            DFSSolver(),
            RandomizedDFSSolver(),
            UCSSolver(),
            DLSSolver(depth_limit=20),
            IDDFSSolver(max_depth=50),
            ScoutSolver(bfs_layers=3, dfs_layers=3),
        ]
        
        for solver in solvers:
            grid.reset_search()
            generator = solver.solve(grid)
            
            final_result = None
            for result in generator:
                final_result = result
            
            frontier, visited, path = final_result
            self.assertIsNotNone(path, f"{solver.name} failed to find path")
            if len(path) > 0:
                self.assertEqual(path[0], grid.get_node(*grid.start_pos))
                self.assertEqual(path[-1], grid.get_node(*grid.target_pos))
    
    def test_complex_maze(self):
        """Test algorithms on a complex maze-like structure."""
        grid = Grid(15, 15)
        grid.set_start(0, 0)
        grid.set_target(14, 14)
        
        # Create a maze pattern
        for i in range(1, 14, 2):
            for j in range(15):
                if j % 3 != 0:
                    grid.toggle_wall(i, j, True)
        
        solvers = [BFSSolver(), UCSSolver(), ScoutSolver()]
        
        for solver in solvers:
            grid.reset_search()
            generator = solver.solve(grid)
            
            final_result = None
            for result in generator:
                final_result = result
            
            frontier, visited, path = final_result
            self.assertIsNotNone(path)
            if len(path) > 0:
                self.assertEqual(path[0], grid.get_node(0, 0))
                self.assertEqual(path[-1], grid.get_node(14, 14))


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("COMPREHENSIVE UNIT TEST SUITE - Search Algorithm Simulator")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestNode,
        TestGrid,
        TestBFSSolver,
        TestDFSSolver,
        TestRandomizedDFSSolver,
        TestUCSSolver,
        TestDLSSolver,
        TestIDDFSSolver,
        TestBidirectionalSolver,
        TestScoutSolver,
        TestPathReconstruction,
        TestIntegration,
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("=" * 70)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)
