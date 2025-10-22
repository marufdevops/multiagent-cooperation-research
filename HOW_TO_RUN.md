# 🚀 How to Run the Project

Complete guide to running your Multi-Agent Fruit Harvesting research implementation.

---

## ⚡ Quick Start (30 seconds)

### 1. Run Quick Test
```bash
/opt/anaconda3/bin/python test_quick.py
```

**Expected Output:**
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
  ...

============================================================
ALL TESTS PASSED ✓
============================================================
```

---

## 📊 Run Experiments

### Option 1: Sandbox Model (2-3 minutes)

Runs 3 test configurations and generates plots:

```bash
/opt/anaconda3/bin/python scripts/run_sandbox.py
```

**What it does:**
- Test 1: Static dynamics, no communication (comm_range=0)
- Test 2: Static dynamics, with communication (comm_range=3)
- Test 3: Replenishing dynamics, with communication (comm_range=3, regen_prob=0.05)
- Each test runs for 100 steps on a 20×20 grid with 5 agents

**Output Files:**
- `sandbox_static_nocomm_results.png` - 2-panel plot (yield, messages)
- `sandbox_static_comm_results.png` - 2-panel plot (yield, messages)
- `sandbox_replenishing_results.png` - 2-panel plot (yield, messages)

**Expected Console Output:**
```
============================================================
SANDBOX MODEL - WEEK 1-2 DELIVERABLE
============================================================

Test 1: Static, no communication
------------------------------------------------------------
Running sandbox model:
  Grid: 20x20
  Agents: 5
  Fruit density: 0.2
  Comm range: 0
  Dynamics: Static
  Regen prob: 0.0
  Steps: 100
  Seed: 42

Final yield: 30
Total messages: 0
Remaining fruit: 50

Saved plot: sandbox_static_nocomm_results.png
...
```

---

### Option 2: Smoke Test (5-10 minutes)

Runs a small factorial experiment (24 configurations):

```bash
/opt/anaconda3/bin/python scripts/run_smoke_test.py
```

**What it does:**
- 2 agent counts (10, 20)
- 3 communication ranges (0, 2, 4)
- 2 dynamics (Static, Replenishing)
- 2 seeds (42, 43)
- Total: 2 × 3 × 2 × 2 = 24 runs
- Each run: 200 steps on 30×30 grid

**Output Files:**
- `smoke_test_results_YYYYMMDD_HHMMSS.csv` - All metrics for all runs
- `smoke_test_plots_YYYYMMDD_HHMMSS.png` - 4-panel visualization

**CSV Columns:**
- `run_id`, `seed`, `dynamics`, `regen_prob`
- `grid_w`, `grid_h`, `fruit_density`, `num_agents`, `comm_range`
- `steps_run`, `final_yield`, `steady_state_yield`, `time_to_depletion`
- `mean_messages_per_step`, `yield_per_message`, `peak_component_ratio`

**Plots Generated:**
1. **Yield vs Communication Range** - Line plot by dynamics
2. **Efficiency vs Communication Range** - Yield per message
3. **Network Connectivity** - Peak component ratio
4. **Heatmap** - Final yield by agents × comm_range (Static only)

**Expected Console Output:**
```
======================================================================
SMOKE TEST - WEEKS 3-4 DELIVERABLE
======================================================================

Total configurations: 24
Parameters:
  Agents: [10, 20]
  Comm ranges: [0, 2, 4]
  Dynamics: ['Static', 'Replenishing']
  Seeds: [42, 43]

Running experiments: 100%|████████████████████| 24/24 [02:15<00:00,  5.65s/it]

Results saved to: smoke_test_results_20241022_225630.csv

======================================================================
SUMMARY STATISTICS
======================================================================

Final Yield by Configuration:
dynamics       comm_range  num_agents
Replenishing   0           10            245.5
                           20            489.0
               2           10            312.0
...
```

---

### Option 3: Interactive Visualization (Real-time)

Launch the web-based interactive visualization:

```bash
/opt/anaconda3/bin/python scripts/run_visualization.py
```

Then open your browser to: **http://localhost:8765**

**Features:**
- ✅ Live grid visualization with agents (blue circles) and fruit (green squares)
- ✅ Interactive parameter sliders:
  - Grid width/height (10-50)
  - Number of agents (1-30)
  - Fruit density (0.05-0.50)
  - Communication range (0-8)
  - Dynamics (Static/Replenishing)
  - Regeneration probability (0.00-0.20)
- ✅ Real-time data collection and metrics
- ✅ Play/pause/step controls
- ✅ Reset button to restart simulation

**Expected Console Output:**
```
============================================================
Starting Solara Visualization Server
============================================================
Open your browser to: http://localhost:8765
Press Ctrl+C to stop the server
============================================================

Solara server is starting at http://localhost:8765
```

**Note:** You may see a warning about Solara hooks - this is from Mesa's internal code and can be safely ignored.

**To Stop:**
Press `Ctrl+C` in the terminal

---

## 📄 Compile Dissertation

Generate the dissertation PDF from LaTeX:

```bash
cd dissertation
./compile.sh
```

**What it does:**
1. Runs `pdflatex main.tex`
2. Runs `bibtex main`
3. Runs `pdflatex main.tex` (twice more for references)
4. Cleans up auxiliary files (.aux, .log, .bbl, .blg, .toc, .lof, .lot)

**Output:** `dissertation/main.pdf`

**Requirements:**
- LaTeX distribution installed (e.g., MacTeX, TeX Live)
- `pdflatex` and `bibtex` in PATH

**Alternative (if compile.sh doesn't work):**
```bash
cd dissertation
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

---

## 🔧 Important Notes

### ⚠️ Use Anaconda Python

All scripts **MUST** be run with Anaconda Python:

```bash
/opt/anaconda3/bin/python <script>
```

**Why?**
- System Python (`/usr/bin/python3`) has Mesa 2.4.0 (incompatible)
- Anaconda Python (`/opt/anaconda3/bin/python`) has Mesa 3.3.0 (required)

**If you get errors like:**
```
TypeError: __init__() missing 1 required positional argument: 'model'
```

**Solution:** Make sure you're using Anaconda Python!

---

### 📊 Non-Interactive Plotting

The sandbox and smoke test scripts use **non-interactive matplotlib backend** (`Agg`):

- ✅ Plots are **saved to PNG files** (not displayed)
- ✅ Scripts won't hang waiting for you to close plot windows
- ✅ Can run on servers without display/GUI

**To view plots:**
```bash
open sandbox_static_nocomm_results.png
# or
ls -lh *.png
```

---

## 📁 Output Files

### Quick Test
- **Output:** Console only (no files)
- **Runtime:** ~10 seconds

### Sandbox Model
- **Files:** 3 PNG plots
  - `sandbox_static_nocomm_results.png`
  - `sandbox_static_comm_results.png`
  - `sandbox_replenishing_results.png`
- **Runtime:** 2-3 minutes

### Smoke Test
- **Files:** 1 CSV + 1 PNG
  - `smoke_test_results_YYYYMMDD_HHMMSS.csv`
  - `smoke_test_plots_YYYYMMDD_HHMMSS.png`
- **Runtime:** 5-10 minutes

### Interactive Visualization
- **Files:** None (web interface)
- **Runtime:** Real-time (runs until stopped)

### Dissertation
- **Files:** `dissertation/main.pdf`
- **Runtime:** ~30 seconds

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'mesa'"

**Solution:** Use Anaconda Python
```bash
/opt/anaconda3/bin/python <script>
```

---

### Problem: "Scripts seem to hang"

**Possible Causes:**
1. Script is still running (check progress bar for smoke test)
2. Matplotlib trying to display plots (should be fixed with `Agg` backend)

**Solution:** Wait for completion, or check for output files:
```bash
ls -lh *.png *.csv
```

---

### Problem: "Can't find output files"

**Solution:** Check current directory
```bash
pwd
ls -lh *.png *.csv
```

Output files are saved in the directory where you run the script.

---

### Problem: "Permission denied: ./compile.sh"

**Solution:** Make script executable
```bash
chmod +x dissertation/compile.sh
./compile.sh
```

---

### Problem: "pdflatex: command not found"

**Solution:** Install LaTeX distribution
- **macOS:** Install MacTeX from https://www.tug.org/mactex/
- **Linux:** `sudo apt-get install texlive-full`
- **Windows:** Install MiKTeX from https://miktex.org/

---

## 📊 What Each Script Does

| Script | Purpose | Runtime | Output |
|--------|---------|---------|--------|
| `test_quick.py` | Validates all functionality | 10 sec | Console |
| `scripts/run_sandbox.py` | Week 1-2 deliverable | 2-3 min | 3 PNG plots |
| `scripts/run_smoke_test.py` | Week 3-4 deliverable | 5-10 min | CSV + PNG |
| `scripts/run_visualization.py` | Interactive web UI | Real-time | Browser :8765 |
| `dissertation/compile.sh` | Build dissertation PDF | 30 sec | main.pdf |

---

## 🎯 Recommended Workflow

### 1. First Time Setup
```bash
# Verify environment
/opt/anaconda3/bin/python -c "import mesa; print(f'Mesa {mesa.__version__}')"
# Should print: Mesa 3.3.0
```

### 2. Quick Validation
```bash
# Run quick test (10 seconds)
/opt/anaconda3/bin/python test_quick.py
```

### 3. Generate Sandbox Plots
```bash
# Run sandbox (2-3 minutes)
/opt/anaconda3/bin/python scripts/run_sandbox.py

# View plots
open sandbox_*.png
```

### 4. Run Smoke Test
```bash
# Run smoke test (5-10 minutes)
/opt/anaconda3/bin/python scripts/run_smoke_test.py

# View results
open smoke_test_plots_*.png
head -20 smoke_test_results_*.csv
```

### 5. Explore Interactively
```bash
# Launch visualization
/opt/anaconda3/bin/python scripts/run_visualization.py

# Open browser to http://localhost:8765
# Adjust parameters and observe behavior
# Press Ctrl+C to stop
```

### 6. Compile Dissertation
```bash
cd dissertation
./compile.sh
open main.pdf
```

---

## 📖 More Information

For detailed documentation, read:
- **START_HERE.md** - Complete quick start guide
- **IMPLEMENTATION_COMPLETE.md** - Full status report
- **SETUP_INSTRUCTIONS.md** - Environment setup details
- **IMPLEMENTATION_GUIDE.md** - Detailed usage instructions
- **README.md** - Research plan and specifications

---

## ✅ Success Checklist

- [ ] Quick test passes (all 4 tests)
- [ ] Sandbox generates 3 PNG plots
- [ ] Smoke test generates CSV + PNG
- [ ] Interactive visualization launches at :8765
- [ ] Dissertation compiles to PDF

---

**Last Updated:** October 22, 2024  
**Status:** ✅ All scripts working and tested

