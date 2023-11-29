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

1. Create graphs that convince Fernando that my heuristic is DA BOMB!!!

8. Setup evaluations:
   1. For different values of neighbourLimit and neighbourDepth, show the average path improvement.
   2. Calculate the global best path using smartDFS, then compare its #hops and #BER to the #hops and #BER of the fast heuristic approach

9. Research multiple pathfinding algorithms & motivate why I chose bidirectional BFS (no advanced knowledge required, which is useful as the internet often changes, etc.) --> Prepare to defend this at thesis




7. Make presentation for Monday's meeting with:
   1. Progress update:
      1. Proof for completeness is done
      2. Experimental setup is done, can collect data
      3. BGP implementation ideas are done
   2. Results of smartDFS vs heuristic with also compared runtimes to see what the shorter runtime 'costs' us
   3. Overview of BGP implementation ideas
   4. Sign green light??


# Planning

By 4 dec: everything
