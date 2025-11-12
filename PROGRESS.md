# Dissertation Progress Tracker

## Project: Communication Range Effects on Multi-Agent Fruit Harvesting Cooperation

**Student**: Ahmed Maruf  
**Program**: MSc Artificial Intelligence  
**Timeline**: 6 weeks (30 days)  
**Current Week**: 2 of 6  
**Overall Progress**: ~40%

---

## Progress by Component

### 1. Dissertation Writing: 50% (3 of 6 chapters)

| Chapter | Status | Progress | Notes |
|---------|--------|----------|-------|
| 1. Introduction | ✅ Complete | 100% | ~2,500 words, needs minor revisions |
| 2. Literature Review | ✅ Complete | 100% | ~3,000 words, comprehensive |
| 3. Methodology | ✅ Complete | 100% | ~2,800 words, experimental design done |
| 4. Implementation | 🔄 Outline | 10% | Have structure, need to write content |
| 5. Results | ⏳ Not Started | 0% | Waiting for experiments to complete |
| 6. Discussion | ⏳ Not Started | 0% | Planned for Week 5 |

**Total Word Count**: ~8,300 / ~15,000 target (55% of writing)

### 2. Mesa Implementation: 60%

| Component | Status | Progress | Notes |
|-----------|--------|----------|-------|
| Model Structure | ✅ Complete | 100% | HarvestModel class working |
| Agent Classes | ✅ Complete | 90% | Basic behavior works, needs refinement |
| Communication | 🔄 Testing | 70% | Implemented but needs verification |
| Metrics Collection | 🔄 Partial | 60% | 3 of 5 metrics implemented |
| Visualization | ✅ Basic | 80% | Solara UI works, could be prettier |
| Testing | 🔄 Manual | 30% | Manual tests only, no automated tests |

**Code Quality**: Basic functionality works, needs polish

### 3. Experiments: 10%

| Task | Status | Progress | Notes |
|------|--------|----------|-------|
| Experiment Design | ✅ Complete | 100% | 20 configs, 30 reps each |
| Batch Runner | ⏳ Not Started | 0% | Need to write script |
| Data Collection | ⏳ Not Started | 0% | Waiting for batch runner |
| Statistical Analysis | ⏳ Not Started | 0% | Planned for Week 4 |
| Figures Generation | ⏳ Not Started | 0% | Waiting for data |

**Experiments Status**: Design complete, execution pending

### 4. Documentation: 30%

| Document | Status | Progress | Notes |
|----------|--------|----------|-------|
| README | ✅ Complete | 100% | Basic project description |
| HOW_TO_RUN | ✅ Complete | 80% | Basic instructions, needs expansion |
| Code Comments | 🔄 Partial | 40% | Some comments, needs more |
| API Documentation | ⏳ Not Started | 0% | Low priority |

---

## Weekly Progress

### Week 1 (Days 1-5)
**Focus**: Literature review and methodology

**Completed**:
- ✅ Read 25+ papers on multi-agent systems
- ✅ Synthesized literature into review chapter
- ✅ Designed experimental methodology
- ✅ Wrote methodology chapter
- ✅ Set up project structure

**Challenges**:
- Finding recent papers on fruit harvesting (limited domain)
- Deciding between Static vs. Replenishing dynamics
- Choosing appropriate statistical tests

### Week 2 (Days 6-10)
**Focus**: Basic implementation

**Completed**:
- ✅ Implemented HarvestModel class
- ✅ Implemented HarvesterAgent and Fruit classes
- ✅ Basic communication protocol
- ✅ Solara visualization
- ✅ Manual testing with different parameters
- ✅ Wrote introduction chapter

**Challenges**:
- Learning Mesa 3.0 API (different from 2.x)
- Debugging agent movement logic
- Getting Solara visualization to work
- Chebyshev distance calculation confusion

**Current Issues**:
- Not sure if communication is working correctly
- Agents sometimes cluster in one area
- Visualization is a bit slow

### Week 3 (Days 11-15) - CURRENT
**Focus**: Complete implementation and start experiments

**Planned**:
- [ ] Fix communication bugs
- [ ] Add remaining metrics (coverage, efficiency)
- [ ] Write batch experiment runner
- [ ] Run initial test experiments
- [ ] Start implementation chapter

**In Progress**:
- 🔄 Testing communication with different ranges
- 🔄 Debugging agent behavior
- 🔄 Adding more code comments

---

## Metrics

### Time Spent (Estimated)
- **Week 1**: ~35 hours (literature + methodology)
- **Week 2**: ~40 hours (implementation + writing)
- **Total**: ~75 hours / ~180 hours planned (42%)

### Code Statistics
- **Python Files**: 7
- **Lines of Code**: ~800
- **Test Coverage**: 0% (no automated tests yet)
- **Documentation**: Minimal

### Dissertation Statistics
- **Total Words**: ~8,300
- **Chapters Complete**: 3 of 6
- **Figures**: 0 of 6 planned
- **References**: 28 (need more)

---

## Risk Assessment

### High Risk ⚠️
- **Experiments taking too long**: Batch experiments might take days to run
  - *Mitigation*: Start early, run overnight, use smaller sample if needed
  
- **Statistical analysis complexity**: Never done Kruskal-Wallis before
  - *Mitigation*: Study examples, ask supervisor, use scipy library

### Medium Risk ⚠️
- **Implementation bugs**: Communication might not work correctly
  - *Mitigation*: Add logging, write tests, manual verification
  
- **Time management**: Behind schedule on experiments
  - *Mitigation*: Focus on essentials, cut nice-to-have features

### Low Risk ✅
- **Writing**: On track with 3 chapters done
- **Basic implementation**: Core functionality works
- **Methodology**: Well-designed and documented

---

## Next Steps (Priority Order)

### This Week (Week 3)
1. **HIGH**: Fix and verify communication protocol
2. **HIGH**: Implement remaining metrics
3. **HIGH**: Write batch experiment runner
4. **MEDIUM**: Run test experiments (small scale)
5. **MEDIUM**: Start implementation chapter outline
6. **LOW**: Add more code comments

### Next Week (Week 4)
1. **HIGH**: Run full batch experiments (600 runs)
2. **HIGH**: Statistical analysis
3. **HIGH**: Generate all figures
4. **MEDIUM**: Complete implementation chapter
5. **LOW**: Code cleanup and refactoring

---

## Questions for Supervisor

1. Is 30 replications enough for statistical power?
2. Should I use Kruskal-Wallis or ANOVA for analysis?
3. Is my communication protocol realistic?
4. Should I implement RQ2 (Replenishing) or just discuss theoretically?
5. Any feedback on methodology chapter?

---

## Lessons Learned

### Technical
- Mesa 3.0 is quite different from 2.x (no unique_id in agents!)
- Solara visualization is powerful but has learning curve
- Chebyshev distance is max(|x1-x2|, |y1-y2|), not Euclidean
- Random seeds are crucial for reproducibility

### Process
- Start implementation early (good decision!)
- Literature review takes longer than expected
- Writing methodology before coding helps clarify design
- Manual testing is time-consuming but necessary

### Personal
- Need to take more breaks (getting tired)
- Should ask for help earlier when stuck
- Documentation while coding is easier than after
- Version control is essential (git is a lifesaver)

---

## Motivation

**Why this matters**: Understanding how communication range affects cooperation can inform design of real-world multi-agent systems (robot swarms, distributed sensors, etc.)

**What I'm learning**: Multi-agent systems, agent-based modeling, experimental design, statistical analysis, academic writing

**Goal**: Achieve 70%+ grade (distinction level) and contribute to MAS research

---

**Last Updated**: End of Week 2  
**Next Update**: End of Week 3  
**Overall Confidence**: 7/10 (on track but need to execute experiments well)

