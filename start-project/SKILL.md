---
name: start-project
description: Design and scaffold a minimal, spec-first software project in an empty or explicitly designated folder. Use when the user invokes start-project or asks Codex to start a new app, service, website, CLI, automation, or data project from a short idea and wants an adaptive architecture, `spec/`, `src/`, `docs/`, `results/`, `tests/`, `AGENTS.md`, `README.md`, `.gitignore`, and optional Git initialization. Apply loop engineering and harness engineering without generating speculative frameworks, integrations, or boilerplate that the project does not yet need.
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
   - keep `docs/` empty except `.gitkeep` unless actual background material exists;
   - define what reproducible artifacts belong in `results/`;
   - define tests that run without production credentials or real user data;
   - make `README.md` short and executable;
   - make `AGENTS.md` project-specific and include the loop and change-specific
     verification rules.
9. Do not implement the application unless the user also asked for implementation.
10. Run `scripts/validate_project.py <root>`. Inspect `git status` when Git exists.
    Report assumptions, created files, deferred decisions, and the next smallest
    development slice.

## Minimality Rules

- Create only `spec/`, `src/`, `docs/`, `results/`, `tests/`, `AGENTS.md`,
  `README.md`, and `.gitignore` as the universal foundation.
- Add `Makefile`, hooks, CI, dependency manifests, deployment files, database
  migrations, authentication, and framework boilerplate only when their commands or
  requirements are known.
- Prefer one first spec over a speculative roadmap of many spec files.
- Prefer feature-oriented source boundaries for applications. Introduce layers only
  at real boundaries such as UI, domain rules, persistence, and external services.
- Do not invent domain documentation, API contracts, credentials, identifiers,
  schemas, or compliance requirements.
- Do not put caches, local build products, secrets, or real user data in `results/`.
- Do not make live API calls while scaffolding.

## Loop and Harness Requirements

Encode this short loop in `AGENTS.md`:

`requirement → plan → implementation → test → artifact review → revision`

For each future change, require a spec check, the narrowest relevant test, generated
artifact review when applicable, and then the full project check. Once real commands
exist, consolidate them under one check command and optionally add a shared
pre-commit hook. Keep hooks local, fast, credential-free, and non-destructive.

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
