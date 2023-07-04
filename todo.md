# Normally distributed privacy & security features + Geolocation

- Create method that generates a mapping of privacy and security features to a list of indexes normally distributed over the list of indexes, ranging from 1-30 features per category per AS, such that lower index support higher numbers of features and higher indexes support lower number of features
- Rewrite the report to reflect that I use a linearly decreasing distribution of features as that is more realistic (bigger ASes have more resources to implement privacy & security features)
- Add to agenda to discuss feature distribution with Adrian
- Make the method flexible such that I can change the distribution with little effort
- Add these features as attributes to the AS nodes, such that the index is NOT directly mapped to AS number, as the AS dataset may be imperfect. Just use the same order (with enumerate(ASes) maybe??)

- Grab geolocation (country) from CAIDA dataset
- Add geolocation (country) as attribute to AS nodes


# Latency: Add latency estimation based on geo distance lookup

- Grab coordinates of AS from CAIDA dataset
- Add coordinates to AS nodes as attributes
- Find geo distance lookup tool
- Create method that spits out geographic distance between two random ASes (with input only the two ASes) using the geo lookup tool
- Research some conversion between geo distance and latency
- Modify geo distance to spit out latency between two ASes instead
- Add this latency as attribute to each link (Add note to later on optimize this by only estimating latency info when needed (when grading the paths))

# Latency triplets

- Update json NIO files with latency triplets (and a random internal latency of 10-20 ms or so)
- Figure out a way to add these triplets as virtual links with the corresponding total latency to the graph, and use them in the pathfinding, while being able to reconstruct the full path afterwards (add middle hop as data entry??)
- Add triplets as virtual links
- Update pathfinder to reconstruct path after using a virtual link

# Path calculator reborn (PCR)

- Intelligently Copy/paste path calculator to new file
- Import internet graph into new file
- Feed internet graph to path calculator
- Create one test PRO based on the internet graph
- Fiddle until paths can be found





---------------------------
Cost of privacy experiment:
---------------------------

# AS Paths

- Create the as paths set for each AS, bucketed by final AS
- Add method to return all paths from a certain AS to a final AS by doing first element lookups in the buckets
- Prepare to use this for 'cost of privacy' experiment