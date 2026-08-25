# Chapter 3 source map: From a Prompt to a Controlled Agent Run

Status: internal source map for the approved Chapter 3 rewrite.

Current living documentation checked: 2026-08-25.

## Chapter contract

Chapter 3 is a companion guide to three selected resources. It helps a learner
combine their practical advice without turning that advice into a new universal
framework:

- OpenAI Prompting supplies the chapter order: result, useful context, output,
  boundaries, verification, and follow-up;
- Claude Code Best Practices adds an agentic-work perspective: give the agent a
  check, explore before implementation when uncertainty warrants it, provide
  concrete references, communicate during the run, and manage the session;
- Anthropic's Claude 5 context-engineering article supplies the current
  corrective lens: simplify accumulated instructions, rely more on judgment,
  make tools and references easy to inspect, and disclose detail progressively.

The chapter does not invent a recurring scenario, a new taxonomy, or a new
diagram. Chapter 2 owns instruction files, MCP, Skills, and their loading
mechanisms. Chapter 4 owns Skill authoring. Chapter 5 owns detailed treatment of
hooks, guardrails, and evals. Graph orchestration is outside this chapter.

After reading, a learner should be able to improve a consequential prompt,
explain which information belongs in the current prompt versus persistent or
on-demand context, define an observable verification signal, steer a run, and
distinguish that work from harness and loop engineering.

## Teaching sequence

| Section | Teaching job | Primary resource and exact portion | What to preserve | What to adapt or add | Visual opportunity | Boundary |
|---|---|---|---|---|---|---|
| Opening | Introduce the three companion readings and a practical meaning of prompting for this chapter | OpenAI, “Prompting overview”; Claude Code, introduction; Claude 5, introduction | Prompting is ordinary language plus iteration; agentic work makes context and verification important | State that the chapter follows the resources rather than proposing a framework | None | Do not present the three sources as a standard |
| 1. Start with the result | Teach Goal, Context, Output, and Boundaries as optional prompt components | OpenAI, “Prompting overview” and “Describe the result you need” | Start with the outcome; specify process only when process matters; use only helpful components | Label the four-part list as a practical checklist, not required syntax | None; use source examples as quoted or paraphrased text | Do not create a book-specific story |
| 2. Add useful context | Teach specificity, references, connected sources, and selective disclosure | OpenAI, “Add useful context”; Claude Code, “Provide specific context” and “Provide rich content”; Claude 5, “Progressive disclosure” and “Rich references” | Add information that can change the result; point to authoritative material and existing patterns; let the agent inspect detail when needed | Separate current-task context from persistent guidance and on-demand resources; link detailed mechanisms back to Chapters 2 and 4 | Source figure from Claude 5 showing context assembly/progressive disclosure, if provenance and reuse are acceptable | Do not reteach CLAUDE.md, MCP, or Skills mechanics |
| 3. Set boundaries and verification | Show how a few consequential constraints and readable checks improve work | OpenAI, “Set boundaries” and “Make the result ready to use”; Claude Code, “Give Claude a way to verify its work”; Claude 5, rules-to-judgment and overconstraint discussion | Use one or two meaningful boundaries; ask for a final check; provide pass/fail evidence; overconstraint can create conflicts | Distinguish a requested check from deterministic enforcement; label Claude 5 advice as model/product-specific evidence | Source “then / now” figure from Claude 5, if provenance and reuse are acceptable | Detailed hooks, evals, and guardrails belong to Chapter 5 |
| 4. Explore before committing | Teach investigation and planning as responses to uncertainty, not rituals | Claude Code, “Explore first, then plan, then code” and “Let Claude interview you”; OpenAI, ChatGPT Work and Codex planning guidance; Fable field guide | Explore-plan-implement when the approach is uncertain; skip overhead for obvious small work; surface unknowns before implementation | Use Fable only to name blind spots, interviews, references, and prototypes as optional discovery moves | Fable knowns/unknowns source figure, linked or reused only after provenance review | Do not prescribe a four-phase process for every task |
| 5. Prompting continues during the run | Teach follow-ups, steering, queuing, course correction, context reset, and compaction | OpenAI, “Improve the result with follow-up messages” and “Steering and queuing”; Claude Code, “Course-correct early and often” and “Manage context aggressively” | The first prompt need not be perfect; correct direction early; start fresh when accumulated context becomes harmful | Separate portable conversational practice from product-specific commands | None | Do not turn session controls into universal syntax |
| 6. Put the pieces together | Give the learner a compact source-derived checklist and a complete prompt anatomy | OpenAI, “Put the pieces together”; Claude Code tables and examples; Claude 5 synthesis | Outcome, useful context, ready-to-use output, meaningful boundaries, check, and follow-up | Annotate the source-derived prompt without creating a new formula | None; semantic text and definition list are sufficient | The checklist stays optional and task-dependent |
| Closing: beyond prompting | Briefly distinguish harness engineering and loop engineering | LangChain, “The Anatomy of an Agent Harness”; Addy Osmani, “Loop Engineering” | Harness as the surrounding system that makes model behavior dependable; loop as repeated work selection, execution, checking, and continuation | Label both as broad practitioner framings, not standards; connect without expanding them into main sections | Use no figure | Do not restore the old harness/loop/graph architecture narrative |
| Practice | Let the learner reconstruct what they would change and where it belongs | Synthesis of the three main resources | Diagnose goal, context, output, boundaries, unknowns, verification, and follow-up | Ask the reader to assign durable or deterministic needs to later layers | None | Do not add an invented case study |

## Approved resource roles

### Main companion readings

1. OpenAI — Prompting
   https://learn.chatgpt.com/docs/prompting
   - Living documentation with no publication date displayed.
   - Teaching spine and chapter order.
2. Anthropic — Best practices for Claude Code
   https://code.claude.com/docs/en/best-practices
   - Living documentation with no publication date displayed.
   - Main agentic-work companion: verification, investigation, concrete
     context, communication, course correction, and context management.
3. Anthropic — The new rules of context engineering for Claude 5 generation
   models
   https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models
   - Published 2026-07-24.
   - Main current-model corrective lens; its claims are explicitly about the
     Claude 5 generation and Anthropic's product experience.

### Supporting reading

- Anthropic — A field guide to Claude Fable: Finding your unknowns
  https://claude.com/blog/a-field-guide-to-claude-fable-finding-your-unknowns
  - Published 2026-07-06.
  - Optional discovery/unknowns perspective, not part of the chapter structure.

### Closing terminology

- LangChain — The Anatomy of an Agent Harness
  https://www.langchain.com/blog/the-anatomy-of-an-agent-harness
  - Published 2026-03-10.
  - Broad practitioner account for the short harness-engineering boundary.
- Addy Osmani — Loop Engineering
  https://addyo.substack.com/p/loop-engineering
  - Published 2026-06-08.
  - Practitioner account for the short loop-engineering boundary.

## Source-role guardrails

- OpenAI's four prompt components are optional practical guidance, not a prompt
  schema or universal taxonomy.
- Claude Code Best Practices describes one agentic coding product. Product
  commands, CLAUDE.md, hooks, Skills, subagents, plugins, permissions, and
  session controls are examples, not universal mechanisms.
- Claude 5 context-engineering claims are current, model-generation-specific
  observations. In particular, “examples to interface design” concerns tool
  exploration and should not be generalized into “examples are bad.”
- Fable is a product field guide. Its unknowns vocabulary is a useful thinking
  aid, not a required prompt framework.
- LangChain uses a deliberately broad definition of harness: essentially the
  system around the model. The chapter presents it as that source's perspective.
- “Loop engineering” is an emerging practitioner term. The article's suggested
  tool stack is illustrative and product-specific, not a standard five-part
  architecture.

## Coverage audit

- OpenAI: overview; result first; useful and connected context; plugins and
  personalization as pointers; meaningful boundaries; ready-to-use output;
  final checks; follow-up messages; steering and queuing; complete prompt; Work
  and Codex implications.
- Claude Code: verification; explore/plan/implement when warranted; specific and
  rich context; durable and on-demand environment pointers without reteaching
  their mechanics; asking questions and interviews; early course correction;
  clear/compact/fresh context; checkpoints/resume as product pointers; common
  failure patterns distilled only when they support these lessons.
- Claude 5: overconstraint and conflicting rules; judgment; interface design for
  tool exploration; progressive disclosure; simple tool descriptions; rich
  references; simplified persistent context; product-specific auto-memory note.
- Supporting close: unknowns as optional discovery support; one compact harness
  explanation; one compact loop explanation.
