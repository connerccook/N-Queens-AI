from geneticAlgo import *
from NQueens import *
from utils import *

board = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]
]

board = [
    [0,0,0,0], 
    [0,0,0,0], 
    [0,0,0,0], 
    [0,0,0,0]
    ]

if __name__ == "__main__":
    solution = (7, 3, 0, 2, 5, 1, 6, 4)
    n = 4
    nqp = NQueensProblem(n)
    solution = genetic_search(nqp)
    print(solution)
    
    #7 will be row 1 column 0
    #3 will be row 5 column 1
    #0 will be row 8 column 2
    # (n-1) - node = row 
    # index of solution = column 

    for idx, val in enumerate(solution):
        row = (n-1) - val 
        column = idx
        board[row][column] = 1
    for row in board:
        print(row)

