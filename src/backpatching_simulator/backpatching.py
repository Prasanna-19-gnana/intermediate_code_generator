from __future__ import annotations

from typing import Sequence

from .models import Instruction


def makelist(i: int) -> list[int]:
    """Create a singleton list for a pending jump target."""

    return [i]


def merge(list1: list[int], list2: list[int]) -> list[int]:
    """Combine two pending lists while preserving order."""

    return list1 + list2


def backpatch(code: Sequence[Instruction], patch_list: Sequence[int], target: int) -> None:
    """Fill unresolved jump targets with the final target instruction index."""

    for instruction_index in patch_list:
        code[instruction_index].target = target
