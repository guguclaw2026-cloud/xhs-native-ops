# Topic Design

Use this reference when turning research into a publishable Xiaohongshu package.

## Core principle

Do not start by writing a long article and cutting it apart later.

Start with:

1. `Hook`
2. `Angle`
3. `Card Outline`

The page is the primary unit of design.

## Required package fields

`package.md` must include frontmatter:

- `topic`
- `goal`
- `platform`
- `post_type`
- `layout`
- `cta`
- `source_signals`
- `audience`
- `tone`
- `notes` (optional)

The body must include:

- `# Hook`
- `# Angle`
- `# Card Outline`
- `# CTA`
- `# Notes`
- `# Comments Angle` (optional)

## Writing the hook

The hook should do one job:

- stop the scroll

Good hook qualities:

- short
- specific
- emotionally or practically loaded
- readable on a cover

Bad hook qualities:

- sounds like a report title
- needs too much context
- tries to explain everything

## Writing the angle

The angle is the single thesis of the post.

It should answer:

- what are we really trying to say here?

If the hook is the door, the angle is the spine.

## Card outline format

Use one bullet per card.

Recommended syntax:

```markdown
- 卡片标题｜这一页想表达的重点
```

Also supported:

```markdown
- 卡片标题: 这一页想表达的重点
- 直接一句重点
```

For v0.1:

- layout `six` means: 1 cover + 5 content cards
- layout `nine` means: 1 cover + 8 content cards

If more bullets exist than the layout needs, the extra bullets are ignored with
a warning.

If fewer bullets exist than required, the package is incomplete.

## Three supported post types

### 1. Opinion

Best for:

- judgment
- stance
- founder/operator perspective

Use when:

- the value is in your take

### 2. How-to

Best for:

- methods
- checklists
- process breakdowns

Use when:

- the reader should save the post and act on it

### 3. Behind-the-scenes

Best for:

- process notes
- field observations
- real work context

Use when:

- you want to look real, not generic

## Definition of done

A topic is ready for packaging when:

- the hook is clear
- the angle is singular
- the card outline can fill the chosen layout
