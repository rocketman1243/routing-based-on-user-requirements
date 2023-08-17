# TOOD

- Write helper script to convert real-life-path-requests to PROs
- Test real-life experiment on small-scale setup

######### HOLIDAY ###################

- Write code for 'cost of being picky' experiment


- Incorporate non-binary values in manrs dataset for rpki and IRR (whatever that is :D)






# ----------------------------
# ----- IJSKAST, VOOR LATER --
# ----------------------------


# Latency triplets

- Update json NIO files with latency triplets (and a random internal latency of 10-20 ms or so)
- Figure out a way to add these triplets as virtual links with the corresponding total latency to the graph, and use them in the pathfinding, while being able to reconstruct the full path afterwards (add middle hop as data entry??)
- Add triplets as virtual links
- Update pathfinder to reconstruct path after using a virtual link

# Proof of concept experiment

- Set everyting up to perform this experiment as smoothly as possible (with one wrapper script and possibilities to easily change variables, and an elegant way to spit out statistics and data)
- test, test, test

# Cost of privacy experiment with AS Paths:

- Create the as paths set for each AS, bucketed by final AS
- Add method to return all paths from a certain AS to a final AS by doing first element lookups in the buckets
- Prepare to use this for 'cost of privacy' experiment

# Scalability experiment:

- Arrange code to test best effort mode scalability & implement improvements

