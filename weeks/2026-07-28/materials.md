# Week 3 Materials

## Session

- Date: 2026-07-28
- Topic: Build an Orders Agent and read Phoenix traces
- Length: 45 minutes

## Workshop notebooks

- [Learner notebook](notebooks/04_orders_agent_exercise_phoenix.ipynb)
- [Solution notebook](notebooks/04_orders_agent_solution_phoenix.ipynb)

## Setup

JupyterHub provides the Google and Phoenix environment variables for the
session. When working locally, copy `.env.example` from this folder to `.env`
and fill in your own `GOOGLE_API_KEY`, `PHOENIX_API_KEY`, and
`PHOENIX_COLLECTOR_ENDPOINT` values. Do not commit `.env` or paste credentials
into notebook cells.

Install the pinned notebook dependencies from
[`notebooks/requirements.txt`](notebooks/requirements.txt) before opening the
learner notebook. The helper uses your JupyterHub username for the Phoenix
project; outside JupyterHub it falls back to your local username.

## What we will practice

1. Read a small, complete tool before changing anything.
2. Give an Agent a grounding instruction and register Python functions.
3. Ask an Agent to list orders, then follow a returned order ID into a detail tool.
4. Use Phoenix to inspect the actual spans, arguments, and token fields.

## Data boundary

The Orders API contains synthetic classroom data. Never use personal or
customer data in these notebooks.
