# Schema Loader Specification
**System:** OpenClaw Local AI Orchestration  
**Purpose:** Define the loader component responsible for ingesting Markdown schema files into structured, AI-consumable objects.

---

## 1. Overview

The **Schema Loader** is a dedicated component that:

- Reads all Markdown files in `/ai-system/schemas/`
- Parses top-level sections (`#`) and nested headings (`##`, `###`)
- Extracts `json` and `text` code blocks
- Converts content into **structured JSON objects**
- Provides runtime access to the Agent Controller, Tool Interface, and other nodes

**Goals:**

1. Deterministic ingestion of schemas
2. Validation of required fields and structure
3. Extensible for future schemas

---

## 2. Directory Placement

- Markdown schemas: `/ai-system/schemas/`
- Loader code: `/ai-system/loader/schema_loader.py`
- Loader spec doc: `/ai-system/docs/schema_loader.md`

This ensures **separation of machine-consumable schemas from documentation**.

---

## 3. Parsing Strategy

### 3.1 Sections

- `#` → top-level schema object  
- `##`, `###` → nested attributes  
- Code blocks (`json` or `text`) → structured data  

### 3.2 Example Mapping

Markdown snippet:

```markdown
## Task Schema

```json
{
  "task_id": "string",
  "category": "maintenance | monitoring"
}

Parsed object:

```json
{
  "Task Schema": [
    {
      "task_id": "string",
      "category": ["maintenance", "monitoring"]
    }
  ]
}

## 4. Loader Interface

Python API Example:

from loader.schema_loader import SchemaLoader

loader = SchemaLoader("/ai-system/schemas/")
schemas = loader.load_all()
task_schema = schemas.get("task-classification", {}).get("Task Schema")
schemas is a nested dictionary of sections → code blocks
Any agent component can query this object for validation, classification, or execution rules
## 5. Validation Layer
Ensure required sections exist in each schema file
Task Schema
Category Definitions
Tool Allowlist
Routing Logic
Ensure all JSON code blocks are well-formed
Optional: enforce schema versioning
## 6. Security
Loader must not execute any code blocks
Only parse content into structured objects
File access restricted to /ai-system/schemas/
## 7. Logging

For each load operation, log:

{
  "file": "task-classification.md",
  "status": "success",
  "sections_found": ["Task Schema", "Category Definitions"]
}
## 8. Extensibility
New schemas added to /schemas/ are automatically loaded
Nested sections create new dictionary keys in the JSON object
Supports multi-node setups and distributed AI orchestration
## 9. Future Enhancements
Hot reload when schemas change
Schema diffing for change detection
Automated tests for schema completeness and consistency
Optional conversion to YAML/JSON for external tools