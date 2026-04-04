from pathlib import Path
import tempfile

from tools.base import ToolRegistry
from tools.file_read import FileReadTool


def test_tool_registry_registers_and_lists_tools():
    registry = ToolRegistry(safe_dir=None)
    tool = FileReadTool(safe_dir=".")

    registry.register(tool)

    assert tool.name in registry.list_tools()
    assert registry.get(tool.name) is tool


def test_tool_registry_executes_tool():
    with tempfile.TemporaryDirectory() as tmpdir:
        safe_dir = Path(tmpdir)
        test_file = safe_dir / "example.txt"
        test_file.write_text("content", encoding="utf-8")

        registry = ToolRegistry(safe_dir=None)
        tool = FileReadTool(safe_dir=str(safe_dir))
        registry.register(tool)

        content = registry.execute(tool.name, path="example.txt")
        assert content == "content"
