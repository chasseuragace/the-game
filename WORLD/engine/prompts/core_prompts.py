"""
Prompts: The Intelligence of the System

These prompts are the actual "code" that makes the system intelligent.
Without these prompts being processed by an LLM, you just have scaffolding.

Each function returns an LLMRequest that can be:
1. Sent to an LLM API (internal mode)
2. Presented to an IDE/human for processing (external mode)
"""

from typing import List, Dict, Any
from core.models import (
    LLMRequest, Conversation, Requirements, Architecture, Component
)


# =============================================================================
# PARSING PROMPTS - Extract structure from natural language
# =============================================================================

def parse_requirements(conversation: Conversation) -> LLMRequest:
    """
    Generate prompt to extract requirements from conversation.
    
    This is the first step: turning natural language into structured requirements.
    """
    return LLMRequest(
        system_prompt="""You are an expert requirements analyst and software architect.
Your job is to extract structured requirements from natural language conversations.
Be thorough but precise. Extract only what is stated or clearly implied.""",
        
        prompt=f"""Analyze this conversation and extract structured requirements for a software system.

CONVERSATION:
{conversation.as_text()}

Extract and categorize into:

1. FUNCTIONAL REQUIREMENTS
   - What the system should DO
   - Features, capabilities, behaviors
   - User actions and system responses

2. NON-FUNCTIONAL REQUIREMENTS  
   - How the system should PERFORM
   - Performance, scalability, security, reliability
   - Quality attributes

3. CONSTRAINTS
   - Technical limitations or mandates
   - Technology choices specified
   - Budget, timeline, compliance requirements

4. BUSINESS RULES
   - Domain-specific logic
   - Policies and regulations
   - Validation rules

5. ENTITIES
   - Key nouns that represent data/services
   - Examples: User, Order, Payment, Product, Message
   - These become components/services

Return as JSON:
```json
{{
  "functional": ["requirement 1", "requirement 2"],
  "non_functional": ["requirement 1", "requirement 2"],
  "constraints": ["constraint 1", "constraint 2"],
  "business_rules": ["rule 1", "rule 2"],
  "entities": ["Entity1", "Entity2"]
}}
```

Be specific. Don't add requirements that aren't stated or implied.""",
        
        expected_format="json",
        temperature=0.3  # Lower temperature for more precise extraction
    )


def identify_statement_types(statements: List[str]) -> LLMRequest:
    """Generate prompt to categorize statements by type."""
    statements_text = "\n".join([f"{i}: {s}" for i, s in enumerate(statements)])
    
    return LLMRequest(
        system_prompt="You are an expert at analyzing natural language statements.",
        
        prompt=f"""Categorize each statement by its primary type.

STATEMENTS:
{statements_text}

CATEGORIES:
- functional: Describes what the system should do
- non_functional: Describes quality attributes (performance, security, etc.)
- constraint: Specifies a limitation or requirement
- business_rule: Describes domain logic
- preference: A nice-to-have, not mandatory
- meta: About the conversation/system itself, not requirements

Return as JSON mapping statement index to category:
```json
{{
  "0": "functional",
  "1": "constraint",
  ...
}}
```""",
        
        expected_format="json",
        temperature=0.2
    )


# =============================================================================
# ARCHITECTURE PROMPTS - Design system from requirements
# =============================================================================

def infer_architecture(requirements: Requirements) -> LLMRequest:
    """
    Generate prompt to infer architecture from requirements.
    
    This is the core transformation: requirements -> architecture.
    """
    reqs_json = {
        "functional": requirements.functional,
        "non_functional": requirements.non_functional,
        "constraints": requirements.constraints,
        "business_rules": requirements.business_rules,
        "entities": requirements.entities
    }
    
    return LLMRequest(
        system_prompt="""You are an expert software architect with deep knowledge of:
- Microservices and distributed systems
- API design and patterns
- Database design
- Cloud architecture
- Security best practices

Design clean, maintainable, scalable architectures.""",
        
        prompt=f"""Design a system architecture based on these requirements.

REQUIREMENTS:
```json
{__import__('json').dumps(reqs_json, indent=2)}
```

Design the architecture with:

1. COMPONENTS
   - Services, APIs, databases, gateways
   - Each component should have single responsibility
   - Name them clearly (UserService, OrderAPI, PaymentGateway, etc.)

2. RELATIONSHIPS
   - How components communicate
   - Dependencies between components
   - Data flow

3. PATTERNS
   - Architectural patterns to apply
   - Examples: Microservices, Event-Driven, CQRS, API Gateway, etc.

4. TECHNOLOGY STACK
   - Backend framework
   - Database
   - Message queue (if needed)
   - Infrastructure

Return as JSON:
```json
{{
  "components": [
    {{
      "name": "ComponentName",
      "type": "service|api|database|gateway|queue",
      "responsibilities": ["responsibility 1", "responsibility 2"],
      "interfaces": ["method1", "method2"],
      "dependencies": ["OtherComponent"]
    }}
  ],
  "patterns": ["Pattern1", "Pattern2"],
  "relationships": {{
    "ComponentA": ["ComponentB", "ComponentC"]
  }},
  "tech_stack": {{
    "backend": ["Python", "FastAPI"],
    "database": ["PostgreSQL"],
    "infrastructure": ["Docker", "Kubernetes"]
  }},
  "quality_attributes": {{
    "scalability": "horizontal",
    "availability": "99.9%"
  }}
}}
```

Design for the requirements given. Don't over-engineer.""",
        
        expected_format="json",
        temperature=0.5
    )


def validate_architecture(architecture: Architecture, requirements: Requirements) -> LLMRequest:
    """Generate prompt to validate architecture against requirements."""
    arch_json = {
        "components": [c.name for c in architecture.components],
        "patterns": architecture.patterns,
        "tech_stack": architecture.tech_stack
    }
    reqs_json = {
        "functional": requirements.functional,
        "non_functional": requirements.non_functional,
        "constraints": requirements.constraints
    }
    
    return LLMRequest(
        system_prompt="You are an expert architecture reviewer.",
        
        prompt=f"""Validate this architecture against the requirements.

ARCHITECTURE:
```json
{__import__('json').dumps(arch_json, indent=2)}
```

REQUIREMENTS:
```json
{__import__('json').dumps(reqs_json, indent=2)}
```

Check:
1. Does every functional requirement have a component to handle it?
2. Are non-functional requirements addressed?
3. Are constraints satisfied?
4. Is the architecture consistent?

Return as JSON:
```json
{{
  "valid": true|false,
  "score": 0.0-1.0,
  "covered_requirements": ["req1", "req2"],
  "uncovered_requirements": ["req3"],
  "issues": ["issue1", "issue2"],
  "suggestions": ["suggestion1"]
}}
```""",
        
        expected_format="json",
        temperature=0.3
    )


# =============================================================================
# CODE GENERATION PROMPTS - Generate actual code
# =============================================================================

def generate_component_code(
    component: Component, 
    architecture: Architecture,
    language: str,
    framework: str
) -> LLMRequest:
    """
    Generate prompt to create code for a specific component.
    
    This generates REAL, WORKING code - not scaffolds.
    """
    comp_json = {
        "name": component.name,
        "type": component.type,
        "responsibilities": component.responsibilities,
        "interfaces": component.interfaces,
        "dependencies": component.dependencies
    }
    
    context = {
        "other_components": [c.name for c in architecture.components if c.name != component.name],
        "patterns": architecture.patterns,
        "tech_stack": architecture.tech_stack
    }
    
    return LLMRequest(
        system_prompt=f"""You are an expert {language} developer specializing in {framework}.
Write clean, production-ready code. Include:
- Proper error handling
- Type hints/annotations
- Documentation
- Logging where appropriate""",
        
        prompt=f"""Generate the complete code for this component.

COMPONENT:
```json
{__import__('json').dumps(comp_json, indent=2)}
```

CONTEXT:
```json
{__import__('json').dumps(context, indent=2)}
```

LANGUAGE: {language}
FRAMEWORK: {framework}

Generate:
1. The main component file with all methods implemented
2. Models/types needed
3. Any helper functions

The code should be:
- Complete and runnable
- Following {framework} best practices
- Properly typed
- With error handling

Return as JSON:
```json
{{
  "files": {{
    "filename.py": "file content here",
    "models.py": "models here"
  }},
  "dependencies": ["package1", "package2"]
}}
```

Write REAL implementations, not placeholders or TODOs.""",
        
        expected_format="json",
        temperature=0.4
    )


def generate_api_endpoints(
    architecture: Architecture,
    language: str,
    framework: str
) -> LLMRequest:
    """Generate prompt to create API endpoints."""
    components = [
        {"name": c.name, "interfaces": c.interfaces, "type": c.type}
        for c in architecture.components
    ]
    
    return LLMRequest(
        system_prompt=f"""You are an expert API developer.
Design clean, RESTful APIs with proper:
- HTTP methods (GET, POST, PUT, DELETE)
- Status codes
- Request/response models
- Validation
- Error handling""",
        
        prompt=f"""Generate API endpoints for this architecture.

COMPONENTS:
```json
{__import__('json').dumps(components, indent=2)}
```

LANGUAGE: {language}
FRAMEWORK: {framework}

Create:
1. Main application file with all routes
2. Request/response models
3. Dependency injection setup
4. Error handlers

Return as JSON:
```json
{{
  "files": {{
    "main.py": "complete main file",
    "routes/user_routes.py": "user routes",
    "models/request_models.py": "pydantic models",
    "models/response_models.py": "response models"
  }},
  "dependencies": ["fastapi", "pydantic", "uvicorn"]
}}
```

Make it complete and runnable.""",
        
        expected_format="json",
        temperature=0.4
    )


def generate_full_application(
    architecture: Architecture,
    language: str,
    framework: str
) -> LLMRequest:
    """
    Generate prompt for complete application code.
    
    This is the big one - generates the entire application.
    """
    arch_json = {
        "components": [
            {
                "name": c.name,
                "type": c.type,
                "responsibilities": c.responsibilities,
                "interfaces": c.interfaces,
                "dependencies": c.dependencies
            }
            for c in architecture.components
        ],
        "patterns": architecture.patterns,
        "relationships": architecture.relationships,
        "tech_stack": architecture.tech_stack
    }
    
    return LLMRequest(
        system_prompt=f"""You are an expert full-stack developer.
Generate complete, production-ready {language}/{framework} applications.
Write real implementations, not scaffolds.
Include proper error handling, validation, and documentation.""",
        
        prompt=f"""Generate a complete {language} application using {framework}.

ARCHITECTURE:
```json
{__import__('json').dumps(arch_json, indent=2)}
```

Generate ALL files needed for a working application:

1. Main application entry point
2. All service/component implementations
3. Models and schemas
4. API routes/endpoints
5. Configuration
6. Database setup (if needed)
7. Dockerfile
8. Requirements/dependencies file
9. README with run instructions

Return as JSON:
```json
{{
  "files": {{
    "main.py": "complete main file with all code",
    "services/user_service.py": "complete service implementation",
    "models/user.py": "complete models",
    "routes/user_routes.py": "complete routes",
    "config.py": "configuration",
    "database.py": "database setup",
    "Dockerfile": "docker file",
    "requirements.txt": "dependencies",
    "README.md": "documentation"
  }},
  "entry_point": "main.py",
  "run_command": "uvicorn main:app --reload",
  "dependencies": ["fastapi", "uvicorn", "sqlalchemy"]
}}
```

CRITICAL: Write COMPLETE, WORKING code. No placeholders. No TODOs.
Each file should be fully implemented and runnable.""",
        
        expected_format="json",
        temperature=0.5
    )


# =============================================================================
# UTILITY PROMPTS
# =============================================================================

def suggest_improvements(architecture: Architecture) -> LLMRequest:
    """Generate prompt to suggest architecture improvements."""
    arch_summary = {
        "components": [c.name for c in architecture.components],
        "patterns": architecture.patterns,
        "tech_stack": architecture.tech_stack
    }
    
    return LLMRequest(
        system_prompt="You are a senior architect reviewing designs.",
        
        prompt=f"""Review this architecture and suggest improvements.

ARCHITECTURE:
```json
{__import__('json').dumps(arch_summary, indent=2)}
```

Consider:
1. Scalability improvements
2. Security enhancements
3. Performance optimizations
4. Maintainability
5. Missing components

Return as JSON:
```json
{{
  "improvements": [
    {{
      "area": "scalability",
      "suggestion": "Add caching layer",
      "priority": "high|medium|low"
    }}
  ],
  "missing_components": ["CacheService", "RateLimiter"],
  "overall_score": 0.0-1.0
}}
```""",
        
        expected_format="json",
        temperature=0.6
    )


def explain_architecture(architecture: Architecture) -> LLMRequest:
    """Generate prompt to explain the architecture in plain language."""
    arch_json = {
        "components": [
            {"name": c.name, "type": c.type, "responsibilities": c.responsibilities}
            for c in architecture.components
        ],
        "patterns": architecture.patterns,
        "relationships": architecture.relationships
    }
    
    return LLMRequest(
        system_prompt="You are a technical writer explaining systems to developers.",
        
        prompt=f"""Explain this architecture in clear, plain language.

ARCHITECTURE:
```json
{__import__('json').dumps(arch_json, indent=2)}
```

Write:
1. A brief overview (2-3 sentences)
2. Explanation of each component and why it exists
3. How data flows through the system
4. Key design decisions and their rationale

Return as plain text (not JSON) suitable for a README.""",
        
        expected_format="text",
        temperature=0.7
    )
