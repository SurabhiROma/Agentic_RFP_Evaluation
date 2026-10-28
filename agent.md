
# Agent Instructions

Read `AGENTS.md` for the authoritative development rules.

Read `PRD.md` for the project requirements, scoring formulas,
acceptance criteria, and current implementation scope.

Read `architecture.md` for component responsibilities, data flow,
database design, and system boundaries.

Read `README.md` for setup, execution, testing, and deployment steps.

## Project objective

Build an agentic RFP evaluation application that evaluates fictional
supplier proposals, explains criterion-wise scores using proposal
evidence, and produces a reproducible supplier leaderboard.

## Core principle

The LLM evaluates proposal content and supplies evidence and
justifications. Python validates the response and calculates all
weighted scores, peer benchmarks, PPI values, tie-breaks, and ranks.

Never claim a feature is complete until it has been implemented
and tested.
