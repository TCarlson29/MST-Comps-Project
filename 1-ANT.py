import math;
import random;
import csv;

#code works by assuming graph is coming in as adjacency matrix
alpha = 1  #weight of pheromones
beta = 1   #weight of edge weights

#optimal for kruskals: a=0, b>=6*wmax*logn

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
    
  
  print(tree)
  print(calcWeight(tree, edges))
  print(len(tree))
  return


#needs to be able to update graph weights 
def runAnt(maxIterations, nodes, edges, phers):

  broderTree = broderUpdate(maxIterations, nodes, edges, phers)
  print("broderDone")

  kruskalTree = kruskalUpdate(maxIterations, nodes, edges, phers)
  print("KruskalDone")

  primTree = primUpdate(maxIterations, nodes, edges, phers)
  print("prim Done")

  deleteTree = deleteConstruction(nodes, edges)
  print("deleteDone")

  print("trees complete")
  # print(deleteTree)
  print("Broder Total edge weight: " + str(calcWeight(broderTree, edges)))
  print("Kruskal Total edge weight: " + str(calcWeight(kruskalTree, edges)))
  print("Prims Total edge weight: " + str(calcWeight(primTree, edges)))
  print("Delete Total edge weight: " + str(calcWeight(deleteTree, edges)))
  # print(len(deleteTree))


# runs iterations of broderConstruct and updates pheromone values
def broderUpdate(maxIterations, nodes, edges, phers):
  i = 0
  broderTree = broderConstruction(nodes, edges, phers)
  bestWeight = calcWeight(broderTree, edges)
  broderBounds = [math.pow(10, -6), 1 / bestWeight]
  # broderBounds = [1, (len(nodes))^3 * 1]
  while (i < maxIterations):
    i += 1
    newTree = broderConstruction(nodes, edges, phers)
    if calcWeight(newTree, edges) <= calcWeight(broderTree, edges):
      #update pheremone values
      for rowIndex in range(len(edges)):
        for colIndex in range(len(edges[rowIndex])):
          if [rowIndex, colIndex] in newTree:
            phers[rowIndex][colIndex] = broderBounds[1]
            phers[colIndex][rowIndex] = broderBounds[1]
          else:
            phers[rowIndex][colIndex] = broderBounds[0]
            phers[colIndex][rowIndex] = broderBounds[0]
      broderTree = newTree
  return broderTree

# runs iterations of kruskalConstruct and updates pheromone values
def kruskalUpdate(maxIterations, nodes, edges, phers):
  i = 0
  kruskalTree = kruskalConstruction(nodes, edges, phers)
  bestWeight = calcWeight(kruskalTree, edges)
  kruskalBounds = [math.pow(10, -6), 1 / bestWeight]
  while (i < maxIterations):
    i += 1
    newTree = kruskalConstruction(nodes, edges, phers)
    # print("new tree made")
    if calcWeight(newTree, edges) <= calcWeight(kruskalTree, edges):
      #update pheremone values
      phers = [[kruskalBounds[0]] * len(edges)] * len(edges)
      for edge in newTree:
        phers[edge[0]][edge[1]] = kruskalBounds[1]
        phers[edge[1]][edge[0]] = kruskalBounds[1]
      kruskalTree = newTree
      # print("better tree found")
  return kruskalTree

# runs iterations of primConstruct and updates pheromone values
def primUpdate(maxIterations, nodes, edges, phers):
  i = 0
  primTree = primConstruction(nodes, edges, phers)
  bestWeight = calcWeight(primTree, edges)
  primBounds = [math.pow(10, -6), 1 / bestWeight] #bounds update with best weight found
  while (i < maxIterations):
    i += 1
    newTree = primConstruction(nodes, edges, phers)
    if calcWeight(newTree, edges) <= bestWeight:
      # print("better tree found")
      bestWeight = calcWeight(primTree, edges)
      primBounds = [math.pow(10, -6), 1 / bestWeight]
      phers = [[primBounds[0]] * len(edges)] * len(edges)
      for edge in newTree:
        phers[edge[0]][edge[1]] = primBounds[1]
        phers[edge[1]][edge[0]] = primBounds[1]

  return primTree

##delete construction doesn't need update rule, also doesn't use iteration

## CONSTRUCTION GRAPHS
def broderConstruction(nodes, edges, phers):

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
      
      # print(math.pow(tau, alpha))
      totalWeight += math.pow(tau, alpha) * math.pow(eta, beta)

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
      totalProb += (math.pow(tau, alpha) * math.pow(eta, beta))/totalWeight

      if (totalProb > num):
        vIndex = edgeIndex
        break
    
    #add neighbor to tree if not visited, change curNode to neighbor
    if nodesVisited[vIndex] == False:
      tree.append([curNodeIndex, vIndex])
      nodesVisited[vIndex] = True
    curNodeIndex = vIndex
  
  return tree

def kruskalConstruction(nodes, edges, phers):
  
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
      weightSum += (math.pow(tau, alpha)) * (math.pow(eta, beta))

    num = random.random()
    totalProb = 0
    #calculate which neighbor to go to
    for edge in posEdges:
      tau = phers[edge[0]][edge[1]]
      eta = 1/edges[edge[0]][edge[1]]
      totalProb += (math.pow(tau, alpha) * math.pow(eta, beta)) / weightSum

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
  
def primConstruction(nodes, edges, phers):
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
            weightSum += (math.pow(tau, alpha)) * (math.pow(eta, beta))

    num = random.random()
    totalProb = 0
    #calculate which neighbor to go to
    for edge in posEdges:
      tau = phers[edge[0]][edge[1]]
      eta = 1 / math.pow(edges[edge[0]][edge[1]], 2)
      totalProb += (math.pow(tau, alpha) * math.pow(eta, beta)) / weightSum

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

  capitals = []
  edges = []


  with open('full-mst-data.csv', mode ='r')as file:
    csvFile = csv.reader(file)
    x = 0
    for lines in csvFile:
      if x == 0:
        x +=1
      else:
        capitals.append(lines[0])
        row = list(map(int, lines[1::]))
        edges.append(row)

  phers = [[1] * len(edges)] * len(edges)

  print("Hello World")


  runAnt(100, capitals, edges, phers)
  print("Optimal: 12148")


if __name__ == "__main__":
  main()