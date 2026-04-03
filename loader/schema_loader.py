# schema_loader.py
from pathlib import Path
import json
import re

class SchemaLoader:
    """
    Load Markdown schema files into structured JSON objects.
    Designed for /ai-system/schemas/
    """

    CODE_BLOCK_RE = re.compile(r"```(json|text)?\s*([\s\S]+?)```", re.MULTILINE)

    def __init__(self, schema_dir: str):
        self.schema_dir = Path(schema_dir)
        self.schemas = {}

    def load_all(self) -> dict:
        """Load all .md files in the schema directory."""
        for md_file in self.schema_dir.glob("*.md"):
            self.schemas[md_file.stem] = self._parse_md(md_file)
        return self.schemas

    def _parse_md(self, md_path: Path) -> dict:
        """Parse a single Markdown file into structured sections."""
        content = md_path.read_text(encoding="utf-8")
        parsed = {}

        current_section = None
        section_lines = []

        for line in content.splitlines():
            # Detect top-level section
            if line.startswith("# "):
                if current_section:
                    parsed[current_section] = self._extract_code_blocks("\n".join(section_lines))
                current_section = line[2:].strip()
                section_lines = []
            else:
                section_lines.append(line)

        # Add last section
        if current_section:
            parsed[current_section] = self._extract_code_blocks("\n".join(section_lines))

        return parsed

    def _extract_code_blocks(self, text: str) -> list:
        """Find all JSON/text code blocks and parse them."""
        blocks = []
        for match in self.CODE_BLOCK_RE.finditer(text):
            lang = match.group(1)
            code = match.group(2).strip()
            if lang == "json":
                try:
                    blocks.append(json.loads(code))
                except json.JSONDecodeError:
                    # fallback: keep as string if invalid JSON
                    blocks.append(code)
            else:
                blocks.append(code)
        return blocks

# Example usage
if __name__ == "__main__":
    loader = SchemaLoader("/ai-system/schemas/")
    all_schemas = loader.load_all()

    # Example: access Task Classification schema
    task_classification = all_schemas.get("task-classification", {})
    print(json.dumps(task_classification, indent=2))