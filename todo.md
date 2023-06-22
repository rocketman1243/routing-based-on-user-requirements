
# The graph
- Generate/create 10 nio json files
- Create a python nio object
- Read json file and create nio object for each file
- create networkx graph based on nio objects


# The filtersets
- Generate/create 10 pro json files
- Create a python pro object
- Read json file and create pro object for each file
- Create filtersets based on the nio objects
- Create a mock loop in which the best effort part of the filterset is continuously updated with the next subset OR shorter list


# The path calculation
- Apply filtersets to filter out graph nodes
- Find single path. If path cannot be found, update filterset and try again
- Create a list of all possible paths
- Score each path both by hops and by latency
- Create method that sorts & selects n best paths & returns them



