# Multi-Agent Fruit Harvesting — Dissertation Research

Masters dissertation investigating communication effects on multi-agent fruit harvesting cooperation using Mesa 3.0 framework.

## Research Focus
Exploring how communication range affects collective yield in a grid-based multi-agent fruit harvesting environment with different resource dynamics (Static vs. Replenishing).

## Current Implementation (Weeks 1-2)

### Technical Specifications
- **Mesa 3.0 conventions**
  - Agent activation: `model.agents.shuffle_do('step')`
  - No `unique_id` in agent constructors
  - Chebyshev distance for communication range
  
- **Environment**
  - Grid: 20×20 (parameterizable)
  - Non-toroidal boundaries
  - Fruit density: 0.2 (20% of cells)
  
- **Agent Behaviors**
  - Movement: Random walk with target navigation
  - Harvesting: Collect fruit from current cell
  - Communication: Broadcast fruit locations within range
  
- **Metrics Collected**
  - `total_yield`: Cumulative fruit harvested
  - `messages_this_step`: Messages sent per step
  - `cumulative_messages`: Total messages sent
  - `remaining_fruit`: Available fruit count

## How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Sandbox Tests
```bash
/opt/anaconda3/bin/python scripts/run_sandbox.py
```
Generates 3 PNG plots showing yield and messages over time.

### 3. Run Interactive Visualization
```bash
/opt/anaconda3/bin/solara run src/visualization/solara_viz.py --port 8765
```
Open browser to http://localhost:8765

### 4. Run Quick Tests
```bash
/opt/anaconda3/bin/python test_quick.py
```

## Project Structure
```
├── src/
│   ├── agents/
│   │   ├── harvester_agent.py    # Agent with movement, harvesting, communication
│   │   └── fruit.py               # Fruit resource
│   ├── models/
│   │   └── harvest_model.py      # Main simulation model
│   └── visualization/
│       └── solara_viz.py          # Interactive visualization
├── scripts/
│   ├── run_sandbox.py             # Sandbox tests
│   └── run_visualization.py       # Visualization launcher
├── dissertation/
│   ├── main.tex                   # Main LaTeX document
│   ├── chapters/
│   │   ├── abstract.tex
│   │   ├── introduction.tex
│   │   └── literature_review.tex
│   └── references.bib
├── docs/
│   └── literature_review_synthesis.md
└── requirements.txt
```

## Current Status (Weeks 1-2 Complete)

✅ **Implemented:**
- Basic simulation model with Mesa 3.0
- Agent behaviors (movement, harvesting, communication)
- Static and Replenishing resource dynamics
- Interactive Solara visualization
- Basic metrics collection
- Sandbox tests with plots
- Literature review (2.5 pages)
- Dissertation structure (Chapters 1-2)

📝 **Next Steps:**
- Expand experimental design
- Implement additional metrics
- Run pilot studies
- Complete methodology chapter
- Conduct full experiments

## Dissertation Status

**Completed Chapters:**
- Abstract
- Chapter 1: Introduction
- Chapter 2: Literature Review

**To Be Written:**
- Chapter 3: Methodology
- Chapter 4: Results
- Chapter 5: Discussion
- Chapter 6: Conclusion

## Key Features

### Simulation
- Grid-based environment with fruit resources
- Autonomous harvester agents
- Communication within configurable range
- Two resource dynamics modes (Static/Replenishing)

### Visualization
- Real-time interactive visualization with Solara
- Adjustable parameters via sliders
- Grid view showing agents and fruit
- Step-by-step or continuous execution

### Data Collection
- Per-step metrics tracking
- Reproducible runs with fixed seeds
- CSV export capability
- Matplotlib plots for analysis

## Requirements

- Python 3.10+
- Mesa 3.3.0
- Solara 1.51.1
- Matplotlib
- NumPy
- Pandas

See `requirements.txt` for complete list.

## Author

Ahmed Maruf  
Masters Dissertation  
2025

