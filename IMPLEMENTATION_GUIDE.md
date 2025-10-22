# Implementation Guide - Multi-Agent Fruit Harvesting Research

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Sandbox Model (Week 1-2 Deliverable)

```bash
# Run sandbox with default parameters
python scripts/run_sandbox.py
```

This will:
- Run 3 test configurations (Static no-comm, Static with-comm, Replenishing)
- Generate plots: `sandbox_*.png`
- Print summary statistics

### Running the Smoke Test (Week 3-4 Deliverable)

```bash
# Run smoke test factorial
python scripts/run_smoke_test.py
```

This will:
- Execute 24 configurations (2 agents × 3 ranges × 2 dynamics × 2 seeds)
- Save results to `smoke_test_results_TIMESTAMP.csv`
- Generate plots: `smoke_test_plots_TIMESTAMP.png`
- Print summary statistics

Expected runtime: ~2-5 minutes

### Running the Visualization Server

```bash
# Launch Solara visualization
python scripts/run_visualization.py
```

Then open your browser to: **http://localhost:8765**

You can:
- Adjust parameters with sliders (grid size, agents, comm range, dynamics)
- Watch agents move and harvest in real-time
- See live plots of yield, messages, and remaining fruit

## Project Structure

```
Dissertation/
├── src/                          # Source code
│   ├── agents/
│   │   ├── harvester_agent.py   # Agent with movement, harvest, communication
│   │   └── fruit.py              # Fruit resource (Static/Replenishing)
│   ├── models/
│   │   └── harvest_model.py     # Main simulation model (Mesa 3.0)
│   └── visualization/
│       └── solara_viz.py        # Solara visualization components
├── scripts/                      # Executable scripts
│   ├── run_sandbox.py           # Week 1-2: Sandbox tests
│   ├── run_smoke_test.py        # Week 3-4: Smoke test factorial
│   └── run_visualization.py     # Launch Solara server
├── dissertation/                 # LaTeX dissertation
│   ├── main.tex                 # Main document
│   ├── chapters/                # Chapter files
│   ├── references.bib           # Bibliography
│   └── compile.sh               # Compile script
├── docs/                         # Documentation
│   └── literature_review_synthesis.md
├── requirements.txt              # Python dependencies
└── README.md                     # Research plan
```

## Implementation Status (Weeks 1-4 Complete)

### ✅ Week 1-2: Literature Review and Sandbox
- [x] Analyzed 13 papers in existing-papers/
- [x] Created literature review synthesis (docs/)
- [x] Implemented minimal sandbox model (20×20 grid, 5-10 agents)
- [x] Added HarvesterAgent with movement, harvesting, communication
- [x] Added Fruit resource with Static/Replenishing dynamics
- [x] Implemented Mesa 3.0 conventions (shuffle_do, no unique_id)
- [x] Created Solara visualization with make_space_component/make_plot_component
- [x] Generated sandbox plots (yield-over-time, messages/step)

### ✅ Week 3-4: Core Environment and Metrics
- [x] Enhanced model with comprehensive metrics collection
- [x] Implemented network connectivity analysis (largest_component_ratio)
- [x] Added Gini coefficient for fairness metrics
- [x] Implemented travel distance tracking
- [x] Created smoke test factorial runner
- [x] Validated all metrics columns:
  - total_yield, messages_this_step, cumulative_messages
  - largest_component_ratio, avg_hops, harvested_cells_this_step
  - remaining_fruit, mean_agent_load, gini_yield, avg_travel_distance
- [x] Generated smoke test visualizations

### ✅ Dissertation LaTeX Structure
- [x] Created complete LaTeX project (main.tex, chapters/, references.bib)
- [x] Wrote Abstract (research summary)
- [x] Wrote Introduction (background, RQs, objectives, significance)
- [x] Wrote Literature Review (foraging, communication, swarm robotics, agriculture)
- [x] Wrote Methodology (architecture, experimental design, metrics, statistics)
- [x] Created Results/Discussion/Conclusion templates
- [x] Added appendices for data and code
- [x] Added 30+ citations in references.bib
- [x] Created compile.sh script

## Next Steps (Weeks 5-6)

### Full Factorial Experiment Runner
- [ ] Create `scripts/run_full_experiment.py`
- [ ] Implement parallel execution across cores
- [ ] Add progress tracking and checkpointing
- [ ] Run pilot study (5 seeds per config)
- [ ] Estimate runtime for full experiment

### Analysis Pipeline
- [ ] Create `src/analysis/statistical_analysis.py`
- [ ] Implement ANOVA functions
- [ ] Implement mixed-effects models
- [ ] Implement post-hoc tests (Tukey HSD)
- [ ] Create visualization functions

### Data Management
- [ ] Create output directory structure
- [ ] Implement metadata logging (JSON)
- [ ] Add data validation checks
- [ ] Create data loading utilities

## Running Tests

```bash
# Run unit tests (when implemented)
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Compiling the Dissertation

```bash
cd dissertation
./compile.sh
```

This generates `main.pdf` with all chapters.

## Key Implementation Decisions

### Mesa 3.0 Conventions
- **Agent activation**: `model.agents.shuffle_do('step')` instead of custom schedulers
- **Agent constructors**: No `unique_id` parameter, only `model`
- **Distance metric**: Chebyshev (Moore neighborhood) for communication range
- **Portrayal**: Dictionaries with `color`, `size`, `marker` keys

### Metrics Collection
- **Per-step**: Collected every step via DataCollector
- **Per-run**: Computed from per-step data after run completes
- **Formulas**: Documented in dissertation/chapters/methodology.tex

### Experimental Design
- **Factorial**: Full factorial across all parameter combinations
- **Replication**: 30 seeds per configuration for statistical power
- **Pilot first**: 5 seeds to validate before full run
- **Total runs**: 12,150 (2,430 Static + 9,720 Replenishing)

## Troubleshooting

### Import Errors
```bash
# Make sure you're in the project root
cd /Users/marufs-air/Downloads/Dissertation

# Run with explicit path
PYTHONPATH=src python scripts/run_sandbox.py
```

### Visualization Not Loading
```bash
# Check Solara is installed
pip install solara>=1.30.0

# Try different port
python scripts/run_visualization.py --port 8080
```

### Memory Issues with Large Runs
- Reduce number of seeds
- Reduce grid size
- Log only every N steps instead of every step
- Use Parquet instead of CSV for storage

## Contact

Ahmed Maruf  
Email: maruf.devops@gmail.com  
GitHub: https://github.com/marufdevops/multiagent-cooperation-research

