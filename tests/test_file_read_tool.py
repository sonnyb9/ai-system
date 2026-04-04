import os
import tempfile
from pathlib import Path

from tools.file_read import FileReadTool


def test_file_read_tool_reads_file_in_safe_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        safe_dir = Path(tmpdir)
        test_file = safe_dir / "example.txt"
        test_file.write_text("hello world", encoding="utf-8")

        tool = FileReadTool(safe_dir=str(safe_dir))
        content = tool.execute(path="example.txt")

        assert content == "hello world"


def test_file_read_tool_rejects_outside_safe_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        safe_dir = Path(tmpdir)
        outside_file = Path(tmpdir).parent / "outside.txt"
        outside_file.write_text("nope", encoding="utf-8")

        tool = FileReadTool(safe_dir=str(safe_dir))
        try:
            tool.execute(path=str(outside_file))
            assert False, "Expected ValueError for outside safe dir"
        except ValueError as exc:
            assert "outside safe directory" in str(exc)
