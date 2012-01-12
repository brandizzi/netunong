def split_name(name):
    splitted_name = name.split(",")
    splitted_name = [name 
            for name in " ".join(reversed(splitted_name)).split() 
            if name]
    first_name = splitted_name[0]
    last_name = splitted_name[-1]
    middle_name = " ".join(splitted_name[1:-1])
    return first_name, middle_name, last_name
