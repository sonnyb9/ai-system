# Testing Plan for ai-system Agent Runtime

This plan outlines a comprehensive testing strategy for the newly migrated `ai-system` components. It's designed for execution by an AI agent, with clear steps, prerequisites, and validation criteria. Tests are categorized by type and can be run incrementally.

## Prerequisites
- Python 3.8+ environment
- Ollama installed and running (for LLM tests)
- `ai-system` repository cloned and checked out to the latest commit
- All dependencies installed (if any, e.g., via `pip install -r requirements.txt` if it exists)

## 1. Code Compilation and Import Tests
**Purpose:** Ensure all new modules compile and import correctly without syntax errors.

**Steps:**
1. Compile all new Python files:
   - `controller/runtime.py`
   - `controller/context.py`
   - `tools/base.py`
   - `tools/provider_tool.py`
   - `tools/file_read.py`
   - `tools/file_write.py`
   - `tools/system_info.py`
   - `llm.py`
   - All files in `tests/`

2. Import all new modules in a Python session:
   - `from controller.runtime import AgentRuntime`
   - `from controller.context import ContextManager`
   - `from tools.base import ToolRegistry, Tool`
   - `from tools.provider_tool import ProviderTool`
   - `from tools.file_read import FileReadTool`
   - `from tools.file_write import FileWriteTool`
   - `from tools.system_info import SystemInfoTool`
   - `from llm import OllamaLLM`

**Validation:** No exceptions during compilation or imports. Log any errors for review.

## 2. Unit Tests
**Purpose:** Test individual components in isolation.

**Steps:**
1. Run existing unit tests:
   - Execute `tests/test_context.py`
   - Execute `tests/test_file_read_tool.py`
   - Execute `tests/test_tool_registry.py`
   - Execute `tests/test_file_write_tool.py`
   - Execute `tests/test_system_info_tool.py`

2. For each test file, check:
   - All functions pass without exceptions
   - Output matches expected results (e.g., file contents, tool execution)

**Validation:** All tests pass. If pytest is available, use `pytest tests/`; otherwise, run each file manually with `python -m tests.test_*.py`.

## 3. Tool Registry Integration Tests
**Purpose:** Verify tool registration, execution, and safety.

**Steps:**
1. Create a test script that:
   - Initializes `ToolRegistry` with a temporary safe directory
   - Registers all tools: `ProviderTool`, `FileReadTool`, `FileWriteTool`, `SystemInfoTool`
   - Tests tool listing and function definition generation
   - Executes each tool with valid parameters
   - Tests safety: Attempt to access files outside safe directory (should fail)

2. Run the script and capture output.

**Validation:** Tools register correctly, execute successfully, and enforce sandboxing. No unauthorized file access.

## 4. Context Manager Tests
**Purpose:** Test conversation history, token budgeting, and tool result integration.

**Steps:**
1. Create a test script that:
   - Initializes `ContextManager` with max_messages=10, token_budget=1000
   - Adds multiple user/assistant messages
   - Adds tool results
   - Tests pruning old messages
   - Tests token estimation and budget checking

2. Run the script and verify behavior.

**Validation:** Context tracks history correctly, prunes as expected, and estimates tokens accurately.

## 5. LLM Wrapper Tests
**Purpose:** Test Ollama integration without full runtime.

**Steps:**
1. Create a test script that:
   - Initializes `OllamaLLM` with test model (e.g., "llama3.2:3b")
   - Sends a simple chat message without tools
   - Tests tool definition passing (mock tools)
   - Verifies response parsing

2. Run the script (requires Ollama running).

**Validation:** LLM responds to prompts, handles tool definitions, and parses responses correctly.

## 6. Agent Runtime Integration Tests
**Purpose:** Test the full runtime loop with mocked components.

**Steps:**
1. Create a test script that:
   - Initializes `AgentRuntime` with mock LLM (or real if Ollama available)
   - Runs a simple task (e.g., "What is 2+2?")
   - Verifies context updates and tool execution (if triggered)
   - Tests error handling for invalid tasks

2. Run the script and check logs/context state.

**Validation:** Runtime processes tasks, updates context, and handles errors gracefully.

## 7. End-to-End Task Execution Tests
**Purpose:** Test full task queue processing.

**Steps:**
1. Set up a test task queue with sample tasks:
   - Simple prompt: "Hello world"
   - Tool-requiring prompt: "Read this file" (with a test file in safe dir)
   - Invalid prompt: Empty or malformed

2. Run `run_agent.py` with the test queue.

3. Check:
   - Task completion status
   - Log output for errors/success
   - Context and tool result persistence

**Validation:** Tasks process correctly, provider routing works, and system remains stable.

## 8. Safety and Sandboxing Tests
**Purpose:** Ensure no unauthorized operations.

**Steps:**
1. Test file tools with paths outside safe directory.
2. Test tool approval callback with dangerous operations.
3. Attempt to execute system commands via tools (should be blocked).

**Validation:** All safety checks pass; no external file access or command execution.

## 9. Performance and Load Tests
**Purpose:** Check runtime under load.

**Steps:**
1. Run multiple concurrent tasks.
2. Test with large context windows.
3. Monitor memory usage and response times.

**Validation:** System handles load without crashes or excessive resource use.

## 10. Documentation and Code Quality Checks
**Purpose:** Ensure maintainability.

**Steps:**
1. Verify all new files have docstrings.
2. Check that `docs/agent_design.md` and `docs/system_notes.md` are up-to-date.
3. Run any linters (e.g., flake8, black) if available.

**Validation:** Code is documented, formatted, and follows conventions.

## Execution Order
- Start with 1-2 (compilation/imports and unit tests).
- Then 3-5 (integration).
- Finally 6-10 (full system and quality).

## Reporting
After each test phase, log results with pass/fail status and any error details. If failures occur, provide root cause analysis and fix suggestions.