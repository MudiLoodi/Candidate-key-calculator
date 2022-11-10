
import functools
def remove_duplicates(str):
    newStr = ""
    for char in str:
        if char not in newStr:
            newStr = newStr + char
    return newStr

def get_input():
    # R: A, B, C, D, E
    relation_input = input("Enter the relation: ")
    # A->B, D->C, C->A
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
    for attribute in attr_lst:
        if attribute.replace(" ", "") not in attributes_left + attributes_right + attributes_both_left_right:
            attributes_not_left_right.append(attribute.replace(" ", ""))
    return attributes_left, attributes_right, attributes_not_left_right, attributes_both_left_right


attributes_left, attributes_right, attributes_not_left_right, attributes_both_left_right = categorize_attributes(functional_depend_lst, attribute_lst)

print("left ", attributes_left) #   ['A', 'C', 'C']
print("right ", attributes_right) # ['B', 'E', 'F']
print("not left or right ", attributes_not_left_right) # []
print("both left and right ", attributes_both_left_right) # ['D']


closure = {}

#if  len(attributes_not_left_right) == 0 and  len(attributes_left) == 0: # Check if lists are empty
combination = ["".join(attributes_not_left_right + attributes_left)] # ['CAD'] #TODO: Remove duplicates

print("Combination ", combination)

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
    result = "".join(attributes)
    updated_determinant_lst = update_det_dep_lst(default_deter_depend_lst)
    final_determinant_lst = update_det_dep_lst(updated_determinant_lst)

    for i in range(len(result)):
        for j in range(len(default_deter_depend_lst)):
            if result[i] in final_determinant_lst[j][0]:
                #print(f"{result[i]} in {final_determinant_lst[j][0]}")
                result = result + final_determinant_lst[j][1]

    # Remove duplicates
    result = ''.join(dict.fromkeys(result))
    return result


def get_closure(attributes): # Input: ['AD', 'BD', 'CD']
    keys = []
    for attr in attributes:
        if len(attr) >= 2:
            sep = " ".join(attr) # 
            v = ""
            #result = sep.replace(" ", "")
            for i in sep:
                v = (v + get_closure_single(i)).replace(" ", "")
                if len(v) == len(attribute_lst):
                    if len(attributes) > 1:
                        keys.append(attr)
                    else:
                        keys.append(v)
        else:
            keys = get_closure_single(attributes)
    return keys



    # TODO: Find the closure for composite attributes


closure_result = get_closure(combination)

if len(list("".join(closure_result))) == len(attribute_lst):
    #print("Final: ", closure_result )
    print("Key: ", combination) 
else:
    perm = ["".join((x,y)) for x in attributes_both_left_right for y in combination] # TODO Check what this returns
    #print("perm ", perm)
    print("Key: ", get_closure(perm)) 
 




#input("Press Enter to continue...")