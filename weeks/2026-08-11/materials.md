# ADK, MCP, Skills, and Subagents Workshop

These materials use Python 3.12 in hosted JupyterLab. Install the environment outside the notebooks:

```bash
python -m pip install -r notebooks/requirements.txt
```

Copy `.env.example` to `.env`, then add your Google and Phoenix credentials. The workshop also checks parent directories and `/etc/skel/.env`, which supports hosted JupyterLab environments. The notebooks connect to the public ecommerce teaching MCP service and send traces to Phoenix.

## Recommended order

1. `01_adk_fundamentals.ipynb` — one agent, one local Store tool, and one readable trace.
2. `02_order_agent_local_tools.ipynb` — a complete Order agent built with ordinary Python tools.
3. `03_order_agent_optimizations.ipynb` — compare local tools, direct MCP, MCP Code, and MCP + Skill with the same request.
4. `04_agent_design_architectures.ipynb` — compare one agent with Skills against a parent with specialist subagents.

All four notebooks are complete and include executed outputs, annotated Phoenix screenshots, trace-reading notes, and a cleanup cell for MCP connections. There is no take-home exercise in this bundle.

The small `workshop/` package keeps environment discovery, Phoenix setup, API plumbing, and display helpers out of teaching cells. The two reusable procedures live under `skills/`.

Source: `npatta01/adk-agent` commit `6dbde52`.
