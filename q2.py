import itertools
import numpy as np

import q1

# function that takes the input of edges in string form and converts it to adjacency matrix.
def ConvertGraphToMatrixForm(n, edges):
    if edges != "": # if there is at least on edge
        edges = edges.split(",")
        edges = [e.split(" ") for e in edges]
        edges = [[int(v1) - 1, int(v2) - 1] for v1, v2 in edges]

    matrix = np.zeros((n, n)).astype(int)
    for v1, v2 in edges:
        matrix[v1][v2] = 1

    return matrix

# function that gets 2 lists and apply bitwise AND. Return list of the result
def AND2Lists(l1, l2):
    return [str(int(x) and int(y)) for x, y in zip(l1, l2)]

# function that gets the input graph G, and the motifs options, G_motifs, and count number of occurences
# of each motif in the input graph.
def FindNumberOfMotifs(G, G_motifs, n):
    numOfMotifs = len(G_motifs)
    G = list(np.array(G).reshape(-1).astype(str))
    counter = np.zeros(numOfMotifs).astype(int)

    # there is no motifs for only 1 vertex
    if n == 1:
        return counter

    # get all permutations of naming the vertices by indices
    all_perm = list(map(list, itertools.product(range(n), repeat=n)))
    all_perm = [m for m in all_perm if len(set(m)) == n]

    # iterate over each motif
    for i in range(len(G_motifs)):
        m = G_motifs[i]
        lst_matrix = np.matrix([m[j:(n + j)] for j in range(0, n * n, n)])  # convert motif to numpy matrix form
        visited_types_of_motif = []

        # for each option to label the vertices
        for p in all_perm:
            l = np.copy(lst_matrix)
            # swap labels to the current option of labeling
            l[range(n)] = l[p]
            l[:, range(n)] = l[:, p]
            l = list(np.array(l).reshape(-1).astype(str))  # convert matrix back to array

            # check if already checked the current motif with other labeling
            if ''.join(l) in visited_types_of_motif:
                continue

            visited_types_of_motif.append(''.join(l))
            # check if the motif is in the input graph
            if AND2Lists(l, G) == l:
                counter[i] += 1

    return counter

# function that saves the results to txt file according to the appropriate format.
def SaveResultsToFile(results:list, motifsCounter, n):
    f = open("./q2_results/n=" + str(n) + ".txt", "w")
    f.writelines(["n="+str(n) + "\n", "count=" + str(len(results)) + "\n"])

    for i in range(len(results)):
        f.writelines(["#" + str(i + 1) + "\n", "count=" + str(motifsCounter[i]) + "\n"])
        for j in range(n):
            row_connections = []
            for k in range(n):
                if results[i][j*n + k] == 1:
                    row_connections.append(str(j + 1) + " " + str(k + 1) + "\n")
            f.writelines(row_connections)

if __name__ == "__main__":
    try: # check errors
        print("Enter number of vertices: ", end="")
        N = int(input())
        if N < 1:
            print("The number of vertices need to be positive!")
            exit(-1)

        print("Enter edges ('a b,c d,...'): ", end="")
        edges = input().replace(", ", ",").replace(" ,", ",")
        G_matrix = ConvertGraphToMatrixForm(N, edges)

        a = q1.Permutations(N) # get all graphs with n nodes and without self loops
        b = q1.RemoveUnConnectedGraphs(N, a) # get all graphs with n nodes and without self loops and connected graphs
        c = q1.RemoveNames(b, N) # get all graphs with n nodes and without self loops and connected graphs and uniques

        motifsCounter = FindNumberOfMotifs(G_matrix, c, N)
        SaveResultsToFile(c, motifsCounter, N)

        ######################################### For drawing the input graph #########################################
        # For drawing, remove the comments below this row

        # import networkx
        # import matplotlib.pyplot as plt
        # import math
        #
        # nx_drawer = networkx.from_numpy_matrix(G_matrix, False, networkx.DiGraph)
        # nx_drawer = networkx.relabel_nodes(nx_drawer, {i:i+1 for i in range(N)})
        # networkx.draw_networkx(nx_drawer)
        # plt.axis('off')
        # plt.plot()
        # plt.show()
    except:
        print("Wrong input!")