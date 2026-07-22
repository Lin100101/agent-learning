from pydantic import ConfigDict, ValidationError, validate_call

@validate_call(config=ConfigDict(strict=True))
def count_items(items: list[str]) -> int:
    return len(items)

@validate_call(
    config=ConfigDict(strict=True),
    validate_return=True,
)
def pydantic_multiply(
    num1: int | float,
    num2: int | float,
) -> int | float:
    return num1 * num2


@validate_call(
    config=ConfigDict(strict=True),
    validate_return=True,
)
def get_number() -> int:
    return "100"

if __name__ == "__main__":
    print(count_items(["Agent", "Tool"]))

    try:
        count_items(["Agent", 123])
    except ValidationError as error:
        print("参数验证失败:")
        print(error)
    
    print(pydantic_multiply(3, 4))
    print(pydantic_multiply(3.5, 4))

    for arguments in [
        {"num1": True, "num2": 4},
        {"num1": "3", "num2": 4},
    ]:
        try:
            print(pydantic_multiply(**arguments))
        except ValidationError as error:
            print("参数验证失败:")
            print(error)

    try:
        print(get_number())
    except ValidationError as error:
        print("返回值验证失败:")
        print(error)