from __future__ import annotations

from html import escape
from typing import Sequence

from .models import Instruction


def _format_target(target: int | None, highlight_mode: str) -> str:
    if target is None:
        return '<span class="target-unresolved">_</span>'
    if highlight_mode == "patched":
        return f'<span class="target-patched">{target}</span>'
    return str(target)


def _instruction_text(instruction: Instruction, highlight_mode: str) -> str:
    if instruction.op == "label":
        return f"{instruction.index}:"

    if instruction.op == "assign":
        left_side = escape(instruction.arg1 or "")
        right_side = escape(instruction.arg2 or "")
        return f"{instruction.index}: {left_side} = {right_side}"

    if instruction.op == "goto":
        return f"{instruction.index}: goto {_format_target(instruction.target, highlight_mode)}"

    if instruction.op == "ifgoto":
        condition = escape(instruction.arg1 or "")
        return f"{instruction.index}: if {condition} goto {_format_target(instruction.target, highlight_mode)}"

    return f"{instruction.index}: {instruction.op}"


def code_block_html(content: str | Sequence[Instruction], highlight_mode: str = "plain", language: str = "text") -> str:
    """Render plain text or instruction lists as a readable HTML code block."""

    if isinstance(content, str):
        lines = escape(content).splitlines() or [""]
        rendered = "".join(f'<div class="line">{line or "&nbsp;"}</div>' for line in lines)
        return f'<div class="codebox">{rendered}</div>'

    lines = []
    for instruction in content:
        css_class = "line"
        if highlight_mode == "removed" or instruction.removed:
            css_class = "line removed-line"
        lines.append(f'<div class="{css_class}">{_instruction_text(instruction, highlight_mode)}</div>')
    return f'<div class="codebox">{"".join(lines)}</div>'


def format_list_block(pending_lists: dict[str, list[int]]) -> str:
    """Render pending backpatching lists as a code-style block."""

    lines = ["PENDING LISTS"]
    for name, values in pending_lists.items():
        lines.append(f"{name} = {values}")
    return code_block_html("\n".join(lines))


def format_summary_rows(metrics: dict[str, int]) -> str:
    """Render optimization metrics as a compact markdown table."""

    rows = ["| Metric | Value |", "| --- | ---: |"]
    for name, value in metrics.items():
        rows.append(f"| {name} | {value} |")
    return "\n".join(rows)
