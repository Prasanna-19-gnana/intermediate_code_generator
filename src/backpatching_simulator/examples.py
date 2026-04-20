from __future__ import annotations

from .backpatching import backpatch, makelist, merge
from .models import ExampleResult, Instruction, clone_code
from .optimizer import optimize_code


def _finalize_example(
    title: str,
    input_statement: str,
    generated_code: list[Instruction],
    pending_lists: dict[str, list[int]],
    patch_plan: list[tuple[list[int], int]],
    pending_notes: list[str],
) -> ExampleResult:
    """Patch the generated code, optimize it, and assemble the final trace."""

    backpatched_code = clone_code(generated_code)
    for patch_list, target in patch_plan:
        backpatch(backpatched_code, patch_list, target)

    optimized = optimize_code(backpatched_code)
    metrics = {
        "Instructions before optimization": len(backpatched_code),
        "Instructions after optimization": len(optimized.optimized_code),
        "Redundant gotos removed": optimized.removed_gotos,
        "Unused labels removed": optimized.removed_labels,
    }

    return ExampleResult(
        title=title,
        input_statement=input_statement,
        generated_code=generated_code,
        pending_lists=pending_lists,
        backpatched_code=backpatched_code,
        optimized_code=optimized.optimized_code,
        removed_lines=optimized.removed_lines,
        metrics=metrics,
        pending_notes=pending_notes,
    )


def build_if_else_result(
    condition: str,
    then_target: str,
    then_value: str,
    else_target: str,
    else_value: str,
) -> ExampleResult:
    """Build the full trace for a user-defined if-else statement."""

    input_statement = f"if ({condition}) {then_target} = {then_value}; else {else_target} = {else_value};"
    generated_code = [
        Instruction(0, "ifgoto", arg1=condition, target=None),
        Instruction(1, "goto", target=None),
        Instruction(2, "assign", arg1=then_target, arg2=then_value),
        Instruction(3, "goto", target=None),
        Instruction(4, "assign", arg1=else_target, arg2=else_value),
        Instruction(5, "label"),
        Instruction(6, "goto", target=7),
        Instruction(7, "label"),
    ]

    truelist = makelist(0)
    falselist = makelist(1)
    nextlist = makelist(3)
    pending_lists = {
        "truelist": truelist,
        "falselist": falselist,
        "nextlist": nextlist,
    }
    pending_notes = [
        "The truelist patches the jump for the true branch.",
        "The falselist patches the jump for the false branch.",
        "The nextlist patches the jump that skips over the else block.",
    ]

    return _finalize_example(
        title="If-Else",
        input_statement=input_statement,
        generated_code=generated_code,
        pending_lists=pending_lists,
        patch_plan=[(truelist, 2), (falselist, 4), (nextlist, 5)],
        pending_notes=pending_notes,
    )


def build_while_result(condition: str, body_target: str, body_value: str) -> ExampleResult:
    """Build the full trace for a user-defined while loop."""

    input_statement = f"while ({condition}) {body_target} = {body_value};"
    generated_code = [
        Instruction(0, "label"),
        Instruction(1, "ifgoto", arg1=condition, target=None),
        Instruction(2, "goto", target=None),
        Instruction(3, "assign", arg1=body_target, arg2=body_value),
        Instruction(4, "goto", target=0),
        Instruction(5, "label"),
        Instruction(6, "goto", target=7),
        Instruction(7, "label"),
    ]

    truelist = makelist(1)
    falselist = makelist(2)
    pending_lists = {
        "truelist": truelist,
        "falselist": falselist,
    }
    pending_notes = [
        "The first label marks the beginning of the loop condition.",
        "The falselist exits the loop when the condition fails.",
    ]

    return _finalize_example(
        title="While Loop",
        input_statement=input_statement,
        generated_code=generated_code,
        pending_lists=pending_lists,
        patch_plan=[(truelist, 3), (falselist, 5)],
        pending_notes=pending_notes,
    )


def build_boolean_and_result(
    left_condition: str,
    right_condition: str,
    then_target: str,
    then_value: str,
    else_target: str,
    else_value: str,
) -> ExampleResult:
    """Build the full trace for a user-defined if statement with short-circuit AND."""

    input_statement = f"if ({left_condition} && {right_condition}) {then_target} = {then_value}; else {else_target} = {else_value};"
    generated_code = [
        Instruction(0, "ifgoto", arg1=left_condition, target=None),
        Instruction(1, "goto", target=None),
        Instruction(2, "ifgoto", arg1=right_condition, target=None),
        Instruction(3, "goto", target=None),
        Instruction(4, "assign", arg1=then_target, arg2=then_value),
        Instruction(5, "goto", target=None),
        Instruction(6, "assign", arg1=else_target, arg2=else_value),
        Instruction(7, "label"),
        Instruction(8, "goto", target=9),
        Instruction(9, "label"),
    ]

    left_truelist = makelist(0)
    left_falselist = makelist(1)
    right_truelist = makelist(2)
    right_falselist = makelist(3)
    merged_falselist = merge(left_falselist, right_falselist)
    nextlist = makelist(5)

    pending_lists = {
        "E1.truelist": left_truelist,
        "E1.falselist": left_falselist,
        "E2.truelist": right_truelist,
        "E2.falselist": right_falselist,
        "Merged truelist": right_truelist,
        "Merged falselist": merged_falselist,
        "nextlist": nextlist,
    }
    pending_notes = [
        "Short-circuit evaluation sends the first true jump to the second condition.",
        "The final falselist merges the false exits from both conditions.",
        "The nextlist skips from the then-branch to the end label.",
    ]

    return _finalize_example(
        title="Boolean AND in If-Else",
        input_statement=input_statement,
        generated_code=generated_code,
        pending_lists=pending_lists,
        patch_plan=[(left_truelist, 2), (right_truelist, 4), (merged_falselist, 6), (nextlist, 7)],
        pending_notes=pending_notes,
    )
