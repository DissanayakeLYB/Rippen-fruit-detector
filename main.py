#input the lambda range
upper_range = input("Upper range : ")
lower_range = input("Lower range : ")

lambda_range = upper_range - lower_range

#limit of the y
y_limit = input("Threshold peak intensity : ")

#x,y coordinates
x_values = (input("x values (with space in between) : ")).split(" ")
y_values = (input("y values (with space in between) : ")).split(" ")

#program
for i in range(lambda_range):

    if i > y_limit:
        print("The fruit is not suitable")

    else:
        pass