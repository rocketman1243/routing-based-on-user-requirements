
def fulfillsStrictRequirements(G, pro, node):
    # If we encountered this node before and deemed it UNWORTHY, Call out the same sentence AGAIN!!!

    if G.nodes[node]["filtered"]:
        return False

    # Measure up this node's abilities to our utmost highly regarded standards of purity and honour,
    # and only return true when this young padawan is WORTHY to meet our gaze
    if set(pro.requirements.strict).issubset(set(G.nodes[node]["features"])):
        if len(set(pro.geolocation.exclude).intersection(set(G.nodes[node]["geolocation"]))) == 0:
            return True

    # Set those who are not deemed worthy with a MARK that will haunt them for the rest of
    # their LIFE such that all that encounter these faulty ones later on will know what
    # use they are to them and the rest of society.
    G.nodes[node]["filtered"] = True
    return False





"""
Source code for the two pathfinding functions below is adapted from networkx version 3.2.1:
https://networkx.org/documentation/stable/_modules/networkx/algorithms/shortest_paths/unweighted.html#bidirectional_shortest_path

Code is adapted to suit my needs. The code is licensed under the 3-clause BSD licence, which allows modifications of code
under the condition of copying with it the full license text. Thus, here it is:

 Copyright (C) 2004-2023, NetworkX Developers
   Aric Hagberg <hagberg@lanl.gov>
   Dan Schult <dschult@colgate.edu>
   Pieter Swart <swart@lanl.gov>
   All rights reserved.

   Redistribution and use in source and binary forms, with or without
   modification, are permitted provided that the following conditions are
   met:

     * Redistributions of source code must retain the above copyright
       notice, this list of conditions and the following disclaimer.

     * Redistributions in binary form must reproduce the above
       copyright notice, this list of conditions and the following
       disclaimer in the documentation and/or other materials provided
       with the distribution.

     * Neither the name of the NetworkX Developers nor the names of its
       contributors may be used to endorse or promote products derived
       from this software without specific prior written permission.

   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
   OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
def find_predecessors_and_successors(G, pro):
    """Bidirectional shortest path helper.

    Returns (pred, succ, w) where
    pred is a dictionary of predecessors from w to the source, and
    succ is a dictionary of successors from w to the target.
    """
    source = pro.as_source
    target = pro.as_destination


    # Do BFS from both source and target and meet in the middle
    if target == source:
        return ({target: None}, {source: None}, source)

    neighbours = G.adj

    # predecessor and successors in search
    pred = {source: None}
    succ = {target: None}

    # initialize fringes, start with forward
    forwardVisited = [source]
    reverseVisited = [target]

    # We only call this method when we are sure there is a path
    while True:
        if len(forwardVisited) <= len(reverseVisited):
            thisLevel = forwardVisited
            forwardVisited = []
            for currentNode in thisLevel:
                if fulfillsStrictRequirements(G, pro, currentNode):
                    for neighbour in neighbours[currentNode]:
                        if fulfillsStrictRequirements(G, pro, neighbour):
                            if neighbour not in pred:
                                forwardVisited.append(neighbour)
                                pred[neighbour] = currentNode
                            if neighbour in succ:  # path found
                                return pred, succ, neighbour
        else:
            thisLevel = reverseVisited
            reverseVisited = []
            for currentNode in thisLevel:
                if fulfillsStrictRequirements(G, pro, currentNode):
                    for neighbour in neighbours[currentNode]:
                        if fulfillsStrictRequirements(G, pro, neighbour):
                            if neighbour not in succ:
                                reverseVisited.append(neighbour)
                                succ[neighbour] = currentNode
                            if neighbour in pred:  # found path
                                return pred, succ, neighbour


def bidirectionalBFSWithFilter(G, pro):
    # call helper to do the real work
    results = find_predecessors_and_successors(G, pro)
    pred, succ, meetupNode = results

    # build path from pred + meetupNode + succ
    path = []

    # from source to meetupNode
    while meetupNode is not None:
        path.append(meetupNode)
        meetupNode = pred[meetupNode]
    path.reverse()

    # from w to target
    meetupNode = succ[path[-1]]
    while meetupNode is not None:
        path.append(meetupNode)
        meetupNode = succ[meetupNode]

    return path