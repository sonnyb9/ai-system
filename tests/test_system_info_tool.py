from tools.system_info import SystemInfoTool


def test_system_info_tool_returns_text():
    tool = SystemInfoTool()
    result = tool.execute()

    assert "platform:" in result
    assert "python_version:" in result
    assert "hostname:" in result
