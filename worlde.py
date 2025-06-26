print("Size")
size = int(input()) #Type casting to int
print("Green letters")
green = str(input()) #Green Typecasted to string
print("Yellow letters")
yellow = str(input()) #Yellow Typecasted to string
print("Grey letters")
grey = str(input()) #Gray Typecasted to string

print("--Input--")
print(size) #print size
print(green)
print(yellow)
print(grey)

#Call solver function
ft_solver(size,green,yellow,grey)
