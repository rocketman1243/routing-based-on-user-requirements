# The actual internet

- Add actual or fake latency metadata ??? 
- Connect to path calculator
- Test path calculator


# Latency triplets

- Update json NIO files with latency triplets (and a random internal latency of 10-20 ms or so)
- Figure out a way to add these triplets as virtual links with the corresponding total latency to the graph, and use them in the pathfinding, while being able to reconstruct the full path afterwards (add middle hop as data entry??)
- Add triplets as virtual links
- Update pathfinder to reconstruct path after using a virtual link
