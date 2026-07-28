# Book question bank

This file collects candidate and published comprehension questions for the
Search Agent Study Group book. A question can be useful before its underlying
concept has a place in the published chapters, so publication status is tracked
separately from the question itself.

## Status labels

- `published`: present in a reader-facing chapter.
- `ready`: supported by material already taught and ready to place.
- `deferred`: worth keeping, but depends on concepts not yet introduced.

## QB-001 — Recognizing final output

- Status: `published`
- Placement: Chapter 1, “Check your understanding”
- Topic: agent-loop termination
- Source:
  [OpenAI Agents SDK — The agent loop](https://openai.github.io/openai-agents-python/running_agents/#the-agent-loop)

**Question**

When does the OpenAI Agents SDK treat an LLM output as a `final_output`?

**Answer**

When the LLM produces text output of the desired type and there are no tool
calls.

**Teaching note**

This tests the runtime’s stopping rule, not merely whether the response contains
some text. If tool calls are present, the runner continues the loop.

## QB-002 — Session callback versus model-input hook

- Status: `deferred`
- Placement: not yet assigned; publish after sessions and model-input hooks have
  been introduced
- Topic: session history and model-input shaping
- Sources:
  [OpenAI Agents SDK — Running agents](https://openai.github.io/openai-agents-python/running_agents/#run-config),
  [OpenAI Agents SDK — Call model input filter](https://openai.github.io/openai-agents-python/running_agents/#call-model-input-filter)

**Question**

What is the difference between `session_input_callback` (callback) and
`call_model_input_filter` (hook)?

**Answer**

`session_input_callback` runs during the earlier session merge step. When using
a Session, it receives the loaded session history and the current turn’s new
input, then returns the combined list of input items.

`call_model_input_filter` runs later, immediately before each model call. At
that point the model input has already been prepared, including instructions
and the input items produced after any session-history merge. It can trim,
replace, reorder, or augment what will be sent to the model.

**Accuracy note**

Do not describe the first step as necessarily loading from a database: Session
implementations can use different storage backends. Do not describe the second
step as necessarily exposing a provider-specific wire payload: the documented
hook receives the SDK’s prepared `ModelInputData`, and the SDK can use model
providers other than OpenAI.
