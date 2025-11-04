#!/usr/bin/env python3
"""
Wolfram Automaton Generator

A simple application to generate and visualize elementary cellular automata
(Wolfram automaton) with different rules, widths, and starting conditions.

Run with: uv run wolfram_automaton.py -r 30
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Literal, Optional


class WolframAutomaton:
    """
    Generate and visualize elementary cellular automata (Wolfram automaton).

    Elementary cellular automata are the simplest class of one-dimensional
    cellular automata. They are defined by a rule number (0-255) that
    determines how each cell evolves based on its current state and the
    states of its two neighbors.
    """

    def __init__(self, rule: int, width: int = 101, generations: int = 100):
        """
        Initialize the Wolfram Automaton generator.

        Args:
            rule: Rule number (0-255) for the cellular automaton
            width: Number of cells in each row (line width)
            generations: Number of generations to simulate
        """
        if not 0 <= rule <= 255:
            raise ValueError("Rule must be between 0 and 255")

        self.rule = rule
        self.width = width
        self.generations = generations
        self.rule_binary = format(rule, '08b')
        self.grid = None

    def _apply_rule(self, left: int, center: int, right: int) -> int:
        """
        Apply the rule to determine the next state of a cell.

        Args:
            left: State of left neighbor (0 or 1)
            center: Current state of cell (0 or 1)
            right: State of right neighbor (0 or 1)

        Returns:
            Next state of the cell (0 or 1)
        """
        # Convert the three-cell neighborhood to a binary number (0-7)
        neighborhood = (left << 2) | (center << 1) | right
        # Return the corresponding bit from the rule
        return int(self.rule_binary[7 - neighborhood])

    def generate(self,
                 start_condition: Literal['single', 'random', 'custom'] = 'single',
                 custom_state: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Generate the cellular automaton.

        Args:
            start_condition: Type of initial condition
                - 'single': Single cell in the middle
                - 'random': Random initial state
                - 'custom': Custom initial state (provide custom_state)
            custom_state: Custom initial state array (only used if start_condition='custom')

        Returns:
            2D numpy array representing the automaton grid
        """
        # Initialize the grid
        self.grid = np.zeros((self.generations, self.width), dtype=int)

        # Set initial condition
        if start_condition == 'single':
            self.grid[0, self.width // 2] = 1
        elif start_condition == 'random':
            self.grid[0] = np.random.randint(0, 2, self.width)
        elif start_condition == 'custom':
            if custom_state is None:
                raise ValueError("custom_state must be provided when start_condition='custom'")
            if len(custom_state) != self.width:
                raise ValueError(f"custom_state must have length {self.width}")
            self.grid[0] = custom_state
        else:
            raise ValueError("start_condition must be 'single', 'random', or 'custom'")

        # Generate subsequent generations
        for i in range(1, self.generations):
            for j in range(self.width):
                # Get neighbors with periodic boundary conditions
                left = self.grid[i-1, (j-1) % self.width]
                center = self.grid[i-1, j]
                right = self.grid[i-1, (j+1) % self.width]

                # Apply rule
                self.grid[i, j] = self._apply_rule(left, center, right)

        return self.grid

    def visualize(self, save_path: Optional[str] = None, show: bool = True):
        """
        Visualize the cellular automaton.

        Args:
            save_path: Path to save the figure (optional)
            show: Whether to display the figure
        """
        if self.grid is None:
            raise ValueError("Must call generate() before visualize()")

        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(self.grid, cmap='binary', interpolation='nearest')
        ax.set_title(f'Wolfram Automaton - Rule {self.rule}', fontsize=16, fontweight='bold')
        ax.set_xlabel('Cell Position', fontsize=12)
        ax.set_ylabel('Generation', fontsize=12)

        # Add grid info as text
        info_text = f'Width: {self.width} | Generations: {self.generations}'
        ax.text(0.5, -0.08, info_text, transform=ax.transAxes,
                ha='center', fontsize=10, style='italic')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Saved to {save_path}")

        if show:
            plt.show()
        else:
            plt.close()


def generate_all_rules(width: int = 101, generations: int = 50,
                       start_condition: Literal['single', 'random'] = 'single',
                       save_dir: str = 'output'):
    """
    Generate visualizations for all 256 elementary cellular automaton rules.

    Args:
        width: Number of cells in each row
        generations: Number of generations to simulate
        start_condition: Initial condition type
        save_dir: Directory to save the images
    """
    import os

    # Create output directory
    os.makedirs(save_dir, exist_ok=True)

    print(f"Generating all 256 rules with width={width}, generations={generations}")
    print(f"Saving to directory: {save_dir}")

    for rule in range(256):
        if rule % 32 == 0:
            print(f"Progress: {rule}/256 rules generated...")

        ca = WolframAutomaton(rule, width, generations)
        ca.generate(start_condition=start_condition)
        ca.visualize(save_path=f'{save_dir}/rule_{rule:03d}.png', show=False)

    print("Complete! All 256 rules generated.")


def main():
    """Main function to demonstrate usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate Wolfram Elementary Cellular Automata',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate Rule 30 with default settings
  python wolfram_automaton.py -r 30

  # Generate Rule 110 with custom width and generations
  python wolfram_automaton.py -r 110 -w 201 -g 150

  # Generate Rule 90 with random start condition
  python wolfram_automaton.py -r 90 -s random

  # Generate all rules and save to output directory
  python wolfram_automaton.py --all -w 101 -g 50 -o output
        """
    )

    parser.add_argument('-r', '--rule', type=int,
                        help='Rule number (0-255)')
    parser.add_argument('-w', '--width', type=int, default=101,
                        help='Width of the automaton (number of cells, default: 101)')
    parser.add_argument('-g', '--generations', type=int, default=100,
                        help='Number of generations (default: 100)')
    parser.add_argument('-s', '--start', choices=['single', 'random'],
                        default='single',
                        help='Starting condition (default: single)')
    parser.add_argument('-o', '--output', type=str,
                        help='Save figure to file')
    parser.add_argument('--all', action='store_true',
                        help='Generate all 256 rules')
    parser.add_argument('--no-show', action='store_true',
                        help='Do not display the figure')

    args = parser.parse_args()

    if args.all:
        # Generate all rules
        output_dir = args.output if args.output else 'output'
        generate_all_rules(
            width=args.width,
            generations=args.generations,
            start_condition=args.start,
            save_dir=output_dir
        )
    else:
        # Generate single rule
        if args.rule is None:
            parser.error("--rule is required unless --all is specified")

        ca = WolframAutomaton(args.rule, args.width, args.generations)
        ca.generate(start_condition=args.start)
        ca.visualize(save_path=args.output, show=not args.no_show)


if __name__ == '__main__':
    main()
