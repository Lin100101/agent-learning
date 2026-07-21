def base_converter(value: str, from_base: int, to_base: int) -> str:
    SUPPORTED_BASES = [2, 8, 10, 16]

    if from_base not in SUPPORTED_BASES:
        raise ValueError(f"不支持的源进制: {from_base}. 支持的进制有: {SUPPORTED_BASES}")
    if to_base not in SUPPORTED_BASES:
        raise ValueError(f"不支持的目标进制: {to_base}. 支持的进制有: {SUPPORTED_BASES}")
    
    try:
        decimal_value = int(value, from_base)
    except ValueError as error:
        raise ValueError(f"无法将值 '{value}' 从进制 {from_base} 转换为十进制，"
                         f"请确保输入值是有效的 {from_base} 进制数.") from error
    
    BASE_FORMATS = {
        2: "b",
        8: "o",
        10: "d",
        16: "X"
    }

    return format(decimal_value, BASE_FORMATS[to_base])


if __name__ == "__main__":
    print(base_converter("100", 10, 2))
    print(base_converter("1100100", 2, 10))
    print(base_converter("255", 10, 16))
    print(base_converter("377", 8, 10))