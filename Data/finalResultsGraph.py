import networkx as nx
import matplotlib.pyplot as plt
import os

#Defines the nodes as 1-148 
nodes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", 
         "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", 
         "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", 
         "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", 
         "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", 
         "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", 
         "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "101", "102", "103", "104", 
         "105", "106", "107", "108", "109", "110", "111", "112", "113", "114", "115", "116", "117", 
         "118", "119", "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", 
         "131", "132", "133", "134", "135", "136", "137", "138", "139", "140", "141", "142", "143", 
         "144", "145", "146", "147", "148"]

#Read edges from each file
def read_edges_from_file(file_path):
    edges = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip().replace('"', '') #Remove quotation marks
            edge_groups = line.split('],[') #Gets each edge pair
            for edge in edge_groups:
                edge = edge.strip('[]') #Remove brackets
                edge = edge.split(',') #Split by comma to get the node pair
                edges.append([int(edge[0].strip()), int(edge[1].strip())]) #Convert to integer form
    return edges

#Function to draw the graph
def draw_graph(graph, pos, fig_num):
    fig, ax = plt.subplots(num=fig_num, figsize=(6, 5), facecolor='none')
    ax.set_facecolor('none')  
    ax.patch.set_alpha(0) 

    nx.draw(graph, pos, with_labels=True, labels={i: nodes[i] for i in graph.nodes()},
            node_color="white", edge_color="black", node_size=200, font_size=7,
            edgecolors="black") #Graph Customizations

    plt.tight_layout()
    plt.show()
    
folder_path = "/Users/reedschubert/Desktop/Data/treeData/NL" 
folder_path2 = "/Users/reedschubert/Desktop/Data/treeData/EMCI" 
fixed_pos = None
fig_num = 1
other_num = 1

for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        edges = read_edges_from_file(file_path) #Gets edges
        
        if edges:
            G = nx.Graph()
            G.add_nodes_from(range(len(nodes)))
            G.add_edges_from(edges)

            #Makes sure the structure of the graph is the same for all graphs
            if fixed_pos is None:
                fixed_pos = nx.fruchterman_reingold_layout(G, seed=42, k=0.8) 

            draw_graph(G, fixed_pos, fig_num)
            fig_num += 1

for file_name in os.listdir(folder_path2):
    file_path2 = os.path.join(folder_path2, file_name)
    if os.path.isfile(file_path2):
        edges2 = read_edges_from_file(file_path2) 
        
        if edges2:
            G = nx.Graph()
            G.add_nodes_from(range(len(nodes)))
            G.add_edges_from(edges2)

            # Makes sure the structure of the graph is the same for all graphs
            if fixed_pos is None:
                fixed_pos = nx.fruchterman_reingold_layout(G, seed=42, k=0.8) 

            draw_graph(G, fixed_pos, other_num)
            other_num += 1

