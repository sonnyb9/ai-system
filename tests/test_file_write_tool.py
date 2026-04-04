import tempfile
from pathlib import Path

from tools.file_write import FileWriteTool


def test_file_write_tool_writes_to_safe_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        safe_dir = Path(tmpdir)
        tool = FileWriteTool(safe_dir=str(safe_dir))

        result = tool.execute(path="hello.txt", content="hello world")
        assert "Wrote" in result

        written = (safe_dir / "hello.txt").read_text(encoding="utf-8")
        assert written == "hello world"


def test_file_write_tool_rejects_outside_safe_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        safe_dir = Path(tmpdir)
        outside_file = safe_dir.parent / "outside.txt"
        tool = FileWriteTool(safe_dir=str(safe_dir))

        try:
            tool.execute(path=str(outside_file), content="nope")
            assert False, "Expected ValueError for outside safe dir"
        except ValueError as exc:
            assert "outside safe directory" in str(exc)
