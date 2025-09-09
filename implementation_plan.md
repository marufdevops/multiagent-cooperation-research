# 12-Week Masters Dissertation Implementation Plan
## "Communication Range Effects on Multi-Agent Fruit Harvesting Cooperation"

---

## **Week 1: Foundation & Setup**

### **Learning Prerequisites (15-20 hours)**
- **Python Basics Review**
  - Classes, inheritance, data structures (lists, dictionaries)
  - File I/O, CSV handling with pandas
  - Basic plotting with matplotlib
- **Multi-Agent Systems Concepts**
  - What are agents, environments, and interactions?
  - Read: Wooldridge Chapter 1-2 (Introduction to MultiAgent Systems)
- **Grid-Based Simulations**
  - Coordinate systems, neighbor detection
  - Spatial relationships and distance calculations

### **Implementation Tasks (10-15 hours)**
- [ ] Install Python environment (Anaconda recommended)
- [ ] Install Mesa framework: `pip install mesa pandas matplotlib`
- [ ] Create project structure:
  ```
  fruit_harvester_simulation/
  ├── agents.py
  ├── environment.py
  ├── simulation.py
  ├── data_collection.py
  └── analysis.py
  ```
- [ ] Build basic grid environment (10x10)
- [ ] Create simple agent that can move randomly

### **Deliverable**
- Working basic simulation with agents moving on grid

---

## **Week 2: Core Agent Implementation**

### **Learning Prerequisites (10-15 hours)**
- **Agent Communication Concepts**
  - Message passing, information sharing
  - Local vs global knowledge
- **Mesa Framework Deep Dive**
  - Agent class structure, step() methods
  - Grid spaces, scheduling
  - Tutorial: Mesa's "Boltzmann Wealth Model"

### **Implementation Tasks (15-20 hours)**
- [ ] Implement `HarvesterAgent` class with:
  - Position tracking
  - Fruit inventory
  - Communication range parameter
  - Basic movement toward fruit
- [ ] Add fruit spawning and regeneration
- [ ] Implement information sharing mechanism
- [ ] Create cooperative vs competitive strategies

### **Code Structure**
```python
class HarvesterAgent:
    def __init__(self, communication_range, strategy):
        self.communication_range = communication_range
        self.strategy = strategy  # "cooperative" or "competitive"
        self.known_fruit_locations = []
        self.fruit_collected = 0
```

### **Deliverable**
- Agents can harvest fruit and share information based on communication range

---

## **Week 3: Data Collection & Metrics**

### **Learning Prerequisites (8-10 hours)**
- **Statistical Concepts**
  - Mean, variance, confidence intervals
  - Experimental design basics
- **Data Analysis with Pandas**
  - DataFrames, groupby operations
  - Basic statistical functions

### **Implementation Tasks (15-20 hours)**
- [ ] Implement Mesa's DataCollector
- [ ] Track key metrics:
  - Total fruit collected per episode
  - Information sharing frequency
  - Agent spatial distribution
  - Individual agent performance
- [ ] Create data export functionality
- [ ] Build basic visualization dashboard

### **Metrics to Implement**
```python
def compute_cooperation_index(self):
    return messages_sent / total_possible_messages

def compute_spatial_clustering(self):
    return average_distance_between_agents

def compute_collective_yield(self):
    return total_fruit_harvested / total_fruit_available
```

### **Deliverable**
- Simulation exports data to CSV files with all key metrics

---

## **Week 4: Experimental Design & Initial Results**

### **Learning Prerequisites (8-10 hours)**
- **Experimental Design**
  - Control variables, independent/dependent variables
  - Statistical significance, p-values
- **Research Methodology**
  - Hypothesis formation
  - Replication importance

### **Implementation Tasks (15-20 hours)**
- [ ] Design experiment matrix:
  - Communication ranges: 0, 1, 2, 3, 4 grid cells
  - Agent counts: 10, 20, 30
  - 30 replications per configuration
- [ ] Run initial experiments
- [ ] Create automated batch processing
- [ ] Basic statistical analysis

### **Experimental Setup**
```python
experiments = [
    {"comm_range": r, "num_agents": n, "replications": 30}
    for r in [0, 1, 2, 3, 4]
    for n in [10, 20, 30]
]
```

### **Deliverable**
- Complete dataset from initial experiments
- Preliminary results showing communication range effects

---

## **Week 5: Advanced Analysis & Visualization**

### **Learning Prerequisites (8-10 hours)**
- **Data Visualization**
  - Matplotlib advanced features
  - Seaborn for statistical plots
- **Statistical Analysis**
  - ANOVA, t-tests
  - Correlation analysis

### **Implementation Tasks (15-20 hours)**
- [ ] Create comprehensive visualization suite:
  - Line plots: yield vs communication range
  - Heatmaps: agent movement patterns
  - Box plots: performance distributions
- [ ] Statistical significance testing
- [ ] Identify optimal communication ranges
- [ ] Document unexpected findings

### **Analysis Code**
```python
import seaborn as sns
import scipy.stats as stats

# ANOVA test for communication range effects
f_stat, p_value = stats.f_oneway(*yield_groups)

# Visualization
sns.boxplot(x='comm_range', y='collective_yield', data=results_df)
```

### **Deliverable**
- Complete analysis with statistical validation
- Professional visualizations for dissertation

---

## **Week 6: Literature Review & Writing**

### **Learning Prerequisites (10-15 hours)**
- **Academic Writing**
  - Research paper structure
  - Citation management (Zotero/Mendeley)
- **Literature Search**
  - Google Scholar, IEEE Xplore
  - Reference management

### **Implementation Tasks (15-20 hours)**
- [ ] Complete literature review (20-30 papers)
- [ ] Write methodology section
- [ ] Document simulation architecture
- [ ] Begin results section
- [ ] Create professional figures

### **Key Papers to Find**
- Multi-agent coordination (Wooldridge, Stone & Veloso)
- Swarm intelligence (Dorigo, Campo)
- Communication in multi-agent systems
- Resource gathering simulations

### **Deliverable**
- 15-20 pages of dissertation draft
- Complete bibliography

---

## **Week 7: Q-Learning Extension (Optional)**

### **Learning Prerequisites (15-20 hours)**
- **Reinforcement Learning Basics**
  - States, actions, rewards
  - Exploration vs exploitation
  - Q-learning algorithm
- **Recommended Resources**
  - Sutton & Barto "Reinforcement Learning" Chapter 6
  - Online RL course (Coursera/edX)

### **Implementation Tasks (20-25 hours)**
- [ ] Implement simple Q-learning agent
- [ ] Define discrete state space
- [ ] Compare RL vs rule-based agents
- [ ] Analyze learned strategies

### **Q-Learning Implementation**
```python
class QLearningAgent(HarvesterAgent):
    def __init__(self, communication_range):
        super().__init__(communication_range)
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.epsilon = 0.1  # Exploration rate
        
    def get_state(self):
        # Discretize environment
        fruit_nearby = min(self.count_nearby_fruit(), 3)
        agents_nearby = min(len(self.get_neighbors()), 2)
        return (fruit_nearby, agents_nearby)
```

### **Deliverable**
- Working Q-learning agents
- Comparison results: RL vs rule-based performance

---

## **Week 8: Advanced Experiments (Optional)**

### **Learning Prerequisites (5-8 hours)**
- **Advanced Statistical Methods**
  - Multi-factor ANOVA
  - Effect size calculations

### **Implementation Tasks (20-25 hours)**
- [ ] Extended experiments with RL agents
- [ ] Cross-validation of results
- [ ] Sensitivity analysis
- [ ] Robustness testing

### **Advanced Metrics**
```python
def analyze_learned_strategies(q_tables):
    # Extract patterns from Q-learning agents
    strategy_patterns = {}
    for state, actions in q_table.items():
        best_action = max(actions, key=actions.get)
        strategy_patterns[state] = best_action
    return strategy_patterns
```

### **Deliverable**
- Enhanced results with machine learning component
- Strategy analysis from learned behaviors

---

## **Week 9: Results Analysis & Discussion**

### **Implementation Tasks (25-30 hours)**
- [ ] Complete statistical analysis
- [ ] Write comprehensive results section
- [ ] Develop discussion of findings
- [ ] Compare with literature
- [ ] Identify limitations

### **Key Analysis Questions**
- What is the optimal communication range?
- How does agent density affect cooperation?
- What strategies did RL agents discover?
- How do results compare to existing research?

### **Deliverable**
- Complete results and discussion sections
- All figures and tables finalized

---

## **Week 10: Future Work & Conclusions**

### **Implementation Tasks (20-25 hours)**
- [ ] Design future research directions
- [ ] Write conclusions section
- [ ] Complete abstract
- [ ] Executive summary
- [ ] Code documentation and cleanup

### **Future Work Topics**
- Deep reinforcement learning extensions
- Dynamic environment changes
- Heterogeneous agent capabilities
- Real-world applications

### **Deliverable**
- Complete dissertation draft
- Well-documented codebase

---

## **Week 11: Review & Refinement**

### **Tasks (25-30 hours)**
- [ ] Complete dissertation review
- [ ] Supervisor feedback integration
- [ ] Grammar and style editing
- [ ] Reference formatting
- [ ] Figure quality improvement

### **Quality Checklist**
- [ ] All claims supported by data
- [ ] Figures are publication-quality
- [ ] Code runs without errors
- [ ] Statistical tests are appropriate
- [ ] Writing is clear and concise

### **Deliverable**
- Polished dissertation ready for submission

---

## **Week 12: Final Submission**

### **Tasks (15-20 hours)**
- [ ] Final proofreading
- [ ] Format according to university guidelines
- [ ] Create presentation slides
- [ ] Practice defense presentation
- [ ] Submit dissertation

### **Submission Checklist**
- [ ] PDF formatted correctly
- [ ] All required sections included
- [ ] Code repository organized
- [ ] Data files properly documented
- [ ] Plagiarism check completed

---

## **Learning Resources**

### **Essential Books**
1. Wooldridge, M. "An Introduction to MultiAgent Systems" (Chapters 1-3)
2. Wilensky, U. & Rand, W. "An Introduction to Agent-Based Modeling"
3. Sutton, R. & Barto, A. "Reinforcement Learning" (Chapter 6 for Q-learning)

### **Online Resources**
- Mesa Documentation: https://mesa.readthedocs.io/
- Python Data Science Handbook (free online)
- Coursera: "Reinforcement Learning Specialization"

### **Programming Skills Needed**
- Python: Classes, inheritance, data structures
- Pandas: Data manipulation and analysis
- Matplotlib/Seaborn: Data visualization
- NumPy: Numerical computations
- Basic statistics and hypothesis testing

---

## **Risk Management**

### **High-Risk Items**
- **Week 7-8 (Q-learning)**: Optional - skip if behind schedule
- **Complex visualizations**: Use simple plots if time-constrained
- **Large-scale experiments**: Reduce parameter space if needed

### **Fallback Plans**
- Focus on core communication range question
- Use smaller grid sizes for faster experiments
- Simplify statistical analysis if needed

### **Success Metrics**
- **Minimum Viable**: Communication range analysis complete
- **Target**: Include basic Q-learning comparison
- **Stretch Goal**: Advanced ML analysis and future work roadmap

---

## **Weekly Time Allocation**
- **Learning/Research**: 40% (8-12 hours/week)
- **Implementation**: 45% (10-15 hours/week)
- **Writing/Documentation**: 15% (3-5 hours/week)
- **Total**: 25-30 hours/week

This plan balances learning fundamentals with practical implementation while maintaining flexibility for your 3-month timeline.