#!/usr/bin/env python3
"""
Statement-to-Reality Demo

This demonstrates the refactored system in action.

The system can work in two modes:
1. INTERNAL: With API key, calls LLM directly
2. EXTERNAL: Without API key, generates prompts for IDE processing

Run this to see how it works.
"""

import sys
import json
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.models import Statement, Conversation, Requirements, Architecture, Component
from core.llm_interface import get_llm, LLMInterface
from prompts.core_prompts import parse_requirements, infer_architecture, generate_full_application
from pipeline import StatementToRealityPipeline, process_statement, process_with_ide


def demo_internal_mode():
    """Demo with internal LLM (requires API key)."""
    print("=" * 60)
    print("INTERNAL MODE DEMO")
    print("=" * 60)
    
    llm = get_llm("auto")
    
    if not llm.is_internal():
        print("No API key found. Skipping internal mode demo.")
        print("Set ANTHROPIC_API_KEY or OPENAI_API_KEY to enable.")
        return
    
    print(f"Using: {llm.get_mode()}")
    
    # Process a statement
    statement = "Create a todo application with user authentication and real-time updates"
    print(f"\nStatement: {statement}\n")
    
    result = process_statement(statement)
    
    print("REQUIREMENTS:")
    print(f"  Functional: {result.requirements.functional}")
    print(f"  Entities: {result.requirements.entities}")
    
    print("\nARCHITECTURE:")
    print(f"  Components: {result.architecture.component_names()}")
    print(f"  Patterns: {result.architecture.patterns}")
    
    print("\nGENERATED CODE:")
    for lang, code in result.code.items():
        print(f"  {lang}/{code.framework}:")
        print(f"    Files: {list(code.files.keys())}")
        print(f"    Run: {code.run_command}")


def demo_external_mode():
    """Demo in external/IDE mode."""
    print("=" * 60)
    print("EXTERNAL MODE DEMO (IDE is the LLM)")
    print("=" * 60)
    
    statement = "Create a todo application with user authentication"
    print(f"\nStatement: {statement}\n")
    
    # Start pipeline in external mode
    pipeline = StatementToRealityPipeline(mode="external")
    result = pipeline.process(statement)
    
    print("Pipeline paused - needs LLM processing.\n")
    
    # Get the prompt that needs processing
    prompt_info = pipeline.get_current_prompt()
    
    if prompt_info:
        print(f"STEP: {prompt_info['step']}")
        print("-" * 40)
        print("SYSTEM PROMPT:")
        print(prompt_info['system'][:200] + "...")
        print()
        print("USER PROMPT:")
        print(prompt_info['prompt'][:500] + "...")
        print()
        print(f"EXPECTED FORMAT: {prompt_info['expected_format']}")
        print("-" * 40)
        print()
        print("In IDE mode, YOU (the IDE LLM) process this prompt.")
        print("Then call: pipeline.provide_response(your_response)")
        print()


def demo_prompt_generation():
    """Demo: Show what prompts the system generates."""
    print("=" * 60)
    print("PROMPT GENERATION DEMO")
    print("=" * 60)
    
    # Create a conversation
    conv = Conversation(
        statements=[
            Statement(content="I need a REST API for managing products"),
            Statement(content="It should have CRUD operations"),
            Statement(content="Include authentication with JWT"),
            Statement(content="Use PostgreSQL for storage")
        ]
    )
    
    print("\nCONVERSATION:")
    print(conv.as_text())
    print()
    
    # Generate parsing prompt
    print("=" * 40)
    print("STEP 1: REQUIREMENTS EXTRACTION PROMPT")
    print("=" * 40)
    req_prompt = parse_requirements(conv)
    print(f"System: {req_prompt.system_prompt[:100]}...")
    print()
    print(f"Prompt:\n{req_prompt.prompt[:800]}...")
    print()
    
    # Simulate requirements (what an LLM would return)
    requirements = Requirements(
        functional=[
            "CRUD operations for products",
            "JWT authentication",
            "RESTful API endpoints"
        ],
        non_functional=["Secure", "Fast"],
        constraints=["Use PostgreSQL"],
        entities=["Product", "User", "Auth"]
    )
    
    print("=" * 40)
    print("STEP 2: ARCHITECTURE INFERENCE PROMPT")
    print("=" * 40)
    arch_prompt = infer_architecture(requirements)
    print(f"Prompt:\n{arch_prompt.prompt[:800]}...")
    print()
    
    # Simulate architecture
    architecture = Architecture(
        components=[
            Component(name="ProductService", type="service", 
                     responsibilities=["Product CRUD"], interfaces=["create", "read", "update", "delete"]),
            Component(name="AuthService", type="service",
                     responsibilities=["JWT auth"], interfaces=["login", "verify"]),
            Component(name="APIGateway", type="gateway",
                     responsibilities=["Routing", "Auth middleware"], interfaces=["route"]),
            Component(name="Database", type="database",
                     responsibilities=["Data storage"], interfaces=["query"])
        ],
        patterns=["Microservices", "API Gateway", "JWT Authentication"],
        tech_stack={"backend": ["Python", "FastAPI"], "database": ["PostgreSQL"]}
    )
    
    print("=" * 40)
    print("STEP 3: CODE GENERATION PROMPT")
    print("=" * 40)
    code_prompt = generate_full_application(architecture, "python", "fastapi")
    print(f"Prompt:\n{code_prompt.prompt[:1000]}...")
    print()


def demo_full_flow_simulation():
    """Demo: Simulate the full flow with mock LLM responses."""
    print("=" * 60)
    print("FULL FLOW SIMULATION")
    print("=" * 60)
    
    statement = "Create a simple user management API"
    print(f"\nInput: {statement}\n")
    
    # Create pipeline in external mode
    pipeline = StatementToRealityPipeline(mode="external")
    
    # Start processing (will pause at first LLM call)
    pipeline.process(statement)
    
    # Simulate LLM response for requirements
    print("Step 1: Providing requirements response...")
    pipeline.provide_response(json.dumps({
        "functional": ["User CRUD operations", "User authentication"],
        "non_functional": ["Fast response times"],
        "constraints": [],
        "business_rules": [],
        "entities": ["User"]
    }))
    print(f"  Requirements extracted: {pipeline.requirements.functional}")
    
    # Continue to architecture
    pipeline._step_infer_architecture()
    
    # Simulate LLM response for architecture
    print("\nStep 2: Providing architecture response...")
    pipeline.provide_response(json.dumps({
        "components": [
            {"name": "UserService", "type": "service", 
             "responsibilities": ["User CRUD"], "interfaces": ["create", "get", "update", "delete"], "dependencies": []},
            {"name": "AuthService", "type": "service",
             "responsibilities": ["Authentication"], "interfaces": ["login", "logout"], "dependencies": ["UserService"]},
            {"name": "APIGateway", "type": "gateway",
             "responsibilities": ["Routing"], "interfaces": ["route"], "dependencies": ["UserService", "AuthService"]}
        ],
        "patterns": ["Microservices", "API Gateway"],
        "relationships": {"APIGateway": ["UserService", "AuthService"]},
        "tech_stack": {"backend": ["Python", "FastAPI"]},
        "quality_attributes": {"scalability": "horizontal"}
    }))
    print(f"  Architecture: {pipeline.architecture.component_names()}")
    
    # Continue to code generation
    pipeline._step_generate_code("python", "fastapi")
    
    # Simulate LLM response for code
    print("\nStep 3: Providing code response...")
    pipeline.provide_response(json.dumps({
        "files": {
            "main.py": '''from fastapi import FastAPI
from routes import user_router, auth_router

app = FastAPI(title="User Management API")
app.include_router(user_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")

@app.get("/health")
def health():
    return {"status": "healthy"}
''',
            "routes/users.py": '''from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def list_users():
    return []

@router.post("/")  
def create_user(user: dict):
    return user
''',
            "requirements.txt": "fastapi\nuvicorn\n"
        },
        "entry_point": "main.py",
        "run_command": "uvicorn main:app --reload",
        "dependencies": ["fastapi", "uvicorn"]
    }))
    
    print(f"  Generated files: {list(pipeline.code.get('python', {}).files.keys()) if pipeline.code else 'None'}")
    
    # Show result
    print("\n" + "=" * 40)
    print("FINAL RESULT")
    print("=" * 40)
    
    result = pipeline._create_result(success=True)
    print(f"Success: {result.success}")
    print(f"Requirements: {len(result.requirements.functional)} functional")
    print(f"Architecture: {len(result.architecture.components)} components")
    print(f"Code: {len(result.code)} languages")
    
    if result.code.get("python"):
        print("\nGenerated main.py:")
        print("-" * 40)
        print(result.code["python"].files.get("main.py", "N/A"))


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("STATEMENT-TO-REALITY SYSTEM - REFACTORED")
    print("=" * 60)
    print()
    print("This system transforms natural language into running code.")
    print("The intelligence comes from LLM processing.")
    print()
    
    # Check mode
    llm = get_llm("auto")
    print(f"Mode detected: {llm.get_mode()}")
    print()
    
    # Run demos
    demo_prompt_generation()
    print("\n")
    
    demo_external_mode()
    print("\n")
    
    demo_full_flow_simulation()
    print("\n")
    
    # Try internal mode if available
    demo_internal_mode()
