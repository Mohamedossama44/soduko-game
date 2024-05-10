from collections import deque
import numpy as np
import copy
import sys
# FINISH THE BACKEND !!

# Define a function to redirect prints to a file
def print_to_file(*args, **kwargs):
    with open('output.log', 'a') as f:
        print(*args, **kwargs, file=f)

# Redefine the print function to point to our custom function
sys.stdout.write = print_to_file


def is_valid_move(board, row, col, num): # num hna byegoli mn 1 l 9
    # Check if the number is not present in the same row
    if num in board[row]:
        return False
    
    # Check if the number is not present in the same column
    if num in [board[i][col] for i in range(9)]: 
        return False
    
    # Check if the number is not present in the 3x3 subgrid
    subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(subgrid_row, subgrid_row + 3):
        for j in range(subgrid_col, subgrid_col + 3):
            if board[i][j] == num:
                return False
    return True


def SelectunassignedVariableUsingMRV(board):
    min_remaining_values = float('inf')
    selected_cell = None
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                remaining_values = len(get_domain_values(board, i, j))
                if remaining_values < min_remaining_values:
                    min_remaining_values = remaining_values
                    selected_cell = (i, j)
    return selected_cell

def get_all_possible_Arcs_to_x(x): # x is destination

    row, col = x
    subgrid_row = row // 3
    subgrid_col = col // 3

    arcs = []

    # Add row arcs
    for i in range(9):
        if i != col:
            arcs.append((row, i))

    # Add column arcs
    for i in range(9):
        if i != row:
            arcs.append((i, col))

    # Add box arcs
    for i in range(3):
        for j in range(3):
            if (subgrid_row * 3 + i, subgrid_col * 3 + j) != x:
                arcs.append((subgrid_row * 3 + i, subgrid_col * 3 + j))

    return list(set(arcs))

def unary_constraint(board ,domains): 
    for v in domains : 
        row,col = v
        if board[row][col]  != 0 :
            print(f"The domain of cell ({row}, {col}) is reduced to {board[row][col]}.")
            domains[v] = set([board[row][ col]])

def ac_3 (domains, arcs = None) :
        queue = deque(arcs)
        while queue:
            node_Y,node_X = queue.popleft()
            print(f"Processing {node_X} <---- {node_Y} ,Domain of node {node_Y} is {domains[node_Y]}.")

            if revise(node_Y,node_X,domains):  
                if len(domains[node_Y]) == 0:
                    print("From AC-3 We infrom that this path will lead to some CELL with no possible domain to fill it ,wrong path (Try another value (lw lesa for loop mkmla) ,Backtrack(forloop 5lst el values) )")
                    return False
                
                if len(domains[node_Y]) == 1:
                    print(f"Domain of {node_Y} is one value ,we need to add AC constraint.")
                    for nodeY_dash in get_all_possible_Arcs_to_x(node_Y):
                        if nodeY_dash != node_X:
                            print(f"Add to the Queue {nodeY_dash},{node_Y} for AC- check")
                            queue.append((nodeY_dash, node_Y))        
        return True
 
def revise(node_Y,node_X,domains):# x <--- y
        revised = False
        if len(domains[node_X]) == 1 and next(iter( domains[node_X] )) in domains[node_Y] : 
                domains[node_Y].remove(next(iter( domains[node_X] )))
                print(f"Revised: The value {next(iter( domains[node_X] ))} is removed from the domain of node {node_Y}, Now the domain is {domains[node_Y]}.")
                # print(f"Now the domain of {node_Y} is {domains[node_Y]}")
                revised = True
        return revised

def inference(assignment, x, board, domains):
    # We may make inferences from Unary Constraint(NodeConsistency) , Binary Constraint (ArcConsistency)

    print("Applying uniaray constraint.")
    # First make  inference from unaryconstraint (NodeConsistency)
    row,col = x
    print (f"Orginal domain of cell ({row}, {col}) before reduction {domains[x]}.") # PRINT FOR TEST (JORDI)
    domains[x] = set([board[row][ col]])
    print(f"The domain of cell ({row}, {col}) is reduced to {board[row][col]}.")
    # print(row,col)
    # print(domains[x])
    # unary_constraint(board,domains) # DONOT USE THIS FUNCTION (dy ht3di 3l board kolha tani)


    print("Applying Binary constraint.")
    # We may make inferences from  Binary Constraint (ArcConsistency)
    # To make the Binary Constraint we will call AC-3 function with all arcs (y,x)
    # where y is neghibor of x
    # we need to visualize the arcs on the graph
    directed_graph = []
    for y in get_all_possible_Arcs_to_x(x):
        directed_graph.append((y,x))
    # print("len arcs of directed graph") # len hyeb2a 20 , shl atwk3ha lw odami rsma
    # print(len(directed_graph))

    # Run AC-3 algorithm to perform arc consistency (Binary Constraint)
    # akml fel path wla la
    # continue_in_path_or_backtrack
    continue_in_path_or_backtrack = ac_3(domains,directed_graph)
    print (f"End of Binary Constraints, Checks done for cell: ({row},{col}).")

    
    inferences = dict()
    if not continue_in_path_or_backtrack:
        return continue_in_path_or_backtrack, inferences
    
    # Collect inferences for variables with singleton domains
    for variable, domain in domains.items():
        row,col = variable
        if board[row][col]==0  and variable not in assignment and len(domain) == 1:
            print(f"After make inferences we see that the domain of cell {variable} is {domain}")
            value = domain.pop()  # Remove and get the single value in the domain
            inferences[variable] = value
            # Restore the domain (since we popped it for checking)
            domain.add(value)
            # print(f"mfrod ytb3 value ::::::  {domains[variable]}")

    return continue_in_path_or_backtrack, inferences

def backtracking(board):
    variables = [(i, j) for i in range(9) for j in range(9)]
    domains = {v: set(range(1, 10)) for v in variables}

    print("Apply uniary constraint to the Initial Board")
    # Unary Constraint(NodeConsistency) To reduce the domain size 
    unary_constraint(board,domains)

    print("Apply Binary constraint to the Initial Board")
    keys_with_length_one = []
    for key, value in domains.items():
        if len(value) == 1:
            keys_with_length_one.append(key)

    for cell_i in keys_with_length_one:
        directed_graph = []
        cell_row,cell_col=cell_i
        all_possiple_arcs_to_x=get_all_possible_Arcs_to_x(cell_i)
        print(f"All posible arcs to ({cell_row},{cell_col}) are {all_possiple_arcs_to_x}")
        for y in all_possiple_arcs_to_x:
            directed_graph.append((y,cell_i)) # y -> x ,

        test=ac_3(domains, directed_graph)
        if not test:
            # a3tkd ana mmkn mn hna 22ol en test fshl w arg3 false , aaol board mtthlsh
            print("AC-3 failed from the intiall board  the board Is Unsolvable")
            return False,None

    print_boolean =True
    initial_assigments={}
    for variable, domain in domains.items():
        row_in,col_in = variable
        if board[row_in][col_in]==0 and len(domain) == 1:
            if(print_boolean): # to print the followint text only one time
                print(f"Inferences we make before start backtracking:")
                print_boolean=False
            print(f"Put in board in cell :{variable} ,value :{domain}.")

            value_i = domain.pop()  # Remove and get the single value in the domain
            initial_assigments[variable] = value_i
            # Restore the domain (since we popped it for checking)

            board[row_in][col_in]=value_i
            domain.add(value_i)

    print(f"Intiall assigment to board before we start backtrack : {initial_assigments}.")
    
    # for test purpose , a3rf domain bta3 cell mo3ina 
    # print(f"  CERTAIN CELL FYHA  ? {domains[(0, 7)]}")

    domains_copy = copy.deepcopy(domains)

    print (f"Domains : {domains}")

    def inear_backtracking(board,domain_backtrack,assigment={},depth=0):
        #var = Select-unassigned-Variable  (using MRC heuristic)
        empty_cell = SelectunassignedVariableUsingMRV(board)
        print(f"MRV cell is {empty_cell}")
        if empty_cell is None:
            return True,assigment # if complete assigment we will return true


        # Order Domain Values
        row,col = empty_cell
        domain_values = get_domain_values(board, row, col)
        # Applying LCV
        # for each num in domain values we count_constrined_values
        # the numbers with fewer constrained values will appear first in the sorted list
        domain_values.sort(key=lambda num: count_constrained_values(board, row, col, num))

        print(f"Attempting to fill cell ({row}, {col}) with domain values: {domain_values}")

        for num in domain_values:
            print(f"Trying value {num} for cell ({row}, {col}), current depth :{depth}")
            if is_valid_move(board, row, col, num):  
                # backtracking algorithm  do - recursion - undo

                # do operation
                board[row][col] = num  
                assigment [(row,col)]=num

                # optimization step before recursion, using Inference for speed up search
                # b3ml copy , 3shan hghyr f domain bsbb eni h3ml inferences
                copy_of_domain = copy.deepcopy(domain_backtrack)

                ac_inform_us_to_continue,inferences = inference(assigment,(row,col),board,copy_of_domain)
                if ac_inform_us_to_continue :  
                    for key, value in inferences.items():
                        print(f"Adding to board in cell :{key},value :{value}")
                        row5,col5 = key
                        board[row5][col5] = value
                        # add the inferences to the assigment 
                        # 3shan wna bback track ab2a 3rf eni 3ml el assigment da
                        assigment[(row5,col5)] = value

                    # for key, value in inferences.items():
                    #     assignment[key] = value


                    # recusrion operation 
                    # send to backtrack the new domain after inferences
                    print(f"Go deep in the search tree parent cell ({row},{col}) with value {num} ,current depth:{depth}")
                    _ , result = inear_backtracking(board,copy_of_domain,assigment,depth+1)
                    if result:
                        return True ,result
                
                # undo operation
                print(f"Undo operation ,current depth : {depth}.")
                print(f"Remove the assigment from the board ,({(row)},{(col)})=0.")
                # Undo the assigment
                board[row][col] = 0 

                if(ac_inform_us_to_continue):
                    print (f"Inference items :{inferences.items()}")
                    print (f"Remove the inferences from the board")
                # undo the Inferences if found
                else :
                    print(f"No inferences made from cell ({row},{col}) to remove it.")
                for key, value in inferences.items():
                    row1,col1=key
                    print(f"Undo the thing that inference tell us, make cell ({(row1)},{(col1)})=0 ")
                    board[row1][col1] = 0
                
                del assigment[(row, col)]
                assigment = {k : v for k, v in assigment.items() if k not in inferences}
       
                
        print(f"Backtracking... No valid value found for cell ({row}, {col}) , current depth: {depth}.")
        return False,None
    

    print ("Start of backtracking")
    return inear_backtracking(board,domains_copy,initial_assigments)

def get_domain_values(board, row, col):
    domain_values = [num for num in range(1, 10) if is_valid_move(board, row, col, num)]
    return domain_values

def count_constrained_values(board, row, col, num): 
    # row w col w num , dy l cell l hl3bh fyha w num da l rkml l hl3bo
    # num da bykon gy mn domain values
    count = 0
    for i in range(9):
        if i != col and not is_valid_move(board, row, i, num):
            count += 1
        if i != row and not is_valid_move(board, i, col, num):
            count += 1

    for i in range(row - row % 3, row - row % 3 + 3):
        for j in range(col - col % 3, col - col % 3 + 3):
            if (i != row or j != col) and not is_valid_move(board, i, j, num):
                count += 1
    return count




##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################
##################################################

# ForGUI , FUNCTIONS

def validate_sudoku(grid):
    # Create a copy of the puzzle
    copy_grid = np.copy(grid)
    # Attempt to solve the puzzle using backtracking
    is_valid, _ = backtracking(copy_grid)
    return is_valid

       
def generate_random_puzzle():
    print("Generate random board")
    # Create an empty Sudoku grid
    grid = np.zeros((9, 9), dtype=int)

    # Fill random places of the puzzle
    for _ in range(np.random.randint(12, 25)):  # Adjust the range for puzzle difficulty
        row, col, num = np.random.randint(9, size=3)
        while not is_valid_move(grid, row, col, num + 1) : # to ensure that the generated soduko is solvable
            row, col, num = np.random.randint(9, size=3)
        grid[row][col] = num + 1

    solvable,_=backtracking(copy.deepcopy(grid))# only check backtracking one time at end , we donot check it every time to not make delay
    if not solvable:
        print("Genration failed , Try new gnration")
        return generate_random_puzzle()
    
    print("Generation done")
    return grid





#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
#################################################################
def print_sudoku(puzzle):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            print(puzzle[i, j] if puzzle[i, j] != 0 else ".", end=" ")
        print() 

# puzzle = np.array([
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 9]
# ])

# puzzle = np.array([
#     [5, 3, 0, 0, 7, 0, 0, 0, 0],
#     [6, 0, 0, 1, 9, 5, 0, 0, 0],
#     [0, 9, 8, 0, 0, 0, 0, 6, 0],
#     [8, 0, 0, 0, 6, 0, 0, 0, 3],
#     [4, 0, 0, 8, 0, 3, 0, 0, 1],
#     [7, 0, 0, 0, 2, 0, 0, 0, 6],
#     [0, 6, 0, 0, 0, 0, 2, 8, 0],
#     [0, 0, 0, 4, 1, 9, 0, 0, 5],
#     [0, 0, 0, 0, 8, 0, 0, 7, 9]
# ])

# puzzle = np.array([
#     [1, 2, 3, 4, 5, 6, 7, 8, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0]
# ])


# puzzle = np.array([
#     [2, 1, 5, 3, 4, 6, 7, 0, 9],
#     [8, 0, 0, 0, 0, 0, 0, 2, 0],
#     [0, 7, 0, 0, 1, 0, 5, 0, 0],
#     [4, 0, 0, 0, 0, 5, 3, 0, 0],
#     [0, 1, 0, 0, 7, 0, 0, 0, 6],
#     [0, 0, 3, 2, 0, 0, 0, 0, 0],
#     [0, 6, 0, 5, 0, 0, 0, 0, 9],
#     [0, 0, 4, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 9, 7, 0, 0]
# ])



# #  jordi test puzzle
# puzzle = np.array([
# [0, 0, 0, 7, 0, 0, 0, 0, 4],
#  [0, 0, 2, 1, 0, 9, 6, 3, 0],
#  [0, 0, 0, 0, 0, 4, 7, 1, 2],
#  [0, 0, 0, 0, 1, 0, 0, 0, 0],
#  [0, 0, 1, 0, 7, 0, 0, 8, 6],
#  [5, 0, 7, 0, 0, 0, 0, 0, 0],
#  [0, 3, 6, 0, 2, 0, 0, 4, 9],
#  [0, 0, 4, 3, 0, 0, 1, 0, 0],
#  [1, 0, 0, 9, 0, 7, 0, 6, 0]]
# )

# solvable , solution = backtracking(puzzle)

# # print(solution)
# # print(puzzle)
# if solvable:
#     print("Solution:")
#     print_sudoku(puzzle)
# else:
#     print("No solution exists.")