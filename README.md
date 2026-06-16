# Event Eco Agent

Teaching project for rebuilding and extending an event/economic analysis pipeline with coding agents.

Students use prompts with tools such as Codex to rebuild parts of a project that studies whether U.S. sports event exposure is associated with local economic activity. The repository includes curated processed data, data cards, notebook lessons, a dbt semantic-layer starter, and agent-design notebooks.

## What Is Included

- processed event and economic datasets under `data/processed/`
- data cards under `docs/data_cards/`
- statistical-testing notebooks under `notebooks/statistics/`
- dbt semantic-layer notebooks under `notebooks/dbt_semantic_layer/`
- Microsoft Agent Framework notebooks under `notebooks/agents/`
- starter dbt project under `dbt/event_eco_semantic/`
- multiphase teaching plan under `docs/multiphase_plan.md`

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter lab
```

Open the notebooks in order:

1. `notebooks/statistics/`
2. `notebooks/dbt_semantic_layer/`
3. `notebooks/agents/`

## Claim Boundary

The included project data supports teaching examples about statistical association. It does not prove that sports events cause economic activity changes.

Use language like:

```text
Sports event exposure is associated with Womply activity in this specification.
```

Avoid language like:

```text
Sports events caused higher economic activity.
```

## Microsoft Agent Framework Notes

The agent notebooks use Microsoft Agent Framework concepts from the official docs:

- overview: https://learn.microsoft.com/en-us/agent-framework/overview/
- function tools: https://learn.microsoft.com/en-us/agent-framework/agents/tools/function-tools
- tools overview: https://learn.microsoft.com/en-us/agent-framework/agents/tools/
- OpenAI providers: https://learn.microsoft.com/en-us/agent-framework/agents/providers/openai
- group chat builder: https://learn.microsoft.com/en-us/python/api/agent-framework-core/agent_framework.groupchatbuilder

The notebooks are written as teaching notebooks. Where live LLM credentials are required, the notebook marks the code as optional and keeps a deterministic local fallback.
