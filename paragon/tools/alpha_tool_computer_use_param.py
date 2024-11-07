from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from alpha_cache_control_ephemeral_param import AlphaCacheControlEphemeralParam

__all__ = ["AlphaToolComputerUseParam"]


class AlphaToolComputerUseParam(TypedDict, total=False):
    display_height_px: Required[int]
    """Height of display in pixels."""
    
    display_width_px: Required[int]
    """Width of display in pixels."""
    
    name: Required[Literal["computer"]]
    """Name of the tool"""
    
    type: Required[Literal["computer"]]
    
    cache_control: Optional[AlphaCacheControlEphemeralParam]
    
    display_number: Optional[int]
    """The X11 display number for the display (0, 1)"""