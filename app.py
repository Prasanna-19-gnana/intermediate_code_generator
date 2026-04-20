from __future__ import annotations

from pathlib import Path
import sys

import streamlit as st

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from backpatching_simulator.examples import (
    build_boolean_and_result,
    build_if_else_result,
    build_while_result,
)
from backpatching_simulator.formatting import code_block_html, format_list_block, format_summary_rows

st.set_page_config(
    page_title="Backpatching Optimization Simulator",
    page_icon="🧩",
    layout="wide",
)

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(15, 118, 110, 0.12), transparent 28%),
                radial-gradient(circle at top right, rgba(180, 83, 9, 0.10), transparent 22%),
                linear-gradient(180deg, #f8fafc 0%, #f3f6fb 100%);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1280px;
        }
        .main-title {
            font-family: Georgia, "Times New Roman", serif;
            font-size: 2.4rem;
            font-weight: 700;
            letter-spacing: 0.01em;
            color: #0f172a;
            margin-bottom: 0.15rem;
        }
        .subtitle {
            color: #475569;
            font-size: 1.02rem;
            margin-bottom: 1rem;
            max-width: 900px;
        }
        .hero-band {
            border: 1px solid rgba(148, 163, 184, 0.28);
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.82);
            backdrop-filter: blur(8px);
            padding: 1rem 1.1rem;
            margin-bottom: 1rem;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
        }
        .eyebrow {
            display: inline-block;
            padding: 0.28rem 0.65rem;
            border-radius: 999px;
            background: #0f766e;
            color: white;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            margin-bottom: 0.55rem;
        }
        .section-card {
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 18px;
            padding: 1rem 1rem 0.85rem 1rem;
            background: rgba(255, 255, 255, 0.88);
            box-shadow: 0 12px 28px rgba(15, 23, 42, 0.05);
        }
        .codebox {
            border: 1px solid #d6dde8;
            border-radius: 12px;
            background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
            padding: 0.85rem 0.9rem;
            overflow-x: auto;
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 0.94rem;
            line-height: 1.55;
        }
        .line {
            white-space: pre;
        }
        .code-title {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #64748b;
            margin-bottom: 0.5rem;
            font-weight: 700;
        }
        .target-unresolved {
            color: #b26a00;
            font-weight: 700;
        }
        .target-patched {
            color: #0f766e;
            font-weight: 700;
        }
        .removed-line {
            color: #9ca3af;
            text-decoration: line-through;
        }
        .metric-strip {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.75rem;
            margin: 0.15rem 0 0.5rem 0;
        }
        .metric-card {
            border: 1px solid rgba(148, 163, 184, 0.25);
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.9);
            padding: 0.75rem 0.85rem;
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
        }
        .metric-label {
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.11em;
            color: #64748b;
            margin-bottom: 0.25rem;
            font-weight: 700;
        }
        .metric-value {
            font-size: 1.45rem;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.1;
        }
        .metric-note {
            color: #475569;
            font-size: 0.88rem;
            margin-top: 0.22rem;
        }
        .status-pill {
            display: inline-block;
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            background: #e2e8f0;
            color: #334155;
            font-size: 0.75rem;
            font-weight: 700;
            margin-bottom: 0.7rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.4rem;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 999px;
            padding: 0.35rem 0.75rem;
            background: rgba(226, 232, 240, 0.6);
        }
        .stTabs [aria-selected="true"] {
            background: #0f766e !important;
            color: white !important;
        }
        div[data-testid="stRadio"] > label,
        div[data-testid="stSelectbox"] > label,
        div[data-testid="stTextInput"] > label {
            font-weight: 700;
            color: #0f172a;
        }
        div[data-testid="stTextInput"] input,
        div[data-testid="stSelectbox"] select,
        div[data-testid="stNumberInput"] input,
        div[data-testid="stTextArea"] textarea {
            color: #0f172a !important;
            -webkit-text-fill-color: #0f172a !important;
        }
        div[data-testid="stTextInput"] input::placeholder,
        div[data-testid="stTextArea"] textarea::placeholder {
            color: #64748b !important;
            opacity: 1 !important;
            -webkit-text-fill-color: #64748b !important;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border-bottom: 1px solid #e2e8f0;
            padding: 0.45rem 0.5rem;
            text-align: left;
        }
        th {
            color: #0f172a;
            background: #f8fafc;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">Backpatching Optimization Simulator</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">A user-driven step-by-step trace of intermediate code generation, backpatching, and simple optimization for a few supported control-flow shapes.</div>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="hero-band">
        <div class="eyebrow">Compiler Design Demo</div>
        <div class="status-pill">Interactive statement builder</div>
        <div>Choose a statement shape in the sidebar, edit the operands, and the simulator will regenerate the unresolved code, pending lists, patched code, and optimized result immediately.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown("### Statement Builder")
statement_type = st.sidebar.selectbox(
    "Shape",
    ["If-Else", "While Loop", "Boolean AND in If-Else"],
)

operator_options = ["<", "<=", ">", ">=", "==", "!="]

if statement_type == "If-Else":
    st.sidebar.markdown("#### Condition")
    left_operand = st.sidebar.text_input("Left operand", value="a")
    operator = st.sidebar.selectbox("Operator", operator_options, index=0)
    right_operand = st.sidebar.text_input("Right operand", value="b")
    st.sidebar.markdown("#### Then branch")
    then_target = st.sidebar.text_input("Target variable", value="x")
    then_value = st.sidebar.text_input("Assigned value", value="1")
    st.sidebar.markdown("#### Else branch")
    else_target = st.sidebar.text_input("Target variable ", value="x")
    else_value = st.sidebar.text_input("Assigned value ", value="2")

    condition = f"{left_operand} {operator} {right_operand}".strip()
    result = build_if_else_result(condition, then_target, then_value, else_target, else_value)

elif statement_type == "While Loop":
    st.sidebar.markdown("#### Loop condition")
    left_operand = st.sidebar.text_input("Left operand", value="a", key="while_left")
    operator = st.sidebar.selectbox("Operator", operator_options, index=0, key="while_operator")
    right_operand = st.sidebar.text_input("Right operand", value="b", key="while_right")
    st.sidebar.markdown("#### Loop body")
    body_target = st.sidebar.text_input("Target variable", value="a", key="while_target")
    body_value = st.sidebar.text_input("Assigned expression", value="a + 1", key="while_value")

    condition = f"{left_operand} {operator} {right_operand}".strip()
    result = build_while_result(condition, body_target, body_value)

else:
    st.sidebar.markdown("#### First condition")
    left1 = st.sidebar.text_input("Left operand", value="a", key="and_left1")
    op1 = st.sidebar.selectbox("Operator", operator_options, index=0, key="and_op1")
    right1 = st.sidebar.text_input("Right operand", value="b", key="and_right1")
    st.sidebar.markdown("#### Second condition")
    left2 = st.sidebar.text_input("Left operand ", value="c", key="and_left2")
    op2 = st.sidebar.selectbox("Operator ", operator_options, index=0, key="and_op2")
    right2 = st.sidebar.text_input("Right operand ", value="d", key="and_right2")
    st.sidebar.markdown("#### Then branch")
    then_target = st.sidebar.text_input("Target variable", value="x", key="and_then_target")
    then_value = st.sidebar.text_input("Assigned value", value="1", key="and_then_value")
    st.sidebar.markdown("#### Else branch")
    else_target = st.sidebar.text_input("Target variable ", value="x", key="and_else_target")
    else_value = st.sidebar.text_input("Assigned value ", value="0", key="and_else_value")

    left_condition = f"{left1} {op1} {right1}".strip()
    right_condition = f"{left2} {op2} {right2}".strip()
    result = build_boolean_and_result(left_condition, right_condition, then_target, then_value, else_target, else_value)

st.sidebar.markdown("---")
st.sidebar.markdown("### Demo Notes")
st.sidebar.markdown(
    """
- Only the three supported control-flow shapes are generated
- No general parser is used
- The values are user-editable, so the trace changes live as you type
- The optimizer keeps the passes simple and explainable
"""
)

st.markdown(f"## Generated Trace: {result.title}")
metric_columns = st.columns(4)
metric_cards = [
    ("Before Opt.", len(result.backpatched_code), "instruction count"),
    ("After Opt.", len(result.optimized_code), "optimized count"),
    ("Gotos Removed", result.metrics["Redundant gotos removed"], "peephole pass"),
    ("Labels Removed", result.metrics["Unused labels removed"], "cleanup pass"),
]
for column, (label, value, note) in zip(metric_columns, metric_cards):
    with column:
        st.markdown(
            f'''
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-note">{note}</div>
            </div>
            ''',
            unsafe_allow_html=True,
        )

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Input Statement")
st.markdown(code_block_html(result.input_statement, language="text"), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Step 1: Generated Code",
        "Step 2: Pending Lists",
        "Step 3: After Backpatching",
        "Step 4: After Optimization",
        "Step 5: Summary",
    ]
)

with tab1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Generated Intermediate Code")
    st.markdown('<div class="code-title">Unresolved targets shown as _</div>', unsafe_allow_html=True)
    st.markdown(code_block_html(result.generated_code, highlight_mode="unresolved"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Pending Lists")
    st.markdown(format_list_block(result.pending_lists), unsafe_allow_html=True)
    if result.pending_notes:
        st.markdown("#### Notes")
        for note in result.pending_notes:
            st.markdown(f"- {note}")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("After Backpatching")
    st.markdown('<div class="code-title">Targets filled with final addresses</div>', unsafe_allow_html=True)
    st.markdown(code_block_html(result.backpatched_code, highlight_mode="patched"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("After Optimization")
    st.markdown('<div class="code-title">Removed instructions are struck through below</div>', unsafe_allow_html=True)
    st.markdown(code_block_html(result.optimized_code, highlight_mode="optimized"), unsafe_allow_html=True)
    if result.removed_lines:
        st.markdown("#### Removed During Optimization")
        st.markdown(code_block_html(result.removed_lines, highlight_mode="removed"), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Summary")
    st.markdown(format_summary_rows(result.metrics), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.subheader("Step-by-Step Presentation Mode")
st.caption("Use this lower panel during a viva or demo to reveal one stage at a time.")
step = st.radio(
    "Choose a stage",
    [
        "Input Statement",
        "Generated Intermediate Code",
        "Pending Lists",
        "After Backpatching",
        "After Optimization",
        "Summary",
    ],
    horizontal=True,
    label_visibility="collapsed",
)

stage_map = {
    "Input Statement": lambda: st.markdown(code_block_html(result.input_statement, language="text"), unsafe_allow_html=True),
    "Generated Intermediate Code": lambda: st.markdown(code_block_html(result.generated_code, highlight_mode="unresolved"), unsafe_allow_html=True),
    "Pending Lists": lambda: st.markdown(format_list_block(result.pending_lists), unsafe_allow_html=True),
    "After Backpatching": lambda: st.markdown(code_block_html(result.backpatched_code, highlight_mode="patched"), unsafe_allow_html=True),
    "After Optimization": lambda: st.markdown(code_block_html(result.optimized_code, highlight_mode="optimized"), unsafe_allow_html=True),
    "Summary": lambda: st.markdown(format_summary_rows(result.metrics), unsafe_allow_html=True),
}

st.markdown('<div class="section-card">', unsafe_allow_html=True)
stage_map[step]()
if step == "After Optimization" and result.removed_lines:
    st.markdown("#### Removed During Optimization")
    st.markdown(code_block_html(result.removed_lines, highlight_mode="removed"), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
