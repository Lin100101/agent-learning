def greet(name):
    return f"Hello, {name}!"

print(greet)
print(type(greet))

another_greet = greet

result1 = greet("小明")
result2 = another_greet("小红")

print(result1)
print(result2)