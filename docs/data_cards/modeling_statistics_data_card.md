# Data Card - Modeling And Statistical Outputs

## Purpose

The modeling and statistics files are the main teaching artifacts for hypothesis testing. They combine event exposure with Womply outcomes and contain precomputed statistical outputs from the source project.

## Modeling Panels

| File | Rows | Columns | Description |
| --- | ---: | ---: | --- |
| `data/processed/us/modeling/county_event_panel.csv` | 9,047 | 46 | County-week modeling panel. |
| `data/processed/us/modeling/cbsa_event_panel.csv` | 7,194 | 45 | CBSA-week modeling panel. |

Important columns:

- `has_event`: whether the geography hosted at least one event that week.
- `event_intensity`: number of hosted games in the week.
- `playoff_event`: whether the week included playoff exposure.
- `revenue_all`, `merchants_all`: primary Womply outcomes.
- `revenue_all_vs_rolling4`, `merchants_all_vs_rolling4`: rolling-baseline deviations.
- `year`, `month`, `week_of_year`: calendar controls.

## Statistical Result Files

| File | Rows | Columns | Description |
| --- | ---: | ---: | --- |
| `baseline_test_results.csv` | 64 | 23 | Welch, Student t-test, Mann-Whitney, ANOVA, and Kruskal-Wallis results. |
| `event_window_test_results.csv` | 48 | 19 | Paired t-test and Wilcoxon event-window results. |
| `controlled_model_results.csv` | 24 | 18 | Controlled OLS association models. |
| `multiple_testing_adjustment.csv` | 136 | 10 | Benjamini-Hochberg p-value adjustment. |
| `robustness_checks.csv` | 56 | 13 | Robustness and league-specific comparisons. |
| `county_cbsa_consistency.csv` | 12 | 8 | County/CBSA controlled coefficient sign checks. |
| `hypothesis_candidates.csv` | 8 | 9 | Advisory hypothesis candidates generated from deterministic outputs. |

## Teaching Uses

- select a statistical test based on a research question
- interpret effect size, p-value, and adjusted p-value
- discuss statistical power and sample size
- compare raw, paired, and controlled designs
- evaluate robustness and multiple testing
- use agent-generated hypotheses as review prompts, not final evidence

## Limitations

- Statistical significance does not imply causality.
- Multiple tests require adjusted interpretation.
- Controlled OLS reduces obvious confounding but does not prove identification.
- Event windows can overlap in sports-heavy markets.
- Hypothesis candidates summarize existing evidence and do not create new evidence.
