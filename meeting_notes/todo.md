Fernando and Adrian's suggestions to improve the algorithm:

- Optimization: Embed strict check into shortest-path and neighbour calculation
- Precompute shortest paths for each BE metric, use it to guide search
- Add weights to BER to create one-number metric to compare neighbours/paths
- Optimization: Tackle bottlenecks by ascending |BER| to fix the worst bottlenecks first

Important for the evaluation:

- Test with different distributions, different paths, give stats
- Look for hard instances in terms of network topologies and try all of them
- Show for various parameters
- But in the end, I can argue: If it works for the one relevant graph (which is the internet), it should be fine (use the paper graph)

When proving the exactness/effectiveness of my algorithm:

- Don't jump to conclusions: An NP-Hard problem remains NP-Hard, so don't fall in the trap of finding a situation that nicely works while the realistic case does not


# TODO

1. Practise presentation

2. Write about other applications of this requirement-based pathfinding problem:
   1. Finding driving routes that fit requirements like requiring nature along the route, avoiding toll ports, requiring silent asphalt to reduce car tire noise, or to avoid naturally fragile areas (to no not disturb that area)
   2. Similar: Walking routes through a city (avoid busy areas, avoid bad neighbourhoods, require walkable areas)
   3. Robotic pathfinding, where node features can encode things like require suitable terrain type (steady rock instead of loose sand), require exposure to the sun (to recharge batteries)

3. Research multiple pathfinding algorithms & motivate why I chose bidirectional BFS (no advanced knowledge required, which is useful as the internet often changes, etc.)
   1. Describe this in the thesis (or update bidirectional DFS if there are better options)
   2. Prepare to defend/explain this at thesis

4. Practice presentation



# Planning

By 4 dec: everything
