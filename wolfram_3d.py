#!/usr/bin/env python3
"""
3D Visualization for Wolfram Automaton

Provides interactive 3D visualizations of cellular automata with:
- Layer-by-layer viewing
- Full 3D structure visualization
- Interactive pan, zoom, and rotate controls
- Multiple visualization styles (voxels, surface, scatter)
"""

import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Optional, Literal, List
from wolfram_automaton import WolframAutomaton


class WolframAutomaton3D(WolframAutomaton):
    """
    Extended Wolfram Automaton with 3D visualization capabilities.

    The 3D structure is created by stacking 2D automaton grids (generations)
    as layers, creating a volumetric representation where:
    - X axis: Cell position
    - Y axis: Generation (time)
    - Z axis: Can represent multiple runs, rules, or parameter variations
    """

    def __init__(self, rule: int, width: int = 101, generations: int = 100):
        """Initialize the 3D Wolfram Automaton generator."""
        super().__init__(rule, width, generations)
        self.volume = None

    def generate_volume(self,
                       depth: int = 50,
                       mode: Literal['multi_run', 'multi_rule', 'evolution'] = 'multi_run',
                       start_condition: Literal['single', 'random', 'custom'] = 'single',
                       rule_range: Optional[tuple] = None) -> np.ndarray:
        """
        Generate a 3D volume of cellular automata.

        Args:
            depth: Number of layers in the Z dimension
            mode: How to generate the 3D volume
                - 'multi_run': Multiple independent runs with same rule
                - 'multi_rule': Different rules across Z axis
                - 'evolution': Continuous evolution in Z direction
            start_condition: Initial condition type
            rule_range: Tuple of (start_rule, end_rule) for multi_rule mode

        Returns:
            3D numpy array (generations, width, depth)
        """
        self.volume = np.zeros((self.generations, self.width, depth), dtype=int)

        if mode == 'multi_run':
            # Generate multiple independent runs
            for z in range(depth):
                self.generate(start_condition=start_condition)
                self.volume[:, :, z] = self.grid

        elif mode == 'multi_rule':
            # Generate with different rules
            if rule_range is None:
                # Use rules around the current rule
                start_rule = max(0, self.rule - depth // 2)
                end_rule = min(255, start_rule + depth)
            else:
                start_rule, end_rule = rule_range

            rules = np.linspace(start_rule, end_rule, depth, dtype=int)
            original_rule = self.rule

            for z, rule in enumerate(rules):
                self.rule = rule
                self.rule_binary = format(rule, '08b')
                self.generate(start_condition=start_condition)
                self.volume[:, :, z] = self.grid

            self.rule = original_rule
            self.rule_binary = format(original_rule, '08b')

        elif mode == 'evolution':
            # Continuous evolution: each Z layer evolves from previous
            self.generate(start_condition=start_condition)
            self.volume[:, :, 0] = self.grid

            for z in range(1, depth):
                # Use last row of previous layer as starting condition
                custom_start = self.volume[-1, :, z-1]
                self.generate(start_condition='custom', custom_state=custom_start)
                self.volume[:, :, z] = self.grid

        return self.volume

    def visualize_3d_voxels(self,
                           opacity: float = 0.3,
                           colorscale: str = 'Viridis',
                           show_edges: bool = True,
                           title: Optional[str] = None) -> go.Figure:
        """
        Create interactive 3D voxel visualization.

        Args:
            opacity: Transparency of voxels (0-1)
            colorscale: Plotly colorscale name
            show_edges: Whether to show voxel edges
            title: Custom title for the plot

        Returns:
            Plotly Figure object
        """
        if self.volume is None:
            raise ValueError("Must call generate_volume() before visualizing")

        # Get coordinates of active cells
        z, y, x = np.where(self.volume == 1)

        if title is None:
            title = f'3D Wolfram Automaton - Rule {self.rule}'

        fig = go.Figure(data=[go.Scatter3d(
            x=x, y=y, z=z,
            mode='markers',
            marker=dict(
                size=4,
                color=z,
                colorscale=colorscale,
                opacity=opacity,
                colorbar=dict(title="Layer (Z)")
            ),
            text=[f'X: {xi}<br>Y: {yi}<br>Z: {zi}' for xi, yi, zi in zip(x, y, z)],
            hoverinfo='text'
        )])

        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title='Cell Position',
                yaxis_title='Generation',
                zaxis_title='Layer/Depth',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            width=1000,
            height=800
        )

        return fig

    def visualize_3d_surface(self,
                            layer: Optional[int] = None,
                            colorscale: str = 'Black',
                            title: Optional[str] = None) -> go.Figure:
        """
        Create 3D surface plot of a layer or integrated volume.

        Args:
            layer: Specific layer to visualize (None for mean across all layers)
            colorscale: Plotly colorscale name
            title: Custom title

        Returns:
            Plotly Figure object
        """
        if self.volume is None:
            raise ValueError("Must call generate_volume() before visualizing")

        if layer is not None:
            data = self.volume[:, :, layer]
            if title is None:
                title = f'3D Surface - Rule {self.rule} - Layer {layer}'
        else:
            data = np.mean(self.volume, axis=2)
            if title is None:
                title = f'3D Surface - Rule {self.rule} - Mean Across All Layers'

        fig = go.Figure(data=[go.Surface(
            z=data,
            colorscale=colorscale,
            showscale=True
        )])

        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title='Cell Position',
                yaxis_title='Generation',
                zaxis_title='State',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            width=1000,
            height=800
        )

        return fig

    def visualize_slices(self,
                        layers: Optional[List[int]] = None,
                        rows: int = 2,
                        cols: int = 3,
                        colorscale: str = 'Gray') -> go.Figure:
        """
        Visualize multiple 2D slices of the 3D volume.

        Args:
            layers: List of layer indices to show (None for evenly spaced)
            rows: Number of rows in subplot grid
            cols: Number of columns in subplot grid
            colorscale: Plotly colorscale name

        Returns:
            Plotly Figure object
        """
        if self.volume is None:
            raise ValueError("Must call generate_volume() before visualizing")

        n_plots = rows * cols

        if layers is None:
            # Evenly spaced layers
            depth = self.volume.shape[2]
            layers = np.linspace(0, depth-1, n_plots, dtype=int)
        else:
            layers = layers[:n_plots]

        fig = make_subplots(
            rows=rows, cols=cols,
            subplot_titles=[f'Layer {layer}' for layer in layers],
            vertical_spacing=0.1,
            horizontal_spacing=0.05
        )

        for idx, layer in enumerate(layers):
            row = idx // cols + 1
            col = idx % cols + 1

            fig.add_trace(
                go.Heatmap(
                    z=self.volume[:, :, layer],
                    colorscale=colorscale,
                    showscale=False
                ),
                row=row, col=col
            )

        fig.update_layout(
            title_text=f'Layer Slices - Rule {self.rule}',
            width=1200,
            height=600
        )

        # Update axes
        for i in range(1, n_plots + 1):
            fig.update_xaxes(title_text='Cell', row=(i-1)//cols + 1, col=(i-1)%cols + 1)
            fig.update_yaxes(title_text='Gen', row=(i-1)//cols + 1, col=(i-1)%cols + 1)

        return fig

    def visualize_layer_animation(self,
                                  colorscale: str = 'Gray',
                                  frame_duration: int = 100) -> go.Figure:
        """
        Create an animated visualization cycling through layers.

        Args:
            colorscale: Plotly colorscale name
            frame_duration: Duration of each frame in milliseconds

        Returns:
            Plotly Figure object with animation
        """
        if self.volume is None:
            raise ValueError("Must call generate_volume() before visualizing")

        depth = self.volume.shape[2]

        # Create frames
        frames = []
        for z in range(depth):
            frames.append(go.Frame(
                data=[go.Heatmap(
                    z=self.volume[:, :, z],
                    colorscale=colorscale,
                    showscale=True
                )],
                name=str(z),
                layout=go.Layout(title_text=f'Rule {self.rule} - Layer {z}/{depth-1}')
            ))

        # Initial frame
        fig = go.Figure(
            data=[go.Heatmap(
                z=self.volume[:, :, 0],
                colorscale=colorscale,
                showscale=True
            )],
            frames=frames
        )

        # Add animation controls
        fig.update_layout(
            title=f'Rule {self.rule} - Layer 0/{depth-1}',
            xaxis_title='Cell Position',
            yaxis_title='Generation',
            width=1000,
            height=800,
            updatemenus=[{
                'type': 'buttons',
                'showactive': True,
                'buttons': [
                    {
                        'label': 'Play',
                        'method': 'animate',
                        'args': [None, {
                            'frame': {'duration': frame_duration, 'redraw': True},
                            'fromcurrent': True,
                            'mode': 'immediate',
                            'transition': {'duration': 0}
                        }]
                    },
                    {
                        'label': 'Pause',
                        'method': 'animate',
                        'args': [[None], {
                            'frame': {'duration': 0, 'redraw': False},
                            'mode': 'immediate',
                            'transition': {'duration': 0}
                        }]
                    }
                ],
                'x': 0.1,
                'y': 0,
                'xanchor': 'right',
                'yanchor': 'top'
            }],
            sliders=[{
                'active': 0,
                'steps': [
                    {
                        'args': [[f.name], {
                            'frame': {'duration': 0, 'redraw': True},
                            'mode': 'immediate',
                            'transition': {'duration': 0}
                        }],
                        'label': str(k),
                        'method': 'animate'
                    }
                    for k, f in enumerate(frames)
                ],
                'x': 0.1,
                'len': 0.9,
                'xanchor': 'left',
                'y': 0,
                'yanchor': 'top'
            }]
        )

        return fig

    def visualize_3d_volume(self,
                           threshold: float = 0.5,
                           opacity: float = 0.1,
                           surface_count: int = 10,
                           colorscale: str = 'Viridis') -> go.Figure:
        """
        Create volumetric 3D visualization with isosurfaces.

        Args:
            threshold: Value threshold for isosurface
            opacity: Transparency of surfaces
            surface_count: Number of isosurfaces to render
            colorscale: Plotly colorscale name

        Returns:
            Plotly Figure object
        """
        if self.volume is None:
            raise ValueError("Must call generate_volume() before visualizing")

        # Create meshgrid
        generations, width, depth = self.volume.shape
        Y, X, Z = np.mgrid[0:generations, 0:width, 0:depth]

        fig = go.Figure(data=go.Volume(
            x=X.flatten(),
            y=Y.flatten(),
            z=Z.flatten(),
            value=self.volume.flatten(),
            isomin=threshold,
            isomax=1,
            opacity=opacity,
            surface_count=surface_count,
            colorscale=colorscale,
            caps=dict(x_show=False, y_show=False, z_show=False)
        ))

        fig.update_layout(
            title=f'Volumetric View - Rule {self.rule}',
            scene=dict(
                xaxis_title='Cell Position',
                yaxis_title='Generation',
                zaxis_title='Layer/Depth',
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.5)
                )
            ),
            width=1000,
            height=800
        )

        return fig


def main():
    """Main function for 3D visualization CLI."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate 3D Wolfram Elementary Cellular Automata',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate 3D voxel visualization
  python wolfram_3d.py -r 30 --mode voxels

  # View layer slices
  python wolfram_3d.py -r 110 --mode slices

  # Animated layer view
  python wolfram_3d.py -r 90 --mode animation

  # Surface plot of specific layer
  python wolfram_3d.py -r 30 --mode surface --layer 25

  # Multi-rule visualization
  python wolfram_3d.py -r 90 --volume-mode multi_rule --mode voxels
        """
    )

    parser.add_argument('-r', '--rule', type=int, required=True,
                        help='Rule number (0-255)')
    parser.add_argument('-w', '--width', type=int, default=101,
                        help='Width of the automaton (default: 101)')
    parser.add_argument('-g', '--generations', type=int, default=100,
                        help='Number of generations (default: 100)')
    parser.add_argument('-d', '--depth', type=int, default=50,
                        help='Depth of 3D volume (default: 50)')
    parser.add_argument('--mode', choices=['voxels', 'surface', 'slices', 'animation', 'volume'],
                        default='voxels',
                        help='Visualization mode (default: voxels)')
    parser.add_argument('--volume-mode', choices=['multi_run', 'multi_rule', 'evolution'],
                        default='multi_run',
                        help='How to generate 3D volume (default: multi_run)')
    parser.add_argument('-s', '--start', choices=['single', 'random'],
                        default='single',
                        help='Starting condition (default: single)')
    parser.add_argument('--layer', type=int,
                        help='Specific layer for surface mode')
    parser.add_argument('--opacity', type=float, default=0.3,
                        help='Opacity for 3D visualization (default: 0.3)')
    parser.add_argument('--colorscale', type=str, default='Viridis',
                        help='Plotly colorscale name (default: Viridis)')
    parser.add_argument('-o', '--output', type=str,
                        help='Save to HTML file')

    args = parser.parse_args()

    # Create 3D automaton
    ca3d = WolframAutomaton3D(args.rule, args.width, args.generations)

    print(f"Generating 3D volume with rule {args.rule}...")
    ca3d.generate_volume(
        depth=args.depth,
        mode=args.volume_mode,
        start_condition=args.start
    )

    print(f"Creating {args.mode} visualization...")

    # Generate appropriate visualization
    if args.mode == 'voxels':
        fig = ca3d.visualize_3d_voxels(
            opacity=args.opacity,
            colorscale=args.colorscale
        )
    elif args.mode == 'surface':
        fig = ca3d.visualize_3d_surface(
            layer=args.layer,
            colorscale=args.colorscale
        )
    elif args.mode == 'slices':
        fig = ca3d.visualize_slices(
            colorscale=args.colorscale
        )
    elif args.mode == 'animation':
        fig = ca3d.visualize_layer_animation(
            colorscale=args.colorscale
        )
    elif args.mode == 'volume':
        fig = ca3d.visualize_3d_volume(
            opacity=args.opacity,
            colorscale=args.colorscale
        )

    if args.output:
        print(f"Saving to {args.output}...")
        fig.write_html(args.output)
        print("Done!")
    else:
        print("Opening interactive visualization...")
        fig.show()


if __name__ == '__main__':
    main()
