# Multiphase Teaching Project Plan

## Goal

Bootstrap a student-facing project where learners can use prompts with coding agents to rebuild pieces of an event/economic analysis pipeline and extend it with statistical testing, semantic modeling, and agentic workflows.

## Phase 0 - Curated Data Foundation

Status: complete.

Deliverables:

- copy curated processed event and economic data into `data/processed/`
- preserve both legacy city-level files and newer U.S. county/CBSA files
- include statistical outputs produced by the source project
- write data cards for dataset families

Student outcome:

Students can inspect real processed project data without needing raw sports or Economic Tracker downloads.

## Phase 1 - Statistical Testing Teaching Notebooks

Status: complete.

Deliverables:

- notebook on Welch t-test, Student t-test, and Mann-Whitney U
- notebook on ANOVA and Kruskal-Wallis
- notebook on paired t-test and Wilcoxon signed-rank event windows
- notebook on controlled OLS, multiple testing, and statistical power

Student outcome:

Students can map each test to a research question, identify assumptions, run small examples, and interpret p-values, effect sizes, and caveats.

## Phase 2 - dbt Semantic Layer Notebooks

Status: complete.

Deliverables:

- notebook introducing semantic-layer concepts
- notebook walking through dbt sources and staging models
- notebook covering marts, metrics, and dbt tests
- starter dbt project in `dbt/event_eco_semantic/`

Student outcome:

Students can understand how curated CSV files become reusable analytical models.

## Phase 3 - Agent Foundations

Status: complete.

Deliverables:

- single-tool t-test agent notebook
- multi-tool statistical test selection notebook
- reflection loop notebook
- statistical code generation/debug/refinement notebook

Student outcome:

Students can reason about when an agent should call tools, how to validate the result, and how reflection can improve statistical reasoning.

## Phase 4 - Multi-Agent Research Teams

Status: complete.

Deliverables:

- hierarchical group-chat notebook
- no-hierarchy peer group notebook
- economist/statistician/charting team experimental-design notebook

Student outcome:

Students can compare manager-led and peer-style agent collaboration patterns in the event/economic analysis context.

## Phase 5 - Student Extension Track

Status: planned.

Recommended extensions:

- add a new sport, league, or event type
- build additional dbt marts for event intensity and playoff exposure
- add a notebook for difference-in-differences or event-study design
- build a small Streamlit or static HTML demo
- write grading rubrics for prompt quality, statistical interpretation, and code validation

## Execution Rules For Students

1. Start from the data cards before writing code.
2. Write the research question before choosing a test.
3. Check assumptions before interpreting p-values.
4. Prefer deterministic tools before live LLM calls.
5. Treat agent outputs as drafts that need validation.
6. Use association language unless a causal design is explicitly justified.
