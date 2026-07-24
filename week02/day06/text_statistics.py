from typing import Literal


def text_statistics(text: str, operation: Literal[
    "character_count",
    "word_count",
    "line_count",
    "non_whitespace_count",
]) -> int:
    """统计文本的字符数、单词数、行数或非空白字符数。"""
    operations = ["character_count", "word_count", "line_count", "non_whitespace_count"]

    if operation not in operations:
        raise ValueError(f"不支持的操作: {operation}")
    
    if operation == "character_count":
        return len(text)
    elif operation == "word_count":
        return len(text.split())
    elif operation == "line_count":
        return len(text.splitlines())
    elif operation == "non_whitespace_count":
        return sum(1 for character in text if not character.isspace())
    

if __name__ == "__main__":
    text = "Hello world\nPython Agent"
    print("Character count:", text_statistics(text, "character_count"))
    print("Word count:", text_statistics(text, "word_count"))
    print("Line count:", text_statistics(text, "line_count"))
    print("Non-whitespace count:", text_statistics(text, "non_whitespace_count"))
    print(text_statistics("", "line_count"))
    try:
        print(text_statistics("Hello", "unknown"))
    except ValueError as error:
        print(f"测试通过, 捕获异常: {error}")