#region Helper functions
def remove_duplicates(str):
    """Removes duplicate characters from a string."""
    newStr = ""
    for c in str:
        if c not in newStr:
            newStr = newStr + c
    return newStr

def remove_similar_elements(lst):
    """Removes an element from the list if another similar element is found.
    
    E.g.

    `lst = ["AB", "BA", "C"]`. `"AB"` and `"BA"` are similar so one of them will be removed.
    """
    result = ["".join(sorted(e)) for e in lst]
    result = list(dict.fromkeys(result))
    return result
#endregion

def get_input():
    """Gets user input.

    Returns:
        A tuple of lists, where first element in the tuple 
        is the attribute list and second is the FD list.
    """
    relation_input = input("Enter the relation: ")
    functional_depend_input = input("Enter the functional dependencies: ")

    attribute_lst = relation_input.split(",")
    functional_depend_lst = functional_depend_input.replace(" ", "").split(",") 

    return attribute_lst, functional_depend_lst

def get_determinant_and_dependent_attr(fd_lst):
    """Get determinant (left side) attributes and dependent (right side) attributes.
    
    Returns:
        A list of tuples containing determinant attributes as the first tuple item its dependent attributes as the second item."""
    result = []
    for dependencies in fd_lst:
        if "->" in dependencies:
            arrow = dependencies.index("-") # Get the index of the arrow 
            result.append((dependencies[0:arrow], dependencies[arrow+2:]+dependencies[0:arrow]))
        else:
            result.append((dependencies[0], dependencies[1]+dependencies[0]))
    return result

def categorize_attributes(fd_lst, attr_lst):
    """Categorizes the attributes.
    
    Returns:
        Four lists that contain the attributes in `left, right, not left or right, both left and right` respectively.
    """
    attributes_temp_left= []
    attributes_temp_right= []

    for fd in fd_lst:
        fd_left = fd[0: fd.index("->")]
        fd_right = fd[fd.index("->")+2:]
        # Check to see if the left and right side consists of a single attribute (non-composite)
        if len(fd_left) == 1 and len(fd_right) == 1:
            attributes_temp_left.append(fd_left)   # From the start of the string upto the ->
            attributes_temp_right.append(fd_right) # After the -> until end of string
        else:
            # Append each attribute in the composite attributes upto the -> 
            for attr in fd_left:
                attributes_temp_left.append(attr)
            # Append each attribute in the composite attributes after the ->  until end of string
            for attr in fd_right:
                attributes_temp_right.append(attr)

    attributes_left = [fd for fd in attributes_temp_left if fd not in attributes_temp_right]
    attributes_right = [fd for fd in attributes_temp_right if fd not in attributes_temp_left]
    attributes_both_left_right = [fd for fd in attributes_temp_left if fd in attributes_temp_right]
    attributes_not_left_right = []

    joined_lst = [*attributes_left, *attributes_right, *attributes_both_left_right]

    for attribute in attr_lst:
        if attribute.replace(" ", "") not in "".join(joined_lst):
            attributes_not_left_right.append(attribute.replace(" ", ""))
            
    attributes_left = remove_similar_elements(attributes_left)
    attributes_right = remove_similar_elements(attributes_right)
    attributes_not_left_right = remove_similar_elements(attributes_not_left_right)
    attributes_both_left_right = remove_similar_elements(attributes_both_left_right)
    return attributes_left, attributes_right, attributes_not_left_right, attributes_both_left_right


def update_dependencies(lst):
    """Updates the dependencies within the FD list.
    
    E.g.
        `lst = ["A->B", "B->C"]` becomes `lst = ["A->BAC", "B->CB"]`.
        
    Returns:
        List with the new FDs.
    """
    lst_map = {i[0]: i[1] for i in lst}
    for k, v in lst_map.items():
        for c in v:
            if c != k:
                lst_map[k] += lst_map.get(c, "")
    result = [[k, v] for k, v in lst_map.items()]
    return result


def compute_closure(attributes, fd_lst):
    """Computes the closure for a single attribute."""
    closure_result = "".join(attributes)
    
    default_deter_depend_lst = get_determinant_and_dependent_attr(fd_lst)
    updated_determinant_lst = update_dependencies(default_deter_depend_lst)
    final_determinant_lst = update_dependencies(updated_determinant_lst)
    attribute_combinatons = ["".join((x,y,)) for x in attributes for y in attributes] + [x for x in attributes]
    for i in range(len(attribute_combinatons)):
        for j in range(len(default_deter_depend_lst)):
            if attribute_combinatons[i] == final_determinant_lst[j][0]:
                closure_result = closure_result + final_determinant_lst[j][1]
                
    # Remove duplicates
    closure_result = ''.join(dict.fromkeys(closure_result))
    return closure_result

def get_closure(attributes, fd_lst):
    """Calculates the closure for multiple attributes."""
    closure_res = []
    for attr in attributes:
        if len(attr) >= 2:
            # Seperate attribute if it is a composite
            seperated_attributes = " ".join(attr).replace(" ", "") 
            closure = ""
            
            for attribute in seperated_attributes:
                # Get the closure for each attribute
                closure = (closure + compute_closure(attribute, fd_lst)).replace(" ", "")
                closure = remove_duplicates(closure)
                
            # Take the calculated closure from before and find its closure
            for _ in range(len(closure)):
                closure = compute_closure(closure, fd_lst).replace(" ", "")
                closure = remove_duplicates(closure)
            closure_res.append((seperated_attributes, closure))
        else:
            closure = ""
            closure = closure + compute_closure(attr, fd_lst).replace(" ", "")
            closure = remove_duplicates(closure)
            closure_res.append((attr, closure))
    return closure_res


def find_key(possible_keys, attribute_lst, fd_lst):
    """Finds the candidate key(s)."""
    result = []
    closure_result = get_closure(possible_keys, fd_lst)

    if len(closure_result) > 0:
        # Check if any of the singular attribute are a candidate key
        for res in closure_result:
            if len(list("".join(res[1]))) == len(attribute_lst):
                result.append(remove_duplicates(res[0]))
                # Remove the key from the list, since when creating permutations
                # any key that contains said key wil lead to a superkey
                possible_keys.remove(res[0])
        # Create permutations from the attributes
        permutations = ["".join((x,y)) for x in attributes_both_left_right for y in possible_keys]
        closure_result = get_closure(permutations, fd_lst)
        for i in closure_result:
            if len(i[1]) == len(attribute_lst):
                result.append(i[0])
        if len(result) == 0:
            permutations = ["".join((x,y,z)) for x in attributes_both_left_right for y in possible_keys for z in attributes_both_left_right]
            permutations = remove_similar_elements(permutations)
            closure_result = get_closure(permutations, fd_lst)
        for i in closure_result:
            if len(i[1]) == len(attribute_lst):
                result.append(i[0])
        result = remove_similar_elements(result)
        return result


if __name__ == '__main__':
    attribute_lst, functional_depend_lst = get_input()
    attributes_left, attributes_right, attributes_not_left_right, attributes_both_left_right = categorize_attributes(functional_depend_lst, attribute_lst)

    print("-"*50)
    print("Attributes: ", attribute_lst)
    print("Left: ", attributes_left)
    print("Right: ", attributes_right) 
    print("Neither left or right: ", attributes_not_left_right) 
    print("Both left and right: ", attributes_both_left_right)
    print("-"*50)

    if len(attributes_not_left_right + attributes_left) == 0:
        possible_key = attributes_both_left_right
    else:
        possible_key = ["".join(attributes_not_left_right + attributes_left)] 
        
    print(f"Key(s): {find_key(possible_key, attribute_lst, functional_depend_lst)}\n")
