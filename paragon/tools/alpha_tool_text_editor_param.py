from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from alpha_cache_control_ephemeral_param import AlphaCacheControlEphemeralParam

__all__ = ["AlphaToolTextEditorParam"]

class AlphaToolTextEditorParam(TypedDict, total=False):
    name: Required[Literal["str_replace_editor"]]
    """Name of the tool
    
    This is how the tool will be called by the model.
    """
    type: Required[Literal["text_editor"]]
    
    cache_control: Optional[AlphaCacheControlEphemeralParam]
    