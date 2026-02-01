# Statement-to-Reality Engine

This is the execution engine for the AI Game Saves framework.

## What It Does

Takes natural language statements and produces:
- System requirements
- Architecture definitions
- Working code (Python, Rust, Go, TypeScript, Java, C++)
- Deployment configurations

## Core Components

```
engine/
├── statement_reality_system.py   # Abstract interfaces (n-1 state)
├── conversation_processor.py     # Concrete implementation (n state)
└── multi_language_generator.py   # Code generation for 6 languages
```

## How Builds Use The Engine

| Build | Uses Engine For |
|-------|-----------------|
| Wizard | Statement → Architecture → Artifacts |
| Warrior | Architecture → Deployment → Execution |
| Ranger | Quick prototyping with templates |
| Paladin | Architecture documentation |
| Rogue | Infrastructure code generation |

## Usage

```python
from statement_reality_system import *
from conversation_processor import *
from multi_language_generator import create_multi_language_generator

# Parse statement
statement = "Create a todo app with auth"

# Generate architecture
parser = ConcreteConversationalParser()
inference = ConcreteArchitecturalInference()
requirements = parser.parse_statements(...)
architecture = inference.infer_architecture(requirements)

# Generate code
gen = create_multi_language_generator()
python_code = gen.generate_code(architecture, 'python', 'fastapi')
rust_code = gen.generate_code(architecture, 'rust', 'axum')
```

## The n-1/n Pattern

- **n-1 state**: Abstract interfaces only (statement_reality_system.py)
- **n state**: Concrete implementations (conversation_processor.py)

Never implement at n-1. Only implement at n.
