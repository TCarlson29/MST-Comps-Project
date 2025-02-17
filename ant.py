import math, random
import csv, sys
from time import process_time


broderOpts = []
primOpts = []
kruskalOpts = []

broderTime = []
primTime = []
kruskalTime = []

#code works by assuming graph is coming in as adjacency matrix

# curOptimal = 12148
maxTime = 30
maxIterations = 200

#actual running of prims to test optimality
def truePrims(nodes, edges):
  seenNodes = [False] * len(nodes)
  seenNodes[0] = True
  tree = []

  while (False in seenNodes):
    oldNodeIndex = None
    newNodeIndex = None
    smallestEdge = 10000000000
    for i in range(len(nodes)):
      if seenNodes[i] == True:
        for j in range(len(edges[i])):
          if edges[i][j] < smallestEdge and edges[i][j] != 0 and seenNodes[j] == False:
            newNodeIndex = j
            oldNodeIndex = i
            smallestEdge = edges[i][j]
            # print(newNodeIndex)

    # print(newNodeIndex)
    tree.append([oldNodeIndex, newNodeIndex])
    seenNodes[newNodeIndex] = True
    
  
  # print(tree)
  # print(calcWeight(tree, edges))
  # print(len(tree))
  return calcWeight(tree, edges)


#needs to be able to update graph weights 
def runAnt(nodes, edges, phers, ratios):
  curOptimal = truePrims(nodes, edges)

  #RATIOS ARE REPRESENTATIONS OF PHER/EDGE WEIGHTING FOR ACO's
  # first value = pher weight
  # second value = edge weight weight
  broderRatios = [0, 1]
  kruskRatios = [0, 6]
  primRatios = [1, 5]
  if len(ratios) != 0:
    broderRatios = ratios
    kruskRatios = ratios
    primRatios = ratios
  
  brodStart = process_time()
  broderTree = broderUpdate(nodes, edges, phers, broderRatios)
  brodEnd = process_time()
  print("broderDone")
  print("brod total time elapsed: " + str(brodEnd - brodStart))

  kruskStart = process_time()
  kruskalTree = kruskalUpdate(nodes, edges, phers, kruskRatios)
  kruskEnd = process_time()
  print("KruskalDone")
  print("krusk total time elapsed: " + str(kruskEnd - kruskStart))

  primStart = process_time()
  primTree = primUpdate(nodes, edges, phers, primRatios)
  primEnd = process_time()
  print("prim Done")
  print("prim total time elapsed: " + str(primEnd - primStart))

  deleteStart = process_time()
  deleteTree = deleteConstruction(nodes, edges)
  deleteEnd = process_time()
  print("deleteDone")
  print("delete total time elapsed: " + str(deleteEnd - deleteStart))


  print("trees complete\n\n")
  brodWeight = calcWeight(broderTree, edges)
  print("Broder Total tree weight: " + str(brodWeight))
  print("Broder Optimality Ratio: " + str(brodWeight / curOptimal))
  # print("Broder # of edges: " + str(len(broderTree)))
  kruskWeight = calcWeight(kruskalTree, edges)
  print("Kruskal Total tree weight: " + str(kruskWeight))
  print("Broder Optimality Ratio: " + str(kruskWeight / curOptimal))
  # print("Kruskal # of edges: " + str(len(kruskalTree)))
  primWeight = calcWeight(primTree, edges)
  print("Prims Total tree weight: " + str(primWeight))
  print("Broder Optimality Ratio: " + str(primWeight / curOptimal))
  # print("Prims # of edges: " + str(len(primTree)))
  deleteWeight = calcWeight(deleteTree, edges)
  print("Delete Total tree weight: " + str(deleteWeight))
  print("Broder Optimality Ratio: " + str(deleteWeight / curOptimal))
  # print("Delete # of edges: " + str(len(deleteTree)))
  # print(len(deleteTree))

  return [[broderOpts, kruskalOpts, primOpts, curOptimal], deleteWeight, [broderTime, kruskalTime, primTime]]


# runs iterations of broderConstruct and updates pheromone values
def broderUpdate(maxIterations, nodes, edges, phers, ratios):
  i = 0
  start = process_time()
  broderTree = broderConstruction(nodes, edges, phers, ratios)
  end = process_time()
  # broderTime.append(end - start)
  bestWeight = calcWeight(broderTree, edges)
  broderBounds = [math.pow(10, -6), 1 / bestWeight]
  # broderBounds = [1, (len(nodes))^3 * 1]
  while (i < maxIterations):
    i += 1
    broderTime.append(end - start)
    # if broderTime[-1] > maxTime:
    #   break
    broderOpts.append(bestWeight)
    newTree = broderConstruction(nodes, edges, phers, ratios)
    end = process_time()
    newWeight = calcWeight(newTree, edges)
    # broderTime.append(end - start)
    if newWeight <= bestWeight:
      bestWeight = newWeight
      phers = [[broderBounds[0]] * len(edges)] * len(edges)
      for edge in newTree:
        phers[edge[0]][edge[1]] = broderBounds[1]
        phers[edge[1]][edge[0]] = broderBounds[1]
      broderTree = newTree
  return broderTree

# runs iterations of kruskalConstruct and updates pheromone values
def kruskalUpdate(maxIterations, nodes, edges, phers, ratios):
  i = 0
  start = process_time()
  kruskalTree = kruskalConstruction(nodes, edges, phers, ratios)
  end = process_time()
  # kruskalTime.append(end - start)
  bestWeight = calcWeight(kruskalTree, edges)
  kruskalBounds = [math.pow(10, -6), 1 / bestWeight]
  while (i < maxIterations):
    kruskalOpts.append(bestWeight)
    kruskalTime.append(end - start)
    i += 1
    newTree = kruskalConstruction(nodes, edges, phers, ratios)
    end = process_time()
    newWeight = calcWeight(newTree, edges)
    # print("new tree made")
    if newWeight <= bestWeight:
      #update pheremone values
      bestWeight = newWeight
      kruskalBounds = [math.pow(10, -6), 1 / bestWeight]
      phers = [[kruskalBounds[0]] * len(edges)] * len(edges)
      for edge in newTree:
        phers[edge[0]][edge[1]] = kruskalBounds[1]
        phers[edge[1]][edge[0]] = kruskalBounds[1]
      kruskalTree = newTree
      # print("better tree found")
  return kruskalTree

# runs iterations of primConstruct and updates pheromone values
def primUpdate(maxIterations, nodes, edges, phers, ratios):
  i = 0
  start = process_time()
  primTree = primConstruction(nodes, edges, phers, ratios)
  end = process_time()
  # primTime.append(end - start)
  bestWeight = calcWeight(primTree, edges)
  primBounds = [math.pow(10, -6), 1 / bestWeight] #bounds update with best weight found
  while (i < maxIterations):
    primOpts.append(bestWeight)
    primTime.append(end - start)
    i += 1
    newTree = primConstruction(nodes, edges, phers, ratios)
    end = process_time()
    newWeight = calcWeight(newTree, edges)
    if newWeight <= bestWeight:
      # print("better tree found")
      bestWeight = newWeight
      primBounds = [math.pow(10, -6), 1 / bestWeight]
      phers = [[primBounds[0]] * len(edges)] * len(edges)
      for edge in newTree:
        phers[edge[0]][edge[1]] = primBounds[1]
        phers[edge[1]][edge[0]] = primBounds[1]

  return primTree

##delete construction doesn't need update rule, also doesn't use iteration


## CONSTRUCTION GRAPHS
def broderConstruction(nodes, edges, phers, ratios):

  #init variables and start node
  tree = []
  nodesVisited = [False] * len(nodes)
  curNodeIndex = random.randrange(0, len(nodes)-1)
  nodesVisited[curNodeIndex] = True

  while (False in nodesVisited):
    totalWeight = 0

    #get all edges that connect to curNode
    for edgeIndex in range(len(edges[curNodeIndex])):
      tau = phers[curNodeIndex][edgeIndex]
      if (edges[curNodeIndex][edgeIndex] == 0):
        continue
      eta = 1/edges[curNodeIndex][edgeIndex]
      
      totalWeight += math.pow(tau, ratios[0]) * math.pow(eta, ratios[1])

    #choose neighbor v based on prob value
    num = random.random()
    totalProb = 0
    vIndex = 0
    #calculate which neighbor to go to
    for edgeIndex in range(len(edges[curNodeIndex])):
      tau = phers[curNodeIndex][edgeIndex]
      if (edges[curNodeIndex][edgeIndex] == 0):
        continue
      eta = 1/edges[curNodeIndex][edgeIndex]
      totalProb += (math.pow(tau, ratios[0]) * math.pow(eta, ratios[1]))/totalWeight

      if (totalProb > num):
        vIndex = edgeIndex
        break
    
    #add neighbor to tree if not visited, change curNode to neighbor
    if nodesVisited[vIndex] == False:
      tree.append([curNodeIndex, vIndex])
      nodesVisited[vIndex] = True
    curNodeIndex = vIndex
  
  return tree

def kruskalConstruction(nodes, edges, phers, ratios):
  
  #start without an edge
  curEdge = [-1, -1]
  curTree = []
  k = 0
  unionImplement = [0 + i for i in range(len(nodes))]

  posEdges = calcPossibleEdges(edges, curTree, unionImplement)

  while posEdges:
    weightSum = 0
    for edge in posEdges:
      tau = phers[edge[0]][edge[1]]
      eta = 1/edges[edge[0]][edge[1]]
      weightSum += (math.pow(tau, ratios[0])) * (math.pow(eta, ratios[1]))

    num = random.random()
    totalProb = 0
    #calculate which neighbor to go to
    for edge in posEdges:
      tau = phers[edge[0]][edge[1]]
      eta = 1/edges[edge[0]][edge[1]]
      totalProb += (math.pow(tau, ratios[0]) * math.pow(eta, ratios[1])) / weightSum

      if (totalProb > num):
        # print('newedge')
        # print(unionImplement)
        # print("edge added: " + str(edge))
        curTree.append(edge)
        union(edge, unionImplement)
        # print(unionImplement)
        break
    posEdges = calcPossibleEdges(edges, curTree, unionImplement)
    k += 1

  # print(calcWeight(curTree, edges))
  return curTree
  # print(curTree)
  # print(len(curTree))
  
def primConstruction(nodes, edges, phers, ratios):
  seenNodes = [False] * len(nodes)
  seenNodes[random.randrange(len(nodes)-1)] = True
  curTree = []

  while False in seenNodes:
    weightSum = 0
    posEdges = []
    for seen in range(len(seenNodes)):
      if seenNodes[seen] == True:
        for new in range(len(edges[seen])):
          if seenNodes[new] == False:
            tau = phers[seen][new]
            eta = 1 / math.pow(edges[seen][new], 2)
            posEdges.append([seen, new])
            weightSum += (math.pow(tau, ratios[0])) * (math.pow(eta, ratios[1]))

    num = random.random()
    totalProb = 0
    #calculate which neighbor to go to
    for edge in posEdges:
      tau = phers[edge[0]][edge[1]]
      eta = 1 / math.pow(edges[edge[0]][edge[1]], 2)
      totalProb += (math.pow(tau, ratios[0]) * math.pow(eta, ratios[1])) / weightSum

      if (totalProb > num):
        # print("added edge")
        curTree.append(edge)
        seenNodes[edge[1]] = True
        break

  return curTree

def deleteConstruction(nodes, edges):
  curTree = []
  totalWeight = 0
  for row in edges:
    for edge in row:
      totalWeight += edge
  totalWeight /= 2
  # edgeProbs = [0] * len(edges) * len(edges)
  calcSum = 0
  for row in range(len(edges)):
    for col in range(row+1, len(edges)):
      calcSum += (totalWeight - edges[row][col])

  #need dict for probs to be able to sort and re-find edges
  edgeProbs = {}
  for row in range(len(edges)):
    for col in range(row+1, len(edges)):
      edgeProbs[(row, col)] = (totalWeight - edges[row][col]) / calcSum

  # print(len(edgeProbs))
  sortedEdgeProbs = dict(sorted(edgeProbs.items(), key = lambda ele: ele[1], reverse=True))
  numDeletedEdges = (len(nodes) * (len(nodes)-1) / 2) - len(nodes) + 1

  curTree = sortedEdgeProbs.copy()
  while (numDeletedEdges > 0):
    # removes the first nth worst edges
    curTree.popitem()
    # print(len(curTree))
    numDeletedEdges -= 1

  unusedEdges = {k:v for k,v in sortedEdgeProbs.items() if k not in curTree} ##stackoverflow solution
  # print(unusedEdges)

  #SECTION 2
  #Adding enough edges to make a full tree
  visited = [False] * len(nodes)
  curVis = isConnected(curTree, 0, nodes, visited)
  # print(curVis)
  while False in curVis:
    # print("still False")
    numFalse = curVis.count(False)
    # print(numFalse)
    tempTree = curTree.copy()
    addedEdges = {}
    for edge in unusedEdges:
      tempTree = curTree.copy()
      tempTree.update({edge: unusedEdges[edge]})
      newVis = isConnected(tempTree, 0, nodes, visited)
      newNumFalse = newVis.count(False)
      if newNumFalse < numFalse:
        curTree.update({edge: unusedEdges[edge]})
        addedEdges.update({edge: unusedEdges[edge]})
        curVis = newVis
    unusedEdges = {k:v for k,v in unusedEdges.items() if k not in addedEdges}

  #SECTION 3
  # Removing all redundant edges from the tree
  curTree = dict(sorted(curTree.items(), key = lambda ele: ele[1]))
  deletedTree = curTree.copy()

  for edge in curTree:
    visited = [False] * len(nodes)
    tempTree = deletedTree.copy()
    tempTree.pop(edge)
    newVis = isConnected(tempTree, 0, nodes, visited)
    # print(newVis)
    if False in newVis:
      # print("false")
      continue
    else:
      deletedTree.pop(edge)
      # print(len(deletedTree))

  curTree = deletedTree
  return curTree



#helper function for kruskalConstruct
def calcPossibleEdges(edges, tree, unionImplement):
  posEdges = []

  #add edges to possible edges if:
  #   the aren't already in the tree
  #   they won't form a cycle with the current tree on the graph
  for row in range(len(edges)):
    for col in range(len(edges)):
      if edges[row][col] == 0:
        continue
      if ([row, col] not in tree) and ([col, row] not in tree):
        if noCycle([row, col], unionImplement):
          posEdges.append([row, col])

  return posEdges

#calculates if added edge would form a cycle (kruskal)
def noCycle(newEdge, unionImplement):
  if (find(newEdge[0], unionImplement) == find(newEdge[1], unionImplement)):
    return False
  return True

#check if graph is connected
#returns a list of seen nodes (DFS)
def isConnected(tree, curNode, nodes, visited):
  # visited = [False] * len(nodes)
  visited[curNode] = True
  # print(tree.)

  for edge in tree.keys():
    if curNode in edge:
      if not visited[edge[1]]:
        visited = isConnected(tree, edge[1], nodes, visited)
      if not visited[edge[0]]:
        visited = isConnected(tree, edge[0], nodes, visited)

  return visited


#Union-Find implementation
def find(x, unionImplement):
  while (x != unionImplement[x]):
    x = unionImplement[x]
  return x

def union(edge, unionImplement):
  rootX = find(edge[0], unionImplement)
  rootY = find(edge[1], unionImplement)
  unionImplement[rootX] = rootY
  return unionImplement

#BIG TODO's:
# visuals to compare methods
# GraphViz

def calcWeight(tree, edges):
  #sum all weights from given collection of edges
  totalWeight = 0
  for edge in tree:
    totalWeight += edges[edge[0]][edge[1]]
  return totalWeight


def main():

  ratios = []
  n = len(sys.argv)
  if (n == 3):
    print("Custom run initiated")
    print("Alpha value: " + sys.argv[1])
    print("Beta value: " + sys.argv[2])
    ratios = [int(sys.argv[1]), int(sys.argv[2])]

  nodes = []
  edges = []
  with open('full-mst-data.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    x = 0
    for lines in csvFile:
      if x == 0:
        x +=1
      else:
        nodes.append(lines[0])
        row = list(map(int, lines[1::]))
        edges.append(row)
  phers = [[1] * len(edges)] * len(edges)
  print("Begin program")

  numIterations = 200
  # runAnt(numIterations, nodes, edges, phers, ratios)
  # print("Optimal: " + str(truePrims(nodes, edges)))
  print("Number of iterations: " + str(numIterations))


if __name__ == "__main__":
  main()