from __future__ import annotations

from typing import Dict, Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from alpha_cache_control_ephemeral_param import AlphaCacheControlEphemeralParam

__all__ = ["AlphaToolParam", "InputSchema"]

class InputSchemaTyped(TypedDict, total="false"):
    type: Required[Literal["object"]]
    
    properties: Optional[object]
    
InputSchema: TypeAlias = Union[InputSchemaTyped, Dict[str, object]]

class AlphaToolParam(TypedDict, total=False):
    input_schema: Required[InputSchema]
    """[JSON schema] for the tool's input.
    
    Definition of the input shape that the tool will accept
    and the model shall produce
    """
    
    name: Required[str]
    """Name of the tool.
    
    How the model shall call the tool and the in tool_use blocks 
    """
    
    cache_control: Optional[AlphaCacheControlEphemeralParam]
    
    description: str
    """Description of what the tool does.
    
    Tool descriptions should be as detailed as possible. 
    """
    
    type: Optional[Literal["custom"]]