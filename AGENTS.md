
# AGENTS.md

## Development rules

1. Preserve the existing project structure unless a change is needed.
2. Use Python for orchestration, validation, calculations, and ranking.
3. Use SQLite for evaluation criteria, run metadata, and supplier results.
4. Use Streamlit for the user interface.
5. Use PyMuPDF to extract PDF text.
6. Use an LLM only for proposal assessment and evidence-based explanations.
7. Validate every LLM response before scoring.
8. Never allow the LLM to determine final arithmetic or ranking.
9. Record warnings for missing, malformed, or out-of-range scores.
10. Never commit API keys, secrets, virtual environments, or local databases.

## Required verification

- Run `python -m pytest -v` after meaningful code changes.
- Test missing criteria, invalid scores, zero benchmarks, and ranking ties.
- Keep supplier ranking deterministic for identical validated inputs.
- Confirm that the active criterion weights total 100%.
- Document any incomplete functionality honestly.

## Coding practices

- Prefer small functions with clear responsibilities.
- Use descriptive names and type hints where practical.
- Handle errors explicitly.
- Keep synthetic supplier data separate from application logic.
- Update README.md when setup or execution changes.
