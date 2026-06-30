number = int(input("Enter a number: "))
print(100 / number)

try:
    number = int(input("Enter a number: "))
    print(100 / number)
except:
    print("Something went wrong")

try:
    number = int(input("Enter a number: "))
except ValueError as e:
    print("Error details:", e)
