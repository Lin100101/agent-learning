
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "对两个数字执行基本的数学运算（加、减、乘、除）",
            "parameters": {
                "type": "object",
                "properties": {
                    "num1": {
                        "type": "number",
                        "description": "第一个数字"
                    },
                    "num2": {
                        "type": "number",
                        "description": "第二个数字"
                    },
                    "operation": {
                        "type": "string",
                        "description": "需要执行的运算",
                        "enum": ["add", "subtract", "multiply", "divide"]
                    },
                },
                "required": ["num1", "num2", "operation"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "text_statistics",
            "description": "对文本进行统计分析(字符数、单词数、行数、非空白字符数)",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "需要分析的文本"
                    },
                    "operation": {
                        "type": "string",
                        "description": "需要执行的统计分析",
                        "enum": ["character_count", "word_count", "line_count", "non_whitespace_count"]
                    }
                },
                "required": ["text", "operation"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "base_converter",
            "description": "在二、八、十、十六进制之间转换数字，十六进制结果使用大写字母",
            "parameters": {
                "type": "object",
                "properties": {
                    "value": {
                        "type": "string",
                        "description": "需要转换的数字"
                    },
                    "from_base": {
                        "type": "integer",
                        "description": "原始进制",
                        "enum": [2, 8, 10, 16],
                    },
                    "to_base": {
                        "type": "integer",
                        "description": "目标进制",
                        "enum": [2, 8, 10, 16],
                    }
                },
                "required": ["value", "from_base", "to_base"]
            }
        }
    }
]