import inspect
from typing import get_type_hints

def add(num1: int, num2: int) -> int:
    return num1 + num2

def get_number() -> int:
    return "100"

print(add(1, 2))
print(add("1", "2"))
print(get_number())

print(add.__annotations__)
print(get_number.__annotations__)

result1 = add("1", "2")
result2 = get_number()

print(type(result1))
print(type(result2))


print(inspect.signature(add))
print(get_type_hints(add))

signature = inspect.signature(add)

bound_arguments = signature.bind(num1=1, num2=2)
print(bound_arguments.arguments)

try:
    bound_arguments = signature.bind(num1=1)
except TypeError as error:
    print(f"缺少参数: {error}")

try:
    bound_arguments = signature.bind(num1=1, num2=2, num3=3)
except TypeError as error:
    print(f"多余参数: {error}")

wrong_type_arguments = signature.bind(
    num1="1",
    num2="2",
)

print(wrong_type_arguments.arguments)
