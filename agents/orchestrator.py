
import json
import uuid
from datetime import datetime, timezone

from database.db import (
    get_active_criteria,
    get_connection,
    initialize_database,
)
from tools.pdf_reader import extract_pdf_text
from tools.validation import validate_evaluation
from tools.ranking import rank_suppliers
from agents.evaluator import evaluate_supplier


def run_evaluation(suppliers):
    """
    Evaluate a batch of supplier PDFs and persist the results.

    Each supplier is a dictionary containing:
      supplier_name, pdf_path, submission_date, experience_rating
    """
    initialize_database()
    criteria = get_active_criteria()

    if not criteria:
        raise ValueError("No active evaluation criteria are configured.")

    total_weight = sum(float(c["weight"]) for c in criteria)
    if abs(total_weight - 100.0) > 0.001:
        raise ValueError(
            f"Active criterion weights must total 100%; found {total_weight}."
        )

    if not suppliers:
        raise ValueError("Upload at least one supplier proposal.")

    run_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    # Create a run record before processing suppliers.
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO rfp_runs (rfp_run_id, created_at, status)
            VALUES (?, ?, ?)
            """,
            (run_id, created_at, "RUNNING"),
        )

    evaluated_suppliers = []

    try:
        for supplier in suppliers:
            name = supplier["supplier_name"].strip()
            if not name:
                raise ValueError("Supplier name cannot be empty.")

            proposal_text = extract_pdf_text(supplier["pdf_path"])

            raw_result = evaluate_supplier(
                supplier_name=name,
                proposal_text=proposal_text,
                criteria=criteria,
            )

            evaluation = validate_evaluation(raw_result, criteria)
            evaluation["supplier_name"] = name

            evaluated_suppliers.append({
                "supplier_name": name,
                "submission_date": supplier["submission_date"],
                "experience_rating": float(
                    supplier["experience_rating"]
                ),
                "evaluation": evaluation,
            })

        ranked = rank_suppliers(evaluated_suppliers)

        with get_connection() as connection:
            for supplier in ranked:
                full_result = {
                    "rfp_run_id": run_id,
                    **supplier,
                }

                connection.execute(
                    """
                    INSERT INTO supplier_results (
                        rfp_run_id,
                        supplier_name,
                        submission_date,
                        experience_rating,
                        absolute_score,
                        ppi,
                        final_rank,
                        result_json
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        run_id,
                        supplier["supplier_name"],
                        supplier["submission_date"],
                        supplier["experience_rating"],
                        supplier["absolute_score"],
                        supplier["ppi"],
                        supplier["final_rank"],
                        json.dumps(full_result, ensure_ascii=False),
                    ),
                )

            connection.execute(
                """
                UPDATE rfp_runs
                SET status = ?
                WHERE rfp_run_id = ?
                """,
                ("COMPLETED", run_id),
            )

        return {
            "rfp_run_id": run_id,
            "created_at": created_at,
            "status": "COMPLETED",
            "results": ranked,
        }

    except Exception:
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE rfp_runs
                SET status = ?
                WHERE rfp_run_id = ?
                """,
                ("FAILED", run_id),
            )
        raise
