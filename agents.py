"""
Mock implementation of the agents module for the deep research agent.
This provides the basic functionality needed to run the application.
"""

import asyncio
from typing import Any, Dict, List, Optional, Callable
from pydantic import BaseModel
import openai
from openai import OpenAI
import requests
import json

# Global clients
_openai_client = None
_groq_client = None
_current_provider = "OpenAI"

def set_default_openai_key(api_key: str):
    """Set the default OpenAI API key."""
    global _openai_client
    _openai_client = OpenAI(api_key=api_key)

def set_groq_key(api_key: str):
    """Set the Groq API key."""
    global _groq_client
    _groq_client = api_key

def set_provider(provider: str):
    """Set the current provider."""
    global _current_provider
    _current_provider = provider

class ModelSettings(BaseModel):
    """Model settings for agents."""
    tool_choice: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

class Agent:
    """Mock Agent class for the deep research application."""
    
    def __init__(self, name: str, instructions: str, tools: List = None, 
                 model: str = "gpt-4o-mini", model_settings: ModelSettings = None,
                 output_type: type = None):
        self.name = name
        self.instructions = instructions
        self.tools = tools or []
        self.model = model
        self.model_settings = model_settings or ModelSettings()
        self.output_type = output_type

class Runner:
    """Mock Runner class for executing agents."""
    
    @staticmethod
    async def run(agent: Agent, input_text: str) -> 'RunResult':
        """Run an agent with the given input."""
        global _current_provider, _openai_client, _groq_client
        
        if _current_provider == "OpenAI":
            if not _openai_client:
                raise ValueError("OpenAI API key not set. Call set_default_openai_key() first.")
            
            # Create a simple chat completion
            messages = [
                {"role": "system", "content": agent.instructions},
                {"role": "user", "content": input_text}
            ]
            
            # Add tool definitions if tools are provided
            tools = None
            if agent.tools:
                tools = []
                for tool in agent.tools:
                    if hasattr(tool, 'function'):
                        tools.append(tool.function)
            
            response = _openai_client.chat.completions.create(
                model=agent.model,
                messages=messages,
                tools=tools,
                tool_choice="auto" if tools else None,
                temperature=getattr(agent.model_settings, 'temperature', 0.7),
                max_tokens=getattr(agent.model_settings, 'max_tokens', 1000)
            )
            
            # Extract the response content
            content = response.choices[0].message.content or ""
            
            # Handle tool calls if any
            if response.choices[0].message.tool_calls:
                # For now, just return the tool call info
                content += f"\n\nTool calls: {response.choices[0].message.tool_calls}"
            
            return RunResult(final_output=content)
        
        elif _current_provider == "Groq":
            if not _groq_client:
                raise ValueError("Groq API key not set. Call set_groq_key() first.")
            
            # Map OpenAI models to Groq models
            model_mapping = {
                "gpt-4o-mini": "llama3-8b-8192",
                "gpt-4o": "llama3-70b-8192",
                "gpt-3.5-turbo": "mixtral-8x7b-32768"
            }
            groq_model = model_mapping.get(agent.model, "llama3-8b-8192")
            
            messages = [
                {"role": "system", "content": agent.instructions},
                {"role": "user", "content": input_text}
            ]
            
            headers = {
                "Authorization": f"Bearer {_groq_client}",
                "Content-Type": "application/json"
            }
            
            # Start with basic payload without tools
            payload = {
                "model": groq_model,
                "messages": messages,
                "temperature": getattr(agent.model_settings, 'temperature', 0.7),
                "max_tokens": getattr(agent.model_settings, 'max_tokens', 1000)
            }
            
            # Only add tools if they exist and are properly formatted
            if agent.tools:
                try:
                    tools = []
                    for tool in agent.tools:
                        if hasattr(tool, 'function'):
                            tools.append(tool.function)
                    
                    if tools:
                        payload["tools"] = tools
                        payload["tool_choice"] = "auto"
                except Exception as e:
                    print(f"Warning: Could not add tools to Groq request: {e}")
            
            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60
                )
                response.raise_for_status()
                result = response.json()
                
                # Debug: Print the response structure
                print(f"Groq API Response: {json.dumps(result, indent=2)}")
                
                # Safely extract content with proper error handling
                if "choices" in result and len(result["choices"]) > 0:
                    choice = result["choices"][0]
                    if "message" in choice:
                        message = choice["message"]
                        content = message.get("content", "")
                        
                        # Handle tool calls if any
                        if "tool_calls" in message and message["tool_calls"]:
                            content += f"\n\nTool calls: {message['tool_calls']}"
                    else:
                        content = "No message content found in response"
                else:
                    content = "No choices found in response"
                
                return RunResult(final_output=content)
                
            except requests.exceptions.RequestException as e:
                raise ValueError(f"Groq API request failed: {str(e)}")
            except json.JSONDecodeError as e:
                raise ValueError(f"Groq API response parsing failed: {str(e)}")
            except Exception as e:
                raise ValueError(f"Groq API call failed: {str(e)}")
        
        else:
            raise ValueError(f"Unknown provider: {_current_provider}")

class RunResult:
    """Result of running an agent."""
    
    def __init__(self, final_output: str):
        self.final_output = final_output

def trace(func: Callable) -> Callable:
    """Decorator for tracing function calls."""
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def function_tool(func: Callable) -> Callable:
    """Decorator for creating function tools."""
    # Add function attribute to the decorated function
    func.function = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
    return func 