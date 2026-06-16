from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": text.strip().splitlines(True)}


def code(text: str) -> dict:
    return {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": text.strip().splitlines(True)}


def notebook(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def write_notebook(path: str, cells: list[dict]) -> None:
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(notebook(cells), indent=2) + "\n")
    print(f"wrote {out.relative_to(ROOT)}")


COMMON_SETUP = """
from pathlib import Path
import pandas as pd
import numpy as np
from scipy import stats

ROOT = next(path for path in [Path.cwd(), *Path.cwd().parents] if (path / "data" / "processed").exists())
DATA = ROOT / "data" / "processed" / "us"
"""


def lesson_prompt(text: str) -> dict:
    return md(
        f"""
## Coding Agent Prompt

```text
{text.strip()}
```
"""
    )


def statistics_notebooks() -> None:
    write_notebook(
        "notebooks/statistics/01_t_tests_and_mann_whitney.ipynb",
        [
            md(
                """
# T-Tests And Mann-Whitney U

This notebook explains the two-group tests used in the project:

- Welch t-test
- Student two-sample t-test
- Mann-Whitney U

Use these when comparing two groups, such as event weeks vs non-event weeks.

## Formula

Welch's test statistic is:

$$
t = \\frac{\\bar{x}_1 - \\bar{x}_2}{\\sqrt{s_1^2/n_1 + s_2^2/n_2}}
$$

Mann-Whitney U is rank-based, so it asks whether one group tends to have larger values than the other.
"""
            ),
            lesson_prompt(
                "Given two groups of geography-week outcomes, decide whether Welch t-test, Student t-test, or Mann-Whitney U is appropriate. State the null hypothesis, assumptions, sample sizes, effect size, p-value interpretation, and why the result is association only."
            ),
            code(COMMON_SETUP),
            md(
                """
## Project Context

In this project, `has_event` separates geography-weeks into:

- event weeks
- non-event weeks

The null hypothesis is that the two groups have equal economic activity.
"""
            ),
            code(
                """
panel = pd.read_csv(DATA / "modeling" / "county_event_panel.csv")
event = panel.loc[panel["has_event"], "revenue_all"].dropna()
non_event = panel.loc[~panel["has_event"], "revenue_all"].dropna()

print(len(event), len(non_event))
print(event.mean(), non_event.mean(), event.mean() - non_event.mean())
"""
            ),
            code(
                """
welch = stats.ttest_ind(event, non_event, equal_var=False)
student = stats.ttest_ind(event, non_event, equal_var=True)
mann_whitney = stats.mannwhitneyu(event, non_event, alternative="two-sided")

pd.DataFrame([
    {"test": "Welch t-test", "statistic": welch.statistic, "p_value": welch.pvalue},
    {"test": "Student t-test", "statistic": student.statistic, "p_value": student.pvalue},
    {"test": "Mann-Whitney U", "statistic": mann_whitney.statistic, "p_value": mann_whitney.pvalue},
])
"""
            ),
            md(
                """
## Assumptions

Welch t-test:

- independent observations
- approximately continuous outcome
- does not require equal variance
- more robust than Student t-test when group variances differ

Student two-sample t-test:

- independent observations
- approximately continuous outcome
- assumes equal variance across groups

Mann-Whitney U:

- independent observations
- ordinal or continuous outcome
- compares distributions/ranks rather than strictly comparing means

## Statistical Power Note

Power depends on sample size, effect size, variance, and alpha threshold. Large samples can make very small differences statistically significant. Always read the effect size and the p-value together.

## Interpretation

A small p-value means the observed group difference is unlikely under the equal-groups null. It does not prove sports events caused the difference.
"""
            ),
        ],
    )

    write_notebook(
        "notebooks/statistics/02_anova_and_kruskal.ipynb",
        [
            md(
                """
# ANOVA And Kruskal-Wallis

This notebook explains multi-group tests used for event intensity:

- no-event weeks
- low-intensity event weeks
- high-intensity event weeks

## Formulas

ANOVA compares between-group variance to within-group variance:

$$
F = \\frac{MS_{between}}{MS_{within}}
$$

Kruskal-Wallis is a rank-based alternative:

$$
H = \\frac{12}{N(N+1)}\\sum_i n_i(\\bar{R}_i - \\bar{R})^2
$$
"""
            ),
            lesson_prompt(
                "Given no-event, low-intensity, and high-intensity groups, choose ANOVA or Kruskal-Wallis. Explain assumptions, group-size power concerns, and what a significant omnibus result does and does not tell us."
            ),
            code(COMMON_SETUP),
            code(
                """
panel = pd.read_csv(DATA / "modeling" / "county_event_panel.csv")
positive = panel.loc[panel["event_intensity"] > 0, "event_intensity"]
threshold = positive.median()

panel["intensity_group"] = "No event"
panel.loc[(panel["event_intensity"] > 0) & (panel["event_intensity"] <= threshold), "intensity_group"] = "Low intensity"
panel.loc[panel["event_intensity"] > threshold, "intensity_group"] = "High intensity"

groups = [
    panel.loc[panel["intensity_group"].eq(label), "merchants_all"].dropna()
    for label in ["No event", "Low intensity", "High intensity"]
]
pd.Series({label: len(values) for label, values in zip(["No event", "Low intensity", "High intensity"], groups)})
"""
            ),
            code(
                """
anova = stats.f_oneway(*groups)
kruskal = stats.kruskal(*groups)

pd.DataFrame([
    {"test": "ANOVA", "statistic": anova.statistic, "p_value": anova.pvalue},
    {"test": "Kruskal-Wallis", "statistic": kruskal.statistic, "p_value": kruskal.pvalue},
])
"""
            ),
            md(
                """
## Assumptions

ANOVA:

- independent observations
- approximately normal residuals within groups
- similar variance across groups
- tests whether at least one group mean differs

Kruskal-Wallis:

- independent observations
- ordinal or continuous outcome
- does not require normality
- tests whether group distributions differ

## Statistical Power Note

Multi-group tests need enough observations in each group. If one event-intensity group is rare, the test may have weak power even when the overall dataset is large.

## Interpretation

A small p-value says at least one group differs. It does not tell you which pair differs or prove a monotonic dose-response relationship.
"""
            ),
        ],
    )

    write_notebook(
        "notebooks/statistics/03_paired_event_window_tests.ipynb",
        [
            md(
                """
# Paired Event-Window Tests

This notebook explains:

- paired t-test
- Wilcoxon signed-rank test

These compare event/post-event windows with pre-event windows inside the same geography.

## Formula

For paired differences $d_i = post_i - pre_i$:

$$
t = \\frac{\\bar{d}}{s_d / \\sqrt{n}}
$$

Wilcoxon signed-rank uses the ranks of non-zero paired differences.
"""
            ),
            lesson_prompt(
                "Given event-window pre and post means for the same geographies, choose paired t-test or Wilcoxon signed-rank. State the paired null hypothesis, overlap risks, power concerns, and interpretation caveats."
            ),
            code(COMMON_SETUP),
            code(
                """
windows = pd.read_csv(DATA / "statistics" / "county_event_window_panel.csv")
one_week = windows.loc[windows["window_size_weeks"].eq(1)].dropna(
    subset=["revenue_all_pre_mean", "revenue_all_post_mean"]
)
pre = one_week["revenue_all_pre_mean"]
post = one_week["revenue_all_post_mean"]
delta = post - pre

print(len(delta), delta.mean(), delta.median())
"""
            ),
            code(
                """
paired_t = stats.ttest_rel(post, pre)
wilcoxon = stats.wilcoxon(post, pre, zero_method="wilcox")

pd.DataFrame([
    {"test": "Paired t-test", "statistic": paired_t.statistic, "p_value": paired_t.pvalue},
    {"test": "Wilcoxon signed-rank", "statistic": wilcoxon.statistic, "p_value": wilcoxon.pvalue},
])
"""
            ),
            md(
                """
## Assumptions

Paired t-test:

- observations are naturally paired
- paired differences are approximately normally distributed
- pairs are independent of other pairs

Wilcoxon signed-rank:

- observations are naturally paired
- paired differences are symmetrically distributed around the median
- less sensitive to non-normality than paired t-test

## Statistical Power Note

Power depends on the number of matched event windows and the variance of paired differences. Pairing can improve power because each geography acts as its own baseline, but overlapping event windows can weaken interpretation.

## Interpretation

Positive `post - pre` means event/post windows are higher than pre-event windows. A small p-value says the average or median paired difference is unlikely to be zero under the null.
"""
            ),
        ],
    )

    write_notebook(
        "notebooks/statistics/04_controlled_models_multiple_testing_power.ipynb",
        [
            md(
                """
# Controlled Models, Multiple Testing, And Power

This notebook explains the controlled OLS model outputs, Benjamini-Hochberg adjustment, and basic statistical power intuition.

## Formulas

Controlled association model:

$$
y_{g,t} = \\beta_0 + \\beta_1 EventExposure_{g,t} + \\gamma_g + \\delta_t + \\theta Trend_{g,t} + \\epsilon_{g,t}
$$

Benjamini-Hochberg adjustment ranks p-values and compares each p-value to:

$$
\\frac{i}{m}Q
$$

where $i$ is rank, $m$ is the number of tests, and $Q$ is the target false-discovery rate.
"""
            ),
            lesson_prompt(
                "Given controlled model outputs and multiple-testing results, identify which associations are strongest. Explain coefficient direction, confidence interval, raw p-value, BH-adjusted p-value, power concerns, and why OLS is not causal proof here."
            ),
            code(COMMON_SETUP),
            code(
                """
controlled = pd.read_csv(DATA / "statistics" / "controlled_model_results.csv")
controlled[["geography_level", "outcome", "treatment", "coefficient", "p_value", "ci_lower", "ci_upper"]].head(10)
"""
            ),
            code(
                """
adjusted = pd.read_csv(DATA / "statistics" / "multiple_testing_adjustment.csv")
adjusted[["test_family", "geography_level", "outcome", "treatment", "raw_p_value", "bh_adjusted_p_value", "significant_bh_0_05"]].head()
"""
            ),
            md(
                """
## Controlled OLS Assumptions

- the model includes the right functional form for the intended association
- residuals are independent enough for ordinary standard errors to be meaningful
- treatment is not perfectly collinear with controls
- omitted variables may still bias coefficients

## Multiple Testing Assumption

Benjamini-Hochberg controls the expected false discovery rate under standard dependence assumptions. It is not a substitute for a good research design.

## Statistical Power Note

Power increases when:

- sample size increases
- effect size increases
- outcome noise decreases
- the test is well matched to the design

Power decreases when:

- event groups are small
- outcomes are noisy
- many comparisons require stricter adjusted interpretation
- model controls absorb much of the variation

## Interpretation

Prefer results that have a meaningful coefficient, reasonable uncertainty, an adjusted p-value below the chosen threshold, and robustness support. Even then, describe the result as association unless a causal design is added.
"""
            ),
        ],
    )


def dbt_notebooks() -> None:
    write_notebook(
        "notebooks/dbt_semantic_layer/01_semantic_layer_concepts.ipynb",
        [
            md(
                """
# Semantic Layer Concepts With dbt

A semantic layer gives names, definitions, and tested transformations to the data that analysts and agents use.

In this project, the semantic layer turns processed CSVs into reusable concepts:

- event exposure
- economic outcomes
- geography-week grain
- treatment flags
- analysis-ready marts

```mermaid
flowchart LR
    CSV[Curated CSV files] --> Sources[dbt sources]
    Sources --> Staging[staging models]
    Staging --> Marts[analysis marts]
    Marts --> Metrics[metrics and tests]
    Metrics --> Agents[agent tools and notebooks]
```
"""
            ),
            lesson_prompt(
                "Act as an analytics engineer. Explain how a semantic layer turns curated CSVs into tested, reusable marts for event/economic analysis. Identify sources, staging models, marts, tests, and metrics."
            ),
            code(COMMON_SETUP),
            code(
                """
county = pd.read_csv(DATA / "modeling" / "county_event_panel.csv", nrows=5)
county.T.head(20)
"""
            ),
            md(
                """
## Why dbt?

dbt helps students learn:

- source definition
- staging model cleanup
- marts for analytical use cases
- tests for not-null and uniqueness assumptions
- documentation close to transformations

The starter project lives in `dbt/event_eco_semantic/`.
"""
            ),
        ],
    )

    write_notebook(
        "notebooks/dbt_semantic_layer/02_sources_and_staging_models.ipynb",
        [
            md(
                """
# dbt Sources And Staging Models

This notebook walks through how the dbt starter project reads curated CSVs and turns them into staging models.

```mermaid
flowchart TD
    RawCSV[event_county_weekly_exposure.csv] --> Staging[stg_event_county_weekly_exposure]
    Womply[womply_county_weekly.csv] --> EconStage[stg_womply_county_weekly]
```
"""
            ),
            lesson_prompt(
                "Create a dbt staging model for one processed CSV. Cast identifiers and numeric columns, document the grain, add not-null tests, and explain how students should validate the model."
            ),
            code(
                """
from pathlib import Path
ROOT = next(path for path in [Path.cwd(), *Path.cwd().parents] if (path / "dbt").exists())
project = ROOT / "dbt" / "event_eco_semantic"
print(project)
print((project / "models/staging/stg_event_county_weekly_exposure.sql").read_text())
"""
            ),
            md(
                """
## Student Exercise

Add a CBSA staging model:

1. read `data/processed/us/event_cbsa_weekly_exposure.csv`
2. cast IDs and numeric fields
3. document not-null columns in `schema.yml`
4. run `dbt run` and `dbt test`
"""
            ),
        ],
    )

    write_notebook(
        "notebooks/dbt_semantic_layer/03_marts_metrics_and_tests.ipynb",
        [
            md(
                """
# dbt Marts, Metrics, And Tests

Marts are teaching-friendly tables that express the analytical grain clearly. Here the mart grain is county-week.

```mermaid
flowchart LR
    ExposureStage[Event exposure staging] --> Mart[County event economic weekly mart]
    EconomicStage[Womply county staging] --> Mart
    Mart --> StatisticalPanel[Statistics-ready panel]
```
"""
            ),
            lesson_prompt(
                "Design a dbt mart for county-week event/economic analysis. Specify the grain, join keys, expected tests, and metrics a student should expose."
            ),
            code(
                """
from pathlib import Path
ROOT = next(path for path in [Path.cwd(), *Path.cwd().parents] if (path / "dbt").exists())
project = ROOT / "dbt" / "event_eco_semantic"
print((project / "models/marts/county_event_economic_weekly.sql").read_text())
"""
            ),
            md(
                """
## Suggested Metrics

- event weeks: count of rows where `has_event`
- total games: sum of `game_count`
- mean revenue: average `revenue_all`
- mean merchants: average `merchants_all`
- playoff weeks: count of rows where `playoff_event`

## Suggested dbt Tests

- county-week should be unique in the mart
- county and week fields should be not null
- event counts should be non-negative
- outcome columns should be documented as nullable because economic coverage can vary
"""
            ),
        ],
    )


AGENT_SETUP = """
from typing import Annotated
import pandas as pd
from scipy import stats

def format_p_value(p: float) -> str:
    return f"{p:.4g}"
"""


def agent_notebooks() -> None:
    write_notebook(
        "notebooks/agents/01_single_t_test_tool_agent.ipynb",
        [
            md(
                """
# Agent 1 - Single T-Test Tool

Goal: build the simplest statistical tool-calling agent.

The live Microsoft Agent Framework pattern is to pass Python functions through `tools=` or decorate with `@tool`. This notebook keeps a deterministic local function first, then shows optional Agent Framework wiring.

```mermaid
flowchart LR
    Prompt[Student prompt with data] --> Agent[TTestCoach]
    Agent --> Tool[Welch t-test tool]
    Tool --> Agent
    Agent --> Answer[Assumptions, p-value, interpretation]
```
"""
            ),
            lesson_prompt(
                "Build a single-tool statistical agent. The agent should ask for two numeric groups, call a Welch t-test tool, report sample sizes, means, p-value, and explain that the result is association evidence only."
            ),
            code(AGENT_SETUP),
            code(
                """
def welch_t_test(group_a: list[float], group_b: list[float]) -> dict:
    \"\"\"Run Welch's t-test for two independent samples.\"\"\"
    result = stats.ttest_ind(group_a, group_b, equal_var=False)
    return {
        "test": "Welch t-test",
        "n_a": len(group_a),
        "n_b": len(group_b),
        "mean_a": sum(group_a) / len(group_a),
        "mean_b": sum(group_b) / len(group_b),
        "p_value": result.pvalue,
        "interpretation": "Small p-values are evidence against equal means, not proof of causality.",
    }

welch_t_test([1.2, 1.5, 1.7, 1.4], [0.8, 1.0, 1.1, 0.9])
"""
            ),
            code(
                """
# Optional live-agent sketch.
# Requires `pip install agent-framework` and model credentials.
#
# from agent_framework import tool
#
# @tool(name="welch_t_test_tool", description="Run Welch's t-test on two numeric groups.")
# def welch_t_test_tool(group_a: list[float], group_b: list[float]) -> dict:
#     return welch_t_test(group_a, group_b)
#
# agent = chat_client.as_agent(
#     name="TTestCoach",
#     instructions="Help students structure and interpret Welch t-tests. Avoid causal claims.",
#     tools=[welch_t_test_tool],
# )
# result = await agent.run("Compare group A [1.2,1.5,1.7] and group B [0.8,1.0,1.1].")
"""
            ),
        ],
    )

    write_notebook(
        "notebooks/agents/02_multi_test_tool_selection_agent.ipynb",
        [
            md(
                """
# Agent 2 - Multiple Statistical Tools

Goal: give the agent several tools and teach it to choose based on scenario.

```mermaid
flowchart TD
    Scenario[Scenario] --> Paired{Paired data?}
    Paired -- Yes --> PairTools[Paired t-test or Wilcoxon]
    Paired -- No --> Groups{How many groups?}
    Groups -- Two --> TwoTools[Welch, Student, or Mann-Whitney]
    Groups -- ThreePlus --> MultiTools[ANOVA or Kruskal-Wallis]
```
"""
            ),
            lesson_prompt(
                "Given a statistical scenario, route to one of this project's tests. Explain the routing rule, assumptions, and what additional information the agent should ask for before calling a tool."
            ),
            code(AGENT_SETUP),
            code(
                """
def student_t_test(a, b):
    return stats.ttest_ind(a, b, equal_var=True)._asdict()

def mann_whitney(a, b):
    result = stats.mannwhitneyu(a, b, alternative="two-sided")
    return {"statistic": result.statistic, "p_value": result.pvalue}

def anova(*groups):
    result = stats.f_oneway(*groups)
    return {"statistic": result.statistic, "p_value": result.pvalue}

def choose_test(scenario: str) -> str:
    scenario = scenario.lower()
    if "three" in scenario or "multiple groups" in scenario or "intensity" in scenario:
        return "ANOVA or Kruskal-Wallis"
    if "non-normal" in scenario or "skew" in scenario:
        return "Mann-Whitney U"
    if "unequal variance" in scenario:
        return "Welch t-test"
    return "Welch t-test as a robust default for two independent groups"

choose_test("Compare event and non-event weeks with unequal variance")
"""
            ),
            md(
                """
## Agent Design Note

Tool selection should be grounded in assumptions:

- two independent groups: Welch or Student t-test
- two skewed groups: Mann-Whitney U
- three or more groups: ANOVA or Kruskal-Wallis
- paired before/after data: paired t-test or Wilcoxon signed-rank
"""
            ),
        ],
    )

    write_notebook(
        "notebooks/agents/03_reflection_loop_for_statistical_reasoning.ipynb",
        [
            md(
                """
# Agent 3 - Reflection Loop

Goal: add a review step before final interpretation.

```mermaid
flowchart LR
    Draft[Draft answer] --> Reflect[Reflection checklist]
    Reflect --> Issues[Assumptions, power, overclaiming]
    Issues --> Revised[Revised interpretation]
```
"""
            ),
            lesson_prompt(
                "Review a statistical answer for missing assumptions, wrong test choice, power concerns, multiple testing, effect-size interpretation, and causal overclaiming. Return a safer revised answer."
            ),
            code(
                """
draft = {
    "claim": "Sports events caused revenue to increase.",
    "test": "Welch t-test",
    "p_value": 0.01,
    "effect": 0.03,
}

def reflect_on_claim(result: dict) -> list[str]:
    issues = []
    if "caused" in result["claim"].lower():
        issues.append("Replace causal language with association language.")
    if result["p_value"] < 0.05 and abs(result["effect"]) < 0.01:
        issues.append("Statistical significance may not be practically large.")
    if result["test"] == "Welch t-test":
        issues.append("Check independence and group definition.")
    return issues

reflect_on_claim(draft)
"""
            ),
            md(
                """
Reflection is useful when the first answer may be statistically overconfident. The reviewer should look for wrong test choice, missing assumptions, overclaiming, and missing effect-size interpretation.
"""
            ),
        ],
    )

    write_notebook(
        "notebooks/agents/04_code_generation_bug_fix_stat_agent.ipynb",
        [
            md(
                """
# Agent 4 - Generate Code, Run It, Learn From Bugs

Goal: show a constrained code-generation loop for statistical examples.

```mermaid
flowchart TD
    Generate[Generate statistical code] --> Run[Run code]
    Run --> Error{Error?}
    Error -- Yes --> Diagnose[Diagnose bug]
    Diagnose --> Fix[Patch code]
    Fix --> Run
    Error -- No --> Interpret[Interpret output]
```
"""
            ),
            lesson_prompt(
                "Generate Python code for a small statistical test, execute it, inspect failures, fix bugs, and rerun. Keep the example limited to pandas and scipy, and end with a guarded interpretation."
            ),
            code(
                """
buggy_code = '''
from scipy import stats
result = stats.ttest_ind(group_a, group_b, equal_var=False)
print(result.pvalue)
'''

context = {"group_a": [1, 2, 3], "group_b": [2, 3, 4]}

def run_generated_code(code_text: str, context: dict) -> tuple[bool, str]:
    namespace = dict(context)
    try:
        exec(code_text, namespace)
        return True, "success"
    except Exception as exc:
        return False, str(exc)

run_generated_code(buggy_code, context)
"""
            ),
            code(
                """
fixed_code = '''
from scipy import stats
result = stats.ttest_ind(group_a, group_b, equal_var=False)
p_value = result.pvalue
'''

ok, message = run_generated_code(fixed_code, context)
ok, message
"""
            ),
            md(
                """
Keep code-generation agents constrained:

- small statistical examples only
- no file deletion
- no network calls
- inspect exceptions
- rerun tests after fixes
"""
            ),
        ],
    )

    write_notebook(
        "notebooks/agents/05_hierarchical_group_chat_research_team.ipynb",
        [
            md(
                """
# Agent 5 - Hierarchical Group Chat

Goal: illustrate a manager-led team.

Roles:

- team lead: asks clarifying questions and assigns work
- statistician: chooses tests and checks assumptions
- charting specialist: proposes plots

Microsoft Agent Framework's `GroupChatBuilder` supports manager-directed group chat where a manager chooses the next speaker.

```mermaid
flowchart TD
    User[User] --> Lead[Team lead]
    Lead --> Economist[Economist]
    Lead --> Statistician[Statistician]
    Lead --> Charting[Charting specialist]
    Economist --> Lead
    Statistician --> Lead
    Charting --> Lead
    Lead --> Final[Final answer]
```
"""
            ),
            lesson_prompt(
                "Design a hierarchical group chat for an event/economic research question. Assign roles to a team lead, economist, statistician, and charting specialist, then define the final synthesis rules."
            ),
            code(
                """
roles = {
    "team_lead": "Clarify the user question and coordinate the response.",
    "statistician": "Choose tests, assumptions, and interpretation caveats.",
    "charting_specialist": "Recommend plots that reveal distributions and uncertainty.",
}

for role, responsibility in roles.items():
    print(role, "->", responsibility)
"""
            ),
            code(
                """
# Optional live-agent sketch:
#
# from agent_framework import GroupChatBuilder
# group = (
#     GroupChatBuilder()
#     .set_participants({"team_lead": lead_agent, "statistician": stats_agent, "charting": chart_agent})
#     .set_manager(manager_agent)
#     .set_max_rounds(6)
#     .build()
# )
# result = await group.run("Design an analysis for playoff games and merchant activity.")
"""
            ),
        ],
    )

    write_notebook(
        "notebooks/agents/06_peer_group_no_hierarchy.ipynb",
        [
            md(
                """
# Agent 6 - Peer Group Without Hierarchy

Goal: compare a no-hierarchy team with a manager-led team.

```mermaid
flowchart LR
    Economist <--> Statistician
    Statistician <--> DataEngineer[Data engineer]
    DataEngineer <--> Visualization[Visualization specialist]
    Visualization <--> Economist
```
"""
            ),
            lesson_prompt(
                "Design a no-hierarchy peer group for the same research question. Explain how peers exchange critiques, how conflicts are resolved, and how the final answer avoids overclaiming."
            ),
            code(
                """
peer_prompts = [
    "Economist: propose a plausible mechanism and confounders.",
    "Statistician: choose tests and assumptions.",
    "Data engineer: identify data joins and missingness risks.",
    "Visualization specialist: propose EDA plots.",
]

for prompt in peer_prompts:
    print(prompt)
"""
            ),
            md(
                """
No-hierarchy teams can generate diverse ideas quickly, but they need a synthesis step. Without one, they may produce inconsistent recommendations.
"""
            ),
        ],
    )

    write_notebook(
        "notebooks/agents/07_economist_statistician_experiment_team.ipynb",
        [
            md(
                """
# Agent 7 - Event/Economic Research Team

Goal: simulate a group of economists and statisticians proposing hypotheses, designing experiments, pulling data, and running tests.

```mermaid
flowchart TD
    Hypothesis[Propose hypothesis] --> Design[Choose design]
    Design --> Data[Pull modeling/statistical data]
    Data --> Test[Run ANOVA, t-test, paired test, or OLS]
    Test --> Review[Robustness and caveat review]
    Review --> Decision[Accept, reject, or revise]
```
"""
            ),
            lesson_prompt(
                "Act as an economist-statistician research team. Propose a hypothesis from the event/economic data, choose an experimental architecture using only tests from this project, run or reference the appropriate output, and accept, reject, or revise with caveats."
            ),
            code(COMMON_SETUP),
            code(
                """
controlled = pd.read_csv(DATA / "statistics" / "controlled_model_results.csv")
controlled.sort_values("p_value").head(5)[
    ["geography_level", "outcome", "treatment", "coefficient", "p_value", "caveat"]
]
"""
            ),
            md(
                """
## Example Team Flow

1. Economist proposes a mechanism.
2. Statistician translates it into a testable hypothesis.
3. Data engineer selects the modeling panel and required columns.
4. Statistician runs Welch, ANOVA, paired tests, or controlled OLS as appropriate.
5. Reviewer checks multiple testing, robustness, and claim language.
6. Team accepts, rejects, or revises the hypothesis.

Acceptance means "supported as an association in this specification", not "causally proven".
"""
            ),
        ],
    )


def main() -> None:
    statistics_notebooks()
    dbt_notebooks()
    agent_notebooks()


if __name__ == "__main__":
    main()
