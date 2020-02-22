print("Here is if_statement(abs) test:")
a = 123
b = 456
Abs = a - b
if Abs >= 0:
    print("|123 - 456| =", Abs)
else:
    Abs = -Abs
    print("|123 - 456| =", Abs)
print('')
a = eval(input("Please enter an integer 'a':"))
b = eval(input("Please enter another integer 'b':"))
if a < b:
    Abs = b - a
else:
    Abs = a - b
print("|a - b| =", Abs)
print('')
