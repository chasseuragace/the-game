"""
Core Data Models for Statement-to-Reality System

These are pure data structures. No logic. No LLM calls.
They serve as the common language between all components.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime


class StatementType(Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    CONSTRAINT = "constraint"
    BUSINESS_RULE = "business_rule"
    PREFERENCE = "preference"
    META = "meta"


@dataclass
class Statement:
    """A single statement from a conversation."""
    content: str
    speaker: str = "human"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    statement_type: Optional[StatementType] = None
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Conversation:
    """A collection of statements."""
    statements: List[Statement]
    id: str = "conv_001"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def as_text(self) -> str:
        """Convert to plain text for LLM consumption."""
        return "\n".join([
            f"{s.speaker}: {s.content}" 
            for s in self.statements
        ])


@dataclass
class Requirements:
    """Extracted requirements from conversation."""
    functional: List[str] = field(default_factory=list)
    non_functional: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    business_rules: List[str] = field(default_factory=list)
    entities: List[str] = field(default_factory=list)  # user, todo, payment, etc.
    
    def is_empty(self) -> bool:
        return not any([
            self.functional, self.non_functional, 
            self.constraints, self.business_rules, self.entities
        ])


@dataclass
class Component:
    """An architectural component."""
    name: str
    type: str  # service, api, database, gateway, etc.
    responsibilities: List[str] = field(default_factory=list)
    interfaces: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Architecture:
    """System architecture."""
    components: List[Component] = field(default_factory=list)
    patterns: List[str] = field(default_factory=list)
    relationships: Dict[str, List[str]] = field(default_factory=dict)
    tech_stack: Dict[str, List[str]] = field(default_factory=dict)
    quality_attributes: Dict[str, str] = field(default_factory=dict)
    
    def component_names(self) -> List[str]:
        return [c.name for c in self.components]


@dataclass
class GeneratedCode:
    """Generated code for a single language."""
    language: str
    framework: str
    files: Dict[str, str]  # filename -> content
    entry_point: str
    run_command: str
    dependencies: List[str] = field(default_factory=list)


@dataclass
class LLMRequest:
    """A request to be processed by an LLM."""
    prompt: str
    system_prompt: str = ""
    expected_format: str = "json"  # json, text, code
    temperature: float = 0.7
    max_tokens: int = 4000
    
    def as_messages(self) -> List[Dict[str, str]]:
        """Convert to OpenAI/Anthropic message format."""
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": self.prompt})
        return messages


@dataclass
class LLMResponse:
    """Response from an LLM."""
    content: str
    raw: Any = None
    success: bool = True
    error: Optional[str] = None
    
    def as_json(self) -> Dict:
        """Parse content as JSON."""
        import json
        try:
            # Handle markdown code blocks
            text = self.content
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            return json.loads(text.strip())
        except:
            return {}


@dataclass 
class PipelineResult:
    """Result of the full pipeline."""
    conversation: Conversation
    requirements: Requirements
    architecture: Architecture
    code: Dict[str, GeneratedCode]  # language -> code
    success: bool = True
    errors: List[str] = field(default_factory=list)
    llm_requests: List[LLMRequest] = field(default_factory=list)  # For external LLM mode
