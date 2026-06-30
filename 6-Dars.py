for i in range(5):
    print(i)

range(5)        # 0, 1, 2, 3, 4
range(2, 6)     # 2, 3, 4, 5
range(0, 10, 2) # 0, 2, 4, 6, 8 (step of 2)

for letter in "Python":
    print(letter)

for fruit in ["apple", "banana", "cherry"]:
    print(fruit)

count = 0
while count < 5:
    print(count)
    count += 1   # same as: count = count + 1

for i in range(10):
    if i == 5:
        break       # stops the loop completely
    print(i)
