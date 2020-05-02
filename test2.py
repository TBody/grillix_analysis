from source.shared import QArray
from source import unit_registry, Quantity, np

A = QArray.from_norm([1.2, 1.2, 1.4, 12, 129, 0, 1], Quantity(37, 'm/s'))
B = QArray.from_norm([1.2, 1.3, 1.4, 12, 129, 0, 1], Quantity(37, 'm/s'))

print(np.unique(A))

print(type(np.unique(A)))
print(type(np.max(A)))

from pint.numpy_func import HANDLED_FUNCTIONS

print(list(HANDLED_FUNCTIONS))

def check_function(name, function_result):

    print(name, function_result)
    for function_res in function_result:
        assert(isinstance(function_res, QArray)), f"{function_res} is {type(function_res)}"

check_function("meshgrid", np.pad(A, B))

# for function_key, function in HANDLED_FUNCTIONS.items():

#     print(function_key, function(A), type(A))

    # assert(isinstance(function(A), QArray)), f"{function_key} returned type {type(function(A))}"