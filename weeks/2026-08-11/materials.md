# MCP, Skills, and Subagents Workshop

These materials use Python 3.12 in hosted JupyterLab. Install the environment outside the notebooks:

```bash
python -m pip install -r notebooks/requirements.txt
```

Copy `.env.example` to `.env`, then add your Google and Phoenix credentials. The notebooks connect to the public ecommerce teaching MCP service and send traces to Phoenix.

## Recommended order

1. `05_mcp_under_the_hood_instructor.ipynb`
2. `05_orders_mcp_skill_subagents_demo_phoenix.ipynb`
3. `06_ecommerce_skills_vs_subagents_instructor_phoenix.ipynb`
4. `07_product_mcp_skill_takehome_exercise_phoenix.ipynb`
5. `07_product_mcp_skill_takehome_solution_phoenix.ipynb`
6. `08_ecommerce_composition_takehome_exercise_phoenix.ipynb`

The exercise notebooks intentionally stop at learner-owned assertions. Instructor and solution notebooks are complete. Close MCP toolsets using the cleanup cells before restarting a notebook.

Source: `npatta01/adk-agent` commit `614c5a8`.
