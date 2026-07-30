# Scaffold Rules

## Folder ownership

- `spec/`: approved behavior, inputs, rules, outputs, errors, security, and acceptance.
- `src/spec/NN_feature_name/`: feature code implementing the matching numbered spec.
- `src/common/`: code reused by at least two features or an explicit shared boundary.
- `docs/`: supplied domain background and durable decisions; never invent material.
- `results/`: reproducible user-facing artifacts, samples, or review captures.
- `tests/`: credential-free automated checks tied to acceptance criteria.

Keep `.gitkeep` only while a directory has no real file.

## Documentation workflow

Prefer Markdown for user-provided background knowledge, requirements, decisions, and
reference notes. When the user supplies rough text, place it in a focused
`docs/*.md` file and improve headings, lists, links, and readability without changing
meaning. Then update affected specs, `AGENTS.md`, and other project files where the
new information changes their instructions.

Do not create filler documentation. A spec should link relevant background files
with relative paths, for example `../docs/main_page.md`, rather than duplicate them.

## Numbered feature specs

Name every spec `NN_feature_name.md` with a zero-padded sequential prefix beginning
at `01`. The prefix communicates implementation order; do not renumber approved or
implemented specs merely to insert a later idea.

Each independently reviewable feature gets one spec. Each spec must include:

- goal and user-visible outcome;
- behavior and primary flow;
- related files using relative links;
- explicit scope and non-scope;
- inputs, outputs, and state changes;
- error, empty, permission, and recovery states;
- privacy/security constraints where relevant;
- measurable acceptance criteria;
- open decisions that block implementation.

Use the same stem for implementation: `spec/02_main_page.md` maps to
`src/spec/02_main_page/`. Tests should make that relationship easy to identify,
preferably under `tests/spec/02_main_page/` when the language and framework permit.

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

Keep it short, imperative, and project-specific. It is persistent context for Codex,
not a beginner tutorial. Include only:

- source-of-truth order: README → target spec → relevant docs → integration docs;
- numbered spec and matching `src/spec/` naming rules;
- short-request interpretation for a referenced docs path or spec path;
- Python as the fallback only when no language or platform choice already exists;
- the compact spec → implementation → verification → revision rule;
- deterministic testing and fake-data requirements;
- secret and real-user-data rules;
- external mutation/dry-run rules;
- change-specific minimum verification;
- instruction to request spec approval instead of silently changing behavior.

Do not put tutorials, prompt catalogs, repeated folder explanations, or user-facing
prose in `AGENTS.md`. Put them in `DEVELOPMENT_GUIDE.md`. Aim to keep the root
`AGENTS.md` under roughly 60 lines unless project-specific risk justifies more.

## DEVELOPMENT_GUIDE.md

Write a friendly guide for a first-time, non-developer user. Explain:

- what `docs/`, `spec/`, `src/spec/`, `src/common/`, `tests/`, and `results/` mean;
- the documentation → numbered spec → approval → implementation → test/result
  review → revision loop;
- that a rough Markdown file can be reformatted with
  `docs/example.md md파일로 수정해줘`;
- that an approved spec can be implemented with
  `spec/01_example.md src로 개발해줘`;
- that Python is the default only when no other language is required;
- that a revision can be requested as a normal sentence without restating the
  current result, file paths, or a form;
- several short copyable prompts and one fuller spec-request example.

Make clear that Codex should infer context and complete normal read, implementation,
test, and result-review steps. Also explain that Codex may ask a short question when
a missing decision would materially change the product.

## README.md

Include only the goal, current scope, folder map, current status, and commands that
actually work. Add a prominent first-use link to `DEVELOPMENT_GUIDE.md`. Do not
document planned commands as if implemented.

## Git and checks

Initialize Git only when requested. Default the initial development branch to `dev`.
Do not create an empty commit.

Add a shared hook only after a real check command exists. A hook may check staged
secrets, formatting, tests, and generated artifacts, but it must not call live
services, delete files, install packages, or modify production state.

## Definition of done for scaffolding

- required folders and root files exist;
- `DEVELOPMENT_GUIDE.md` exists and README recommends it to first-time users;
- the first spec is specific to the project idea;
- every spec uses a numeric prefix and the project explains how it maps to source;
- `src/common/` and `src/spec/` exist without speculative feature code;
- architecture matches the platform and first slice;
- no speculative implementation or credentials exist;
- README contains no fake commands;
- AGENTS is concise and contains interpretation, test, security, and change rules;
- validation passes and Git status is reported.
