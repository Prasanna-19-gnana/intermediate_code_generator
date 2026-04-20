from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Sequence


@dataclass
class Instruction:
    """Represents one intermediate-code instruction used by the simulator."""

    index: int
    op: str
    arg1: str | None = None
    arg2: str | None = None
    target: int | None = None
    removed: bool = False

    def clone(self) -> "Instruction":
        """Create a shallow copy of the instruction."""

        return Instruction(
            index=self.index,
            op=self.op,
            arg1=self.arg1,
            arg2=self.arg2,
            target=self.target,
            removed=self.removed,
        )


@dataclass
class OptimizationResult:
    """Holds the optimized instruction list and the removed instructions."""

    optimized_code: List[Instruction]
    removed_lines: List[Instruction]
    removed_gotos: int
    removed_labels: int
    index_map: Dict[int, int]


@dataclass
class ExampleResult:
    """Full trace for one predefined example shown in the Streamlit UI."""

    title: str
    input_statement: str
    generated_code: List[Instruction]
    pending_lists: Dict[str, List[int]]
    backpatched_code: List[Instruction]
    optimized_code: List[Instruction]
    removed_lines: List[Instruction]
    metrics: Dict[str, int]
    pending_notes: List[str] = field(default_factory=list)


def clone_code(code: Sequence[Instruction]) -> List[Instruction]:
    """Clone a sequence of instructions so later stages can mutate safely."""

    return [instruction.clone() for instruction in code]
