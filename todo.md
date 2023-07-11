# Model accuracy (combine connected graph with rich metadata)

- Make a list of metadata items I want for each node (ONLY MUST HAVE!)
- See how many ASes from the connected dataset appear in the rich dataset to get a feel for it
- Rewrite graph to only have nodes based on connected model
- Enhance model with attributes from other datasets, such as:
    - Country
    - Lat
    - Lon
    - Amount of peers (from peeringdb)


# Better feature distribution

- Add metadata about number of peers for each AS from peeringdb or sth else
- Distribute privacy & security features over ASes based on number of peers: More peers increases amount of supported features. Do use something random: Higher peering amount = higher probability (but not absolute). This is more realistic, since some big players might still implement little features, and some small players might be implementing many features.


# Latency: Add latency estimation based on geo distance lookup

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

# Path Requirement Object v2 (PROv2)

- Add switch to PRO that allows the user to either allow or deny fallback to  eBGP routing if we cannot find a route using the ASes that are entered into the NIP
- 

# Path optimization tie breaker

If two or more paths are tied in optimization score, use the path with the most AS peering connections. Do this by doing the following:

- Create method that retrieves the peers of each AS in the path and returns them in a list:
    - https://bgpview.io/asn/1103#peers-v4
    - https://bgpview.docs.apiary.io/#reference/0/asn-peers/view-asn-peers
    - https://www.w3schools.com/python/ref_requests_response.asp
- Create a method that returns true or false based on whether a certain AS is peering with another AS
- In the optimization stage: If paths are tied, score them based on the number of peering edges they use & sort based on that


---------------------------
Cost of privacy experiment:
---------------------------

# AS Paths

- Create the as paths set for each AS, bucketed by final AS
- Add method to return all paths from a certain AS to a final AS by doing first element lookups in the buckets
- Prepare to use this for 'cost of privacy' experiment