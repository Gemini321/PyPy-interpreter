print("Here is fibonacci_loop test:")
n = input("Please input a number less than 20:")
n = eval(n)
a = 0
b = 1
for i in range(n):
    a += b
    a, b = b, a
print("The nth fibonacci number is", a)
