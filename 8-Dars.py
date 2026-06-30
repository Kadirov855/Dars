person = {
    "name": "Abdulloh",
    "age": 13,
    "hobby": "gaming"
}

print(person.get("school"))          # None (no error)
print(person.get("school", "N/A"))   # N/A (custom default)

del person["hobby"]
# or
person.pop("hobby")

if "name" in person:
    print("Name is set")

contacts = {
    "Alex": {"phone": "123-456", "city": "Kyiv"},
    "Maria": {"phone": "789-012", "city": "Lviv"}
}

print(contacts["Alex"]["phone"])   # 123-456
