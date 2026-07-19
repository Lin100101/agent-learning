def calculate_total(price, quantity, discount=0):
    original_price = price * quantity
    total = original_price * (1 - discount)
    return total


if __name__ == "__main__":
    # 测试 calculate_total 函数
    result1 = calculate_total(100, 2)
    result2 = calculate_total(
        price=100,
        quantity=2,
        discount=0.2,
    )

    print(result1)
    print(result2)