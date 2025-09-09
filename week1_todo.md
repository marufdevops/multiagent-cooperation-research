## Overview

Below is a concise, practical primer on the core multi-agent systems (MAS) concepts relevant to studying how communication range impacts cooperation in fruit-harvesting on a grid. Each section ties theory to concrete foraging/harvesting examples and ends with implications for analyzing optimal communication ranges.

---

## Agent Architecture

### What defines an agent
- An agent is an autonomous entity that perceives its environment, reasons using a policy or controller, and acts to achieve goals.
- Core loop: perceive → interpret/update internal state → decide (policy) → act.

### Agent properties
- Autonomy: acts without direct human control (e.g., harvester picks fruit based on local map).
- Reactivity: responds to environmental changes (e.g., obstacle appears, reroutes).
- Proactivity: goal-directed behavior beyond immediate stimuli (e.g., scouting unvisited rows).
- Social ability: communicates and coordinates with others (e.g., share fruit hotspot locations).

### Perception and action in environments
- Perception: local sensing (cells within sensor radius), messages from neighbors, stigmergic signals.
- Action: move (N/S/E/W/diagonals), harvest, broadcast message, drop marker/pheromone, wait.

Foraging example:
- Each agent maintains a local costmap and a fruit heatmap; it fuses sensor detections with received messages to choose next cell via A* or greedy ascent on heat.

Implication for range analysis:
- Larger range broadens the perceived state via messages, shifting policies from local-greedy to more globally informed, but can increase noise, congestion, and herding.

---

## Multi-Agent Coordination

### Forms of coordination
- Cooperation: agents increase collective yield (e.g., split orchard rows).
- Competition: agents pursue individual reward (e.g., rush to nearest fruit), often hurting collective yield if unregulated.
- Collaboration: tightly coupled joint tasks (e.g., two robots lift heavy fruit).
- Distributed decision-making: each agent decides locally; alignment emerges via protocols or incentives.

### Common coordination mechanisms
- Task allocation: auction/Contract Net, market-based assignment, threshold policies.
- Role assignment: scouts (explore) vs harvesters (exploit); dynamic switching by need.
- Spatial partitioning: divide orchard by regions to reduce overlap.
- Consensus/gossip: converge on shared estimates (e.g., global fruit density trend).
- Avoidance rules: local collision and interference avoidance.

Foraging example:
- Contract Net: a scout announces a fruit cluster; nearby agents bid based on travel cost; lowest-cost agent “wins” the cluster.

Implication for range analysis:
- Too small range: fragmented auctions/partitions ⇒ duplicate work and missed synergies.
- Too large range: global auctions everywhere ⇒ high message overhead, delays, and herding to the same few clusters.

---

## Communication in MAS

### Types
- Direct messaging: point-to-point or many-to-one (e.g., unicast to nearest harvester).
- Broadcast/multicast: send to all within range R or to a topic.
- Stigmergy: indirect via environment (e.g., digital pheromones marking high-yield rows).
- Gossip/epidemic: random neighbor exchanges spreading info gradually.

### Protocol patterns
- Periodic beacons vs event-triggered messages (send on significant change).
- Flooding with TTL (time-to-live) vs bounded-radius broadcast.
- Publish/subscribe (topics: “hotspot”, “blocked path”), auction-based protocols, consensus rounds.

### Range effects
- Connectivity: as range increases, the communication graph moves from fragmented to connected (random geometric graph threshold). Below threshold, info dies locally; above it, info percolates.
- Latency vs load: larger range reduces hops (lower latency) but raises per-message recipients (higher load, contention).
- Information quality: more range → faster global awareness, but also more redundant/conflicting data; may reduce exploration diversity (herding).
- Robustness: moderate range balances resilience (multiple paths) without overwhelming traffic.

Foraging example:
- Event-triggered local broadcast of “cluster at (x,y), size s,” with R=8 cells and TTL=2 hops reduces duplicates while informing nearby agents.

Implication for range analysis:
- Expect a non-monotonic yield curve Y(R): increases as connectivity emerges, then plateaus or declines as overhead and herding dominate. The optimum R* depends on agent density, fruit spatial clustering, bandwidth limits, and protocol.

---

## Collective Behavior

### Emergence and swarm principles
- Local rules → global patterns (self-organization).
- Exploration–exploitation trade-off governs coverage vs depth.
- Positive feedback: hotspots attract agents (faster harvest) but risk congestion.
- Negative feedback: pheromone evaporation, cost penalties for crowding maintain diversity.

### Collective yield optimization
- Goal: maximize total fruit harvested per time or per energy.
- Levers: spatial partitioning, role ratios, adaptive thresholds (join/leave cluster based on marginal gain), and message suppression (don’t broadcast trivial updates).

Foraging example:
- Virtual pheromone field: deposit “harvested” pheromones to discourage revisiting; deposit “fruit” pheromones where detection confidence is high; evaporation manages staleness.

Implication for range analysis:
- With stigmergy, smaller direct-communication ranges can still yield strong coordination via shared fields; the optimal R can be smaller when stigmergy is effective.

---

## Grid-Based Environments

### Spatial relationships and neighborhoods
- Von Neumann (4-neighbors) vs Moore (8-neighbors).
- Line-of-sight and obstacles; toroidal vs bounded edges.
- Costs: step cost, turning cost, harvesting time.

### Navigation and interaction
- Planning: greedy next-best cell, A*, D*, frontier-based exploration.
- Collision avoidance: prioritized moves, reservation tables, ORCA-like rules in discrete form.
- Resource dynamics: static fruit vs replenishing; cluster size distribution; occlusion noise.

Foraging example:
- Partition a 100×100 grid into 10×10 tiles; assign agents to tiles; allow spillover to adjacent tiles when a tile’s fruit falls below a threshold.

Implication for range analysis:
- The spatial correlation length of fruit distribution and the tile size relative to R determine how useful nonlocal messages are. If clusters are large, moderate R helps agents coordinate across tile boundaries without full broadcast.

---

## Key Terminology (definitions + examples)

- Agent: autonomous decision-maker; a robot harvester.
- Policy: mapping from state to action; “move to cell with highest fruit score.”
- Local vs global state: local sensor map vs shared orchard map.
- Autonomy/reactivity/proactivity/social ability: see Agent Architecture.
- Cooperation: increase team yield; e.g., divide rows.
- Competition: agents race for the same fruit, causing conflicts.
- Collaboration: joint action; lifting heavy crates.
- Coordination: mechanisms aligning actions; auctions, roles.
- Task allocation: assigning clusters to agents; Contract Net.
- Role assignment: scout vs harvester roles.
- Communication graph: nodes = agents; edges if distance ≤ R.
- Communication range (R): max distance for direct exchange.
- Bandwidth/latency: message capacity/delay; impacts timeliness.
- Stigmergy: indirect coordination via environment; digital pheromones.
- Gossip: randomized neighbor exchanges; robust, gradual spread.
- Broadcast/multicast/unicast: many-to-all/group/single messaging.
- Flooding/TTL: propagate messages with hop limit to bound scope.
- Consensus: protocol to agree on values; e.g., shared yield estimate.
- Emergence/self-organization: global patterns from local rules.
- Exploration vs exploitation: discover new fruit vs harvest known clusters.
- Redundancy/overlap: multiple agents harvesting same area unnecessarily.
- Herding: too many agents chase the same hotspot.
- Connectivity threshold: R at which the graph becomes connected.
- Random geometric graph (RGG): model of agents connected by distance.
- Percolation: emergence of large connected components as R increases.
- Congestion/overhead: increased traffic, processing with large R.
- Grid neighborhood: Von Neumann/Moore adjacency.
- Partitioning/tiling: divide grid into regions for teams.
- Evaporation (stigmergy): decay of markers to avoid staleness.
- TTL (time-to-live): cap on message hops to contain spread.
- Reservation table: time–cell booking to avoid collisions.
- Utility/reward: objective function; e.g., fruit per time/energy.

---

## Applying Concepts to Find Optimal Communication Range

### Hypotheses
- H1 (Connectivity gain): Y(R) rises sharply near the connectivity threshold of the agent RGG on the grid.
- H2 (Diminishing returns): Benefits saturate as R grows once information becomes redundant.
- H3 (Overhead/herding): Beyond a point, Y(R) decreases due to congestion, synchronization delay, and reduced exploration diversity.
- H4 (Environment dependence): Optimal R* increases when fruit is sparse/clustered widely; decreases when stigmergy is effective or agent density is high.

### Experimental design (practical)
- Control variables: agent count/density, fruit spatial autocorrelation, replenishment, sensor noise, obstacles, update synchronicity, protocol type (event-triggered vs periodic).
- Sweep: R ∈ {0, 2, 4, 6, 8, 12, 16, 24} cells; repeat across random seeds.
- Protocol variants:
  - Baseline: no messages (R=0) + stigmergy only.
  - Local broadcast with TTL=1–2 hops; event-triggered on hotspot discovery/decay.
  - Auction-based (Contract Net) within range R.
  - Gossip with k neighbors per step.
- Metrics:
  - Yield: total fruit/time; fruit per agent-hour; energy-normalized yield.
  - Efficiency: unique-cells-covered, duplication rate, idle time, collision count.
  - Communication: msgs/agent/s, bytes/agent/s, latency to awareness of a hotspot.
  - Spatial: coverage entropy, Gini of workload, clustering coefficient of comm graph.
- Analysis:
  - Plot Y(R) with confidence intervals; also overhead vs yield to find Pareto front.
  - Identify R where marginal benefit ≈ marginal cost (B′(R)=C′(R)).
  - Check robustness across densities and clustering levels.

### Modeling intuition
- Benefit curve B(R): increasing, saturating (faster info spread, better task allocation).
- Cost curve C(R): increasing, often convex (traffic, processing, contention, herding).
- Optimum R*: near where B′=C′; often moderate, not maximal.

### Design recommendations
- Prefer event-triggered, bounded-radius broadcasts with TTL and rate limits.
- Combine light direct messaging with stigmergy so effective R can be smaller.
- Use spatial partitioning and role assignment to reduce overlap and traffic.
- Employ message summarization (e.g., top-k hotspots, decay over time) to limit redundancy.

---

## Short, Concrete Example Scenario

- Environment: 100×100 grid, 60 agents, Moore moves, obstacles = 10% cells.
- Fruit: 1500 items in clusters (Gaussian blobs; correlation length ≈ 8 cells).
- Protocol: event-triggered local broadcast of hotspots with R sweep, TTL=1, decay 0.95/step; reservation table for movement; partition into 10×10 tiles.
- Observation:
  - R=0: yield low; duplication high; many clusters undiscovered.
  - R=4–8: yield jumps; duplication drops; timely reinforcement to large clusters.
  - R=16+: message load spikes; agents herd to top clusters; remote tiles under-explored; net yield plateaus or dips.
- Result: optimal R around 6–8 cells for these settings; smaller when agent density is high or stigmergy decay is tuned well.

---

## Want this in your week1_todo.md?

I can insert a cleaned, paper-ready version of this content into week1_todo.md, organized by the same headings. Would you like me to do that now or prefer a shorter checklist version?
