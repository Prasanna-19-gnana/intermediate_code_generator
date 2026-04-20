from __future__ import annotations

from typing import Sequence

from .models import Instruction, OptimizationResult, clone_code


def _next_live_index(code: Sequence[Instruction], position: int) -> int | None:
    for next_position in range(position + 1, len(code)):
        if not code[next_position].removed:
            return code[next_position].index
    return None


def _merge_consecutive_labels(code: list[Instruction], removed_lines: list[Instruction]) -> bool:
    changed = False
    for position in range(1, len(code)):
        previous = code[position - 1]
        current = code[position]
        if previous.removed or current.removed:
            continue
        if previous.op == "label" and current.op == "label":
            for instruction in code:
                if instruction.target == current.index:
                    instruction.target = previous.index
            current.removed = True
            removed_lines.append(current.clone())
            changed = True
    return changed


def optimize_code(code: Sequence[Instruction]) -> OptimizationResult:
    """Apply small, deterministic peephole optimizations to the instruction list."""

    working = clone_code(code)
    removed_lines: list[Instruction] = []
    removed_gotos = 0
    removed_labels = 0

    changed = True
    while changed:
        changed = False
        if _merge_consecutive_labels(working, removed_lines):
            changed = True

        referenced_targets = {
            instruction.target
            for instruction in working
            if not instruction.removed and instruction.target is not None
        }

        for position, instruction in enumerate(working):
            if instruction.removed:
                continue

            if instruction.op == "goto":
                next_live_index = _next_live_index(working, position)
                if next_live_index is not None and instruction.target == next_live_index:
                    instruction.removed = True
                    removed_lines.append(instruction.clone())
                    removed_gotos += 1
                    changed = True
                    continue

            if instruction.op == "label" and instruction.index not in referenced_targets:
                instruction.removed = True
                removed_lines.append(instruction.clone())
                removed_labels += 1
                changed = True

    live_instructions = [instruction.clone() for instruction in working if not instruction.removed]
    index_map = {instruction.index: new_index for new_index, instruction in enumerate(live_instructions)}

    for new_index, instruction in enumerate(live_instructions):
        instruction.index = new_index
        if instruction.target is not None:
            instruction.target = index_map.get(instruction.target, instruction.target)

    return OptimizationResult(
        optimized_code=live_instructions,
        removed_lines=removed_lines,
        removed_gotos=removed_gotos,
        removed_labels=removed_labels,
        index_map=index_map,
    )
