from registry import AVAILABLE_TOOLS
from tool_schemas import TOOLS

def validate_tool_configuration():
    schema_tool_names = {
        tool["function"]["name"]
        for tool in TOOLS
    }

    registered_tool_names = set(AVAILABLE_TOOLS)

    missing_in_registry = schema_tool_names - registered_tool_names
    missing_in_schema = registered_tool_names - schema_tool_names


    if missing_in_registry:
        print("Schema 中存在但未注册：")
        for tool_name in sorted(missing_in_registry):
            print(f"- {tool_name}")

    if missing_in_schema:
        print("注册表中存在但缺少 Schema：")
        for tool_name in sorted(missing_in_schema):
            print(f"- {tool_name}")


    if missing_in_registry or missing_in_schema:
        raise RuntimeError("Schema 与工具注册表不一致。")

    print("检查通过: Schema 与工具注册表一致。")
    print(f"工具数量: {len(schema_tool_names)}")
    print(f"工具列表: {', '.join(sorted(schema_tool_names))}")


if __name__ == "__main__":
    validate_tool_configuration()