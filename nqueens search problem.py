from simpleai.search import SearchProblem, breadth_first, uniform_cost, depth_first, limited_depth_first, iterative_limited_depth_first, greedy, astar, hill_climbing, hill_climbing_random_restarts, genetic
from simpleai.search.viewers import BaseViewer
import random
import math
import time

#class definition for NQueens
class NQueens():
    """ class constructor
    initializes the instance attributes N and state """
    def __init__(self, N):
        self.N = N
        self.set_state()

    """ returns a formatted string
    that represents the instance """        
    def __str__(self):
        return f"N: {self.N}, state: {self.state}"

    """ Sets the instance attribute state by displaying 
    a menu to the user. The user either enters the state 
    manually or prompts the system to generate a random state.
    Check if the input state is a valid state. """         
    def set_state(self):
        while True :
            selection = int(input("How do you want to set state? \n" +
                "1. Set state manually \n" +
                "2. Set state randomly \n" +
                "Enter selection: "))

            if selection == 1 :
                state = input("enter state: ")
                if self._is_valid(state) :
                    self.state = state
                    break
                else :
                    print("invalid state! try again")
        
            if selection == 2 :
                self.state = self.generate_random_state()
                break

    """ generates and returns a valid random state """
    def generate_random_state(self):
        state = ""
        for x in range(self.N):
            state += str(random.randint(1,self.N))
        return state
    
    """ This is an internal function that takes a state_str as input
    and return if this is a valid state or not """
    def _is_valid(self,state_str):
        if not str.isdigit(state_str):
            return False
        
        if not len(state_str) == self.N:
            return False
        
        for digit in state_str:
            if int(digit) < 1 or int(digit) > self.N :
                return False

        return True

    """ This is the primary function of this class.
    It returns the number of attacking pairs in the board.
    """  
    def count_attacking_pairs(self, state = None):
        if state is None :
            state = self.state
        attacking_pairs = 0
        queens = []
        for b in range(-1 * (self.N - 2), self.N - 1): #positive slopes
            for x in range(1, self.N + 1) :
                if (int(state[x - 1]) == x + b ):
                    queens.append(int(state[x - 1]))
            if(len(queens) >= 2):
                attacking_pairs += math.comb(len(queens),2)
            queens.clear()

        for b in range (3, self.N * 2): #negative slopes
            for x in range(1, self.N + 1) :
                if (int(state[x - 1]) == -x + b ):
                    queens.append(int(state[x - 1]))
            if(len(queens) >= 2):
                attacking_pairs += math.comb(len(queens),2)
            queens.clear()

        searched_items = [] 
        for digit in state: # same row
            count = 0
            if not searched_items.__contains__(digit):
                for current_digit in state : 
                    if digit == current_digit:
                        count += 1
                attacking_pairs += math.comb(count,2)
                searched_items.append(digit)
                
        return attacking_pairs


class NQueensProblem(SearchProblem):
    def __init__(self, N):
        self.N = N
        self.nqueens = NQueens(N)
        super(NQueensProblem,self).__init__(initial_state=self.nqueens.state)

    def actions(self, state):
        actions = []
        for i in range(1, self.N + 1):
            for j in range(1, self.N + 1):
                if j != int(state[i - 1]):
                    actions.append([f"Move queen {i} to row {j}", (i, j)])
        return actions

    def is_goal(self, state):
        return self.nqueens.count_attacking_pairs(state) == 0

    def heuristic(self, state):
        return self.nqueens.count_attacking_pairs(state)

    def result(self, state, action):
        new_state = ""
        for i in range(0, self.N):
            if i == (action[1][0] - 1):
                new_state += str(action[1][1])
            else:
                new_state += state[i]
        return new_state

    def value(self, state):
        return math.comb(self.N,2) - self.nqueens.count_attacking_pairs(state)
    
    def generate_random_state(self):
        return self.nqueens.generate_random_state()

    def crossover(self, state1, state2):
        state = ""
        crossover_point = random.randint(1, self.N - 1)
        for i in range(0, self.N):
            if i >= crossover_point:
                state += state2[i]
            else:
                state += state1[i]
        return state

    def mutate(self, state):
        new_state = ""
        mutation_point = random.randint(0,self.N - 1)
        new_number = random.randint(1, self.N)
        for i in range(0, self.N):
            if(i == mutation_point):
                new_state += str(new_number)
            else:
                new_state += state[i]
        return new_state

problem = NQueensProblem(5)
graph_search = True


def print_result(problem, algorithm, name, graph_search = None, limit = None, restarts_limit = None, population_size = None) :
    viewer = BaseViewer()
    start_time = time.perf_counter()
    if limit is not None :
        result = algorithm(problem, limit, graph_search=graph_search, viewer=viewer)
    else :
        if graph_search is None :
            if restarts_limit is not None:
                result = algorithm(problem, restarts_limit = restarts_limit, viewer=viewer)
            elif population_size is not None:
                result = algorithm(problem, population_size = population_size, viewer=viewer)
            else:
                result = algorithm(problem, viewer=viewer)
        else :
            result = algorithm(problem, graph_search=graph_search, viewer=viewer)
    end_time = time.perf_counter()
    stats = viewer.stats
    print("*****************")
    if(graph_search is not None):
        print(f"Graph search? {graph_search}")
    print(name)
    if limit is not None :
        print(f"Depth limit: {limit}")
    if restarts_limit is not None :
        print(f"Restarts limit: {restarts_limit}")
    if population_size is not None :
        print(f"Population size: {population_size}")
    if result is not None :
        print("Resulting path:")
        print(result.path())
        print(f"Resulting state: {result.state}")
        print(f"Total cost: {str(result.cost)}")
        print("Viewer stats:")
        print(stats)
        print(f"Time taken {(end_time - start_time):0.4f} seconds")
        print(
            f"Correct solution? {problem.nqueens.count_attacking_pairs(state = result.state) == 0}")
    else :
        print("No solution found!")
    print("*****************")
    for i in range(0, 4):
        print()

print(f"Initial state: {problem.initial_state}")
print("*** Uninformed Search Algorithms ***")
for i in range(0, 2):
    print()
print_result(problem,breadth_first,"BFS",graph_search)
print_result(problem,uniform_cost,"UCS",graph_search)
print_result(problem,depth_first,"DFS",graph_search)
print_result(problem,limited_depth_first,"L-DFS",graph_search,1)
print_result(problem,limited_depth_first,"L-DFS",graph_search,2)
print_result(problem,limited_depth_first,"L-DFS",graph_search,3)
print_result(problem,iterative_limited_depth_first,"IDS",graph_search)

print("*** Informed Search Algorithms ***")
for i in range(0, 2):
    print()
print_result(problem,greedy,"Greedy",graph_search)
print_result(problem,astar,"A Star",graph_search)

print("*** Local Search Algorithms ***")
for i in range(0, 2):
    print()
print_result(problem,hill_climbing,"Hill Climbing")
print_result(problem,hill_climbing_random_restarts,"Hill Climbing Random Restarts", restarts_limit=1)
print_result(problem,hill_climbing_random_restarts,"Hill Climbing Random Restarts", restarts_limit=2)
print_result(problem,hill_climbing_random_restarts,"Hill Climbing Random Restarts", restarts_limit=3)
print_result(problem,genetic,"Genetic", population_size=5)
print_result(problem,genetic,"Genetic", population_size=25)
print_result(problem,genetic,"Genetic", population_size=50)
print_result(problem,genetic,"Genetic", population_size=100)