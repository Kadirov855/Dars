def greet():
    print("Hello!")

greet()   # calling the function
greet()   # can call it as many times as needed


def greet(name):
    print(f"Hello, {name}!")

greet("Alex")
greet("Maria")

def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alex")              # Hello, Alex!
greet("Alex", "Hi")        # Hi, Alex!
