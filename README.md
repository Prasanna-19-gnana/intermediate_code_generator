# Backpatching Optimization Simulator

## 1. Project Overview

Backpatching Optimization Simulator is a small educational Streamlit project for compiler design topics. It demonstrates how intermediate code is generated for a few control-flow patterns, how unresolved jump targets are stored and later patched, and how a few simple optimization passes reduce unnecessary instructions.

This is **not a full compiler**. It does not parse arbitrary source code. Instead, it gives you a controlled, explainable environment for showing the idea of:

- intermediate code generation
- backpatching
- control-flow handling
- simple code optimization

The project is meant for college demos, viva explanations, and presentations where you want to show the compiler pipeline step by step rather than dump final code only.

## 2. How This Project Relates to "Simulation of Intermediate Code Generation Using Backpatching"

The topic "Simulation of Intermediate Code Generation Using Backpatching" usually means:

- take a source statement with control flow
- generate intermediate code
- keep jump targets unresolved at first
- store those unresolved locations in pending lists
- fill them later when target addresses become known

This project follows that exact teaching model.

For each supported case, the simulator shows:

1. the input statement
2. the raw intermediate code with `_` for unknown jump targets
3. the pending lists used for patching
4. the code after backpatching
5. the optimized code after simple cleanup passes
6. summary metrics

So this app is a live, visual simulation of the same compiler-design concept, not a production compiler.

## 3. What the App Supports

The sidebar lets you choose one of three control-flow shapes:

1. If-Else
2. While Loop
3. Boolean AND in If-Else

Each one is built from user-entered text fields and dropdowns.

## 4. How to Run the Project

### 4.1 Install dependencies

Create a Python 3 environment if needed, then install the requirements:

```bash
pip install -r requirements.txt
```

### 4.2 Start the app

Run the Streamlit application from the project root:

```bash
streamlit run app.py
```

### 4.3 Open the browser

Streamlit usually opens automatically. If not, open:

```text
http://localhost:8501
```

## 5. Project Structure

```text
Backpatching Optimization Simulator/
├── app.py
├── requirements.txt
├── README.md
└── src/
    └── backpatching_simulator/
        ├── __init__.py
        ├── backpatching.py
        ├── examples.py
        ├── formatting.py
        ├── models.py
        └── optimizer.py
```

### File roles

- `app.py`: Streamlit UI and presentation layer
- `models.py`: instruction and result data models
- `backpatching.py`: classic backpatching helpers
- `examples.py`: manual example builders for the three supported shapes
- `optimizer.py`: small optimization passes
- `formatting.py`: HTML/text formatting for the UI

## 6. Backend Logic Explained

The backend is intentionally simple and deterministic.

### 6.1 Instruction model

Each intermediate-code line is represented using an `Instruction` dataclass with fields like:

- `index`: instruction number
- `op`: operation type such as `ifgoto`, `goto`, `assign`, or `label`
- `arg1`: first operand or condition text
- `arg2`: second operand or assigned value
- `target`: jump target index if known
- `removed`: flag used during optimization

This makes the code easy to display, patch, and optimize.

### 6.2 Backpatching helpers

The simulator implements the standard helpers used in compiler design:

- `makelist(i)` creates a list containing one unresolved jump location
- `merge(list1, list2)` combines two pending lists
- `backpatch(code, patch_list, target)` fills the target field for all instructions in the list

These are the core ideas behind backpatching.

### 6.3 How example generation works

The project does **not** parse input using a grammar.

Instead, for each supported shape, the app manually constructs a list of intermediate instructions. This is deliberate because the goal is to teach the algorithm, not to build a parser.

The builder functions are:

- `build_if_else_result(...)`
- `build_while_result(...)`
- `build_boolean_and_result(...)`

Each builder:

1. creates raw intermediate code with unresolved targets
2. creates the pending lists
3. applies backpatching
4. runs optimization
5. packages everything into a result object for the UI

### 6.4 Optimization logic

After backpatching, the optimizer applies small cleanup passes:

- remove unconditional `goto` instructions that jump to the immediately next instruction
- remove unused labels and empty labels
- merge consecutive labels if present
- reindex instructions after removal
- update jump targets after reindexing

These are simple optimization passes, but they are enough to show why post-processing improves control flow.

## 7. How the UI Works

The app is split into two main presentation areas:

1. the sidebar statement builder
2. the main output panel

### 7.1 Sidebar statement builder

The sidebar is where you give input.

#### If-Else input format

You enter:

- left operand
- comparison operator
- right operand
- then-branch target variable
- then-branch assigned value
- else-branch target variable
- else-branch assigned value

Example:

- Left operand: `a`
- Operator: `<`
- Right operand: `b`
- Then variable: `x`
- Then value: `1`
- Else variable: `x`
- Else value: `2`

This becomes:

```text
if (a < b) x = 1; else x = 2;
```

#### While Loop input format

You enter:

- left operand
- comparison operator
- right operand
- loop body target variable
- loop body assigned expression

Example:

- Left operand: `a`
- Operator: `<`
- Right operand: `b`
- Target variable: `a`
- Expression: `a + 1`

This becomes:

```text
while (a < b) a = a + 1;
```

#### Boolean AND in If-Else input format

You enter:

- first condition: left operand, operator, right operand
- second condition: left operand, operator, right operand
- then-branch target variable and assigned value
- else-branch target variable and assigned value

Example:

- First condition: `a < b`
- Second condition: `c < d`
- Then variable: `x`
- Then value: `1`
- Else variable: `x`
- Else value: `0`

This becomes:

```text
if (a < b && c < d) x = 1; else x = 0;
```

### 7.2 Main output sections

The app always shows five visible sections:

1. Input Statement
2. Generated Intermediate Code
3. Pending Lists
4. After Backpatching
5. After Optimization
6. Summary

It also provides a lower step-by-step presentation mode for demos.

## 8. How the Output Is Generated

The output is produced in a strict sequence.

### Step 1: Input statement

The app first builds a readable source-style statement from the sidebar fields.

### Step 2: Generated intermediate code

The app manually creates intermediate code. At this stage, jump targets may not be known, so they appear as `_`.

Example:

```text
0: if a < b goto _
1: goto _
2: x = 1
3: goto _
4: x = 2
5:
```

### Step 3: Pending lists

The app displays the unresolved lists used for patching.

Example:

```text
truelist = [0]
falselist = [1]
nextlist = [3]
```

### Step 4: Backpatching

The unresolved targets are replaced with real instruction numbers.

Example:

```text
0: if a < b goto 2
1: goto 4
2: x = 1
3: goto 5
4: x = 2
5:
```

### Step 5: Optimization

The optimizer removes trivial jumps and unused labels, then reindexes the surviving instructions.

Example optimized result:

```text
0: if a < b goto 2
1: goto 4
2: x = 1
3: x = 2
4:
```

The exact final output depends on the selected statement and input values.

## 9. Understanding the Three Condition Types

This project demonstrates three different control-flow patterns.

### 9.1 If-Else condition

This is the simplest case.

Input pattern:

```text
if (condition) then-statement; else else-statement;
```

What happens:

- one true jump is stored in `truelist`
- one false jump is stored in `falselist`
- a `nextlist` is used to skip from the then block to the end

Output behavior:

- unresolved targets appear in the raw code
- after backpatching, the true branch jumps to the then block
- the false branch jumps to the else block
- the optimizer may remove a redundant jump if it goes to the next instruction

### 9.2 While Loop condition

This demonstrates looping and backward control flow.

Input pattern:

```text
while (condition) body;
```

What happens:

- the loop condition is checked first
- if true, control goes to the loop body
- if false, control jumps out of the loop
- the body usually ends with a backward `goto` to the condition label

Output behavior:

- backpatching fills the loop exit target
- the backward jump remains, because it is required for the loop
- optimization is usually small here, because the control flow is already compact

### 9.3 Boolean AND in If-Else

This demonstrates short-circuit evaluation.

Input pattern:

```text
if (cond1 && cond2) then-statement; else else-statement;
```

What happens:

- the first condition is checked
- if it is true, the second condition is evaluated
- if either condition is false, control goes to the false branch
- the true path goes to the then branch only when both conditions succeed

Output behavior:

- the pending lists are more interesting here because the false exits from both conditions must be merged
- backpatching shows how `&&` is implemented using jumps
- the optimized code may still keep the short-circuit structure, because it is semantically important

## 10. How to Read the Pending Lists

The lists are the most important theory part of backpatching.

### truelist

Contains instruction indices that should be patched to the true destination.

### falselist

Contains instruction indices that should be patched to the false destination.

### nextlist

Contains instruction indices that should be patched to the next statement or join point.

If a list is empty or not used in a specific example, the app simply does not show it.

## 11. How to Read the Intermediate Code

The app displays code in this style:

```text
0: if a < b goto _
1: goto _
2: x = 1
3: goto _
4: x = 2
5:
```

Meaning:

- `0:` is the instruction number
- `if ... goto _` is a conditional jump with an unresolved target
- `goto _` is an unconditional jump with an unresolved target
- `x = 1` is an assignment statement
- `5:` may represent a label or join point

A blank target means the target is not known yet.

## 12. How to Use the Step-by-Step Demo Mode

At the bottom of the app, there is a step-by-step mode.

This is useful for presentation because you can reveal one stage at a time:

1. Input Statement
2. Generated Intermediate Code
3. Pending Lists
4. After Backpatching
5. After Optimization
6. Summary

This is the best mode to use during viva or classroom explanation.

## 13. Metrics Shown in the Summary

The summary section shows:

- instructions before optimization
- instructions after optimization
- redundant gotos removed
- unused labels removed

These metrics make the optimization effect measurable.

## 14. Example Walkthrough

Suppose you enter:

- If-Else
- left operand: `a`
- operator: `<`
- right operand: `b`
- then assignment: `x = 1`
- else assignment: `x = 2`

The app will generate:

1. a source-style input statement
2. raw intermediate code with unresolved targets
3. pending lists
4. backpatched code with real addresses
5. optimized code with unnecessary jumps removed
6. summary metrics

This is the exact teaching sequence expected in a backpatching simulator.

## 15. Design Choices

A few intentional design decisions were made to keep the project easy to explain:

- no parser was added
- no database was used
- no authentication was added
- the examples are limited to three well-known control-flow forms
- the output is deterministic
- the UI is clean and presentation-friendly

These choices keep the project focused on compiler design rather than framework complexity.

## 16. Troubleshooting

### The app does not open

Try starting it again from the project root:

```bash
streamlit run app.py
```

### Safari says it cannot connect

Check that Streamlit is running on port 8501 and open:

```text
http://localhost:8501
```

If needed, try:

```text
http://127.0.0.1:8501
```

### The text in input fields looks wrong

Refresh the page after the latest app update. The CSS forces black text in white input controls for readability.

## 17. Example Screenshots

Add screenshots here after running the app and capturing the main interactive views.

- Statement builder screen
- Input statement view
- Raw intermediate code view
- Backpatched output view
- Optimized output view
- Step-by-step presentation mode

## 18. Short Viva Answer

If someone asks what this project does, you can say:

> This project simulates intermediate code generation using backpatching for a few control-flow statements. It shows how unresolved jump targets are stored in lists, patched later, and then optimized using simple cleanup passes.

## 19. In One Sentence

Backpatching Optimization Simulator is a small Streamlit-based compiler education tool that turns user-entered control-flow statements into intermediate code, patches unresolved jumps, and shows the optimized result step by step.
