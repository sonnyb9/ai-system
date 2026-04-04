# Agent Design and Runtime Architecture

## Overview

This document describes the `ai-system` runtime architecture, including the new agent runtime, tool registry, and provider integration.

The goal is to make `ai-system` more capable and flexible by adopting a structured agent design:

- `controller/runtime.py` — runtime orchestration layer
- `controller/context.py` — conversation context manager
- `tools/base.py` — generic tool abstraction and registry
- `tools/provider_tool.py` — provider routing via tool execution
- `tools/file_read.py` — safe read tool
- `tools/file_write.py` — safe write tool
- `tools/system_info.py` — system metadata tool
- `llm.py` — Ollama chat and tool calling wrapper

---

## Architecture

`ai-system` now supports a layered agent architecture:

1. **Runtime**
   - Orchestrates tasks, context, tools, and LLM interaction.
   - Uses `AgentRuntime` in `controller/runtime.py`.

2. **Context**
   - Tracks messages, tool results, and budgeted conversation state.
   - Implemented in `controller/context.py`.

3. **Tool Registry**
   - Registers available tools at runtime.
   - Provides function definitions for LLM tool calling.
   - Implemented in `tools/base.py`.

4. **Tools**
   - Concrete operations that the agent can call.
   - Current tools:
     - `call_provider` — routes prompt through provider chain
     - `file_read` — safe file read access
     - `file_write` — safe file write access
     - `system_info` — environment and system metadata

5. **LLM Integration**
   - `llm.py` wraps Ollama chat completion calls.
   - Supports tool calling through function definitions.

---

## Runtime Flow

1. A task enters `run_agent.py` from `tasks/task_queue.json`.
2. `AgentRuntime` adds the prompt to `ContextManager`.
3. The runtime calls `OllamaLLM.generate(...)` with current context and tool definitions.
4. If the LLM requests a tool, `AgentRuntime` executes it via `ToolRegistry`.
5. Tool results are added back into the context.
6. The loop repeats until the LLM returns plain text.

This enables multi-step, tool-driven workflows while preserving provider routing.

---

## Provider Routing

Provider calls are now exposed as a tool through `tools/provider_tool.py`.

- The provider tool wraps the existing `AgentController` provider selection logic.
- This preserves the current routing behavior from `agents/*.json` and `routing/routing.json`.
- The runtime can now execute provider queries as part of the LLM tool loop.

---

## Tool Safety and Sandbox

`AgentRuntime` constructs tools with a `safe_dir`.

- `file_read` and `file_write` are restricted to this safe directory.
- Tool approval is handled through the registry callback.

This is a foundation for later enhancements such as per-agent allowlists and risk policies.

---

## Future Enhancements

Potential next steps:

- Add a `tool_allowlist` system driven by `agents/*.json`.
- Add runtime policy enforcement for dangerous tools.
- Add `system_info` to agent metadata and diagnostic dashboards.
- Add tests for tool loop behavior and provider retries.
