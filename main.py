
import functools
def remove_duplicates(str):
    newStr = ""
    for char in str:
        if char not in newStr:
            newStr = newStr + char
    return newStr

def get_input():
    relation_input = input("Enter the relation: ")
    functional_depend_input = input("Enter the functional dependencies: ")

    attribute_lst = relation_input.split(",")
    functional_depend_lst = functional_depend_input.replace(" ", "").split(",") # ["A->B", "B->C", "C->A"]
    return attribute_lst, functional_depend_lst


def get_determinant_and_dependent_attr(fd_lst):
    """Returns a list of tuples containing determinant attributes in the first tuple item and dependent in the second."""
    result = []
    for dependencies in fd_lst:
        if "->" in dependencies:
            arrow = dependencies.index("-") # Get the index of the arrow 
            result.append((dependencies[0:arrow], dependencies[arrow+2:]+dependencies[0:arrow]))
        else:
            result.append((dependencies[0], dependencies[1]+dependencies[0]))
    return result


attribute_lst, functional_depend_lst = get_input()

print(functional_depend_lst) # ['A->B', 'C->E', 'D->F', 'C->D']
determinant_attr = get_determinant_and_dependent_attr(functional_depend_lst) # [('A', 'B'), ('C', 'E'), ('D', 'F'), ('C', 'D')]
print(determinant_attr)

def categorize_attributes(fd_lst, attr_lst):
    """Returns a tuple of lists."""
    attributes_temp_left= []
    attributes_temp_right= []
    for fd in fd_lst:
        attributes_temp_left.append(fd[0: fd.index("->")]) # From the start of the string upto the ->
        attributes_temp_right.append(fd[fd.index("->")+2:])# After the -> until end of string

    attributes_left = [fd for fd in attributes_temp_left if fd not in attributes_temp_right]
    attributes_right = [fd for fd in attributes_temp_right if fd not in attributes_temp_left]
    attributes_both_left_right = [fd for fd in attributes_temp_left if fd in attributes_temp_right]
    attributes_not_left_right = []

    joined_lst = [*attributes_left, *attributes_right, *attributes_both_left_right]

    for attribute in attr_lst:
        if attribute.replace(" ", "") not in "".join(joined_lst):
            attributes_not_left_right.append(attribute.replace(" ", ""))
    return attributes_left, attributes_right, attributes_not_left_right, attributes_both_left_right


attributes_left, attributes_right, attributes_not_left_right, attributes_both_left_right = categorize_attributes(functional_depend_lst, attribute_lst)

print("left ", attributes_left) #   ['A', 'C', 'C']
print("right ", attributes_right) # ['B', 'E', 'F']
print("not left or right ", attributes_not_left_right) # []
print("both left and right ", attributes_both_left_right) # ['D']


closure = {}

possible_key = ["".join(attributes_not_left_right + attributes_left)] 

print("Combination ", possible_key)

def update_det_dep_lst(lst):
    lst_map = {i[0]: i[1] for i in lst}
    for k, v in lst_map.items():
        for c in v:
            if c != k:
                lst_map[k] += lst_map.get(c, "")
    result = [[k, v] for k, v in lst_map.items()]
    return result



def get_closure_single(attributes):
    default_deter_depend_lst = get_determinant_and_dependent_attr(functional_depend_lst)
    closure_result = "".join(attributes)
    # TODO: Improve this
    updated_determinant_lst = update_det_dep_lst(default_deter_depend_lst)
    final_determinant_lst = update_det_dep_lst(updated_determinant_lst)

    for i in range(len(closure_result)):
        for j in range(len(default_deter_depend_lst)):
            if closure_result[i] in final_determinant_lst[j][0]:
                closure_result = closure_result + final_determinant_lst[j][1]

    # Remove duplicates
    closure_result = ''.join(dict.fromkeys(closure_result))
    return closure_result


def get_closure(attributes): 
    closure_res = []
    for attr in attributes:
        if len(attr) >= 2:
            # Seperate attribute if it is a composite
            seperated_attributes = " ".join(attr).replace(" ", "") 
            closure = ""
            for attribute in seperated_attributes:
                # Get the closure for each attribute
                closure = (closure + get_closure_single(attribute)).replace(" ", "")
                # Check if closure covers all attributes
                if len(closure) == len(attribute_lst):
                    closure_res.append(closure)
    return closure_res


def find_key(possible_keys, attribute_lst):
    closure_result = get_closure(possible_key)
    if len(list("".join(closure_result))) == len(attribute_lst):
        return possible_keys
    else:
        perm = ["".join((x,y)) for x in attributes_both_left_right for y in possible_key]
        closure_result = get_closure(perm)
    return perm


print("\n")
print("Key(s):", find_key(possible_key, attribute_lst))


 




#input("Press Enter to continue...")