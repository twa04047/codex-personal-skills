---
name: obsidian-docs
description: "Summarize important, user-selected content from the current Codex conversation into a new Markdown knowledge note in this user's Obsidian Vault Docs folder, then create bidirectional wiki links between that note and the date's Daily note. Use when the user invokes $obsidian-docs, says obsidian_docs, or asks to save, archive, document, or record a chat topic in Obsidian Docs and connect it to a daily note."
---

# Obsidian Docs

Convert the durable knowledge from the current conversation into one concise Korean Obsidian note and connect it to the current date's daily note.

## Vault conventions

- Resolve the Vault root from the current working directory and accessible workspace roots. Prefer a directory that contains `.obsidian/`, `Docs/`, `Daily/`, and `Templates/`; accept the current directory or the nearest matching ancestor. If no unique Vault root is available, ask the user for its path and stop without changing files. Never assume a machine-specific absolute path.
- Store knowledge notes in `Docs/`.
- Store daily notes as `Daily/YYYY-MM-DD.md`.
- Resolve the current date in the `Asia/Seoul` timezone.
- Use `Templates/Daily Templete.md` when today's daily note does not exist.
- Preserve existing content and formatting in every Vault file.

## Workflow

1. Identify the topic the user explicitly marks as important or asks to record. Use the current conversation as the source of truth. Do not browse, add outside facts, or invent missing details unless the user explicitly requests research.
2. Derive a specific Korean title that communicates the topic without reopening the chat. Prefer 3–12 words.
3. Convert the title to a safe filename. Remove or replace `/`, `\\`, `:`, `#`, `|`, `^`, `?`, `*`, `[[`, and `]]`; trim trailing spaces and periods.
4. Inspect `Docs/` for filename collisions. Always create a new note for this invocation. Use `<제목>.md`; if it exists, use `<제목> (YYYY-MM-DD).md`, then append `-2`, `-3`, and so on without overwriting any file.
5. Write the new Docs note with valid YAML frontmatter and the structure below. Adapt sections to the source and omit empty sections.
6. Add the Docs note link to today's daily note under `## 새로 알게 된 내용`.
7. Verify both directions of the link and report the two changed files.

## Docs note format

Use this shape, keeping the writing concise and self-contained:

```markdown
---
type: doc
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - codex-summary
  - <one-to-three topic tags when confidently derivable>
---

# <제목>

<One paragraph explaining what this note captures and why it matters.>

> [!summary] 핵심 요약
> - <key conclusion>
> - <key conclusion>

[[Daily/YYYY-MM-DD|YYYY-MM-DD 데일리 노트]] · [[Docs/_Docs|Docs 목록으로]]

## 주요 내용

<Organized summary of the conversation's useful content.>

## 질문과 답변

<Include only when the Q&A form helps preserve meaning. Paraphrase rather than copying the whole chat.>

## 결정 및 적용 포인트

<Record decisions, procedures, examples, cautions, or commands that will be useful later.>

## 후속 과제

- [ ] <Only unresolved or explicitly requested next steps.>
```

Do not create empty headings, fabricate tags, or copy long conversational filler. Preserve important qualifications, disagreements, and uncertainty.

## Daily-note linking

- If `Daily/YYYY-MM-DD.md` exists, edit it in place.
- Under `## 새로 알게 된 내용`, add exactly one bullet in this form:

```markdown
- <one-line topic summary> — 상세: [[Docs/<filename without .md>]]
```

- If the section does not exist, append it with that heading and bullet.
- If the exact Docs link is already present, do not add a duplicate.
- If today's daily note does not exist, copy the current contents of `Templates/Daily Templete.md` into it, then insert the link. If the template is missing, create a minimal daily note with `type: daily`, a `daily` tag, `# 데일리 노트`, and `## 새로 알게 된 내용`.
- Keep the Docs note's daily link and the daily note's Docs link as wiki links without the `.md` extension.

## Verification

Before finishing:

1. Confirm the new Docs file exists and no pre-existing file was overwritten.
2. Confirm its frontmatter dates match the Seoul date.
3. Confirm it contains `[[Daily/YYYY-MM-DD|...]]`.
4. Confirm the daily note contains `[[Docs/<filename>]]` exactly once.
5. Return clickable absolute paths for both notes and a one-sentence summary of what was recorded.
