
# System Architecture

## 1. Project Objective

Build an AI-assisted RFP evaluation application that reads supplier
proposals, assesses them against active procurement criteria, and
produces an explainable supplier leaderboard.

## 2. Technology Stack

- Python: application logic and orchestration
- Streamlit: user interface
- OpenAI API: supplier proposal evaluation
- PyMuPDF: PDF text extraction
- SQLite: criteria and evaluation result storage
- pytest: automated testing
- GitHub: version control
- Streamlit Community Cloud: deployment

## 3. Component Responsibilities

### Streamlit UI — app.py
Accepts PDF uploads and supplier metadata, starts evaluations,
displays rankings and scorecards, and provides JSON downloads.

### Evaluation Agent — agents/evaluator.py
Sends the supplier proposal text and active criteria to the LLM.
Returns structured JSON with scores, evidence, justifications,
risks, and a summary.

### Orchestrator — agents/orchestrator.py
Coordinates database access, PDF extraction, AI evaluation,
validation, ranking, and result persistence.

### PDF Reader — tools/pdf_reader.py
Extracts selectable text from supplier PDF documents.

### Validation — tools/validation.py
Checks the AI response, normalizes criterion results, and records
warnings for missing or invalid scores.

### Ranking Engine — tools/ranking.py
Calculates weighted scores, criterion benchmarks, score gaps,
relative performance, PPI, and deterministic final ranks.

### Database — database/db.py
Initializes the SQLite database and manages criteria, run records,
and supplier evaluation results.

## 4. End-to-End Workflow

1. User uploads supplier PDFs and enters metadata.
2. Application loads active criteria from SQLite.
3. Orchestrator creates an evaluation run ID.
4. PDF Reader extracts proposal text.
5. Evaluation Agent assesses each supplier against the criteria.
6. Validation Tool checks and normalizes the AI response.
7. Ranking Engine calculates scores, benchmarks, PPI, and ranks.
8. Database stores the results and evaluation status.
9. Streamlit displays the leaderboard and detailed scorecards.
10. User downloads the evaluation results as JSON.

## 5. Scoring and Ranking

The weighted score is calculated by Python using the normalized
criterion score multiplied by its weight.

PPI compares each supplier's criterion scores with the best
score achieved by any supplier on each criterion.

Final ranking uses this tie-break order:
1. Higher PPI.
2. Earlier submission date.
3. Higher historical experience rating.
4. Supplier name in ascending alphabetical order.

The LLM does not calculate the final ranking.

## 6. Security and Reliability

- Store API keys outside source control.
- Treat proposal contents as untrusted input.
- Validate all LLM output before scoring.
- Do not treat unsupported supplier claims as verified facts.
- Record warnings and failed evaluation runs.
- Test calculations and tie-break rules with pytest.

## 7. Deployment

The application entry point is app.py.
Dependencies are declared in requirements.txt.
Source code is maintained in GitHub.
The API key is configured using Streamlit Community Cloud secrets.
Database initialization runs when the application starts.
