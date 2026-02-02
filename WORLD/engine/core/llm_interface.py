"""
LLM Interface: The Intelligence Layer

This module provides a unified interface for LLM operations.
It can work in two modes:

1. INTERNAL MODE: Calls LLM APIs directly (OpenAI, Anthropic)
2. EXTERNAL MODE: Returns prompts for processing by an external LLM (IDE, human)

The key insight: The system's intelligence comes from LLM processing.
Without it, you just have scaffolding. With it, you have real inference.
"""

import os
import json
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

from core.models import LLMRequest, LLMResponse


class LLMProvider(ABC):
    """Abstract LLM provider."""
    
    @abstractmethod
    def complete(self, request: LLMRequest) -> LLMResponse:
        """Process a request and return a response."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider is available (has API key, etc.)."""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI API provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4-turbo-preview"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self._client = None
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def complete(self, request: LLMRequest) -> LLMResponse:
        if not self.is_available():
            return LLMResponse(content="", success=False, error="No API key")
        
        try:
            import openai
            if not self._client:
                self._client = openai.OpenAI(api_key=self.api_key)
            
            response = self._client.chat.completions.create(
                model=self.model,
                messages=request.as_messages(),
                max_tokens=request.max_tokens,
                temperature=request.temperature
            )
            return LLMResponse(
                content=response.choices[0].message.content,
                raw=response,
                success=True
            )
        except Exception as e:
            return LLMResponse(content="", success=False, error=str(e))


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API provider."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        self.model = model
        self._client = None
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def complete(self, request: LLMRequest) -> LLMResponse:
        if not self.is_available():
            return LLMResponse(content="", success=False, error="No API key")
        
        try:
            from anthropic import Anthropic
            if not self._client:
                self._client = Anthropic(api_key=self.api_key)
            
            response = self._client.messages.create(
                model=self.model,
                max_tokens=request.max_tokens,
                system=request.system_prompt if request.system_prompt else "You are an expert software architect.",
                messages=[{"role": "user", "content": request.prompt}]
            )
            return LLMResponse(
                content=response.content[0].text,
                raw=response,
                success=True
            )
        except Exception as e:
            return LLMResponse(content="", success=False, error=str(e))


class ExternalProvider(LLMProvider):
    """
    External/IDE mode provider.
    
    Instead of calling an API, this collects prompts for external processing.
    Use this when the IDE (Claude, Cursor, etc.) IS your LLM.
    """
    
    def __init__(self):
        self.pending_requests: List[LLMRequest] = []
        self.responses: Dict[int, str] = {}  # request_index -> response
    
    def is_available(self) -> bool:
        return True  # Always available - the IDE is the LLM
    
    def complete(self, request: LLMRequest) -> LLMResponse:
        """
        In external mode, we don't complete - we collect.
        The actual completion happens when a human/IDE processes the prompt.
        """
        idx = len(self.pending_requests)
        self.pending_requests.append(request)
        
        # Check if we have a pre-provided response
        if idx in self.responses:
            return LLMResponse(content=self.responses[idx], success=True)
        
        # Return a placeholder indicating this needs external processing
        return LLMResponse(
            content="",
            success=False,
            error=f"EXTERNAL_PROCESSING_REQUIRED::{idx}"
        )
    
    def provide_response(self, request_index: int, response: str):
        """Provide a response for a pending request."""
        self.responses[request_index] = response
    
    def get_pending_prompts(self) -> List[Dict[str, Any]]:
        """Get all pending prompts for external processing."""
        return [
            {
                "index": i,
                "system": r.system_prompt,
                "prompt": r.prompt,
                "expected_format": r.expected_format
            }
            for i, r in enumerate(self.pending_requests)
            if i not in self.responses
        ]
    
    def export_for_ide(self) -> str:
        """Export pending prompts as a document an IDE can process."""
        output = "# LLM Processing Required\n\n"
        output += "The following prompts need to be processed by an LLM.\n"
        output += "Process each one and provide the response.\n\n"
        
        for item in self.get_pending_prompts():
            output += f"## Request {item['index']}\n\n"
            if item['system']:
                output += f"**System:** {item['system']}\n\n"
            output += f"**Prompt:**\n```\n{item['prompt']}\n```\n\n"
            output += f"**Expected format:** {item['expected_format']}\n\n"
            output += "---\n\n"
        
        return output


class LLMInterface:
    """
    Unified LLM interface.
    
    Automatically selects the best available provider:
    1. If Anthropic key available -> use Claude
    2. If OpenAI key available -> use GPT-4
    3. Otherwise -> external mode (IDE is the LLM)
    """
    
    def __init__(self, mode: str = "auto"):
        """
        Initialize LLM interface.
        
        Args:
            mode: "auto", "anthropic", "openai", or "external"
        """
        self.mode = mode
        self.provider = self._select_provider()
    
    def _select_provider(self) -> LLMProvider:
        if self.mode == "external":
            return ExternalProvider()
        
        if self.mode == "anthropic" or (self.mode == "auto" and os.getenv("ANTHROPIC_API_KEY")):
            provider = AnthropicProvider()
            if provider.is_available():
                return provider
        
        if self.mode == "openai" or (self.mode == "auto" and os.getenv("OPENAI_API_KEY")):
            provider = OpenAIProvider()
            if provider.is_available():
                return provider
        
        # Fallback to external mode
        return ExternalProvider()
    
    def complete(self, request: LLMRequest) -> LLMResponse:
        """Process an LLM request."""
        return self.provider.complete(request)
    
    def is_internal(self) -> bool:
        """Check if we have an internal LLM available."""
        return not isinstance(self.provider, ExternalProvider)
    
    def get_mode(self) -> str:
        """Get current mode."""
        if isinstance(self.provider, AnthropicProvider):
            return "anthropic"
        elif isinstance(self.provider, OpenAIProvider):
            return "openai"
        else:
            return "external"
    
    def get_pending_prompts(self) -> List[Dict[str, Any]]:
        """Get pending prompts (only in external mode)."""
        if isinstance(self.provider, ExternalProvider):
            return self.provider.get_pending_prompts()
        return []
    
    def export_for_ide(self) -> str:
        """Export for IDE processing (only in external mode)."""
        if isinstance(self.provider, ExternalProvider):
            return self.provider.export_for_ide()
        return "# Internal LLM mode - no export needed"


# Singleton for easy access
_default_interface: Optional[LLMInterface] = None

def get_llm(mode: str = "auto") -> LLMInterface:
    """Get the LLM interface."""
    global _default_interface
    if _default_interface is None or _default_interface.mode != mode:
        _default_interface = LLMInterface(mode)
    return _default_interface
