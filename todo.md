# Model accuracy (combine connected graph with rich metadata)

# Convert internet_graph into NIO

- (If needed) Update internet_graph to incorporate all randomly generated attributes of the NIO to be somewhat true 
- (If needed) Update NIO structure to incorporate info from internet_graph, in:
    - Code
    - Report
- Update internet_graph.py script to convert full graph into NIO objects, and spit those out into a new NIO folder

# Path calculator reborn (PCR)

- Save copy of working path calculator in archive
- Update latency calculation to not use info from NIO but latency estimation based on lat/lon
- Update path calculator based on other NIO changes
- Test, test, test


# Path Requirement Object v2 (PROv2)

- Add switch to PRO that allows the user to either allow or deny fallback to  eBGP routing if we cannot find a route using the ASes that are entered into the NIP
- 

# Path optimization tie breaker

- If two or more paths are tied in optimization score, use the path with the most AS peering connections, based on total degree of nodes in path. In other words:
- In the optimization stage: If paths are tied, score them based on the number of peering edges they use & sort based on that

---------------------------
Cost of privacy experiment:
---------------------------

# AS Paths

- Create the as paths set for each AS, bucketed by final AS
- Add method to return all paths from a certain AS to a final AS by doing first element lookups in the buckets
- Prepare to use this for 'cost of privacy' experiment



# ----------------------------
# ----- IJSKAST, VOOR LATER --
# ----------------------------


# Latency triplets

- Update json NIO files with latency triplets (and a random internal latency of 10-20 ms or so)
- Figure out a way to add these triplets as virtual links with the corresponding total latency to the graph, and use them in the pathfinding, while being able to reconstruct the full path afterwards (add middle hop as data entry??)
- Add triplets as virtual links
- Update pathfinder to reconstruct path after using a virtual link
