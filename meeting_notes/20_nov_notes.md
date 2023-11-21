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

1. Perform evaluations:
   1. For different values of neighbourLimit and neighbourDepth, show the average path improvement.
   2. Calculate the global best path using smartDFS, then compare its #hops and #BER to the #hops and #BER of the fast heuristic approach

2. Design integration into BGP without changing BGP
3. Proof as much as possible the exactness or applicability of my approach

# Planning

By 4 dec: everything
