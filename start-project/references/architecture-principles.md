# Architecture Principles

## Choose boundaries from risk

Start with the first user-visible vertical slice. Separate code where change or risk
differs:

- UI and platform lifecycle;
- domain rules and deterministic transformations;
- persistence;
- external services and device capabilities;
- application composition.

Keep domain code independent from network, filesystem, UI frameworks, clocks, and
randomness when practical. Inject time and external transports so tests remain
repeatable.

## Adapt to the project type

### Mobile or desktop application

Prefer feature-oriented groups with small shared platform adapters. For an iOS app,
keep Photos, notifications, location, persistence, and networking behind protocols
or adapters so unit tests can use fakes. Do not create all adapters up front.

### Web application

Separate browser/UI concerns from server-side secrets and external API calls. Keep
business calculations shared between screen and exports. Add a server only when the
feature requires protected credentials, persistence, or server-side integration.

### Service or API

Keep transport handlers thin. Put validation and domain behavior in testable
functions, and put database/external calls behind adapters. Start with one endpoint
or job rather than a complete layered framework.

### CLI or automation

Separate argument parsing, domain operation, and I/O. Provide dry-run before
destructive or remote actions. Use explicit paths and deterministic outputs.

### Data or reporting project

Separate input normalization, rules/calculation, and rendering/export. Use the same
calculation snapshot for screen and downloadable artifacts. Fix dates/locales in
tests.

## External integration rules

For each external system, record:

1. permissions and user consent;
2. data read and data written;
3. offline, denial, timeout, partial-failure, and retry behavior;
4. adapter interface and fake implementation;
5. secret storage and log masking;
6. dry-run or sandbox path before live mutation.

Do not copy an external API's request schema across UI or domain modules.

## Evolution rule

Add a folder or abstraction only when one of these is true:

- the first slice requires it;
- two implemented features share it;
- a sensitive/external boundary must be isolated;
- a test needs a replaceable dependency;
- an artifact has a distinct lifecycle.

Otherwise record the decision as deferred rather than generating code.
