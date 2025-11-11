NOTE: While implementing don't mention which module or topic you are covering from the Msc in AI course. The implementioant folows should be natural. 


# Dissertation Redesign Plan: 30-Day Timeline
## "Communication Range Effects on Multi-Agent Fruit Harvesting Cooperation"

**Target Grade**: 70% (Distinction)  
**Timeline**: 30 days  
**Expertise Level**: Learning (non-expert, MSc student)  
**Focus**: Showcase MSc AI coursework knowledge naturally

---

## Executive Summary

**RQ1 (PRIMARY - FULL IMPLEMENTATION)**: "Does the distance over which robots can communicate actually matter for how much fruit they harvest? And if so, how?"
- Full experimental design with multiple communication ranges (0, 2, 4, 6, 8 cells)
- Statistical analysis and validation
- Complete results chapter with findings

**RQ2 (THEORETICAL ONLY)**: "Does it make a difference whether the fruit grows back or not?"
- Keep implementation (Static vs. Replenishing already exists)
- Discuss theoretically in methodology and future work
- No full experimental runs for RQ2

---

## MSc Topics Integration Map

### From Your Coursework → Dissertation Application

| MSc Module | Topics Covered | Natural Integration into Dissertation |
|------------|----------------|--------------------------------------|
| **Machine Learning** | Supervised learning, regression, performance analysis, hyperparameter tuning | - Performance metrics evaluation<br>- Experimental design methodology<br>- Statistical validation of results<br>- Baseline comparisons |
| **Multi-Agent Systems** | Intelligent agents, practical reasoning, multi-agent interactions, game theory, negotiation, resource allocation | - **CORE OF DISSERTATION**<br>- Agent architecture design<br>- Coordination mechanisms<br>- Communication protocols<br>- Resource allocation strategies |
| **Data Mining** | EDA, model evaluation, generalisation performance, balanced accuracy, feature engineering | - Exploratory data analysis of simulation results<br>- Performance metric selection<br>- Statistical testing methodology<br>- Results visualization |
| **Computational Intelligence** | Swarm intelligence, evolutionary algorithms, parameter tuning, experimental methodology | - Swarm-inspired coordination (lit review)<br>- Parameter selection justification<br>- Experimental design principles<br>- Comparative analysis framework |

---

## Revised Dissertation Structure (6 Chapters)

### **Chapter 1: Introduction** (Current - Keep as is)
- Background and motivation
- Research questions (RQ1 primary, RQ2 theoretical)
- Objectives
- Scope and contributions
- Structure

### **Chapter 2: Literature Review** (Current - Keep simplified version)
- Multi-agent coordination and foraging
- Communication in multi-agent systems
- Agricultural robotics
- Resource dynamics (theoretical discussion)
- Agent-based modeling with Mesa

### **Chapter 3: Methodology** ⭐ **NEW - SHOWCASE MSC KNOWLEDGE**

#### 3.1 Problem Formulation
- Define the communication range optimization problem
- State space, action space, objective function
- Constraints and assumptions

#### 3.2 Alternative Approaches (Demonstrate Breadth)
Discuss multiple possible approaches with pros/cons:

**Approach 1: Reinforcement Learning (Q-Learning)**
- **Description**: Agents learn optimal communication policies through trial and error
- **Pros**: Adaptive, can discover non-obvious strategies, handles dynamic environments
- **Cons**: Requires extensive training time, sample inefficiency, difficult to interpret
- **Why not chosen**: 30-day timeline insufficient for proper RL training and validation
- **Citations**: Your ML module covered Q-learning; cite relevant RL papers

**Approach 2: Evolutionary Algorithms / Swarm Optimization**
- **Description**: Evolve communication range parameters using GA or PSO
- **Pros**: Good for parameter optimization, population-based search
- **Cons**: Computationally expensive, requires many fitness evaluations
- **Why not chosen**: Simulation runtime makes fitness evaluation costly
- **Citations**: Your Computational Intelligence module; cite swarm papers

**Approach 3: Game-Theoretic Analysis**
- **Description**: Model agent interactions as cooperative game, find Nash equilibrium
- **Pros**: Theoretical guarantees, elegant mathematical framework
- **Cons**: Assumes rational agents, difficult to model complex spatial dynamics
- **Why not chosen**: Complexity of spatial foraging doesn't fit game-theoretic assumptions well
- **Citations**: Your Multi-Agent Systems module covered game theory

**Approach 4: Systematic Parameter Sweep with Statistical Analysis** ⭐ **CHOSEN**
- **Description**: Test discrete communication ranges, analyze with statistical methods
- **Pros**: 
  - Interpretable results
  - Feasible within 30 days
  - Rigorous statistical validation
  - Clear experimental design
  - Matches MSc coursework methodology
- **Cons**: 
  - Doesn't discover novel strategies
  - Limited to predefined parameter values
  - Requires many simulation runs
- **Why chosen**: 
  - Aligns with ML module's experimental methodology
  - Feasible timeline
  - Demonstrates understanding of experimental design
  - Provides defensible conclusions with statistical backing

#### 3.3 Simulation Environment Design
- Mesa 3.0 framework justification
- Grid world specification (50x50, non-toroidal)
- Agent architecture (BDI-inspired: Beliefs, Desires, Intentions)
- Communication protocol (broadcast within range)
- Resource dynamics (Static vs. Replenishing - theoretical comparison)

#### 3.4 Experimental Design ⭐ **SHOWCASE DATA MINING / ML KNOWLEDGE**

**Independent Variables**:
- Communication range: {0, 2, 4, 6, 8} cells (5 levels)
- Team size: {10, 20} agents (2 levels)
- Resource density: {0.15, 0.25} (2 levels)
- **Total configurations**: 5 × 2 × 2 = 20 configurations

**Dependent Variables (Performance Metrics)**:
- **Primary**: Total yield (fruit harvested)
- **Secondary**: 
  - Messages sent (communication cost)
  - Efficiency ratio: yield / messages (cost-benefit)
  - Coverage: unique cells visited
  - Time to completion

**Experimental Protocol**:
- Replications: 30 runs per configuration (following ML module best practices)
- Random seeds: Fixed for reproducibility
- Episode length: 500 steps
- Data collection: Per-step metrics via Mesa DataCollector

**Baseline Comparisons**:
- Range 0 (no communication) as baseline
- Compare all ranges against baseline
- Identify optimal range(s)

#### 3.5 Statistical Analysis Plan ⭐ **SHOWCASE ML / DATA MINING KNOWLEDGE**

**Exploratory Data Analysis**:
- Distribution plots (histograms, box plots)
- Scatter plot matrices
- Correlation analysis
- Outlier detection

**Statistical Tests**:
- **Kruskal-Wallis H-test**: Non-parametric test for comparing multiple groups (communication ranges)
  - Why: Don't assume normal distribution
  - Null hypothesis: All ranges have same median yield
- **Post-hoc Dunn's test**: Pairwise comparisons if Kruskal-Wallis significant
  - Bonferroni correction for multiple comparisons
- **Effect size**: Cohen's d for pairwise comparisons
  - Quantify practical significance, not just statistical

**Performance Evaluation**:
- Mean ± standard deviation for each configuration
- Confidence intervals (95%)
- Statistical significance threshold: α = 0.05

**Validation**:
- Check for data leakage (none expected in simulation)
- Verify reproducibility with fixed seeds
- Sensitivity analysis: vary episode length

### **Chapter 4: Implementation** ⭐ **NEW**

#### 4.1 System Architecture
- Model class structure
- Agent class design
- Communication mechanism implementation
- Data collection pipeline

#### 4.2 Agent Behavior Algorithm
- Pseudocode for agent step function
- Movement strategy (random walk with memory)
- Harvesting logic
- Message broadcasting and receiving

#### 4.3 Parameter Selection Justification
- Grid size: 50x50 (balance between complexity and runtime)
- Episode length: 500 steps (sufficient for convergence)
- Communication ranges: {0, 2, 4, 6, 8} (cover spectrum from isolated to well-connected)
- Fruit density: {0.15, 0.25} (sparse vs. moderate)

#### 4.4 Verification and Validation
- Unit tests for agent behaviors
- Sanity checks (e.g., range 0 should have 0 messages)
- Visualization for qualitative validation

### **Chapter 5: Results and Analysis** ⭐ **NEW - FULL EXPERIMENTAL RESULTS**

#### 5.1 Exploratory Data Analysis
- Distribution of yields across all runs
- Box plots by communication range
- Scatter plots: yield vs. messages
- Identify outliers and anomalies

#### 5.2 Statistical Test Results
- Kruskal-Wallis test results (H-statistic, p-value)
- Post-hoc pairwise comparisons table
- Effect sizes (Cohen's d) for significant differences

#### 5.3 Performance Comparison
- Mean yield by communication range (table + bar chart)
- Efficiency ratio analysis (yield per message)
- Optimal range identification

#### 5.4 Impact of Team Size and Density
- Interaction effects (if any)
- Does optimal range change with team size?
- Does optimal range change with resource density?

#### 5.5 Qualitative Analysis
- Visualization snapshots showing agent behavior
- Communication network topology at different ranges
- Emergent patterns observed

#### 5.6 Answer to RQ1
- Clear statement: "Yes, communication range significantly affects yield"
- Optimal range identified: e.g., "Range 4 maximizes yield while maintaining efficiency"
- Evidence-based conclusion with statistical backing

### **Chapter 6: Discussion and Conclusion** ⭐ **NEW**

#### 6.1 Interpretation of Results
- Why does optimal range exist? (information sharing vs. overhead trade-off)
- Comparison with literature findings
- Limitations of current study

#### 6.2 Theoretical Discussion of RQ2 (Resource Dynamics)
- **No experimental results**, but discuss:
  - How Static vs. Replenishing might affect optimal range
  - Hypothesis: Replenishing environments may benefit from sustained communication
  - Theoretical framework for future investigation
  - Cite relevant literature on resource dynamics

#### 6.3 Contributions
- Systematic experimental methodology for communication range optimization
- Statistical validation framework
- Open-source Mesa 3.0 implementation
- Insights for agricultural robotics

#### 6.4 Limitations
- Simplified agent behaviors (no learning)
- Grid-based abstraction (not continuous space)
- Limited environmental complexity
- No obstacles or terrain variation

#### 6.5 Future Work
- **RQ2 Full Investigation**: Systematic experiments on Static vs. Replenishing
- Reinforcement learning for adaptive communication
- Heterogeneous agent teams
- Real-world validation with physical robots
- Dynamic communication range adjustment

#### 6.6 Conclusion
- Summary of findings
- Practical implications
- Final thoughts

---

## 30-Day Timeline

### Week 1 (Days 1-7): Methodology Chapter + Experimental Setup
- **Days 1-2**: Write Chapter 3 (Methodology)
  - Sections 3.1-3.2: Problem formulation and alternative approaches
  - Research and cite papers for each approach
- **Days 3-4**: Complete Chapter 3
  - Sections 3.3-3.5: Simulation design, experimental design, statistical plan
- **Days 5-7**: Prepare experimental infrastructure
  - Write batch runner script
  - Test with small runs
  - Verify data collection

### Week 2 (Days 8-14): Run Experiments + Implementation Chapter
- **Days 8-10**: Run all experiments
  - 20 configurations × 30 replications = 600 runs
  - Estimate: ~2-3 hours runtime (test first!)
  - Save all data to CSV
- **Days 11-14**: Write Chapter 4 (Implementation)
  - System architecture
  - Agent algorithms
  - Parameter justifications
  - Verification

### Week 3 (Days 15-21): Results Analysis + Results Chapter
- **Days 15-16**: Exploratory Data Analysis
  - Generate all plots
  - Statistical tests in Python (scipy.stats)
- **Days 17-19**: Write Chapter 5 (Results)
  - All subsections with figures and tables
  - Statistical test results
  - Answer RQ1 definitively
- **Days 20-21**: Review and refine results chapter

### Week 4 (Days 22-30): Discussion, Conclusion, Final Polish
- **Days 22-24**: Write Chapter 6 (Discussion and Conclusion)
  - Interpretation
  - RQ2 theoretical discussion
  - Limitations and future work
- **Days 25-26**: Update Chapters 1-2 if needed
  - Ensure consistency with new chapters
- **Days 27-28**: Full dissertation review
  - Check citations
  - Proofread
  - Verify all figures/tables
- **Days 29-30**: Final polish and submission prep
  - Generate PDF
  - Check formatting
  - Final read-through

---

## Key Success Factors

### 1. Demonstrate MSc Knowledge Naturally
- **ML Module**: Experimental design, statistical validation, performance metrics
- **Multi-Agent Systems**: Agent architecture, coordination, communication protocols
- **Data Mining**: EDA, visualization, model evaluation
- **Computational Intelligence**: Parameter tuning, experimental methodology

### 2. Maintain Realistic Scope
- Focus on RQ1 with full experimental results
- RQ2 theoretical only (no experiments)
- Simple agent behaviors (no RL)
- Feasible within 30 days

### 3. Target 70% Grade Criteria
- Systematic approach to solution methodologies ✓
- Appropriate range of options considered ✓
- Critical analysis with pros/cons ✓
- Well-designed solution ✓
- Written justification with supporting evidence ✓
- Relevant references ✓

### 4. Keep It Simple and Working
- Use existing Mesa 3.0 simulation (already works)
- Standard statistical tests (Kruskal-Wallis, not complex models)
- Clear visualizations (matplotlib/seaborn)
- Interpretable results

---

## Deliverables Checklist

- [ ] Chapter 3: Methodology (NEW)
- [ ] Chapter 4: Implementation (NEW)
- [ ] Chapter 5: Results and Analysis (NEW)
- [ ] Chapter 6: Discussion and Conclusion (NEW)
- [ ] Experimental data (600 runs, CSV files)
- [ ] Statistical analysis scripts (Python notebooks)
- [ ] All figures and tables
- [ ] Updated references.bib
- [ ] Complete dissertation PDF

---

## Next Steps

1. **Review this plan** - Does it align with your vision?
2. **Start Chapter 3** - Methodology is the foundation
3. **Test experimental setup** - Verify runtime is feasible
4. **Begin writing immediately** - Don't wait for experiments to finish

This plan showcases your MSc knowledge while remaining achievable in 30 days!

