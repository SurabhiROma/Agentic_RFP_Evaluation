
from copy import deepcopy


def calculate_supplier_score(evaluation):
    """
    Calculate the weighted supplier score out of 100.

    Each criterion score is normalized against its maximum score,
    then multiplied by its weight.
    """
    total = 0.0

    for criterion in evaluation["criteria"]:
        max_score = float(criterion["max_score"])
        weight = float(criterion["weight"])
        score = float(criterion["score"])

        if max_score <= 0:
            raise ValueError(
                f"Maximum score must be positive for {criterion.get('name')}."
            )

        if weight < 0:
            raise ValueError("Criterion weight cannot be negative.")

        if not 0 <= score <= max_score:
            raise ValueError(
                f"Score for {criterion.get('name')} is out of range."
            )

        total += (score / max_score) * weight

    return round(total, 4)


def rank_suppliers(suppliers):
    """
    Calculate benchmarks, gaps, relative performance, PPI and ranks.

    Required supplier fields:
        supplier_name
        submission_date (ISO date string: YYYY-MM-DD)
        experience_rating
        evaluation

    The evaluation must contain a criteria list with:
        criterion_id, name, score, max_score, weight
    """
    if not suppliers:
        return []

    results = deepcopy(suppliers)

    # All suppliers must be evaluated against the same criteria.
    first_criteria = results[0]["evaluation"]["criteria"]
    expected_ids = {c["criterion_id"] for c in first_criteria}

    if not expected_ids:
        raise ValueError("No evaluation criteria were supplied.")

    for supplier in results:
        actual_ids = {
            c["criterion_id"]
            for c in supplier["evaluation"]["criteria"]
        }

        if actual_ids != expected_ids:
            raise ValueError(
                "All suppliers must have the same active evaluation criteria."
            )

    # Validate weights and their total.
    total_weight = sum(float(c["weight"]) for c in first_criteria)

    if abs(total_weight - 100.0) > 0.001:
        raise ValueError(
            f"Criterion weights must total 100; received {total_weight}."
        )

    # Find the highest score achieved for each criterion.
    benchmarks = {}

    for criterion_id in expected_ids:
        criterion_scores = []

        for supplier in results:
            for criterion in supplier["evaluation"]["criteria"]:
                if criterion["criterion_id"] == criterion_id:
                    score = float(criterion["score"])
                    max_score = float(criterion["max_score"])

                    if max_score <= 0 or not 0 <= score <= max_score:
                        raise ValueError(
                            f"Invalid score for criterion {criterion_id}."
                        )

                    criterion_scores.append(score)

        benchmarks[criterion_id] = max(criterion_scores, default=0.0)

    # Calculate each supplier's absolute score and PPI.
    for supplier in results:
        evaluation = supplier["evaluation"]

        supplier["absolute_score"] = calculate_supplier_score(evaluation)

        weighted_relative_total = 0.0
        total_weight = 0.0
        detailed_criteria = []

        for criterion in evaluation["criteria"]:
            criterion_id = criterion["criterion_id"]
            score = float(criterion["score"])
            max_score = float(criterion["max_score"])
            weight = float(criterion["weight"])
            benchmark = benchmarks[criterion_id]

            # A zero benchmark means every supplier scored zero.
            relative = (
                score / benchmark * 100.0
                if benchmark > 0
                else 0.0
            )

            gap = score - benchmark

            detailed_criteria.append({
                **criterion,
                "benchmark": benchmark,
                "gap": round(gap, 4),
                "relative_performance_pct": round(relative, 4),
            })

            weighted_relative_total += relative * weight
            total_weight += weight

        supplier["ppi"] = round(
            weighted_relative_total / total_weight
            if total_weight > 0 else 0.0,
            4,
        )

        supplier["criteria_details"] = detailed_criteria

    # Deterministic tie-break order:
    # 1. Higher PPI
    # 2. Earlier submission date
    # 3. Higher historical experience rating
    # 4. Supplier name alphabetically
    results.sort(
        key=lambda supplier: (
            -supplier["ppi"],
            supplier["submission_date"],
            -float(supplier["experience_rating"]),
            supplier["supplier_name"].casefold(),
        )
    )

    for rank, supplier in enumerate(results, start=1):
        supplier["final_rank"] = rank

    return results
