#!/usr/bin/env python3
"""
3D Examples for Wolfram Automaton Generator

Demonstrates various 3D visualization capabilities including:
- Interactive voxel visualization
- Layer-by-layer viewing
- Animated transitions
- Multiple visualization modes
"""

from wolfram_3d import WolframAutomaton3D
import numpy as np


def example_3d_voxels():
    """Basic 3D voxel visualization with interactive controls."""
    print("Example 1: 3D Voxel Visualization")
    print("=" * 50)
    print("Creating Rule 30 with 3D voxel visualization...")
    print("Features: Pan, Zoom, Rotate with mouse")

    ca3d = WolframAutomaton3D(rule=30, width=101, generations=80)
    ca3d.generate_volume(depth=30, mode='multi_run', start_condition='single')

    fig = ca3d.visualize_3d_voxels(
        opacity=0.4,
        colorscale='Plasma'
    )

    fig.show()
    print("✓ Interactive 3D voxel plot displayed")
    print()


def example_layer_slices():
    """View multiple 2D slices of the 3D volume."""
    print("Example 2: Layer Slices")
    print("=" * 50)
    print("Creating Rule 110 with layer slice visualization...")

    ca3d = WolframAutomaton3D(rule=110, width=101, generations=80)
    ca3d.generate_volume(depth=30, mode='multi_run', start_condition='single')

    fig = ca3d.visualize_slices(
        rows=2,
        cols=3,
        colorscale='Binary'
    )

    fig.show()
    print("✓ Layer slices displayed")
    print()


def example_animated_layers():
    """Animated transition through layers."""
    print("Example 3: Animated Layer Transition")
    print("=" * 50)
    print("Creating Rule 90 with animation...")
    print("Use Play/Pause buttons and slider to control animation")

    ca3d = WolframAutomaton3D(rule=90, width=101, generations=80)
    ca3d.generate_volume(depth=40, mode='multi_run', start_condition='single')

    fig = ca3d.visualize_layer_animation(
        colorscale='Greys',
        frame_duration=100
    )

    fig.show()
    print("✓ Animated visualization displayed")
    print()


def example_3d_surface():
    """3D surface plot of automaton."""
    print("Example 4: 3D Surface Plot")
    print("=" * 50)
    print("Creating Rule 30 with 3D surface...")

    ca3d = WolframAutomaton3D(rule=30, width=101, generations=80)
    ca3d.generate_volume(depth=30, mode='multi_run', start_condition='single')

    # Surface of specific layer
    fig = ca3d.visualize_3d_surface(
        layer=15,
        colorscale='Hot'
    )

    fig.show()
    print("✓ 3D surface plot displayed")
    print()


def example_multi_rule():
    """Visualize different rules across the Z-axis."""
    print("Example 5: Multi-Rule Visualization")
    print("=" * 50)
    print("Creating volume with rules 20-40 across layers...")

    ca3d = WolframAutomaton3D(rule=30, width=101, generations=60)
    ca3d.generate_volume(
        depth=21,
        mode='multi_rule',
        start_condition='single',
        rule_range=(20, 40)
    )

    fig = ca3d.visualize_3d_voxels(
        opacity=0.3,
        colorscale='Viridis'
    )
    fig.update_layout(title='Multi-Rule Visualization: Rules 20-40')

    fig.show()
    print("✓ Multi-rule 3D visualization displayed")
    print()


def example_evolution_mode():
    """Continuous evolution across layers."""
    print("Example 6: Evolution Mode")
    print("=" * 50)
    print("Creating Rule 110 with continuous evolution...")

    ca3d = WolframAutomaton3D(rule=110, width=101, generations=60)
    ca3d.generate_volume(
        depth=30,
        mode='evolution',
        start_condition='single'
    )

    fig = ca3d.visualize_3d_voxels(
        opacity=0.35,
        colorscale='Electric'
    )
    fig.update_layout(title='Rule 110 - Continuous Evolution Mode')

    fig.show()
    print("✓ Evolution mode visualization displayed")
    print()


def example_volumetric():
    """Volumetric rendering with isosurfaces."""
    print("Example 7: Volumetric Rendering")
    print("=" * 50)
    print("Creating Rule 30 with volumetric visualization...")
    print("This may take a moment to render...")

    ca3d = WolframAutomaton3D(rule=30, width=80, generations=60)
    ca3d.generate_volume(depth=25, mode='multi_run', start_condition='single')

    fig = ca3d.visualize_3d_volume(
        threshold=0.5,
        opacity=0.1,
        surface_count=15,
        colorscale='Jet'
    )

    fig.show()
    print("✓ Volumetric rendering displayed")
    print()


def example_random_start():
    """3D visualization with random starting conditions."""
    print("Example 8: Random Starting Conditions")
    print("=" * 50)
    print("Creating Rule 90 with random starts...")

    ca3d = WolframAutomaton3D(rule=90, width=101, generations=80)
    ca3d.generate_volume(depth=25, mode='multi_run', start_condition='random')

    fig = ca3d.visualize_slices(
        rows=3,
        cols=3,
        colorscale='RdBu'
    )

    fig.show()
    print("✓ Random start visualization displayed")
    print()


def example_save_to_html():
    """Save interactive visualization to HTML file."""
    print("Example 9: Save to HTML File")
    print("=" * 50)
    print("Creating visualization and saving to file...")

    ca3d = WolframAutomaton3D(rule=30, width=101, generations=80)
    ca3d.generate_volume(depth=30, mode='multi_run', start_condition='single')

    fig = ca3d.visualize_3d_voxels(
        opacity=0.4,
        colorscale='Viridis'
    )

    filename = 'rule_30_3d.html'
    fig.write_html(filename)
    print(f"✓ Saved to {filename}")
    print(f"  Open this file in a web browser for interactive visualization")
    print()


def example_comparison():
    """Compare different rules side by side."""
    print("Example 10: Rule Comparison")
    print("=" * 50)
    print("Comparing Rules 30, 90, and 110...")

    rules = [30, 90, 110]

    for rule in rules:
        print(f"  Generating Rule {rule}...")
        ca3d = WolframAutomaton3D(rule=rule, width=101, generations=60)
        ca3d.generate_volume(depth=20, mode='multi_run', start_condition='single')

        fig = ca3d.visualize_3d_voxels(
            opacity=0.35,
            colorscale='Inferno'
        )

        filename = f'rule_{rule}_3d.html'
        fig.write_html(filename)
        print(f"    Saved to {filename}")

    print("✓ All comparisons saved!")
    print()


def main():
    """Run selected examples."""
    print("\n" + "="*60)
    print("Wolfram Automaton 3D Visualization Examples")
    print("="*60 + "\n")

    print("These examples demonstrate interactive 3D visualizations.")
    print("Controls:")
    print("  - Left mouse: Rotate")
    print("  - Right mouse: Pan")
    print("  - Scroll: Zoom")
    print("  - Double-click: Reset view")
    print("\n" + "="*60 + "\n")

    # Run examples (uncomment the ones you want to try)

    example_3d_voxels()           # Basic 3D voxels
    # example_layer_slices()        # View multiple slices
    # example_animated_layers()     # Animated layer transition
    # example_3d_surface()          # 3D surface plot
    # example_multi_rule()          # Multiple rules across Z-axis
    # example_evolution_mode()      # Continuous evolution
    # example_volumetric()          # Volumetric rendering (slower)
    # example_random_start()        # Random starting conditions
    # example_save_to_html()        # Save to HTML file
    # example_comparison()          # Compare different rules

    print("\n" + "="*60)
    print("Examples complete!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
