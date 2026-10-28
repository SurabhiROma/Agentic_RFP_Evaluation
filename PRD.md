
# Product Requirements Document (PRD)

## 1. Project Overview

**Project:** Agentic RFP Evaluation and Supplier Ranking

Build an AI-assisted application that evaluates multiple supplier
proposals against configurable procurement criteria and generates
an explainable, deterministic supplier leaderboard.

## 2. Business Problem

Procurement teams receive multiple supplier RFP responses as PDFs.
Manual comparison is time-consuming and may produce inconsistent
evaluations.

The application will extract proposal text, use an LLM to assess
each supplier, validate the assessments, calculate scores using
Python, compare suppliers, and display the results.

## 3. Technology Stack

- Python: application logic and orchestration
- Streamlit: user interface
- SQLite: evaluation criteria and results
- PyMuPDF: PDF text extraction
- OpenAI API: proposal evaluation
- Pydantic or custom Python validation: response validation
- pytest: automated testing
- GitHub: source control
- Streamlit Community Cloud: deployment

## 4. Evaluation Criteria

| Criterion | Weight | Maximum Score |
|---|---:|---:|
| Technical Capability | 30% | 10 |
| Implementation Plan | 20% | 10 |
| Commercial Value | 20% | 10 |
| Security & Compliance | 20% | 10 |
| Support & Experience | 10% | 10 |

The active criterion weights must total 100%.

## 5. Functional Requirements

1. Load active evaluation criteria from SQLite.
2. Allow multiple supplier PDF uploads.
3. Collect supplier name, submission date, and historical
   experience rating.
4. Create a unique identifier for every evaluation run.
5. Extract text from every supplier PDF.
6. Ask the LLM to evaluate every active criterion.
7. Require JSON output containing criterion IDs, scores,
   justifications, evidence, risks, and an overall summary.
8. Validate and normalize AI responses.
9. Calculate weighted scores in Python.
10. Calculate criterion benchmarks, gaps, relative performance,
    and the Peer Performance Index (PPI).
11. Rank suppliers using the required deterministic tie-break order.
12. Save complete results to SQLite.
13. Display a leaderboard and detailed supplier scorecards.
14. Allow users to download evaluation results as JSON.

## 6. Scoring Rules

### Absolute Weighted Score

Sum the following for every active criterion:

(score / maximum score) * criterion weight

The result is expressed on a scale of 0 to 100.

### Criterion Benchmark

The highest valid score achieved by any supplier for that criterion.

### Criterion Gap

Supplier criterion score minus criterion benchmark.

### Relative Performance Percentage

(supplier score / benchmark score) * 100

Define safe handling when the benchmark is zero.

### Peer Performance Index (PPI)

Weighted average of criterion relative-performance percentages.

## 7. Required Ranking Order

1. Higher PPI first.
2. Earlier submission date first.
3. Higher historical experience rating first.
4. Supplier name in ascending alphabetical order.

Assign sequential ranks only after sorting.

## 8. User Interface

The Streamlit application must contain:

- Active criteria and weights
- Supplier upload and metadata input
- Validation messages
- Evaluate button
- Supplier leaderboard
- Detailed criterion scorecards
- Benchmark, gap, relative performance, evidence, and justification
- Evaluation run ID
- Warnings and tie-break explanations
- JSON download

## 9. Synthetic Test Suppliers

- Apex Systems: strong technical design and security; higher price.
- BrightPath Tech: low price and fast delivery; weaker compliance evidence.
- NexaWorks: balanced proposal; strong implementation and support.
- Orbit Digital: strong experience and references; vague integration plan.

## 10. Acceptance Criteria

- All four synthetic supplier PDFs can be read.
- Invalid or missing AI scores are handled safely.
- Active criteria weights are validated.
- Scoring and ranking are deterministic for validated inputs.
- Supplier evidence and explanations are available.
- Evaluation results are stored and downloadable.
- Automated tests pass.
- The deployed application can complete an evaluation run.

## 11. Security and Limitations

- Never expose API keys in source code or GitHub.
- Treat proposal text as untrusted input.
- Do not allow the LLM to decide final scores mathematically,
  peer benchmarks, or ranks.
- Clearly report missing evidence and evaluation warnings.
- Use fictional supplier proposals for demonstrations.
