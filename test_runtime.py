import sys
import os
import tempfile
from pathlib import Path

sys.path.insert(0, '.')
os.environ['AI_SYSTEM_MODEL'] = 'llama3.1:8b'

from controller.runtime import AgentRuntime

print('=== Testing Agent Runtime with llama3.1:8b ===\n')

with tempfile.TemporaryDirectory() as tmpdir:
    safe_dir = Path(tmpdir)
    
    print('1. Initializing runtime...')
    runtime = AgentRuntime(
        safe_dir=str(safe_dir),
        max_turns=5,
        context_window=10,
        token_budget=5000
    )
    print(f'   Runtime initialized with model: {runtime.llm.model}')
    print(f'   Tools available: {runtime.tools.list_tools()}\n')
    
    print('2. Testing simple task...')
    result = runtime.run_task({'prompt': 'What is 2+2? Answer with just the number.'})
    print(f'   Success: {result["success"]}')
    if result['result']:
        print(f'   Response: {result["result"][:100]}')
    
    print('\n✅ Agent Runtime test complete!')
