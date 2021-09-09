# copy function

def copy():

    try:
        lines = input() # take input from the user
        
        print(lines) # print the lines as it is

        copy() # call the function to print the lines

    except:  # if any exception occurs, pass them

        pass

copy()


