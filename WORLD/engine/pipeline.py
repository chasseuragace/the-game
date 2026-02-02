"""
Statement-to-Reality Pipeline

This is the main flow that transforms statements into running systems.

The pipeline can operate in two modes:

1. INTERNAL MODE (LLM API available):
   Statement -> [LLM] -> Requirements -> [LLM] -> Architecture -> [LLM] -> Code
   
2. EXTERNAL MODE (IDE is the LLM):
   Statement -> [Generate Prompts] -> [Human/IDE processes] -> [Continue pipeline]

The key insight: The intelligence comes from LLM processing.
This pipeline orchestrates WHAT to ask, the LLM provides the intelligence.
"""

import json
from typing import Optional, Dict, List, Any
from dataclasses import asdict

from core.models import (
    Statement, Conversation, Requirements, Architecture, Component,
    GeneratedCode, PipelineResult, LLMRequest, LLMResponse
)
from core.llm_interface import LLMInterface, get_llm
from prompts.core_prompts import (
    parse_requirements,
    infer_architecture,
    validate_architecture,
    generate_full_application,
    generate_component_code,
    explain_architecture
)


class StatementToRealityPipeline:
    """
    Main pipeline for transforming statements into reality.
    
    Usage (Internal mode with API key):
        pipeline = StatementToRealityPipeline()
        result = pipeline.process("Create a todo app with auth")
        
    Usage (External mode with IDE):
        pipeline = StatementToRealityPipeline(mode="external")
        result = pipeline.process("Create a todo app with auth")
        prompts = pipeline.get_pending_prompts()
        # Process prompts with IDE, then:
        pipeline.provide_responses(responses)
        result = pipeline.continue_processing()
    """
    
    def __init__(self, mode: str = "auto"):
        """
        Initialize pipeline.
        
        Args:
            mode: "auto" (try API, fallback to external), "external" (IDE mode), 
                  "anthropic", or "openai"
        """
        self.llm = get_llm(mode)
        self.mode = self.llm.get_mode()
        
        # Pipeline state
        self.conversation: Optional[Conversation] = None
        self.requirements: Optional[Requirements] = None
        self.architecture: Optional[Architecture] = None
        self.code: Dict[str, GeneratedCode] = {}
        
        # For external mode
        self.pending_step: Optional[str] = None
        self.pending_request: Optional[LLMRequest] = None
    
    def process(self, input_text: str, language: str = "python", framework: str = "fastapi") -> PipelineResult:
        """
        Process a statement through the full pipeline.
        
        In internal mode: runs to completion.
        In external mode: runs until LLM processing needed, then pauses.
        """
        # Create conversation from input
        if isinstance(input_text, str):
            self.conversation = Conversation(
                statements=[Statement(content=input_text)],
                id="pipeline_conv"
            )
        else:
            self.conversation = input_text
        
        # Step 1: Parse requirements
        requirements_result = self._step_parse_requirements()
        if not requirements_result.success:
            return self._create_result(success=False, errors=[requirements_result.error or "Failed to parse requirements"])
        
        # Step 2: Infer architecture
        architecture_result = self._step_infer_architecture()
        if not architecture_result.success:
            return self._create_result(success=False, errors=[architecture_result.error or "Failed to infer architecture"])
        
        # Step 3: Generate code
        code_result = self._step_generate_code(language, framework)
        if not code_result.success:
            return self._create_result(success=False, errors=[code_result.error or "Failed to generate code"])
        
        return self._create_result(success=True)
    
    def _step_parse_requirements(self) -> LLMResponse:
        """Step 1: Parse requirements from conversation."""
        request = parse_requirements(self.conversation)
        response = self.llm.complete(request)
        
        if response.success:
            data = response.as_json()
            self.requirements = Requirements(
                functional=data.get("functional", []),
                non_functional=data.get("non_functional", []),
                constraints=data.get("constraints", []),
                business_rules=data.get("business_rules", []),
                entities=data.get("entities", [])
            )
        elif "EXTERNAL_PROCESSING_REQUIRED" in (response.error or ""):
            self.pending_step = "parse_requirements"
            self.pending_request = request
        
        return response
    
    def _step_infer_architecture(self) -> LLMResponse:
        """Step 2: Infer architecture from requirements."""
        if not self.requirements:
            return LLMResponse(content="", success=False, error="No requirements to process")
        
        request = infer_architecture(self.requirements)
        response = self.llm.complete(request)
        
        if response.success:
            data = response.as_json()
            
            # Parse components
            components = []
            for comp_data in data.get("components", []):
                components.append(Component(
                    name=comp_data.get("name", "Unknown"),
                    type=comp_data.get("type", "service"),
                    responsibilities=comp_data.get("responsibilities", []),
                    interfaces=comp_data.get("interfaces", []),
                    dependencies=comp_data.get("dependencies", [])
                ))
            
            self.architecture = Architecture(
                components=components,
                patterns=data.get("patterns", []),
                relationships=data.get("relationships", {}),
                tech_stack=data.get("tech_stack", {}),
                quality_attributes=data.get("quality_attributes", {})
            )
        elif "EXTERNAL_PROCESSING_REQUIRED" in (response.error or ""):
            self.pending_step = "infer_architecture"
            self.pending_request = request
        
        return response
    
    def _step_generate_code(self, language: str, framework: str) -> LLMResponse:
        """Step 3: Generate code from architecture."""
        if not self.architecture:
            return LLMResponse(content="", success=False, error="No architecture to process")
        
        request = generate_full_application(self.architecture, language, framework)
        response = self.llm.complete(request)
        
        if response.success:
            data = response.as_json()
            
            self.code[language] = GeneratedCode(
                language=language,
                framework=framework,
                files=data.get("files", {}),
                entry_point=data.get("entry_point", "main.py"),
                run_command=data.get("run_command", "python main.py"),
                dependencies=data.get("dependencies", [])
            )
        elif "EXTERNAL_PROCESSING_REQUIRED" in (response.error or ""):
            self.pending_step = "generate_code"
            self.pending_request = request
        
        return response
    
    def _create_result(self, success: bool, errors: List[str] = None) -> PipelineResult:
        """Create pipeline result."""
        return PipelineResult(
            conversation=self.conversation,
            requirements=self.requirements or Requirements(),
            architecture=self.architecture or Architecture(),
            code=self.code,
            success=success,
            errors=errors or [],
            llm_requests=self.llm.get_pending_prompts() if hasattr(self.llm, 'get_pending_prompts') else []
        )
    
    # =========================================================================
    # External Mode Methods
    # =========================================================================
    
    def get_pending_prompts(self) -> List[Dict[str, Any]]:
        """Get prompts that need external processing."""
        return self.llm.get_pending_prompts()
    
    def get_current_prompt(self) -> Optional[Dict[str, Any]]:
        """Get the current prompt that needs processing."""
        if self.pending_request:
            return {
                "step": self.pending_step,
                "system": self.pending_request.system_prompt,
                "prompt": self.pending_request.prompt,
                "expected_format": self.pending_request.expected_format
            }
        return None
    
    def provide_response(self, response_text: str) -> bool:
        """Provide response for pending prompt and continue."""
        if not self.pending_step:
            return False
        
        # Parse response based on step
        if self.pending_step == "parse_requirements":
            data = self._parse_json_response(response_text)
            self.requirements = Requirements(
                functional=data.get("functional", []),
                non_functional=data.get("non_functional", []),
                constraints=data.get("constraints", []),
                business_rules=data.get("business_rules", []),
                entities=data.get("entities", [])
            )
            
        elif self.pending_step == "infer_architecture":
            data = self._parse_json_response(response_text)
            components = []
            for comp_data in data.get("components", []):
                components.append(Component(
                    name=comp_data.get("name", "Unknown"),
                    type=comp_data.get("type", "service"),
                    responsibilities=comp_data.get("responsibilities", []),
                    interfaces=comp_data.get("interfaces", []),
                    dependencies=comp_data.get("dependencies", [])
                ))
            self.architecture = Architecture(
                components=components,
                patterns=data.get("patterns", []),
                relationships=data.get("relationships", {}),
                tech_stack=data.get("tech_stack", {}),
                quality_attributes=data.get("quality_attributes", {})
            )
            
        elif self.pending_step == "generate_code":
            data = self._parse_json_response(response_text)
            self.code["python"] = GeneratedCode(
                language="python",
                framework="fastapi",
                files=data.get("files", {}),
                entry_point=data.get("entry_point", "main.py"),
                run_command=data.get("run_command", "python main.py"),
                dependencies=data.get("dependencies", [])
            )
        
        self.pending_step = None
        self.pending_request = None
        return True
    
    def _parse_json_response(self, text: str) -> Dict:
        """Parse JSON from response text."""
        try:
            # Handle markdown code blocks
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            return json.loads(text.strip())
        except:
            return {}
    
    def export_for_ide(self) -> str:
        """Export current state for IDE processing."""
        output = "# Statement-to-Reality Pipeline\n\n"
        output += f"## Mode: {self.mode}\n\n"
        
        if self.conversation:
            output += "## Input Statement\n"
            output += f"```\n{self.conversation.as_text()}\n```\n\n"
        
        if self.pending_request:
            output += "## Current Step: " + self.pending_step + "\n\n"
            output += "### System Prompt\n"
            output += f"```\n{self.pending_request.system_prompt}\n```\n\n"
            output += "### Prompt\n"
            output += f"```\n{self.pending_request.prompt}\n```\n\n"
            output += f"### Expected Format: {self.pending_request.expected_format}\n\n"
            output += "---\n"
            output += "Process the above prompt and provide the response.\n"
        
        if self.requirements and not self.requirements.is_empty():
            output += "## Extracted Requirements\n"
            output += f"```json\n{json.dumps(asdict(self.requirements), indent=2)}\n```\n\n"
        
        if self.architecture and self.architecture.components:
            output += "## Architecture\n"
            output += f"Components: {self.architecture.component_names()}\n"
            output += f"Patterns: {self.architecture.patterns}\n\n"
        
        if self.code:
            output += "## Generated Code\n"
            for lang, code in self.code.items():
                output += f"### {lang}/{code.framework}\n"
                output += f"Files: {list(code.files.keys())}\n"
                output += f"Run: `{code.run_command}`\n\n"
        
        return output


# =============================================================================
# Convenience Functions
# =============================================================================

def process_statement(statement: str, language: str = "python", framework: str = "fastapi") -> PipelineResult:
    """
    Quick function to process a statement.
    
    Uses auto mode - will use API if available, otherwise external mode.
    """
    pipeline = StatementToRealityPipeline(mode="auto")
    return pipeline.process(statement, language, framework)


def process_with_ide(statement: str) -> Dict[str, Any]:
    """
    Process statement in IDE mode - returns prompts for external processing.
    
    Returns a dict with the prompt to process.
    The IDE (Claude, Cursor, etc.) processes the prompt.
    Then call continue_with_response() with the result.
    """
    pipeline = StatementToRealityPipeline(mode="external")
    result = pipeline.process(statement)
    
    return {
        "pipeline": pipeline,
        "current_prompt": pipeline.get_current_prompt(),
        "export": pipeline.export_for_ide()
    }


def continue_with_response(pipeline: StatementToRealityPipeline, response: str) -> Dict[str, Any]:
    """
    Continue pipeline with a response from external LLM.
    """
    pipeline.provide_response(response)
    
    # Try to continue to next step
    if not pipeline.architecture and pipeline.requirements:
        pipeline._step_infer_architecture()
    elif not pipeline.code and pipeline.architecture:
        pipeline._step_generate_code("python", "fastapi")
    
    return {
        "pipeline": pipeline,
        "current_prompt": pipeline.get_current_prompt(),
        "result": pipeline._create_result(success=bool(pipeline.code)),
        "export": pipeline.export_for_ide()
    }
