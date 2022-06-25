
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



attribute_lst, functional_depend_lst = get_input()



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
        if attribute not in "".join(fd_lst):
            attributes_not_left_right.append(attribute)
    return attributes_left, attributes_right, attributes_not_left_right, attributes_both_left_right


attributes_left, attributes_right, attributes_not_left_right, attributes_both_left_right = categorize_attributes(functional_depend_lst, attribute_lst)

closure = {}

#if  len(attributes_not_left_right) == 0 and  len(attributes_left) == 0: # Check if lists are empty
combination = attributes_not_left_right + attributes_left
print("Combination ", combination)
def get_closure(attributes):
    for i in range(0, len(functional_depend_lst)):
     #   for attr in attributes: # ["E", "D"]
     #       if len(attr) == 1:
     #           if attr in functional_depend_lst[i]:
     #               closure[attr] = functional_depend_lst[i].replace("->", " ")
     #           elif attr in closure: # Fixes bug where an attribute will be update because it is checked twice for different FD
     #               pass
     #           else:
     #               closure[attr] = attr
     #       elif len(attr) > 1: #['AD', 'BD', 'CD']
        for attr_set in attributes:
            for attr in attr_set:
                if attr in functional_depend_lst[i][0 : functional_depend_lst[i].index("->")+2 :]: # ["A->B", "B->C", "C->A"]
                    closure[attr] = functional_depend_lst[i][functional_depend_lst[i].index("->")+2 : ] + f" {attr}"  #functional_depend_lst[i].replace("->", " ")
                elif attr in closure: # Fixes bug where an attribute will be update because it is checked twice for different FD
                    pass
                else:
                    closure[attr] = attr
    closure_lst = list(functools.reduce(lambda x, y: x + y, closure.items()))
    print("CLOSURE ", closure)
    for i in range(0, len(closure.keys())):
        for str in closure_lst:
            if set(str).intersection(set(closure_lst[i])):
                combined_closure = str.join(closure_lst[i])
    #closure_str = "".join(closure_lst).replace(" ", "")
    #closure_res = "".join(set(closure_str))
    print(closure)
    return remove_duplicates(combined_closure.replace(" ", ""))

closure_result = get_closure(combination)

if len(closure_result) == len(attribute_lst):
    print("Final ", closure_result )
else:
    perm = ["".join((x,y)) for x in attributes_both_left_right for y in combination] 
    print("perm ", perm)
    print(get_closure(perm))





#input("Press Enter to continue...")