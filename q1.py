import itertools
import numpy as np

# this function returns all possibilities to graph with n nodes without self loops that represented by adjacency matrix.
# the results include non connected graphs and isometric graphs.
def Permutations(n):
    # ask if okay to use built in permutations function
    # get all possibilities of adjacency matrix that represents a graph without self loops
    lst = list(map(list, itertools.product([0, 1], repeat=(n*(n-1)))))

    # insert 0 in the diagonal of each matrix to avoid self loops
    for i in range(len(lst)):
        for j in range(n):
            lst[i].insert(j + n * j,0)

    return lst

def DFS_header(g_matrix, n):
    visited_vertices = {k:False for k in range(n)}
    count = 0
    for i in range(n):
        if count == 1 and visited_vertices[i] != True:
            return 0

        if visited_vertices[i] != True:
            DFS(visited_vertices, i, g_matrix, n)
            count += 1

    return count

def DFS(visited_vertices, v, g_matrix, n):
    visited_vertices[v] = True
    row_i = g_matrix[v*n:(v*n+n)]
    for j in range(len(row_i)):
        if row_i[j] == 1 and visited_vertices[j] == False:
            DFS(visited_vertices, j, g_matrix, n)

# this function removes all graphs that not connected.
def RemoveUnConnectedGraphs(n, G_all:list):
    # remove graphs that their number of edges small than v - 1 (non connected for sure)
    lst = []
    for i in range(len(G_all)):
        if sum(G_all[i]) >= n - 1:
            lst.append(G_all[i])
    G_all = list(lst)

    # build undirected graph and run DFS over each graph for number of components and remove all graphs
    # with number of components != 1 (checks if the graph is a connected graph).
    lst = []
    for i in range(len(G_all)):
        temp = [G_all[i][j:(n + j)] for j in range(0,n * n, n)] # convert array of graph to matrix form
        temp = np.array(np.maximum(np.matrix(temp), np.matrix(temp).transpose())).reshape(-1) # convert to undirected
        if DFS_header(temp, n) == 1: # run DFS and check connectivity
            lst.append(G_all[i])

    return list(lst)

# this function removes all isometric graphs and output only unique graphs (motifs).
def RemoveNames(G_all:list, n):
    G_lst = []
    if n == 1:
        return G_lst

    G_all_it = list(G_all)
    # get all permutations of naming the vertices by indices
    all_perm = list(map(list, itertools.product(range(n), repeat=n)))
    all_perm = [m for m in all_perm if len(set(m)) == n]

    for i in range(len(G_all)): # for each graph
        lst_matrix = np.matrix([G_all[i][j:(n + j)] for j in range(0,n * n, n)]) # convert to numpy matrix form
        inside = False

        # for each option to label the vertices
        for p in all_perm:
            l = np.copy(lst_matrix)
            # swap labels to the current option of labeling
            l[range(n)] = l[p]
            l[:, range(n)] = l[:, p]

            l = list(np.array(l).reshape(-1)) # convert matrix back to array

            # if our new labeling of the current graph is exist in the graphs, we need to remove it
            if l in G_all_it and l != G_all[i]:
                inside = True
                break
        # check if the graph is a unique
        if inside == False:
            G_lst.append(G_all[i])
        else:
            G_all_it.remove(G_all[i])

    return G_lst

# function that saves the results to txt file according to the appropriate format.
def SaveResultsToFile(results:list, n):
    f = open("./q1_results/n=" + str(n) + ".txt", "w")
    f.writelines(["n="+str(n) + "\n", "count=" + str(len(results)) + "\n"])

    for i in range(len(results)):
        f.writelines(["#" + str(i + 1) + "\n"])
        for j in range(n):
            row_connections = []
            for k in range(n):
                if results[i][j*n + k] == 1:
                    row_connections.append(str(j + 1) + " " + str(k + 1) + "\n")
            f.writelines(row_connections)


######################################################### main #########################################################
if __name__ == "__main__":
    print("Enter number of nodes: ", end="")

    # check errors
    try:
        N = int(input())
    except:
        print("Wrong Type of input!")
        exit(-1)

    if N < 1:
        print("The number of vertices need to be positive!")
        exit(-1)

    a = Permutations(N) # get all graphs with n nodes and without self loops
    b = RemoveUnConnectedGraphs(N, a) # get all graphs with n nodes and without self loops and connected graphs
    c = RemoveNames(b, N) # get all graphs with n nodes and without self loops and connected graphs and uniques
    SaveResultsToFile(c, N) # save graphs to file in the appropriate format

    ############################################# For drawing the sub graphs #############################################
    # For drawing, remove the comments below this row

    # import networkx
    # import matplotlib.pyplot as plt
    # import math
    #
    # c_matrices = [networkx.from_numpy_matrix(np.array(m).reshape(N, N), False, networkx.DiGraph) for m in c]
    #
    # for i in range(len(c_matrices)):
    #     plt.subplot(math.ceil(math.sqrt(len(c_matrices))) + 1, math.floor(math.sqrt(len(c_matrices))) + 1, i + 1)
    #     networkx.draw_networkx(c_matrices[i], with_labels=False)
    #     plt.axis('off')
    #     plt.plot()
    #
    # plt.axis('off')
    # plt.plot()
    # plt.show()