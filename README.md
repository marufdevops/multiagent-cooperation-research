# Multi‑Agent Fruit Harvesting — Dissertation Research Plan

Masters dissertation investigating optimal communication ranges for maximizing collective yield in Mesa 3.0 multi‑agent fruit harvesting simulations. This README is a structured, actionable roadmap and reference for implementation and analysis.

## Research Questions
- RQ1: What communication range maximizes collective yield in a grid‑based multi‑agent fruit harvesting environment?
- RQ2 (refined): How do resource dynamics (Static one‑off harvest vs. Replenishing with regeneration probability) shift the optimal communication range and impact collective yield and efficiency? Specifically, to what extent does regeneration probability change the range that maximizes yield and yield‑per‑message?

## Technical Specifications (Implementation Decisions)
- Mesa 3.0 conventions
  - Step loop: call `model.agents.shuffle_do('step')` each tick; avoid custom schedulers unless justified.
  - Agent constructors: do not require `unique_id`; pass only `model` and parameters needed by behavior.
  - Distances: use Chebyshev (Moore neighborhood) for communication range on grid; movement can be Von Neumann or Moore (document chosen rule; default Moore).
- Environment and scalability
  - Grid: square, non‑toroidal by default; parameterizable size. Defaults: 50×50; allow 10×10 to 200×200. Obstacles: none (baseline); fruit occupies cells with capacity 1.
  - Scalability targets: support up to 200 agents and comm_range up to 8 on 200×200 without timeouts; O(N) per step behaviors; no quadratic message broadcasts (use neighborhood queries).
- Agents and portrayal (for Solara/Mesa visualization)
  - Portrayal dictionaries per agent: keys `color` (e.g., '#1f77b4'), `size` (float px), `marker` (e.g., 'circle', 'triangle'). No image sprites.
- Visualization (SolaraViz)
  - Use Solara components: `make_space_component(model)` for grid view; `make_plot_component(df)` for time‑series/summary plots.
- Data collection schema
  - Per‑step log (CSV/Parquet): `run_id, seed, dynamics, regen_prob, grid_w, grid_h, fruit_density, num_agents, comm_range, step, total_yield, messages_this_step, cumulative_messages, largest_component_ratio, avg_hops, harvested_cells_this_step, remaining_fruit, mean_agent_load, gini_yield, avg_travel_distance`.
  - Per‑run summary: `run_id, seed, dynamics, regen_prob, grid_w, grid_h, fruit_density, num_agents, comm_range, steps_run, final_yield, steady_state_yield, time_to_depletion, mean_messages_per_step, yield_per_message, peak_component_ratio`.
  - Reproducibility: fix RNG seeds; persist config with each run; write metadata JSON alongside outputs.

## Experimental Design (Consolidated)
- Independent variables and levels
  - Communication range (cells): {0,1,2,3,4,5,6,7,8}
  - Team size (agents): {10, 20, 30}
  - Resource dynamics: {Static, Replenishing}
  - Regeneration probability (per step, per empty fruit cell): {0.00, 0.01, 0.05, 0.10} — applicable only when dynamics=Replenishing (ignore for Static)
  - Initial fruit density (fraction of cells with fruit at t=0): {0.10, 0.20, 0.30}
- Design structure and expected runs (example with 30 seeds, 500 steps)
  - Static: 9 (range) × 3 (agents) × 3 (density) × 30 (seeds) = 2,430 runs
  - Replenishing: 9 × 3 × 3 × 4 (regen) × 30 = 9,720 runs
  - Total: 12,150 runs. Pilot first: 5 seeds to estimate effects; scale to full if runtime allows.
- Parameter applicability
  - `regen_prob` is only used for Replenishing. For Static, set no regeneration and compute `time_to_depletion` when remaining_fruit hits 0.
- Computational requirements and runtime estimates
  - Target machine: Apple M‑series laptop. Estimate 0.5–2.0 s per run at 500 steps and ≤30 agents; total 1.7–6.7 hours per 10k runs. Parallelize across cores; batch by condition; checkpoint outputs.

## Metrics and Analysis Plan
- Categories and definitions
  - Performance: `final_yield`, `steady_state_yield` (mean over last 25% steps), `time_to_depletion` (Static only).
  - Communication: `messages_this_step`, `mean_messages_per_step`, `cumulative_messages`, `avg_hops` (mean shortest‑path length for successful message deliveries), `largest_component_ratio` (|Vmax|/N via comm graph at current range).
  - Efficiency: `yield_per_message = final_yield / max(cumulative_messages, 1)`; `harvested_cells_per_step`.
  - Fairness: `gini_yield` over per‑agent harvested counts; also report per‑agent yield variance.
- Statistical pipeline
  - Primary outcome: `final_yield`; secondary: `yield_per_message`, `largest_component_ratio`, `steady_state_yield`.
  - Static condition: two/three‑way ANOVA `final_yield ~ comm_range * num_agents * fruit_density`. Replenishing adds `regen_prob` as a factor.
  - Mixed‑effects model (robustness): LMM with random intercept for `seed` (and/or map init): `final_yield ~ comm_range + num_agents + fruit_density + dynamics + regen_prob:dynamics + interactions + (1|seed)`.
  - Post‑hoc: Tukey HSD on significant factors. Significance α=0.05; report 95% CIs. Effect sizes: partial η² for ANOVA, Cohen’s d for pairwise.
  - Assumptions: check residual normality and homoscedasticity; if violated, transform or use Kruskal‑Wallis + Dunn’s post‑hoc with Holm correction.
- Visualization requirements
  - Line: yield vs. comm_range (facets by dynamics; lines by num_agents).
  - Heatmap: yield over (comm_range × num_agents) per density level.
  - Line: largest_component_ratio vs. comm_range.
  - Line: yield_per_message vs. comm_range.
  - Time‑series: yield‑over‑time (Static vs. Replenishing) with ribbons for 95% CI.

## Weekly Timeline (standardized blocks)
- Weeks 1–2
  - Objectives/Deliverables: literature review synthesis; sandbox model; Mesa 3.0 API mastery.
  - Technical requirements: implement minimal 20×20 grid, 5–10 agents; `model.agents.shuffle_do('step')`; DataCollector writing per‑step logs; Solara `make_space_component` and `make_plot_component` demo.
  - Success criteria: reproducible sandbox runs; two plots (yield‑over‑time, messages/step); 2–3 page lit summary.
  - Dependencies: none.
- Weeks 3–4
  - Objectives/Deliverables: core environment, agents, communication behaviors; parameterizable grid; portrayal dicts.
  - Technical requirements: comm_range (0–8), Chebyshev neighborhood; Static and Replenishing with `regen_prob`; portrayal keys `color/size/marker`.
  - Success criteria: small factorial smoke test completes (ranges × agents × dynamics with 2 seeds); metrics columns populated as specified.
  - Dependencies: Weeks 1–2.
- Weeks 5–6
  - Objectives/Deliverables: full data schema; batch execution tooling; pilot factorial (5 seeds).
  - Technical requirements: CLI/runner for parameter sweeps; per‑run summaries; caching and resume; parallel execution.
  - Success criteria: pilot results table and plots; preliminary ANOVA; runtime estimates for full sweep.
  - Dependencies: Weeks 3–4.
- Weeks 7–8
  - Objectives/Deliverables: full experiment execution; statistical analysis; result figures.
  - Technical requirements: run full (or pruned) factorial; store all outputs; scripts for ANOVA/LMM and plots.
  - Success criteria: statistically defensible optimal range(s) per condition; effect sizes + CIs; finalized plots.
  - Dependencies: Weeks 5–6.
- Weeks 9–10 (Optional extension; proceed only if Weeks 7–8 complete on time)
  - Objectives/Deliverables: minimal adaptive policy that toggles communication (e.g., heuristic threshold on local density); compare to best fixed range.
  - Technical requirements: small ablation; no deep RL training pipeline; re‑use metrics/plots.
  - Success criteria: extension results reported or explicitly skipped without affecting core deliverables.
  - Dependencies: Weeks 7–8.
- Weeks 11–12
  - Objectives/Deliverables: final analysis pass; dissertation write‑up; artifact packaging.
  - Technical requirements: clean code, docs, reproducible scripts, archived datasets.
  - Success criteria: complete dissertation draft with all sections; rerunnable experiments; presentation deck.
  - Dependencies: all prior.

NOTE: I should be able to run and see the implementation on my local server and command line where applicable.

## Dissertation Writing Integration
- LaTeX structure: Abstract, Introduction, Literature Review, Methodology, Results, Discussion, Conclusion, References, Appendices. Use BibTeX; manage citations with Zotero/Mendeley; IEEE/APA consistent style per department.
- Milestones
  - Week 2: Literature Review draft (first pass) + related work matrix.
  - Week 4: Methodology skeleton (system description, specs, design).
  - Week 6: Methodology full draft; Experimental Design section locked.
  - Week 8: Results (initial) + figures; revise Intro based on findings.
  - Week 11: Discussion/Conclusion drafts; finalize Results.
  - Week 12: Integrate, proofread, finalize references and appendices.

## Risk Management
- Computational bottlenecks: start with pilot (≤5 seeds); early stopping for Static when depleted; parallelize; reduce density levels or seeds if needed; log every k steps only if I/O bound.
- Unexpected results: perform sensitivity analyses (range, density); ablations (disable messaging); validate metrics on toy cases.
- Timeline slippage: drop optional extension; prune factorial (e.g., {0,2,4,6,8}); prioritize core metrics and RQ analyses.

## Deliverables Checklist
- Code: Mesa 3.0 simulation model; batch runner; analysis scripts; Solara visualization components.
- Data: raw per‑step logs; per‑run summaries; metadata JSON; processed analysis tables.
- Documentation: README (this plan); code docs; experimental protocol; config files; environment/requirements.
- Dissertation: complete LaTeX project with all chapters and references.
- Presentation: slide deck (figures, key results, methods).
