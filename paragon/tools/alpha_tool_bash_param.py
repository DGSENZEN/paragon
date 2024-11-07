from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from alpha_cache_control_ephemeral_param import AlphaCacheControlEphemeralParam

__all__ = ["AlphaToolBashParam"]

class AlphaToolBashParam(TypedDict, total=False):
    name: Required[Literal["bash"]]
    """The name of the tool."""
    
    type: Required[Literal["bash_20241106"]]
    
    cache_control: Optional[AlphaCacheControlEphemeralParam]
    