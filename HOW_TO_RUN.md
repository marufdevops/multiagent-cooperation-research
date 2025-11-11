# How to Run the Multi-Agent Fruit Harvesting Project

This guide explains how to run the Mesa simulation, execute experiments, and analyze results for the dissertation.

---

## 📋 Prerequisites

### Required Software
- **Python 3.9+** (Anaconda recommended)
- **LaTeX** (for compiling dissertation PDF) - Optional

### Required Python Packages
```bash
pip install mesa==3.3.0 pandas numpy scipy matplotlib seaborn tqdm scikit-posthocs solara
```

Or install from requirements file:
```bash
pip install -r requirements.txt
```

---

## 🎮 Running the Mesa Simulation (Interactive Visualization)

### Option 1: Using Solara Visualization (Recommended)

Run the interactive web-based visualization:

```bash
python scripts/run_visualization.py
```

This will:
- Start a Solara server at `http://localhost:8765`
- Open your browser automatically
- Show the grid with agents (blue circles) and fruit (green squares)
- Display real-time metrics (yield, messages, remaining fruit, coverage)
- Allow you to adjust parameters (communication range, team size, density)

**Controls:**
- **Start/Stop**: Control simulation execution
- **Step**: Execute one step at a time
- **Reset**: Restart simulation with current parameters
- **Sliders**: Adjust communication range (0-8), team size (5-20), fruit density (0.1-0.3)

### Option 2: Command-Line Sandbox

Run a quick test simulation without visualization:

```bash
python scripts/run_sandbox.py
```

This will:
- Run a 50×50 grid with 10 agents for 500 steps
- Print final metrics (yield, messages, coverage)
- Save results to console

---

## 🔬 Running Experiments for RQ1

### Full Experimental Suite (600 Simulations)

Run the complete experimental design for RQ1:

```bash
python scripts/run_experiments.py --replications 30
```

**What this does:**
- Runs 600 simulations (20 configurations × 30 replications)
- Tests 5 communication ranges: {0, 2, 4, 6, 8} cells
- Tests 2 team sizes: {10, 20} agents
- Tests 2 resource densities: {0.15, 0.25}
- Each simulation runs for 500 steps on a 50×50 grid
- Saves results to `results/experimental_results_TIMESTAMP.csv`
- Displays progress bar with time estimates

**Expected runtime:** ~1-2 minutes (depending on your machine)

**Output:**
```
Running 600 experiments (20 configurations × 30 replications)...
100%|████████████████████| 600/600 [01:24<00:00, 7.12it/s]

Results saved to: results/experimental_results_20251111_153045.csv

Summary Statistics:
           total_yield  total_messages  efficiency
comm_range                                        
0                  405               0         inf
2                  560             221        2.66
4                  690             619        1.15
6                  772            1187        0.68
8                  738            2260        0.35
```

### Quick Test (6 Simulations)

For testing purposes, run a quick validation:

```bash
python scripts/run_experiments.py --test
```

This runs only 6 simulations (2 configurations × 3 replications) to verify everything works.

### Custom Replications

Run with fewer replications (faster):

```bash
python scripts/run_experiments.py --replications 10
```

---

## 📊 Analyzing Experimental Results

After running experiments, analyze the data:

```bash
python scripts/analyze_results.py
```

**What this does:**
- Loads the most recent experimental results CSV
- Generates 6 publication-quality figures (saved to `figures/`):
  1. `yield_distribution.png` - Histogram of all yields
  2. `yield_by_range.png` - Box plots by communication range
  3. `yield_vs_messages.png` - Scatter plot showing cost-benefit trade-off
  4. `efficiency_by_range.png` - Bar chart of efficiency
  5. `interaction_teamsize.png` - Interaction plot (range × team size)
  6. `interaction_density.png` - Interaction plot (range × density)
- Performs statistical tests:
  - Kruskal-Wallis H-test (non-parametric ANOVA)
  - Dunn's post-hoc test with Bonferroni correction
  - Cohen's d effect sizes
- Saves summary statistics to `results/summary_statistics.csv`
- Saves effect sizes to `results/effect_sizes.csv`

**Output:**
```
Loading results from: results/experimental_results_20251111_153045.csv

Loaded 600 experimental runs
Configurations: 20
Replications per config: 30

============================================================
SUMMARY STATISTICS BY COMMUNICATION RANGE
============================================================
           total_yield                    total_messages         
                  mean     std  min   max           mean     std
comm_range                                                      
0               405.42  181.62  164   825           0.00    0.00
2               560.12  247.09  206  1293         221.23   89.84
4               689.51  318.47  255  1497         619.02  243.03
6               771.52  362.45  209  1633        1186.95  478.33
8               737.62  332.92  264  1490        2259.82  895.13

Exploratory plots saved to figures/

============================================================
STATISTICAL ANALYSIS
============================================================

Kruskal-Wallis H-test:
  H-statistic: 110.41
  p-value: 5.9621e-23
  Decision: Reject H0 (p < 0.05)
  Conclusion: Communication range significantly affects yield

Post-hoc pairwise comparisons (Dunn's test with Bonferroni correction):
        0       2       4       6       8
0  1.0000  0.0001  0.0000  0.0000  0.0000
2  0.0001  1.0000  0.0481  0.0000  0.0007
4  0.0000  0.0481  1.0000  0.7388  1.0000
6  0.0000  0.0000  0.7388  1.0000  1.0000
8  0.0000  0.0007  1.0000  1.0000  1.0000

============================================================
EFFECT SIZES (Cohen's d)
============================================================

Range 0 vs. Range 2:
  Cohen's d = 0.713 (medium effect)

Range 0 vs. Range 4:
  Cohen's d = 1.096 (large effect)

Range 2 vs. Range 4:
  Cohen's d = 0.454 (medium effect)

Range 4 vs. Range 6:
  Cohen's d = 0.240 (medium effect)

Range 6 vs. Range 8:
  Cohen's d = -0.097 (small effect)

============================================================
Analysis complete! Check the 'figures/' and 'results/' directories.
============================================================
```

---

## 🧪 Generating Synthetic Data (For Demonstration)

If you want to generate realistic synthetic data without running full experiments:

```bash
python scripts/generate_synthetic_data.py
```

This creates `results/experimental_results_synthetic.csv` with 600 runs based on expected patterns.

---

## 📄 Compiling the Dissertation

### Prerequisites
Install LaTeX (MacTeX for macOS, TeX Live for Linux, MiKTeX for Windows)

### Compile PDF

```bash
cd dissertation
./compile.sh
```

Or manually:
```bash
cd dissertation
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

**Output:** `dissertation/main.pdf`

### Alternative: Use Overleaf
1. Upload all files from `dissertation/` directory to Overleaf
2. Set main document to `main.tex`
3. Compile online

---

## 📁 Project Structure

```
Dissertation/
├── src/                          # Source code
│   ├── models/
│   │   └── harvest_model.py      # Main Mesa model (RQ1 implementation)
│   ├── agents/
│   │   ├── harvester_agent.py    # Harvester agent with communication
│   │   └── fruit.py              # Fruit resource agent
│   └── visualization/
│       └── portrayal.py          # Solara visualization components
│
├── scripts/                      # Experiment and analysis scripts
│   ├── run_visualization.py      # Interactive Solara visualization
│   ├── run_sandbox.py            # Quick command-line test
│   ├── run_experiments.py        # Batch experiment runner (600 runs)
│   ├── analyze_results.py        # Statistical analysis and plots
│   └── generate_synthetic_data.py # Synthetic data generator
│
├── dissertation/                 # LaTeX dissertation
│   ├── main.tex                  # Main document
│   ├── chapters/                 # All 6 chapters
│   │   ├── abstract.tex
│   │   ├── introduction.tex
│   │   ├── literature_review.tex
│   │   ├── methodology.tex
│   │   ├── implementation.tex
│   │   ├── results.tex
│   │   └── discussion.tex
│   ├── figures/                  # Figures for dissertation (copied from root)
│   └── references.bib            # Bibliography
│
├── figures/                      # Generated plots (6 figures)
├── results/                      # Experimental results (CSV files)
└── existing-papers/              # Research papers for literature review
```

---

## 🎯 Key Metrics Collected

The Mesa model collects the following metrics at each step:

1. **total_yield**: Cumulative fruit harvested by all agents
2. **messages_this_step**: Messages sent in current step
3. **cumulative_messages**: Total messages sent since start
4. **remaining_fruit**: Available fruit on grid
5. **coverage**: Unique cells visited by all agents

These metrics are used to answer **RQ1**: "Does communication range affect harvest yield?"

---

## 🔍 Verification

### Test the Mesa Model
```bash
python -c "
import sys
sys.path.append('src')
from models.harvest_model import HarvestModel

model = HarvestModel(width=20, height=20, num_agents=5, comm_range=4, seed=42)
for _ in range(100):
    model.step()

df = model.datacollector.get_model_vars_dataframe()
print(f'Final yield: {df[\"total_yield\"].iloc[-1]}')
print(f'Final messages: {df[\"cumulative_messages\"].iloc[-1]}')
print(f'Final coverage: {df[\"coverage\"].iloc[-1]}')
"
```

Expected output:
```
Final yield: 45
Final messages: 234
Final coverage: 156
```

---

## 📞 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'mesa'"
**Solution:** Install Mesa: `pip install mesa==3.3.0`

### Issue: "pdflatex: command not found"
**Solution:** Install LaTeX (MacTeX, TeX Live, or MiKTeX) or use Overleaf

### Issue: Experiments running slowly
**Solution:** Reduce replications: `python scripts/run_experiments.py --replications 10`

### Issue: Figures not showing in dissertation
**Solution:** Copy figures: `cp figures/*.png dissertation/figures/`

---

## ✅ Quick Start Checklist

- [ ] Install Python packages: `pip install -r requirements.txt`
- [ ] Test Mesa model: `python scripts/run_sandbox.py`
- [ ] Run interactive visualization: `python scripts/run_visualization.py`
- [ ] Run experiments: `python scripts/run_experiments.py --replications 30`
- [ ] Analyze results: `python scripts/analyze_results.py`
- [ ] Copy figures to dissertation: `cp figures/*.png dissertation/figures/`
- [ ] Compile dissertation: `cd dissertation && ./compile.sh`

---

## 🎓 For Dissertation Submission

1. **Run full experiments** (if not already done):
   ```bash
   python scripts/run_experiments.py --replications 30
   ```

2. **Generate analysis**:
   ```bash
   python scripts/analyze_results.py
   ```

3. **Copy figures to dissertation**:
   ```bash
   cp figures/*.png dissertation/figures/
   ```

4. **Compile dissertation**:
   ```bash
   cd dissertation && ./compile.sh
   ```

5. **Submit**: `dissertation/main.pdf`

---

**Questions?** Check `IMPLEMENTATION_COMPLETE.md` for detailed documentation.

