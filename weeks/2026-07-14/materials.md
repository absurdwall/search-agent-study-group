# Week 1 Materials

## Session

- Date: 2026-07-14
- Topic: Agentic AI systems and a complete ADK run

## Selected Public Material

- [Google ADK personalized-shopping sample](https://github.com/google/adk-samples/tree/main/python/agents/personalized-shopping)
- [Google ADK: Get started with Python](https://adk.dev/get-started/python/)
- [ADK fundamentals workshop notebook](notebooks/01_adk_fundamentals.ipynb) — follow one example from stateless OpenRouter calls to an ADK session and catalog tool, with an embedded public-trace walkthrough.

## Workshop Notebook Setup

From the repository root, copy `.env.example` to `.env`, fill the OpenRouter and Langfuse credentials locally, then open the notebook and run it from top to bottom. Never commit `.env` or paste credentials into notebook cells.

## Session Goals

1. Give a high-level overview of the main components of an agentic AI system and why each component matters.
2. Use the personalized-shopping sample to trace one complete agent run: user prompt, model requests, tool calls, state changes, approvals or guardrails where applicable, and final response.

## Source Boundary

This public week page should contain public material only. The group’s own ADK playbook will be added separately when it is ready to share.
