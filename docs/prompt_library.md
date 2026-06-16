# Prompt Library

Use these prompts with a coding agent to rebuild or extend the teaching project.

## Phase 0 - Data Inventory

```text
Act as a data engineer. Inspect `data/processed/` and the data cards. Produce a table of dataset families, row counts, grain, primary keys, and caveats. Do not infer causality.
```

## Phase 1 - Statistical Test Selection

```text
Act as a statistician. I will give you a treatment, outcome, geography level, and comparison design. Choose the appropriate test from this project only: Welch t-test, Student t-test, Mann-Whitney U, ANOVA, Kruskal-Wallis, paired t-test, Wilcoxon signed-rank, or controlled OLS. Explain the null hypothesis, assumptions, power concerns, and interpretation caveats.
```

## Phase 2 - dbt Semantic Layer

```text
Act as an analytics engineer. Build a dbt source, staging model, and mart for one processed CSV family. Explain the model grain, column casts, tests, and how the mart supports statistical analysis.
```

## Phase 3 - Single Tool Agent

```text
Act as an agent engineer. Create a tool that runs Welch's t-test on two numeric groups. Then define an agent instruction that asks clarifying questions, calls the tool only when data is sufficient, and explains the result without causal language.
```

## Phase 4 - Multi-Test Agent

```text
Act as an agent engineer and statistician. Create tools for Welch t-test, Mann-Whitney U, ANOVA, Kruskal-Wallis, paired t-test, and Wilcoxon signed-rank. Write routing rules that choose the test based on independent vs paired data, number of groups, distribution concerns, and sample size.
```

## Phase 5 - Reflection Agent

```text
Act as a reviewer agent. Given a proposed statistical answer, check for wrong test choice, missing assumptions, weak power, multiple testing, missing effect size, and causal overclaiming. Return a revised interpretation.
```

## Phase 6 - Code Generation And Repair

```text
Act as a constrained coding agent. Generate Python code for a statistical example, run it, inspect any error, fix it, and rerun. Limit yourself to pandas, scipy, and statsmodels examples. Never delete files or use network access.
```

## Phase 7 - Multi-Agent Research Team

```text
Act as a manager of a research team with an economist, statistician, data engineer, and visualization specialist. Given an event/economic research question, assign tasks, synthesize the findings, choose a test architecture, and state what evidence would support or reject the hypothesis. Use association language only.
```
