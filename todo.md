
# The filtersets

- Implement looping system that decreases the best effort portion of the requirements each time (maybe create a filterset object method (1 for privacy and 1 for security) that updates the internal best effort list to the less demanding one, after which the drop method can be called again? This would create a nice readable loop in the main file)

- Test this setup!

- Create a mock loop in which the best effort part of the filterset is continuously updated with the next subset OR shorter list


# The path calculation
- Apply filtersets to filter out graph nodes
- Find single path. If path cannot be found, update filterset and try again
- Create a list of all possible paths
- Score each path both by hops and by latency
- Create method that sorts & selects n best paths & returns them



