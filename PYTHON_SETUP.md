# Python Setup Notes

## Issue

The system `python3` is version 3.9.6, which is too old for Mesa 3.3.0 (requires Python 3.11+).

## Solution

Use Anaconda Python which has Python 3.12 and Mesa 3.3.0 already installed:

```bash
/opt/anaconda3/bin/python scripts/run_sandbox.py
```

## Quick Reference

**Check Python versions:**
```bash
# System python (3.9.6 - too old)
python3 --version

# Anaconda python (3.12 - works!)
/opt/anaconda3/bin/python --version
```

**Check Mesa versions:**
```bash
# System python has Mesa 2.4.0
python3 -c "import mesa; print(mesa.__version__)"

# Anaconda python has Mesa 3.3.0
/opt/anaconda3/bin/python -c "import mesa; print(mesa.__version__)"
```

## Running Scripts

Always use the Anaconda Python:

```bash
# Run sandbox test
/opt/anaconda3/bin/python scripts/run_sandbox.py

# Run visualization
/opt/anaconda3/bin/python scripts/run_visualization.py

# Run experiments (when ready)
/opt/anaconda3/bin/python scripts/run_experiments.py
```

## Why This Matters

Mesa 3.3.0 changed the Agent API:
- **Mesa 2.4.0**: `Agent(unique_id, model)` 
- **Mesa 3.3.0**: `Agent(model)` - unique_id auto-generated

Our code is written for Mesa 3.3.0, so we must use Python 3.11+ with Mesa 3.3.0.

