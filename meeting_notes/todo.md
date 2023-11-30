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

1. Create graphing script for large paper network & visualize it nicely

2. Look into precomputation:
   1. What would you want to precompute?
   2. How can you precompute it?
   3. How much faster would things become?

3. Practice presentation

4. Research multiple pathfinding algorithms & motivate why I chose bidirectional BFS (no advanced knowledge required, which is useful as the internet often changes, etc.) --> Prepare to defend this at thesis


# Planning

By 4 dec: everything
