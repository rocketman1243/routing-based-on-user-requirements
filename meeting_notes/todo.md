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

1. Include pseudocode of pathfinding method

2. Run global best path vs MP path (with a 500ms cap on MP runtime) to show quality of results of MP

3. Update accompanying text for the algorithm according to code changes, and include explanation of the bidirectional bfs code

4. BGP: Describe how the values for local preference should (and will) be set by ASes themselves such that it vibes with the local policy they already (might) have around using local prefs for their paths. If their policies already use values between 100 (default) and (say) 200, the supported-features values should start at 201 whereas 101 is enough for ASes that do not use the local pref yet. SO: Thats why I did not hardcode values in the report (#BANGGGGGGG)

5. Setup evaluations:
   1. For different values of neighbourLimit and neighbourDepth, show the average path improvement.
   2. Calculate the global best path using smartDFS, then compare its #hops and #BER to the #hops and #BER of the fast heuristic approach

6. Research multiple pathfinding algorithms & motivate why I chose bidirectional BFS (no advanced knowledge required, which is useful as the internet often changes, etc.) --> Prepare to defend this at thesis

# Planning

By 4 dec: everything
