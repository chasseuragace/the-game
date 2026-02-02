# Statement-to-Reality System (Refactored)

**Transform natural language into running code.**

## The Key Insight

The original v7 system had hardcoded keyword matching that looked intelligent but wasn't. 

This refactored version fixes that by:

1. **Generating real prompts** instead of hardcoded if/else
2. **Using LLMs for actual intelligence** (not simulating it)
3. **Working in two modes**: internal (API) or external (IDE)

## How It Works

```
Statement
    │
    ▼
┌─────────────────┐
│ Parse Prompt    │ ──► [LLM] ──► Requirements
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Arch Prompt     │ ──► [LLM] ──► Architecture  
└─────────────────┘
    │
    ▼
┌─────────────────┐
│ Code Prompt     │ ──► [LLM] ──► Running Code
└─────────────────┘
```

The `[LLM]` can be:
- **Internal**: Claude API, OpenAI API (with keys)
- **External**: Your IDE (Claude, Cursor, Copilot) - YOU are the LLM

## Two Modes

### 1. Internal Mode (API)

```python
# With ANTHROPIC_API_KEY or OPENAI_API_KEY set
from pipeline import process_statement

result = process_statement("Create a todo app with auth")

print(result.requirements.functional)  # Extracted requirements
print(result.architecture.component_names())  # Designed architecture
print(result.code["python"].files)  # Generated code
```

### 2. External Mode (IDE is the LLM)

```python
from pipeline import StatementToRealityPipeline

# Force external mode
pipeline = StatementToRealityPipeline(mode="external")
result = pipeline.process("Create a todo app with auth")

# Get the prompt that needs processing
prompt = pipeline.get_current_prompt()
print(prompt["prompt"])  # This is what YOU (the IDE) process

# After YOU process it, provide the response
pipeline.provide_response(your_json_response)

# Continue to next step...
```

In external mode, the system generates prompts that YOU process using your IDE's LLM capabilities.

## File Structure

```
v7-refactored/
├── core/
│   ├── models.py         # Data structures (no logic)
│   └── llm_interface.py  # Unified LLM interface (internal/external)
├── prompts/
│   └── core_prompts.py   # THE ACTUAL INTELLIGENCE
├── generators/           # Code generation (uses prompts)
├── pipeline.py           # Main flow
├── demo.py              # Working demonstration
└── README.md
```

## The Prompts (Where Intelligence Lives)

See `prompts/core_prompts.py`:

- `parse_requirements()` - Extracts structured requirements from conversation
- `infer_architecture()` - Designs system architecture from requirements
- `generate_full_application()` - Generates complete working code

These prompts ARE the system. Without LLM processing, they're just text. With LLM processing, they create real systems.

## Running the Demo

```bash
cd v7-refactored
python demo.py
```

This shows:
1. What prompts are generated
2. How external mode works
3. A simulated full flow

## With API Keys (Full Power)

```bash
export ANTHROPIC_API_KEY="your-key"
# or
export OPENAI_API_KEY="your-key"

python demo.py  # Now runs in internal mode
```

## Using From IDE (Claude, Cursor, etc.)

1. Load the `pipeline.py` and `prompts/core_prompts.py`
2. Create a conversation/statement
3. Generate the parsing prompt
4. Process it yourself (you ARE the LLM)
5. Feed results back to continue

This is what you're doing RIGHT NOW - reading this system, understanding its prompts, and being the intelligence that makes it work.

## The Philosophy

> "Without an LLM in the loop, they are just well-fabricated magic."

The original v7 had:
- Hardcoded keyword matching
- Placeholder code generation
- Simulated intelligence

This refactored version has:
- Real prompts that require real LLM processing
- No fake intelligence
- Works with any LLM (API or IDE)

The system is honest about what it needs: **LLM processing at each step**.

## What This Enables

1. **IDE as LLM**: Your coding environment becomes the intelligence
2. **Transparent Flow**: You see exactly what's being asked
3. **Debuggable**: Every step is a clear prompt/response
4. **Extensible**: Add new prompts for new capabilities
5. **Honest**: No hidden magic, no simulated intelligence

## Next Steps

1. Add more prompts (testing, documentation, deployment)
2. Build prompt chains for complex systems
3. Create IDE integrations that streamline external mode
4. Add memory/context for multi-session development

---

*"The intelligence isn't in the code. It's in the prompts. The code just orchestrates."*
