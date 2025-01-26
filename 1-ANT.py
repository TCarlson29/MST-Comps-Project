import math;
import random;
import csv;

#code works by assuming graph is coming in as adjacency matrix
alpha = 1
beta = 1

#needs to be able to update graph weights 
def runAnt(maxIterations, nodes, edges, phers):
  i = 0
  lowBound = 1
  highBound = (len(nodes))^3 * lowBound

  curTree = pathConstruction(nodes, edges, phers)
  while (i < maxIterations):
    i += 1
    newTree = pathConstruction(nodes, edges, phers)
    if calcWeight(newTree, edges) <= calcWeight(curTree, edges):
      #update pheremone values
      for rowIndex in range(len(edges)):
        for colIndex in range(len(edges[rowIndex])):
          if [rowIndex, colIndex] in newTree:
            phers[rowIndex][colIndex] = highBound
          else:
            phers[rowIndex][colIndex] = lowBound
      curTree = newTree

  # print("tree complete")
  print(curTree)
  # print(len(curTree))

#input: needs to be able to navigate full graph G with weights and everything else
def pathConstruction(nodes, edges, phers):

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

    #TODO
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

#BIG TODO's:
# make calcWeight function
# find way to store pheremone and edge weights
# implement randomWalk for init
# finish equations

def calcWeight(tree, edges):
  #sum all weights from given collection of edges
  totalWeight = 0
  for edge in tree:
    totalWeight += edges[edge[0]][edge[1]]
  return totalWeight


def main():

  capitals = []
  edges = []
  phers = [[1] * 50] * 50


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

  print("Hello World")
  # print(capitals)
  # print(edges[5])
  # print(len(phers))
  # print(len(phers[0]))

  runAnt(200, capitals, edges, phers)


if __name__ == "__main__":
  main()