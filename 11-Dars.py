file = open("notes.txt", "w")   # "w" = write mode (creates or overwrites the file)
file.write("Hello, this is saved!")
file.close()   # always close the file when done

with open("notes.txt", "w") as file:
    file.write("Hello, this is saved!")
# file is automatically closed here, even if an error happens

with open("notes.txt", "a") as file:
    file.write("\nAnother line")   # \n = new line

with open("notes.txt", "r") as file:
    content = file.read()
print(content)
