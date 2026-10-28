
def validate_evaluation(raw_result, criteria):
    """Validate and normalize an AI evaluation against active criteria."""

    warnings = []

    if not isinstance(raw_result, dict):
        raw_result = {}
        warnings.append("AI response was not a valid JSON object.")

    supplied = raw_result.get("criteria", [])

    if not isinstance(supplied, list):
        supplied = []
        warnings.append("AI criteria field was not a list.")

    # Index the AI results by criterion ID.
    by_id = {}
    for item in supplied:
        if isinstance(item, dict):
            criterion_id = item.get("criterion_id")
            if criterion_id not in by_id:
                by_id[criterion_id] = item

    validated = []

    for criterion in criteria:
        criterion_id = criterion["criterion_id"]
        max_score = float(criterion["max_score"])
        item = by_id.get(criterion_id)

        if item is None:
            warnings.append(
                f"Missing result for {criterion['name']}; score set to zero."
            )
            item = {}

        try:
            score = float(item.get("score", 0))
            if not (score == score):  # Detect NaN
                raise ValueError("Invalid numeric score")
        except (TypeError, ValueError):
            score = 0.0
            warnings.append(
                f"Invalid score for {criterion['name']}; score set to zero."
            )

        if score < 0 or score > max_score:
            warnings.append(
                f"Score for {criterion['name']} was outside the permitted "
                "range and has been clipped."
            )
            score = max(0.0, min(score, max_score))

        validated.append({
            "criterion_id": criterion_id,
            "name": criterion["name"],
            "score": score,
            "max_score": max_score,
            "weight": float(criterion["weight"]),
            "justification": str(
                item.get("justification") or "No justification supplied."
            ),
            "evidence": str(
                item.get("evidence") or "No supporting evidence supplied."
            ),
        })

    risks = raw_result.get("risks", [])
    if not isinstance(risks, list):
        risks = [str(risks)]

    return {
        "supplier_name": str(raw_result.get("supplier_name", "Unknown")),
        "criteria": validated,
        "risks": risks,
        "overall_summary": str(raw_result.get("overall_summary", "")),
        "warnings": warnings,
    }
