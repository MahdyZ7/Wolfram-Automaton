# Wolfram Automaton Generator

A powerful Python application to generate and visualize elementary cellular automata (Wolfram automaton) with different rules, line widths, and starting conditions. Now with **interactive 3D visualization** featuring pan, zoom, and rotate controls!

## What are Elementary Cellular Automata?

Elementary cellular automata are the simplest class of one-dimensional cellular automata. Each cell can be in one of two states (0 or 1), and the next state of a cell is determined by its current state and the states of its two neighbors according to a rule.

There are 256 possible rules (numbered 0-255), each producing unique patterns. Some famous rules include:
- **Rule 30**: Chaotic, used in Mathematica's random number generator
- **Rule 110**: Turing complete, capable of universal computation
- **Rule 90**: Generates Sierpinski triangle pattern

## Features

### 2D Visualization
- Generate automaton for any rule (0-255)
- Customizable line width (number of cells)
- Multiple starting conditions:
  - **Single**: Single active cell in the center
  - **Random**: Random initial state
  - **Custom**: Provide your own initial state
- High-quality visualizations using matplotlib
- Batch generation for all 256 rules
- Save outputs as PNG images

### 3D Visualization (New!)
- **Interactive 3D voxel visualization** with full pan, zoom, and rotate controls
- **Layer-by-layer viewing** with animated transitions
- **Volumetric rendering** with isosurfaces
- **Multiple generation modes**:
  - Multi-run: Independent runs stacked in 3D
  - Multi-rule: Different rules across layers
  - Evolution: Continuous evolution through depth
- **Multiple visualization modes**:
  - 3D voxel scatter plots
  - 3D surface plots
  - Layer slice grids
  - Animated layer transitions
  - Volumetric isosurface rendering
- Export to interactive HTML files

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast Python package management and execution.

1. Install uv (if not already installed):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Clone this repository:
```bash
git clone <repository-url>
cd Wolfram-Automaton
```

3. Dependencies will be automatically installed when you run the scripts with `uv run`!

Alternatively, if you prefer traditional pip:
```bash
pip install -r requirements.txt
```

## Usage

### 2D Visualization

#### Basic Usage

Generate a specific rule (e.g., Rule 30):
```bash
uv run wolfram_automaton.py -r 30
```

### Customize Width and Generations

```bash
uv run wolfram_automaton.py -r 110 -w 201 -g 150
```

### Different Starting Conditions

Random starting condition:
```bash
uv run wolfram_automaton.py -r 90 -s random
```

### Save to File

```bash
uv run wolfram_automaton.py -r 30 -o rule_30.png
```

### Generate All Rules

Generate all 256 rules and save them to a directory:
```bash
uv run wolfram_automaton.py --all -w 101 -g 50 -o output
```

#### Command Line Options

```
  -r, --rule RULE           Rule number (0-255)
  -w, --width WIDTH         Width of the automaton (number of cells, default: 101)
  -g, --generations GEN     Number of generations (default: 100)
  -s, --start {single,random}  Starting condition (default: single)
  -o, --output PATH         Save figure to file
  --all                     Generate all 256 rules
  --no-show                 Do not display the figure
```

### 3D Visualization

The 3D visualization module provides interactive exploration of cellular automata with full pan, zoom, and rotate controls.

#### Quick Start - 3D

Generate an interactive 3D visualization:
```bash
uv run wolfram_3d.py -r 30 --mode voxels
```

This will open an interactive 3D plot in your browser where you can:
- **Rotate**: Left-click and drag
- **Pan**: Right-click and drag
- **Zoom**: Scroll wheel or pinch
- **Reset**: Double-click

#### 3D Visualization Modes

**Voxel Mode** - 3D scatter plot with interactive controls:
```bash
uv run wolfram_3d.py -r 30 --mode voxels -d 40
```

**Layer Slices** - View multiple 2D slices simultaneously:
```bash
uv run wolfram_3d.py -r 110 --mode slices
```

**Animated Layers** - Transition through layers with animation:
```bash
uv run wolfram_3d.py -r 90 --mode animation
```

**Surface Plot** - 3D surface visualization:
```bash
uv run wolfram_3d.py -r 30 --mode surface --layer 20
```

**Volumetric Rendering** - Advanced isosurface rendering:
```bash
uv run wolfram_3d.py -r 30 --mode volume --opacity 0.2
```

#### 3D Generation Modes

**Multi-Run Mode** - Stack multiple independent runs:
```bash
uv run wolfram_3d.py -r 30 --volume-mode multi_run -d 50
```

**Multi-Rule Mode** - Different rules across layers:
```bash
uv run wolfram_3d.py -r 90 --volume-mode multi_rule -d 30
```

**Evolution Mode** - Continuous evolution through depth:
```bash
uv run wolfram_3d.py -r 110 --volume-mode evolution -d 40
```

#### Save 3D Visualizations

Save to interactive HTML file:
```bash
uv run wolfram_3d.py -r 30 --mode voxels -o rule_30_3d.html
```

The HTML file can be opened in any web browser with full interactivity preserved!

#### 3D Command Line Options

```
  -r, --rule RULE               Rule number (0-255)
  -w, --width WIDTH             Width (number of cells, default: 101)
  -g, --generations GEN         Number of generations (default: 100)
  -d, --depth DEPTH             Depth of 3D volume (default: 50)
  --mode {voxels,surface,slices,animation,volume}
                                Visualization mode (default: voxels)
  --volume-mode {multi_run,multi_rule,evolution}
                                3D generation mode (default: multi_run)
  -s, --start {single,random}   Starting condition (default: single)
  --layer LAYER                 Specific layer for surface mode
  --opacity OPACITY             Opacity for 3D visualization (default: 0.3)
  --colorscale NAME             Plotly colorscale (default: Viridis)
  -o, --output PATH             Save to HTML file
```

## Using as a Library

### 2D Library Usage

You can use the `WolframAutomaton` class in your own Python code:

```python
from wolfram_automaton import WolframAutomaton
import numpy as np

# Create automaton with Rule 30
ca = WolframAutomaton(rule=30, width=101, generations=100)

# Generate with single cell start
ca.generate(start_condition='single')
ca.visualize()

# Generate with random start
ca.generate(start_condition='random')
ca.visualize()

# Generate with custom start
custom_start = np.zeros(101)
custom_start[40:60] = 1  # Active cells from position 40 to 59
ca.generate(start_condition='custom', custom_state=custom_start)
ca.visualize(save_path='custom_rule30.png')
```

### 3D Library Usage

Use the `WolframAutomaton3D` class for interactive 3D visualizations:

```python
from wolfram_3d import WolframAutomaton3D

# Create 3D automaton
ca3d = WolframAutomaton3D(rule=30, width=101, generations=80)

# Generate 3D volume with multiple runs
ca3d.generate_volume(depth=30, mode='multi_run', start_condition='single')

# Create interactive 3D voxel visualization
fig = ca3d.visualize_3d_voxels(opacity=0.4, colorscale='Plasma')
fig.show()  # Opens in browser with interactive controls

# View layer slices
fig = ca3d.visualize_slices(rows=2, cols=3)
fig.show()

# Create animated layer transition
fig = ca3d.visualize_layer_animation(frame_duration=100)
fig.show()

# Save to HTML file
fig = ca3d.visualize_3d_voxels(opacity=0.3)
fig.write_html('my_automaton_3d.html')
```

**Different 3D generation modes:**

```python
# Multi-rule mode: Different rules across layers
ca3d.generate_volume(depth=30, mode='multi_rule', rule_range=(20, 50))
fig = ca3d.visualize_3d_voxels()
fig.show()

# Evolution mode: Continuous evolution through depth
ca3d.generate_volume(depth=40, mode='evolution')
fig = ca3d.visualize_3d_voxels()
fig.show()
```

## Examples

### Example Scripts

Run the included example scripts to see what's possible:

**2D Examples:**
```bash
uv run examples.py
```

**3D Examples:**
```bash
uv run examples_3d.py
```

### Famous Rules to Try

**2D Visualizations:**
```bash
# Rule 30 - Chaotic pattern
uv run wolfram_automaton.py -r 30

# Rule 110 - Turing complete
uv run wolfram_automaton.py -r 110

# Rule 90 - Sierpinski triangle
uv run wolfram_automaton.py -r 90

# Rule 184 - Traffic flow model
uv run wolfram_automaton.py -r 184

# Rule 54 - Complex but regular pattern
uv run wolfram_automaton.py -r 54
```

**3D Visualizations:**
```bash
# Rule 30 in 3D with voxels
uv run wolfram_3d.py -r 30 --mode voxels

# Rule 110 with layer animation
uv run wolfram_3d.py -r 110 --mode animation

# Rule 90 with evolution mode
uv run wolfram_3d.py -r 90 --volume-mode evolution --mode voxels
```

### Wider Patterns

For more detailed visualization:
```bash
# 2D
uv run wolfram_automaton.py -r 30 -w 301 -g 200

# 3D
uv run wolfram_3d.py -r 30 -w 301 -g 150 -d 50 --mode voxels
```

## Output

The program generates black and white images where:
- **Black cells (1)**: Active/alive cells
- **White cells (0)**: Inactive/dead cells

Each row represents one generation in time, with time flowing downward.

## Requirements

- Python 3.6+
- NumPy
- Matplotlib
- Plotly (for 3D visualization)
- Kaleido (for static image export from Plotly)

## License

MIT License - Feel free to use and modify as needed.

## References

- [Wolfram MathWorld - Elementary Cellular Automaton](https://mathworld.wolfram.com/ElementaryCellularAutomaton.html)
- [A New Kind of Science by Stephen Wolfram](https://www.wolframscience.com/)
