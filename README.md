# Multi-Agent Fruit Harvesting Simulation

MSc AI Dissertation Project - Communication Range Effects on Cooperative Harvesting

## Project Overview

This project investigates how communication range affects cooperation in multi-agent fruit harvesting using Mesa framework.

**Research Question**: Does communication range affect harvest yield in multi-agent systems?

## Current Status

Week 2 of development - basic implementation working, experiments not yet run.

See `TODO.md` for remaining tasks and `PROGRESS.md` for detailed progress tracking.

## Quick Start

### Requirements

- Python 3.11+ (required for Mesa 3.3.0)
- If using system python3, make sure it's version 3.11 or higher

### Install Dependencies

```bash
pip install mesa==3.3.0 pandas numpy matplotlib solara
```

**Note**: If you have Anaconda installed, use:
```bash
/opt/anaconda3/bin/python -m pip install mesa==3.3.0 pandas numpy matplotlib solara
```

### Run Basic Test

```bash
# If using Anaconda Python:
/opt/anaconda3/bin/python scripts/run_sandbox.py

# Or if your system python3 is 3.11+:
python3 scripts/run_sandbox.py
```

### Run Visualization

```bash
/opt/anaconda3/bin/python scripts/run_visualization.py
```

Then open browser to http://localhost:8765

## Project Structure

```
├── src/
│   ├── models/          # Mesa model implementation
│   ├── agents/          # Agent classes
│   └── visualization/   # Solara visualization
├── scripts/             # Test and experiment scripts
├── dissertation/        # LaTeX dissertation
└── docs/               # Documentation
```

## Notes

- Currently implements Static dynamics only (no fruit regeneration)
- Communication uses Chebyshev distance
- Grid is 50x50 with non-toroidal boundaries
- Experiments designed but not yet run

## Contact

Ahmed Maruf - maruf.devops@gmail.com

