from simpleai.search import CspProblem, backtrack, MOST_CONSTRAINED_VARIABLE, HIGHEST_DEGREE_VARIABLE, LEAST_CONSTRAINING_VALUE
import itertools
import time

N = int(input("Enter N: "))
variables_list = []
for i in range(1,N + 1):
    variables_list.append(f"Q{i}")

variables = tuple(variables_list)
domains = dict((v, list(range(1, N + 1))) for v in variables)

combinations = list(itertools.combinations(variables,2))


def not_attacking(variables, values):
        column_difference = abs(int(variables[0][1]) - int(variables[1][1])) 
        row_difference = abs(values[0] - values[1])
        if(column_difference == row_difference): #diagonal attack
            return False

        if(values[0] == values[1]): #same row
            return False

        return True

constraints = []

for pair in combinations:
    constraints.append((pair, not_attacking))

my_problem = CspProblem(variables, domains, constraints)

print("Default")
start = time.perf_counter()
print(backtrack(my_problem))
print(f"Time elapsed: {(time.perf_counter() - start):0.4f} seconds")
print()

print("Most constrained variable")
start = time.perf_counter()
print(backtrack(my_problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE))
print(f"Time elapsed: {(time.perf_counter() - start):0.4f} seconds")
print()

print("Highest degree variable")
start = time.perf_counter()
print(backtrack(my_problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE))
print(f"Time elapsed: {(time.perf_counter() - start):0.4f} seconds")
print()

print("Least constraining value")
start = time.perf_counter()
print(backtrack(my_problem, value_heuristic=LEAST_CONSTRAINING_VALUE))
print(f"Time elapsed: {(time.perf_counter() - start):0.4f} seconds")
print()

print("Most constrained variable + Least constraining value")
start = time.perf_counter()
print(backtrack(my_problem, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE))
print(f"Time elapsed: {(time.perf_counter() - start):0.4f} seconds")
print()

print("Highest degree variable + Least constraining value")
start = time.perf_counter()
print(backtrack(my_problem, variable_heuristic=HIGHEST_DEGREE_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE))
print(f"Time elapsed: {(time.perf_counter() - start):0.4f} seconds")

