
import json
import tempfile
from pathlib import Path
from datetime import date

import pandas as pd
import streamlit as st

from database.db import initialize_database, get_active_criteria
from agents.orchestrator import run_evaluation


st.set_page_config(
    page_title="Agentic RFP Evaluation",
    page_icon="📊",
    layout="wide",
)

st.title("Agentic RFP Evaluation")
st.caption("AI-assisted supplier evaluation with explainable scoring.")

try:
    initialize_database()
    criteria = get_active_criteria()
except Exception as exc:
    st.error(f"Database initialization failed: {exc}")
    st.stop()

if not criteria:
    st.error("No active evaluation criteria were found in the database.")
    st.stop()

total_weight = sum(float(c["weight"]) for c in criteria)

with st.sidebar:
    st.header("Evaluation Criteria")
    for criterion in criteria:
        st.write(
            f"**{criterion['name']}** — "
            f"{float(criterion['weight']):g}%"
        )
    st.metric("Total weight", f"{total_weight:g}%")

    if abs(total_weight - 100.0) > 0.001:
        st.error("Criterion weights must total 100%.")

st.header("1. Upload proposals")

files = st.file_uploader(
    "Upload supplier PDF proposals",
    type=["pdf"],
    accept_multiple_files=True,
)

suppliers = []

if files:
    for i, file in enumerate(files):
        with st.expander(file.name, expanded=True):
            name = st.text_input(
                "Supplier name",
                value=Path(file.name).stem.replace("_", " ").title(),
                key=f"name_{i}",
            )

            submitted = st.date_input(
                "Submission date",
                value=date.today(),
                key=f"date_{i}",
            )

            experience = st.number_input(
                "Historical experience rating (0–10)",
                min_value=0.0,
                max_value=10.0,
                value=5.0,
                step=0.5,
                key=f"experience_{i}",
            )

            suppliers.append({
                "supplier_name": name.strip(),
                "submission_date": submitted.isoformat(),
                "experience_rating": experience,
                "uploaded_file": file,
            })

st.header("2. Evaluate")

if st.button(
    "Evaluate proposals",
    type="primary",
    disabled=(
        not suppliers
        or abs(total_weight - 100.0) > 0.001
    ),
):
    if any(not s["supplier_name"] for s in suppliers):
        st.error("Please enter a name for every supplier.")
        st.stop()

    temp_paths = []

    try:
        prepared = []

        for supplier in suppliers:
            with tempfile.NamedTemporaryFile(
                suffix=".pdf",
                delete=False,
            ) as temp:
                temp.write(supplier["uploaded_file"].getvalue())
                temp_paths.append(temp.name)

            prepared.append({
                "supplier_name": supplier["supplier_name"],
                "submission_date": supplier["submission_date"],
                "experience_rating": supplier["experience_rating"],
                "pdf_path": temp.name,
            })

        with st.spinner(
            "Reading proposals, evaluating evidence, and ranking suppliers..."
        ):
            result = run_evaluation(prepared)

        st.session_state["latest_result"] = result
        st.success("Evaluation completed.")

    except Exception as exc:
        st.error(f"Evaluation failed: {exc}")

    finally:
        for path in temp_paths:
            try:
                Path(path).unlink(missing_ok=True)
            except OSError:
                pass

result = st.session_state.get("latest_result")

if result:
    st.divider()
    st.header("3. Supplier leaderboard")

    st.write(f"**Run ID:** `{result['rfp_run_id']}`")
    st.write(f"**Status:** {result['status']}")

    leaderboard = pd.DataFrame([
        {
            "Rank": s["final_rank"],
            "Supplier": s["supplier_name"],
            "Absolute Score": s["absolute_score"],
            "PPI (%)": s["ppi"],
            "Submission Date": s["submission_date"],
            "Experience": s["experience_rating"],
        }
        for s in result["results"]
    ])

    st.dataframe(
        leaderboard,
        use_container_width=True,
        hide_index=True,
    )

    st.header("4. Supplier scorecard")

    selected_name = st.selectbox(
        "Select supplier",
        [s["supplier_name"] for s in result["results"]],
    )

    selected = next(
        s for s in result["results"]
        if s["supplier_name"] == selected_name
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Final rank", selected["final_rank"])
    col2.metric("Absolute score", f"{selected['absolute_score']:.2f}/100")
    col3.metric("PPI", f"{selected['ppi']:.2f}%")

    st.dataframe(
        pd.DataFrame([
            {
                "Criterion": c["name"],
                "Score": c["score"],
                "Maximum": c["max_score"],
                "Weight (%)": c["weight"],
                "Benchmark": c["benchmark"],
                "Gap": c["gap"],
                "Relative (%)": c["relative_performance_pct"],
                "Evidence": c["evidence"],
                "Justification": c["justification"],
            }
            for c in selected["criteria_details"]
        ]),
        use_container_width=True,
        hide_index=True,
    )

    with st.expander("Overall summary and risks"):
        st.write(selected["evaluation"]["overall_summary"])
        st.write("Risks:", selected["evaluation"]["risks"])
        st.write("Warnings:", selected["evaluation"]["warnings"])

    st.download_button(
        "Download evaluation JSON",
        data=json.dumps(result, indent=2, ensure_ascii=False),
        file_name=f"rfp_evaluation_{result['rfp_run_id']}.json",
        mime="application/json",
    )
