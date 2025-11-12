# Multi-Agent Fruit Harvesting Simulation

MSc AI Dissertation Project - Communication Range Effects on Cooperative Harvesting

## Project Overview

This project investigates how communication range affects cooperation in multi-agent fruit harvesting using Mesa framework.

**Research Question**: Does communication range affect harvest yield in multi-agent systems?

## Current Status

Week 2 of development - basic implementation working, experiments not yet run.

See `TODO.md` for remaining tasks and `PROGRESS.md` for detailed progress tracking.

## Quick Start

### Install Dependencies

```bash
pip install mesa==3.3.0 pandas numpy matplotlib solara
```

### Run Basic Test

```bash
python scripts/run_sandbox.py
```

### Run Visualization

```bash
python scripts/run_visualization.py
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

