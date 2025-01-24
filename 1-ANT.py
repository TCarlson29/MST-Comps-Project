import math;

#code works by assuming graph is coming in as adjacency list

#needs to be able to update graph weights 
def runAnt(numIterations, nodes, edges):
  i = 0
  curTree = 0 #TODO: implement random walk init
  while (i < numIterations):
    i += 1
    newTree = pathConstruction(nodes, edges)
    if calcWeight(newTree) <= calcWeight(curTree):
      #update pheremone values
      curTree = newTree


  print("Recalculating pheremones...")

#input: needs to be able to navigate full graph G with weights and everything else
def pathConstruction(nodes, edges):

  #init variables and start node
  tree = []
  nodesVisited = [False] * len(nodes)
  curNodeIndex = 0
  nodesVisited[0] = True

  while (False in nodesVisited):
    totalWeight = 0
    for edge in edges:

      #TODO
      #add pheremone value and 1/w value to totalWeight
      totalWeight += 1

    #TODO
    #choose neighbor v based on prob value
    vIndex = 1

    if nodes[vIndex] == False:
      tree.append((0, 1)) #add edge to tree
      nodes[vIndex] = True
    curNodeIndex = vIndex
  
  return tree

#BIG TODO's:
# make calcWeight function
# find way to store pheremone and edge weights
# implement randomWalk for init
# finish equations

def calcWeight(tree):
  #sum all weights from given collection of edges
  return 0


def main():
  print("Hello World")
  pathConstruction([0, 1, 2], [])


if __name__ == "__main__":
  main()