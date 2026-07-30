---
name: start-project
description: Design and scaffold a minimal, beginner-friendly, spec-first software project in an empty or explicitly designated folder. Use when the user invokes start-project or asks Codex to start a new app, service, website, CLI, automation, or data project from a short idea and wants an adaptive architecture, a Korean development guide, Markdown background docs, numbered feature specs, spec-aligned source folders, `results/`, `tests/`, concise `AGENTS.md`, `README.md`, `.gitignore`, and optional Git initialization. Apply a documented requirement-to-review loop without generating speculative frameworks, integrations, or boilerplate.
---

# Start Project

Create a small, evolvable project foundation from the user's product idea. Treat the
approved spec as the source of truth, keep external systems behind adapters, and add
automation only when it has a real command to run.

## Workflow

1. Inspect the target directory and all applicable `AGENTS.md` files.
2. Refuse to overwrite a non-empty project unless the user explicitly requests an
   update. Preserve all existing files.
3. Extract a brief containing:
   - product goal and primary user;
   - platform and deliverable;
   - external integrations and permissions;
   - sensitive data, offline/network constraints, and deterministic outputs;
   - decisions that materially change architecture.
4. Ask only blocking questions. For reversible omissions, choose the smallest
   reasonable scope and record the choice or open decision in the first spec.
5. Read [references/architecture-principles.md](references/architecture-principles.md)
   before choosing source boundaries. Read
   [references/scaffold-rules.md](references/scaffold-rules.md) before writing files.
6. Briefly state the proposed architecture and assumptions, then scaffold unless the
   user requested proposal-only work.
7. Run `scripts/scaffold_project.py` for the universal base. Pass an explicit root,
   project name, one-sentence summary, and platform. Use `--init-git` only when the
   user requested Git and the target is not already a repository.
8. Tailor every generated file to the idea:
   - expand `spec/01_project_foundation.md` with inputs, behavior, outputs, failure
     states, privacy/security, and acceptance criteria;
   - describe only the source modules needed for the first vertical slice;
   - convert user-supplied notes and durable background knowledge into readable
     `docs/*.md`; keep `docs/` empty except `.gitkeep` when no material exists;
   - keep every implementable feature in one zero-padded, sequentially numbered spec;
   - map each feature spec to `src/spec/<same-prefix-and-name>/`, while keeping
     genuinely reused code in `src/common/`;
   - define what reproducible artifacts belong in `results/`;
   - define tests that run without production credentials or real user data;
   - make `README.md` short and executable, and recommend
     `DEVELOPMENT_GUIDE.md` to first-time users;
   - make `DEVELOPMENT_GUIDE.md` a friendly human guide with plain-language workflow
     and copyable prompt examples;
   - keep `AGENTS.md` concise and project-specific. Include only instructions that
     change Codex behavior; do not duplicate the human explanations or examples.
9. Do not implement the application unless the user also asked for implementation.
10. Run `scripts/validate_project.py <root>`. Inspect `git status` when Git exists.
    Report assumptions, created files, deferred decisions, and the next smallest
    development slice.

## Minimality Rules

- Create only `spec/`, `src/`, `docs/`, `results/`, `tests/`, `AGENTS.md`,
  `DEVELOPMENT_GUIDE.md`, `README.md`, and `.gitignore` as the universal foundation.
- Inside `src/`, create only `common/` and `spec/` as universal code categories.
  Create feature folders under `src/spec/` only when their specs are approved for
  implementation. Do not place feature code directly in `src/`.
- Add `Makefile`, hooks, CI, dependency manifests, deployment files, database
  migrations, authentication, and framework boilerplate only when their commands or
  requirements are known.
- Name specs `NN_feature_name.md`, starting with `01_`, so development order is
  visible. Use the same `NN_feature_name` for its source folder.
- Prefer one first spec over a speculative roadmap. Add one spec per smallest
  independently reviewable feature when that feature is requested.
- Prefer feature-oriented source boundaries for applications. Introduce layers only
  at real boundaries such as UI, domain rules, persistence, and external services.
- Do not invent domain documentation, API contracts, credentials, identifiers,
  schemas, or compliance requirements.
- Do not put caches, local build products, secrets, or real user data in `results/`.
- Do not make live API calls while scaffolding.

## Loop and Harness Requirements

Encode this short loop in `AGENTS.md`:

`docs → numbered spec → spec review/approval → src/spec implementation → test →
artifact review → spec/code revision`

For each feature or behavior change, require:

1. Capture supplied context in readable Markdown under `docs/`; link only relevant
   files from the spec with relative paths.
2. Create or revise one numbered feature spec containing goal, behavior, related
   docs, non-scope, errors, and measurable acceptance criteria.
3. Ask the user to review missing or ambiguous behavior; do not implement until the
   spec is approved, unless the user explicitly requested an uninterrupted
   implementation and the remaining decisions are reversible.
4. Implement only that approved spec under its matching `src/spec/NN_feature_name/`
   folder. Move code to `src/common/` only after real reuse or when it represents an
   explicit cross-feature boundary.
5. Verify code completion with the narrowest relevant automated test and inspect the
   running or rendered result.
6. If the result needs behavior changes, update and re-approve the spec before
   revising source code; repeat verification.

Interpret these short user requests without demanding a form:

- `<docs path> md파일로 수정해줘`: restructure and format the referenced Markdown
  for readability while preserving meaning, then update affected project guidance.
- `<spec path> src로 개발해줘`: read the referenced spec and linked docs, implement
  it in the matching `src/spec/` folder, test it, and inspect the result. Use Python
  when neither the user, spec, platform, nor existing project selects another
  language.
- A plain-language change request after implementation: infer the current target
  from conversation and project state. Ask for a path only when ambiguity would
  materially change the result. Update the spec first when behavior changes.

Once real commands exist, consolidate them under one check command and optionally
add a shared pre-commit hook. Keep hooks local, fast, credential-free, and
non-destructive.

Use harness controls proportionate to risk:

- always: `AGENTS.md`, deterministic tests, secret exclusions, explicit folder
  ownership, and acceptance criteria;
- when executable code exists: one repeatable check command;
- when generated UI/artifacts exist: render or run and inspect them;
- when a remote repository exists: CI may repeat the check command;
- when an external system is introduced: adapter boundary, fake transport, dry-run,
  masking, and approval before live mutation.

## Example

For “iOS diary app that loads photos and videos from diary days,” choose a first
slice such as local diary entry plus read-only Photos selection. Record Photos
permission denial, limited-library access, missing media, date/time-zone matching,
privacy, and simulator/fake-library tests. Do not add cloud sync, accounts, a backend,
analytics, or video processing unless requested.
