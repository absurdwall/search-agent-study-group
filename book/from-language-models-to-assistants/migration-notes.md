# Chapter 0 migration notes: From Language Models to Assistants

Status: internal source notes for the planned Chapter 0. This is preserved
working material, not a reader-facing draft of that chapter.

## Why this material moved

Chapter 1 now begins with an agent-capable model, tools, and a runtime-controlled
loop. The material below previously introduced the model foundations that make
that mechanism meaningful. It belongs in the planned Chapter 0 so Chapter 1 can
stay focused on the agent-system boundary.

## Preserved foundations

### Tokens and autoregressive generation

A token is a unit of text the model processes. It may be a whole word, part of a
word, punctuation, or whitespace; boundaries depend on the particular model and
tokenizer. OpenAI describes input text being split into tokens and a response
being generated as a sequence of tokens. [OpenAI — What are tokens and how to
count them](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)

A next-token model estimates possible continuations of the tokens so far,
selects one according to decoding settings, appends it, and repeats. This is
autoregressive generation because every new token becomes part of the history
for the next one. The GPT-4 Technical Report describes GPT-4 as pre-trained to
predict the next token in a document. [GPT-4 Technical
Report](https://cdn.openai.com/papers/gpt-4.pdf)

The training objective is simple to state, while the training data and scale can
let a model learn statistical regularities about language, code, and recurring
patterns. That can produce useful language behavior without making every answer
reliable or requiring a claim of human-like understanding. [OpenAI — How ChatGPT
and our foundation models are developed](https://openai.com/policies/how-chatgpt-and-our-foundation-models-are-developed/)

### Prompted completion and assistant behavior

A base model is trained to continue text. A prompt ending with `Question: What
is the weather in Boston? Answer:` can lead to a continuation that looks like an
answer, but this pattern alone does not make a reliably helpful,
instruction-following assistant. GPT-4 documentation describes next-token
pretraining; OpenAI’s InstructGPT work describes post-training that builds on
pretraining to improve instruction following and preferred assistant behavior.
[GPT-4 Technical Report](https://cdn.openai.com/papers/gpt-4.pdf) · [OpenAI —
InstructGPT](https://openai.com/index/instruction-following/) · [InstructGPT
paper](https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)

Pretraining and post-training happen before a model is used. Prompting happens
when an application sends a particular inference request. Post-training changes
the model available at inference time; a prompt supplies the context for one
run.

### API boundary and structured output

It is useful to separate the API shape a developer writes from the information
the model uses to generate. A public API request may use JSON fields such as
messages, roles, tools, and output options. The provider parses and processes
that request, prepares model input, then returns a response in the API’s public
format. The model does not literally receive the public API JSON string by
default, and roles are not universally literal tokens. [Anthropic — Messages
API](https://platform.claude.com/docs/en/api/messages/create)

Structured output and tool calls remain model generation. They request a
particular output shape, such as an object matching a schema or a tool-call
request. OpenAI documents a feature-specific approach that combines training for
complicated schemas with constrained output matching developer-supplied schemas;
this should not be generalized to every provider’s undisclosed internals.
[OpenAI — Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) ·
[OpenAI — Introducing Structured Outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/)

## Planned Chapter 0 additions not yet drafted

- A beginner comparison of BERT and GPT.
- A clear progression from pretraining to fine-tuning and post-training, using
  terms carefully across providers.
- A reader-facing treatment of JSON schemas and constrained structured
  generation, with provider-specific claims kept explicit.

## Preserved visual source

`../../assets/book/tokenizer-example.png` remains available as a Chapter 0
source candidate. It is the Microsoft Generative AI for Beginners tokenizer
image, copied under the MIT License. Its attribution and complete license notice
are in [`../../assets/book/THIRD_PARTY_NOTICES.md`](../../assets/book/THIRD_PARTY_NOTICES.md).
