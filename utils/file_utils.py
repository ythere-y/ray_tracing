

def write_prefix(file, width, height):
    if file == None:
        print("P3\n{} {}\n255\n".format(width, height), end='')
    else:
        file.write("P3\n{} {}\n255\n".format(width, height))
