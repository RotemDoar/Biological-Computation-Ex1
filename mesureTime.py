import timeit
import time
code_file = open("q1.py", "r")
code_file = code_file.read()

print("Enter number of vertices: ", end="")
try:
    N = input()

    code_file = code_file.replace("N = int(input())", "N = " + str(N))
    code_file = code_file.replace("Enter number of nodes", "Execution time")
    print("n = " + str(N))
    print(timeit.timeit(code_file, number=1))
except:
    print("An error occurred :(")