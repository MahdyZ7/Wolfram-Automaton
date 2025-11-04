# Wolfram Automaton Generator

A simple Python application to generate and visualize elementary cellular automata (Wolfram automaton) with different rules, line widths, and starting conditions.

## What are Elementary Cellular Automata?

Elementary cellular automata are the simplest class of one-dimensional cellular automata. Each cell can be in one of two states (0 or 1), and the next state of a cell is determined by its current state and the states of its two neighbors according to a rule.

There are 256 possible rules (numbered 0-255), each producing unique patterns. Some famous rules include:
- **Rule 30**: Chaotic, used in Mathematica's random number generator
- **Rule 110**: Turing complete, capable of universal computation
- **Rule 90**: Generates Sierpinski triangle pattern

## Features

- Generate automaton for any rule (0-255)
- Customizable line width (number of cells)
- Multiple starting conditions:
  - **Single**: Single active cell in the center
  - **Random**: Random initial state
  - **Custom**: Provide your own initial state
- High-quality visualizations using matplotlib
- Batch generation for all 256 rules
- Save outputs as PNG images

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Wolfram-Automaton
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Generate a specific rule (e.g., Rule 30):
```bash
python wolfram_automaton.py -r 30
```

### Customize Width and Generations

```bash
python wolfram_automaton.py -r 110 -w 201 -g 150
```

### Different Starting Conditions

Random starting condition:
```bash
python wolfram_automaton.py -r 90 -s random
```

### Save to File

```bash
python wolfram_automaton.py -r 30 -o rule_30.png
```

### Generate All Rules

Generate all 256 rules and save them to a directory:
```bash
python wolfram_automaton.py --all -w 101 -g 50 -o output
```

### Command Line Options

```
  -r, --rule RULE           Rule number (0-255)
  -w, --width WIDTH         Width of the automaton (number of cells, default: 101)
  -g, --generations GEN     Number of generations (default: 100)
  -s, --start {single,random}  Starting condition (default: single)
  -o, --output PATH         Save figure to file
  --all                     Generate all 256 rules
  --no-show                 Do not display the figure
```

## Using as a Library

You can also use the `WolframAutomaton` class in your own Python code:

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

## Examples

### Famous Rules to Try

```bash
# Rule 30 - Chaotic pattern
python wolfram_automaton.py -r 30

# Rule 110 - Turing complete
python wolfram_automaton.py -r 110

# Rule 90 - Sierpinski triangle
python wolfram_automaton.py -r 90

# Rule 184 - Traffic flow model
python wolfram_automaton.py -r 184

# Rule 54 - Complex but regular pattern
python wolfram_automaton.py -r 54
```

### Wider Patterns

For more detailed visualization:
```bash
python wolfram_automaton.py -r 30 -w 301 -g 200
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

## License

MIT License - Feel free to use and modify as needed.

## References

- [Wolfram MathWorld - Elementary Cellular Automaton](https://mathworld.wolfram.com/ElementaryCellularAutomaton.html)
- [A New Kind of Science by Stephen Wolfram](https://www.wolframscience.com/)
