a = int(input("Enter a number: "))
b = int(input("Enter a second number: "))
c = input("Enter + or -: ")

if c == "+":
    print(str(a) + " + " + str(b) + " = " + str(a + b))

elif c == "-":
    print(str(a) + " - " + str(b) + " = " + str(a - b))

else:
    print("Unkown operator")