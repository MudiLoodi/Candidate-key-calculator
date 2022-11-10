
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
combination = ["".join(attributes_not_left_right + attributes_left)] # ['A', 'C', 'C'] #TODO: Remove duplicates

print("Combination ", combination)

def get_closure(attributes): # Input: ['C', 'A', 'D']

    for attr in attributes:
        if len(attr) >= 2:
            separator = " "
            sep = separator.join(attr) # C A D
            t = get_determinant_and_dependent_attr(functional_depend_lst)
            result = sep.replace(" ", "")# CAD
            print("init ", result)
            print("t ", t)
            for i in range(len(result)):
                for j in range(len(t)):
                    if result[i] in t[j][0]:
                        print(f"{result[i]} in {t[j][0]}")
                        result = result + t[j][1]
            # Remove duplicates
            result = ''.join(dict.fromkeys(result))
            
            return result


    # TODO: Find the closure for composite attributes


closure_result = get_closure(combination)
print("closure res", closure_result)
#closure_result = list(dict.fromkeys(closure_result))

if len(closure_result) == len(attribute_lst):
    print("Final: ", closure_result )
    print("Key: ", combination)





#input("Press Enter to continue...")