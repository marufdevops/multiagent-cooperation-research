# Multi-Agent Fruit Harvesting Simulation

A Mesa-based agent-based model investigating how **communication range affects harvesting efficiency** in multi-agent foraging systems.

## About

This project implements a multi-agent simulation where harvester agents collect fruit from a grid environment. Agents use a **Belief-Desire-Intention (BDI)** architecture and can share fruit location information with nearby teammates within a configurable communication range (Chebyshev distance).

**Research Question:** *How does communication range influence harvesting efficiency in multi-agent foraging systems?*

**Key Finding:** Local communication (r=2) outperforms both no communication and long-range communication, with efficiency dropping 83% at r=8 due to coordination interference.

## Project Structure

```
├── src/                    # Source code
│   ├── agents/             # Agent implementations (HarvesterAgent, Fruit)
│   ├── models/             # Mesa model (HarvestModel)
│   └── visualization/      # Solara visualization
├── scripts/                # Experiment scripts
├── results/                # Experimental data (CSV)
└── dissertation/           # LaTeX dissertation
```

## Requirements

```bash
pip install mesa numpy pandas matplotlib solara
```

## Running the Code

### 1. Run Experiments

```bash
python scripts/run_experiments.py
```

Runs 400 simulations across 5 communication ranges (0, 2, 4, 6, 8), 2 team sizes (10, 20), and 2 densities (0.15, 0.25). Results saved to `results/`.

### 2. Analyze Results

```bash
python scripts/analyze_results.py results/experimental_results_YYYYMMDD_HHMMSS.csv
```

### 3. Generate Figures

```bash
python scripts/generate_figures.py results/experimental_results_YYYYMMDD_HHMMSS.csv
```

### 4. Interactive Visualization

```bash
python scripts/run_visualization.py
```

Opens browser at `http://localhost:8765` for real-time simulation visualization.

### 5. Compile Dissertation (requires LaTeX)

```bash
cd dissertation && ./compile.sh
```

## Quick Test

```bash
python quick_test.py
```

Runs a single simulation to verify the setup.

