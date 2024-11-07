from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from alpha_tool_param import AlphaToolParam 
from alpha_tool_computer_use_param import AlphaToolComputerUseParam
from alpha_tool_bash_param import AlphaToolBashParam
from alpha_tool_text_editor_param import AlphaToolTextEditorParam

__all__ = ["BetaToolUnionParam"]

AlphaToolUnionParam: TypeAlias = Union[
    AlphaToolParam, AlphaToolComputerUseParam, AlphaToolBashParam, AlphaToolTextEditorParam
]