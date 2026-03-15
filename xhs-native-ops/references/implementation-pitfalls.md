# Implementation Pitfalls

Use this file when implementing or extending `xhs-native-ops`.

This is the short list of places where the first implementation usually drifts
away from the intended skill shape.

## 1. Turning the package back into an article

Wrong direction:

- write a long article first
- split it later
- treat cards as screenshots of prose

Correct direction:

- decide the hook
- lock the angle
- design one page at a time
- keep each page responsible for one point

If the output reads like a blog post cut into slides, it is off track.

## 2. Making visual output too "tool-like"

Wrong direction:

- over-dense cards
- too many bullets on one page
- generic infographic style
- technical memo tone

Correct direction:

- strong cover
- short page titles
- one clear message per page
- enough spacing to feel native to Xiaohongshu

The goal is not "pretty automation." The goal is "native-looking content."

## 3. Letting docs outrun the implementation

Wrong direction:

- document fields the scripts do not validate
- promise outputs the scripts do not generate
- describe a publish flow that the code cannot support

Correct direction:

- if a field is required in docs, validate it in scripts
- if `manifest.json` is part of the contract, actually generate it
- if the final click is manual, keep that boundary explicit everywhere

Keep:

1. references
2. scripts
3. sample outputs

in sync.

## 4. Making the skill depend on account-private context

Wrong direction:

- writing account-specific persona rules into the skill
- requiring one private workflow's research files
- assuming one account voice

Correct direction:

- shared skill
- optional compatibility with upstream research outputs
- no hard dependency on private account context

This skill must survive extraction into a public GitHub repo.

## 5. Treating Chrome attach as optional

Wrong direction:

- mixing multiple logged-in browser paths
- using PinchTab for login-state actions
- adding relay-based publish logic

Correct direction:

- logged-in Xiaohongshu operations use Google Chrome + DevTools MCP attach
- PinchTab stays out of login-state publishing
- relay stays out of the flow

If a future version changes this, that should be a deliberate versioned change,
not a quiet drift.

## 6. Over-automating the publish boundary

Wrong direction:

- making the agent auto-click publish in v0.1
- treating "draft filled" as "safe to post"

Correct direction:

- review-first by default
- package first
- checklist second
- final publish confirmation remains human-owned unless explicitly authorized

The current trust boundary is part of the product, not a temporary omission.

## 7. Letting output formats sprawl

Wrong direction:

- each script writes its own incompatible JSON shape
- no stable manifest
- no single package contract

Correct direction:

- `package.md` is the source of truth
- `titles.json`, `score.json`, and `cards/manifest.json` are the machine-readable outputs
- if formats change, update scripts, sample outputs, and reference docs together

See:

- `references/artifact-formats.md`
- `references/sample-run.md`

## 8. Chasing too much in v0.1

Wrong direction:

- adding research crawlers immediately
- supporting every layout and media type
- building a complete Xiaohongshu super-platform

Correct direction:

- keep v0.1 to a runnable closed loop
- validate one package contract
- support six-card and nine-card paths well
- stop before final publish by default

The real test is not "how much is implemented."
The real test is "can a clean sample package run end-to-end without confusion."
