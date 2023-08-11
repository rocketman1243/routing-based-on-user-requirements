# Path optimization tie breaker

- If two or more paths are tied in optimization score, use the path with the most AS peering connections, based on total degree of nodes in path. In other words:
- In the optimization stage: If paths are tied, score them based on the number of peering edges they use & sort based on that






# ---------------------------
# Proof of concept experiment
# ---------------------------

- Set everyting up to perform this experiment as smoothly as possible (with one wrapper script and possibilities to easily change variables, and an elegant way to spit out statistics and data)
- test, test, test

# ---------------------------
# Cost of privacy experiment:
# ---------------------------

# AS Paths

- Create the as paths set for each AS, bucketed by final AS
- Add method to return all paths from a certain AS to a final AS by doing first element lookups in the buckets
- Prepare to use this for 'cost of privacy' experiment


# ---------------------------
# Scalability experiment:
# ---------------------------

- Arrange code to test best effort mode scalability & implement improvements







# ----------------------------
# ----- IJSKAST, VOOR LATER --
# ----------------------------


# Latency triplets

- Update json NIO files with latency triplets (and a random internal latency of 10-20 ms or so)
- Figure out a way to add these triplets as virtual links with the corresponding total latency to the graph, and use them in the pathfinding, while being able to reconstruct the full path afterwards (add middle hop as data entry??)
- Add triplets as virtual links
- Update pathfinder to reconstruct path after using a virtual link
