# TODO List - Dissertation Progress

## Current Status: ~40% Complete (Week 2)

### ✅ Completed (Weeks 1-2)
- [x] Literature review complete
- [x] Methodology chapter written
- [x] Basic Mesa model implemented
- [x] Agent classes working (harvester, fruit)
- [x] Simple Solara visualization
- [x] Basic sandbox testing
- [x] Introduction chapter drafted

### 🔄 In Progress (Week 3)
- [ ] Debugging communication protocol
  - Messages are being sent but need to verify correctness
  - Check Chebyshev distance calculation
- [ ] Testing different communication ranges
  - Need to run systematic tests for ranges 0, 2, 4, 6, 8
- [ ] Implementing full metrics collection
  - Currently have: yield, messages, remaining_fruit
  - TODO: Add coverage metric (cells visited)
  - TODO: Add efficiency metric (yield/messages)

### 📋 Planned (Weeks 3-4)
- [ ] **Implementation Chapter**
  - Write system architecture section
  - Document design decisions
  - Add code snippets and explanations
  - Create architecture diagrams

- [ ] **Batch Experiments**
  - Design experiment runner script
  - Run 600 simulations (20 configs × 30 reps)
  - Save results to CSV
  - Implement progress tracking

- [ ] **Statistical Analysis**
  - Learn Kruskal-Wallis test (non-parametric ANOVA)
  - Implement Dunn's post-hoc test
  - Calculate effect sizes (Cohen's d)
  - Generate statistical tables

- [ ] **Figures Generation**
  - Yield distribution histogram
  - Box plots by communication range
  - Scatter plot: yield vs messages
  - Efficiency by range
  - Additional plots for team size and density

### 📋 Planned (Weeks 5-6)
- [ ] **Results Chapter**
  - Write statistical analysis section
  - Integrate all figures
  - Interpret findings
  - Answer RQ1

- [ ] **Discussion Chapter**
  - Interpret results in context of literature
  - Discuss RQ2 theoretically (no experiments)
  - Limitations section
  - Future work section

- [ ] **Final Polish**
  - Proofread all chapters
  - Check citations
  - Format references
  - Generate table of contents
  - Compile final PDF

## Known Issues

### Code
- [ ] Communication range calculation might have off-by-one error
- [ ] Agent movement sometimes gets stuck in corners
- [ ] Visualization is slow with many agents (>10)
- [ ] No error handling for invalid parameters
- [ ] Hardcoded grid size in some places

### Dissertation
- [ ] Need more recent references (2023-2024)
- [ ] Introduction needs stronger motivation
- [ ] Methodology could use more justification for choices
- [ ] Missing some key citations in literature review

### Experiments
- [ ] Haven't tested with large grids (>50x50)
- [ ] Need to verify reproducibility with seeds
- [ ] Unsure about optimal number of replications (30?)
- [ ] Need to decide on episode length (500 steps?)

## Questions to Resolve

1. **Statistical Tests**: Is Kruskal-Wallis the right choice? Should I use ANOVA instead?
2. **Effect Size**: How to interpret Cohen's d values in this context?
3. **Sample Size**: Is 30 replications enough for statistical power?
4. **Communication Cost**: Should I count messages per agent or total?
5. **Baseline**: Should Range=0 be the baseline or should I have a "no agents" control?

## Resources Needed

- [ ] Access to university cluster for batch experiments (or run locally overnight)
- [ ] Statistical analysis library (scipy? statsmodels?)
- [ ] Plotting library (matplotlib? seaborn?)
- [ ] LaTeX figure integration guide
- [ ] Example dissertations for formatting reference

## Timeline

### Week 3 (Current)
- Fix known bugs in communication
- Implement remaining metrics
- Start implementation chapter outline

### Week 4
- Run batch experiments
- Generate all figures
- Complete implementation chapter

### Week 5
- Statistical analysis
- Write results chapter
- Start discussion chapter

### Week 6
- Complete discussion chapter
- Final revisions
- Proofread and format
- Submit!

## Notes

- Communication protocol seems to work but need more testing
- Agents are harvesting fruit correctly
- Visualization helps debug agent behavior
- Need to be careful about random seeds for reproducibility
- Should probably add more comments to code
- Consider adding unit tests?

## Ideas for Future Work (Post-Submission)

- Implement RQ2 (Replenishing dynamics)
- Try different communication protocols (broadcast vs. targeted)
- Test with heterogeneous agents (different speeds, ranges)
- Add obstacles to the grid
- Implement learning agents (Q-learning?)
- Compare with other coordination mechanisms

---

**Last Updated**: Week 2  
**Next Review**: End of Week 3

