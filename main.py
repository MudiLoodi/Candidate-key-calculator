
def get_input():
    # R: A, B, C, D, E
    relation_input = input("Enter the relation: ")
    # A->B, D->C, C->A
    functional_depend_input = input("Enter the functional dependencies: ")

    attribute_lst = relation_input.split(",")
    functional_depend_lst = functional_depend_input.replace(" ", "").split(",") # ["A->B", "D->C"]
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

    attributes_not_left_right = []
    for attribute in attr_lst:
        if attribute not in "".join(fd_lst):
            attributes_not_left_right.append(attribute)
    return attributes_left, attributes_right, attributes_not_left_right


print(categorize_attributes(functional_depend_lst, attribute_lst))





#input("Press Enter to continue...")