# Setup Instructions

## Important: Python Environment

This project requires **Mesa 3.0+** which is installed in Anaconda Python, not the system Python.

### Use Anaconda Python

```bash
# Check Mesa version
/opt/anaconda3/bin/python -c "import mesa; print(mesa.__version__)"
# Should output: 3.3.0

# Run scripts with Anaconda Python
/opt/anaconda3/bin/python scripts/run_sandbox.py
/opt/anaconda3/bin/python scripts/run_smoke_test.py
/opt/anaconda3/bin/python scripts/run_visualization.py
```

### Quick Test

```bash
# Run quick validation test (takes ~10 seconds)
/opt/anaconda3/bin/python test_quick.py
```

Expected output:
```
============================================================
QUICK IMPLEMENTATION TEST
============================================================

Test 1: Static model (no communication)
✓ Completed 20 steps
  Final yield: 6
  Messages sent: 0

Test 2: Static model (with communication)
✓ Completed 20 steps
  Final yield: 14
  Messages sent: 0

Test 3: Replenishing model
✓ Completed 20 steps
  Final yield: 15
  Messages sent: 0
  Remaining fruit: 8

Test 4: Metrics collection
✓ DataCollector has 11 rows
  Columns: ['total_yield', 'messages_this_step', ...]
  Final metrics:
    - Total yield: 10
    - Messages this step: 2
    - Largest component ratio: 1.00
    - Gini yield: 0.320

============================================================
ALL TESTS PASSED ✓
============================================================
```

## Running the Full Implementation

### 1. Sandbox Model (Week 1-2)

```bash
/opt/anaconda3/bin/python scripts/run_sandbox.py
```

This will:
- Run 3 test configurations (100 steps each)
- Generate 3 PNG plots: `sandbox_static_nocomm_results.png`, `sandbox_static_comm_results.png`, `sandbox_replenishing_results.png`
- Print summary statistics

**Runtime**: ~2-3 minutes

### 2. Smoke Test (Week 3-4)

```bash
/opt/anaconda3/bin/python scripts/run_smoke_test.py
```

This will:
- Run 24 configurations (2 agents × 3 ranges × 2 dynamics × 2 seeds)
- Save results to `smoke_test_results_TIMESTAMP.csv`
- Generate `smoke_test_plots_TIMESTAMP.png` with 4-panel visualization
- Print summary statistics

**Runtime**: ~5-10 minutes

### 3. Interactive Visualization

```bash
/opt/anaconda3/bin/python scripts/run_visualization.py
```

Then open browser to: **http://localhost:8765**

Features:
- Adjust parameters with sliders
- Watch agents move and harvest in real-time
- See live plots of yield, messages, remaining fruit

## Compiling the Dissertation

```bash
cd dissertation
./compile.sh
```

This generates `main.pdf` with all chapters.

**Requirements**: LaTeX installation (pdflatex, bibtex)

## Project Status

### ✅ Completed (Weeks 1-4)

- [x] Literature review synthesis (13 papers analyzed)
- [x] Sandbox model with Mesa 3.0 conventions
- [x] HarvesterAgent with movement, harvesting, communication
- [x] Fruit resource (Static/Replenishing dynamics)
- [x] Solara visualization with interactive controls
- [x] Comprehensive metrics collection (10 metrics)
- [x] Smoke test factorial runner
- [x] Complete dissertation LaTeX structure
- [x] All chapters written (Abstract, Intro, Lit Review, Methodology)
- [x] Results/Discussion/Conclusion templates
- [x] Bibliography with 30+ citations

### 📋 Next Steps (Weeks 5-6)

- [ ] Create full factorial experiment runner
- [ ] Implement parallel execution
- [ ] Run pilot study (5 seeds)
- [ ] Create statistical analysis scripts
- [ ] Generate publication-quality plots

## Git Commit History

```
2024-10-22 10:30 - Documentation: Implementation guide and completion report
2024-10-15 16:45 - Dissertation LaTeX structure and initial chapters
2024-10-05 14:20 - Weeks 3-4: Full model with comprehensive metrics
2024-09-15 10:30 - Week 1-2: Initial project setup and sandbox model
```

## Troubleshooting

### "Import mesa" fails
Make sure you're using Anaconda Python:
```bash
/opt/anaconda3/bin/python
```

### Matplotlib display issues
Scripts use non-interactive backend ('Agg') and save plots to files instead of displaying them.

### Scripts seem to hang
They may be running - check for output PNG files:
```bash
ls -lh *.png
```

## Contact

Ahmed Maruf  
Email: maruf.devops@gmail.com  
GitHub: https://github.com/marufdevops/multiagent-cooperation-research

