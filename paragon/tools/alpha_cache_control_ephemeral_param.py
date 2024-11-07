# Creation of cache control parameters data type

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["AlphaCacheControlEphemeralParam"]

class AlphaCacheControlEphemeralParam(TypedDict, total=False):
    type: Required[Literal["ephemeral"]]