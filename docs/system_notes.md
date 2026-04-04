# System Notes

## Current state

The `ai-system` repository now includes a lightweight agent runtime architecture inspired by `selfhosted-agent`.

Key additions:

- `controller/runtime.py`: Agent runtime orchestrates context, tools, and LLM interactions.
- `controller/context.py`: Conversation context manager with message history and token budget tracking.
- `tools/base.py`: Generic tool abstraction and registry.
- `tools/provider_tool.py`: Provider routing exposed as a callable tool.
- `tools/file_read.py`: Safe, read-only file access tool.
- `tools/file_write.py`: Safe, write access tool.
- `tools/system_info.py`: System environment and runtime metadata tool.
- `llm.py`: Ollama chat wrapper enabling tool definitions.
- `docs/agent_design.md`: Detailed agent design and runtime architecture documentation.

## Purpose

These changes make `ai-system` more capable of handling multi-step tool-driven workflows while preserving the current provider routing model.

The runtime can now:

- execute tools from an LLM tool-call loop
- add tool results back into context
- route prompts through configured Ollama providers
- enforce safe file access boundaries

## Notes for future work

- Add per-agent tool allowlists from `agents/*.json`
- Add policy enforcement for dangerous tool actions
- Add tests for the runtime loop and tool execution
- Add `README` or top-level documentation index if needed
