#!/usr/bin/env python3
"""
Example usage of the Wolfram Automaton Generator

Run with: uv run examples.py
"""

from wolfram_automaton import WolframAutomaton
import numpy as np


def example_basic():
    """Basic example with Rule 30"""
    print("Generating Rule 30 with default settings...")
    ca = WolframAutomaton(rule=30, width=101, generations=100)
    ca.generate(start_condition='single')
    ca.visualize()


def example_different_widths():
    """Example showing different widths"""
    print("\nGenerating Rule 110 with different widths...")

    widths = [51, 101, 201]
    for width in widths:
        ca = WolframAutomaton(rule=110, width=width, generations=80)
        ca.generate(start_condition='single')
        ca.visualize(save_path=f'rule110_width_{width}.png', show=False)
        print(f"  Saved rule110_width_{width}.png")


def example_random_start():
    """Example with random starting condition"""
    print("\nGenerating Rule 90 with random start...")
    ca = WolframAutomaton(rule=90, width=101, generations=100)
    ca.generate(start_condition='random')
    ca.visualize()


def example_custom_start():
    """Example with custom starting condition"""
    print("\nGenerating Rule 30 with custom pattern...")

    # Create a custom starting pattern
    width = 101
    custom_start = np.zeros(width)

    # Set specific cells to 1
    custom_start[30:35] = 1   # Small block on the left
    custom_start[50] = 1        # Single cell in center
    custom_start[65:75] = 1    # Larger block on the right

    ca = WolframAutomaton(rule=30, width=width, generations=100)
    ca.generate(start_condition='custom', custom_state=custom_start)
    ca.visualize()


def example_famous_rules():
    """Generate several famous rules"""
    print("\nGenerating famous Wolfram rules...")

    famous_rules = {
        30: "Chaotic",
        90: "Sierpinski Triangle",
        110: "Turing Complete",
        184: "Traffic Flow",
        54: "Complex Pattern"
    }

    for rule, description in famous_rules.items():
        print(f"  Generating Rule {rule} ({description})...")
        ca = WolframAutomaton(rule=rule, width=101, generations=100)
        ca.generate(start_condition='single')
        ca.visualize(save_path=f'rule_{rule}.png', show=False)


def example_comparison():
    """Compare same rule with different starting conditions"""
    print("\nComparing Rule 30 with different starting conditions...")

    conditions = ['single', 'random']

    for condition in conditions:
        ca = WolframAutomaton(rule=30, width=101, generations=100)
        ca.generate(start_condition=condition)
        ca.visualize(save_path=f'rule30_{condition}.png', show=False)
        print(f"  Saved rule30_{condition}.png")


if __name__ == '__main__':
    print("Wolfram Automaton Examples")
    print("=" * 50)

    # Run examples
    # Uncomment the ones you want to try:

    example_basic()              # Simple Rule 30
    # example_different_widths()   # Different line widths
    # example_random_start()       # Random starting condition
    # example_custom_start()       # Custom starting pattern
    # example_famous_rules()       # Generate famous rules
    # example_comparison()         # Compare starting conditions

    print("\nExamples complete!")
