# How to Run the Multi-Agent Fruit Harvesting Project (WORK IN PROGRESS)

**Status**: Week 2 - Basic functionality working, experiments not yet run

TODO: Expand this guide after completing experiments
TODO: Add troubleshooting section
TODO: Add examples of expected output

---

## 📋 Prerequisites

### Required Software
- **Python 3.9+** (Anaconda recommended)
- **LaTeX** (for compiling dissertation PDF) - Optional

### Required Python Packages
```bash
pip install mesa==3.3.0 pandas numpy matplotlib solara
```

TODO: Create requirements.txt file

---

## 🎮 Running the Mesa Simulation

### Quick Test (Sandbox)

Run a quick test simulation:

```bash
python scripts/run_sandbox.py
```

This will run a simple simulation and print results to console.

### Interactive Visualization

Run the Solara visualization:

```bash
python scripts/run_visualization.py
```

This will open a web browser with an interactive visualization.

TODO: Add more details about controls and features
TODO: Add screenshots

---

## 🔬 Running Experiments (NOT YET READY)

TODO: Complete batch experiment runner script
TODO: Test with small sample first
TODO: Run full 600 simulations

Planned command:
```bash
python scripts/run_experiments.py
```

This will run 600 simulations (estimated 2-3 hours).

TODO: Verify this works before running full experiments

---

## 📊 Analyzing Results (NOT YET READY)

TODO: Write analysis script after experiments complete
TODO: Generate figures
TODO: Perform statistical tests

---

## 📝 Compiling Dissertation

To compile the LaTeX dissertation:

```bash
cd dissertation
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

TODO: Add more details about LaTeX compilation

---

## ❓ Troubleshooting

TODO: Add common issues and solutions

---

## 📧 Contact

For questions or issues, contact: maruf.devops@gmail.com
