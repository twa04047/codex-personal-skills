# Scaffold Rules

## Folder ownership

- `spec/`: approved behavior, inputs, rules, outputs, errors, security, and acceptance.
- `src/`: application code for approved specs.
- `docs/`: supplied domain background and durable decisions; never invent material.
- `results/`: reproducible user-facing artifacts, samples, or review captures.
- `tests/`: credential-free automated checks tied to acceptance criteria.

Keep `.gitkeep` only while a directory has no real file.

## First spec

`spec/01_project_foundation.md` must cover:

- purpose and first user outcome;
- explicit scope and non-scope;
- input and output;
- core behavior;
- external integrations and permissions;
- error and empty states;
- privacy/security;
- architecture boundaries;
- acceptance criteria;
- open decisions that block later slices.

Avoid dates, versions, framework choices, and policies that the user did not provide
unless they are clearly marked as provisional.

## AGENTS.md

Keep it short but project-specific. Include:

- source-of-truth order: README → target spec → relevant docs → integration docs;
- folder responsibilities;
- short implementation loop;
- deterministic testing and fake-data requirements;
- secret and real-user-data rules;
- external mutation/dry-run rules;
- change-specific minimum verification;
- instruction to request spec approval instead of silently changing behavior.

## README.md

Include only the goal, current scope, folder map, current status, and commands that
actually work. Do not document planned commands as if implemented.

## Git and checks

Initialize Git only when requested. Default the initial development branch to `dev`.
Do not create an empty commit.

Add a shared hook only after a real check command exists. A hook may check staged
secrets, formatting, tests, and generated artifacts, but it must not call live
services, delete files, install packages, or modify production state.

## Definition of done for scaffolding

- required folders and root files exist;
- the first spec is specific to the project idea;
- architecture matches the platform and first slice;
- no speculative implementation or credentials exist;
- README contains no fake commands;
- AGENTS contains test, security, and change verification rules;
- validation passes and Git status is reported.
