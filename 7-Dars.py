fruits = ["apple", "banana", "cherry"]
numbers = [10, 20, 30]
mixed = ["text", 5, True]   # lists can mix types

fruits = ["apple", "banana", "cherry"]
print(fruits[0])   # apple
print(fruits[1])   # banana
print(fruits[-1])  # cherry (negative index counts from the end)

fruits = ["apple", "banana", "cherry"]
fruits[1] = "blueberry"
print(fruits)   # ["apple", "blueberry", "cherry"]

fruits = ["banana", "apple", "cherry"]
fruits.append("mango")
fruits.sort()
print(fruits)   # ["apple", "banana", "cherry", "mango"]

point = (10, 20)
print(point[0])   # 10
