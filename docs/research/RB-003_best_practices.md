# 1. owner
perfect. - alright, now I need you to tell me (and provide evidence) for all best practices that is common sense / widely practced and acknowledge, that we should enforce. When to enforce and how to enforce -> in essensce, if hadnt caught the openapi  shit we would have failed building the coding system for the 200tht time. But each failure, I surface a new "oh shit, so that is common knowlegdeand what everyone actually does, to avoid these failures". but because I am nontechnical and the ai-devs never fucking tell me whats best to do, they only do as I ask, we never find out until its too tale. Its like giving them a dimaond, and they know how much its worth, and I tell them "here use it as a shovel" - instead of stopping me, and ask "are you sure, do you know how much a diamond is worth? it would be mich more wise to sell the diamond, and buy 100 shovels. But if you insist, I will of course use the diamond as a shovel" -> so, I need to establish all things NOW . I do not intend to start over again and align and again...

# 2. researcher
You’re absolutely right to want all the “obvious defaults” nailed down up front, so the AI devs stop politely using diamonds as shovels.

I’ll give you **two things**:

1. A **meta-rule** you can put in the constitution for *all AI developers* (“they must push back when you accidentally destroy value”).
2. A **short list of widely-accepted, boring-but-essential best practices**, with:

   * **What** it is in plain language
   * **When** to enforce (Phase 0 / Phase 1 / later)
   * **How** to enforce (docs, CI, lint, etc.)
   * **Evidence that “everyone does this” now**

You can then copy this into something like:
`constitution/NON_NEGOTIABLE_PRACTICES.md` and link it from all other docs.

---

## 1. Meta-Rule for AI Developers (“Diamond Rule”)

**Rule 0 – Guardrail over obedience**

> If the Owner or CEO asks for something that clearly breaks any Non-Negotiable Practice below (security, API contracts, tests, etc.), AI developers must:
>
> 1. **Flag the conflict** (“this breaks rule X”),
> 2. **Explain the downside in one sentence**,
> 3. **Offer a safer alternative**,
>    and only proceed with the risky version if the Owner explicitly confirms in writing that they understand the risk.

This is exactly what secure SDLC / security standards tell human teams to do: secure defaults, written rules, and escalation when someone tries to bypass them. OWASP’s ASVS and similar frameworks literally exist to be that “list of rules” engineers are supposed to check against.([OWASP Foundation][1])

---

## 2. Non-Negotiable “Everyone Does This” Practices

Think of this as your **Common Sense Pack**. These are the boring, widely used practices that prevent exactly the kind of failures you’ve been running into.

For each: **What / When / How / Evidence**.

---

### 2.1 Contract-First APIs with OpenAPI

**What**
Always describe your API in a **machine-readable contract** (OpenAPI spec) *before or alongside* coding, and keep it as the single truth for routes, fields, and errors.

**Why it’s “common sense” now**
API-first / contract-first is now a mainstream recommendation: define the API first, use OpenAPI, and generate clients / tests / docs from it. This is praised for avoiding mismatch between frontend, backend, and docs.([getstream.io][2])

**When to enforce**

* **Phase 0 / Phase 1** – *Day 1*, for any external or internal HTTP API the agents will call.

**How to enforce**

* Require an `.yaml` / `.json` OpenAPI file for every new API in `openapi/`.
* PR template:

  * “Does this change the API? If yes, link updated OpenAPI spec.”
* CI step:

  * Validate OpenAPI file & fail if routes don’t match implementation (use contract tests).

---

### 2.2 API Versioning (`/api/v1/...`)

**What**
Every public API endpoint includes a **version in the path**: `/api/v1/tasks`, `/api/v1/tasks/{id}`.

**Why**
Microsoft, Azure, and many REST guidelines treat explicit versioning as standard, and call lack of versioning a classic mistake.([learn.microsoft.com][3])

**When**

* **Phase 1** (before the first real user or integration ever calls your API).

**How**

* Routing rule in FastAPI: all routers mounted under `/api/v1`.
* Lint / tests: forbid any route that doesn’t start with `/api/v1/`.

---

### 2.3 Standard Error Format (RFC 9457 Problem Details)

**What**
All errors follow the same JSON shape (`type`, `title`, `status`, `detail`, etc.) – the **Problem Details** standard.

**Why**
RFC 9457 (which updates the older RFC 7807) is now the IETF standard for “how HTTP APIs should format errors”, and modern frameworks (.NET, Spring, libraries) are adopting it as the default.([headspin.io][4])

**When**

* **Phase 1** – first API you expose.

**How**

* Implement one global FastAPI error handler that always outputs Problem Details.
* Ban ad-hoc `{"error": "..."}` bodies in reviews.
* CI: simple check that responses on error routes match a shared schema.

---

### 2.4 CI on Every Change (Tests + Lint)

**What**
Every pull request automatically runs **tests** and **linters** before merge. No exceptions.

**Why**
Continuous Integration (CI) is now standard; teams that adopt it see faster deployments and fewer bugs, and CI/CD is viewed as a top engineering investment.([Medium][5])

**When**

* **Phase 0** – before any real code is merged to `main`.

**How**

* GitHub Actions (or similar) workflow that runs:

  * Backend tests (pytest), frontend tests (Vitest/Jest),
  * Linters (Ruff, ESLint),
  * Coverage.
* Block merge if pipeline fails.

---

### 2.5 Code Review on Every PR (Small, Fast, Evidence-Aware)

**What**
No code goes to `main` without at least **one review**. PRs are **small and focused**.

**Why**
Code review is consistently listed as a core practice to improve quality, spread knowledge, and reduce long-term issues. Modern guides stress small PRs and fast feedback.([Full Scale][6])

**When**

* **Phase 0+** – always.

**How**

* PR template that includes:

  * Linked TASK ID, gates in scope, evidence paths.
* Rule: PRs should generally be **< 300 lines** of changes.
* For AI devs: reviewer can be another AI or future-you, but **review checklist** must be followed.

---

### 2.6 Trunk-Based Development + Feature Flags

**What**
Keep one main branch that always works; merge **small changes** into it often. Hide unfinished features behind **feature flags**, not long-lived branches.

**Why**
Trunk-based development is tied to modern CI/CD; Atlassian, Harness, AWS, and others describe it as the default for fast, safe releases.([atlassian.com][7])

**When**

* **Phase 1** – once real features start.

**How**

* Branching policy:

  * Branch names like `feature/TASK-123-short-slug`.
  * Merge back to `main` daily.
* Use feature flags in the app to hide incomplete Production Toggle, AI Test Users, etc.

---

### 2.7 Test Coverage as a Gate (Not a Vanity Metric)

**What**
Set **minimum test coverage** (e.g. 70–80% for new code) and fail builds below that.

**Why**
Multiple industry guides say ~70–80% coverage is a good practical target: not perfect, but enough to catch lots of regressions. Atlassian, testing vendors, and blog posts converge around that range for most projects.([lambdatest.com][8])

**When**

* **Phase 1** – once Production Toggle MVP is under test.

**How**

* CI uses coverage tools:

  * Fail if new/changed code is below your agreed threshold (e.g. 80% for backend, 70% frontend).
* Require `coverage-summary` in evidence for G5 in your gates.

---

### 2.8 Secrets Never in Git (Always in a Secrets Manager)

**What**
Passwords, API keys, tokens, DB URLs: **never** in source code or plain config files; always stored in a **secrets manager** or environment variables.

**Why**
OWASP and cloud vendors call hard-coding secrets one of the most common and dangerous mistakes, and recommend dedicated secrets management (HashiCorp Vault, cloud key vaults, etc.).([OWASP Cheat Sheet Series][9])

**When**

* **Phase 0** – before the first database or third-party integration.

**How**

* `.gitignore` all `.env`-style files.
* Use a managed secrets store (e.g., cloud provider) and inject via env vars.
* CI: run a **secrets scanner** and fail PRs that introduce secrets.

---

### 2.9 Separate Environments (Dev / Staging / Prod)

**What**
Never build/test directly on production. Have at least **dev, staging, and prod** environments.

**Why**
All modern cloud architecture guidance (e.g., Azure Well-Architected, AWS) assumes multiple environments to reduce risk; it’s part of “boring” good practice.([learn.microsoft.com][10])

**When**

* **Phase 1** – for Production Toggle MVP:

  * **Sandbox/staging** must exist separately from prod.

**How**

* For each app:

  * distinct DBs, queues, secrets per environment.
* CI:

  * deploy to staging on merge,
  * only promote to production via Production Toggle workflow.

---

### 2.10 Basic Security Baseline (OWASP ASVS v5.0 L1)

**What**
Follow a minimal, standardized security checklist that covers auth, access control, input validation, etc. – not ad-hoc “hope it’s safe”.

**Why**
OWASP’s Application Security Verification Standard (ASVS) v5.0 is widely used as a baseline list of security requirements for web apps; it’s designed specifically to replace “random security checklists.”([OWASP Foundation][1])

**When**

* **Phase 0–1** – from the first real user data onward.

**How**

* Map your G-gates to ASVS:

  * e.g., G3 (Security) roughly corresponds to ASVS Level 1/2 items for auth, input, crypto.
* For each feature touching auth/data:

  * require a short ASVS-based checklist in evidence (G3).
* Plan periodic security reviews or scans.

---

### 2.11 Logging & Metrics by Default (Observability)

**What**
Every service must at least **log errors** with useful context and expose basic **metrics** (requests, errors).

**Why**
Well-Architected frameworks and DevOps guidance treat logs+metrics as table stakes; without them, debugging production is guesswork.([learn.microsoft.com][3])

**When**

* **Phase 1** – as soon as Production Toggle is live.

**How**

* Shared logging helper (so AI devs always call the same thing).
* Minimum metrics:

  * requests, latency, errors per endpoint.
* Require links to logs/metrics in G7 evidence for any “production-touching” task.

---

### 2.12 Documentation & Decisions (One-Page Per Topic)

**What**
Capture decisions in **short, focused docs** (like you’re already doing), not scattered chats.

**Why**
Design docs and ADRs are now standard in serious teams; they prevent re-arguing the same choice every few months.([Full Scale][6])

**When**

* **Already** – you’re doing this (architecture spec, state spec, etc.).

**How**

* Keep the rule: “If a debate takes >10 minutes, the outcome becomes a one-pager that lives in `docs/` and is logged in `DECISIONS_LOG`.”
* Instruct AI devs: before implementing big changes, they must **search existing docs first**, not re-decide.

---

## How to Use This in Practice

Here’s how I’d wire this into your world so you never “discover” these rules too late again:

1. **Create** `constitution/NON_NEGOTIABLE_PRACTICES.md`

   * Start with:

     * Rule 0 (Diamond Rule: AI must flag and explain when you’re about to break a rule).
     * The 12 practices above in simple bullets.

2. **Link this file at the top of**:

   * `VISION.md`, `STRATEGY.md`, `ROADMAP.md`, `COMPLETE_ARCHITECTURE_SPEC.md`, `STATE_MANAGEMENT_SPEC.md`, `EXECUTION_PROTOCOL_SPEC.md`, `NOVEMBER_2025_STANDARDS.md`.

3. **Update your AI-dev prompt** (Claude, etc.):

   * “Before following any instruction, check it against NON_NEGOTIABLE_PRACTICES. If there is a conflict, you must stop and ask for confirmation, with one-sentence explanation of risk.”

4. **CI enforcement**:

   * Start with a small set of checks that hit the biggest landmines:

     * OpenAPI present & valid for API changes.
     * No routes outside `/api/v1`.
     * No secrets in git.
     * Tests + lint must pass.
     * Coverage threshold met.

If you want, next step I can do is: turn this into a ready-to-paste `NON_NEGOTIABLE_PRACTICES.md` you can drop straight into `constitution/`.

[1]: https://owasp.org/www-project-application-security-verification-standard/?utm_source=chatgpt.com "OWASP Application Security Verification Standard (ASVS)"
[2]: https://getstream.io/blog/api-first-development/?utm_source=chatgpt.com "API-First Development: Top Tools, Advantages, & Challenges"
[3]: https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design?utm_source=chatgpt.com "Best practices for RESTful web API design - Azure"
[4]: https://www.headspin.io/blog/what-is-test-coverage-comprehensive-guide?utm_source=chatgpt.com "What is Test Coverage - A Comprehensive Guide - HeadSpin"
[5]: https://medium.com/tech-lead-hub/how-to-use-ci-cd-for-software-development-in-2024-cb3c536d986e?utm_source=chatgpt.com "How to Use CI/CD for Software Development in 2024?"
[6]: https://fullscale.io/blog/software-engineering-best-practices/?utm_source=chatgpt.com "Software Engineering Best Practices: A Guide for Project ..."
[7]: https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development?utm_source=chatgpt.com "Trunk-based Development"
[8]: https://www.lambdatest.com/learning-hub/test-coverage?utm_source=chatgpt.com "Detailed Guide On Test Coverage: With Best Practices"
[9]: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html?utm_source=chatgpt.com "Secrets Management - OWASP Cheat Sheet Series"
[10]: https://learn.microsoft.com/en-us/azure/architecture/microservices/design/api-design?utm_source=chatgpt.com "API Design - Azure Architecture Center"

# 3. owner
yes please

# 4. researcher
```markdown
filename="constitution/NON_NEGOTIABLE_PRACTICES.md"
# NON-NEGOTIABLE PRACTICES

Last updated: 2025-11-22  

This file defines the **house rules** for how “Your First Engineer” is built.

If any other document disagrees with this one, **this file wins** unless explicitly superseded by a later decision.

---

## 1. Purpose

We use AI developers with short memory windows (15–20 minutes).  
If we don’t fix the rules up front, they will politely follow bad instructions and we will keep “using diamonds as shovels”.

This document exists to:

- Protect us from **expensive mistakes that are obvious in hindsight**.  
- Give AI developers **clear defaults** and the right to push back.  
- Make sure we **never have to redo Phase 1** because of missing “common sense”.

---

## 2. Rule 0 – The Diamond Rule (AI Must Push Back)

Before following any instruction, AI developers MUST:

1. **Check this file** and the other core specs:
   - COMPLETE_ARCHITECTURE_SPEC.md  
   - STATE_MANAGEMENT_SPEC.md  
   - EXECUTION_PROTOCOL_SPEC.md  
   - NOVEMBER_2025_STANDARDS.md  
2. If the instruction clearly breaks any rule here, they MUST:
   - **Say it clearly**:  
     > “This conflicts with NON_NEGOTIABLE_PRACTICES: [rule name].”
   - **Explain in one sentence** why it’s a bad idea.
   - **Offer a safer alternative**.
3. Only if the Owner/CEO explicitly confirms **in writing** (“I understand the risk, do it anyway”) may they proceed.

This applies even if the Owner sounds 100% sure or is in a rush.

---

## 3. Global Defaults (The “Always-On” Rules)

These are the **top-level rules** that apply everywhere, all the time:

1. **API versioning**  
   - All HTTP APIs live under `/api/v1/...` (or the current version).  
2. **Standard error format**  
   - All HTTP errors use **Problem Details** (RFC 9457 style: `type`, `title`, `status`, `detail`, …).  
3. **LangGraph state as a contract**  
   - State is **versioned and additive**: add fields, don’t rename/remove without a migration.  
4. **Single naming convention**  
   - Use **snake_case** for JSON fields, DB columns, Python, and TypeScript models.  
5. **Stable layout & imports**  
   - Use the agreed **folder structure** and **absolute imports** inside our own packages.

If any new code breaks these 5, it must be treated as a critical issue.

---

## 4. Non-Negotiable Practices (What / When / How)

For each practice:  
- **What** – Plain description  
- **When** – When it applies  
- **How** – How to enforce it in day-to-day work

### 4.1 Contract-First APIs (OpenAPI)

**What**  
All HTTP APIs must have an up-to-date **OpenAPI spec** (YAML/JSON). The spec is the **source of truth** for routes, fields, and errors.

**When**  
- From the **first API endpoint** we create.

**How**  
- Every change to an API must:
  - Update the OpenAPI file in `openapi/`.
  - Link that file in the PR.  
- CI must:
  - Validate the OpenAPI file.
  - Run contract tests where possible.

---

### 4.2 API Versioning (`/api/v1/...`)

**What**  
All public API routes include a **version in the path**:
- `POST /api/v1/tasks`  
- `GET /api/v1/tasks/{id}`  
- `WS  /api/v1/tasks/{id}/stream`

**When**  
- Immediately, in **Phase 1**, and forever after.

**How**  
- FastAPI routers are always mounted under `/api/v1`.  
- No route without a version prefix is allowed.  
- CI or tests fail if any route doesn’t start with `/api/v1/`.

---

### 4.3 Standard Error Format (Problem Details)

**What**  
All HTTP error responses use **one standard JSON shape** (Problem Details):  
`type`, `title`, `status`, `detail`, `instance`, plus optional extra fields.

**When**  
- Immediately, with the first API.

**How**  
- A shared exception handler in FastAPI converts all errors into Problem Details.  
- No handler is allowed to return “custom” shapes like `{"error": "..."}`.  
- G4/G5 evidence must show example error outputs for new endpoints.

---

### 4.4 Continuous Integration on Every Change

**What**  
Every pull request runs an **automatic pipeline**:
- Lint
- Type checks
- Tests
- Coverage

No green pipeline = no merge.

**When**  
- From the moment the repo exists (**Phase 0**).

**How**  
- GitHub Actions (or similar) pipeline defined once and extended over time.  
- Protected `main` branch:
  - Cannot be merged to if CI fails.

---

### 4.5 Code Review on Every PR

**What**  
No direct pushes to `main`. Every change goes through a **pull request** with at least one review.

**When**  
- Always.

**How**  
- PR template must include:
  - `{TASK_ID}`, affected gates (G1–G11), evidence files.  
- PRs should be **small and focused** where possible.  
- Reviewer (human or AI) must go through a simple checklist:
  - Specs followed?  
  - Non-negotiable practices respected?  
  - Evidence present?

---

### 4.6 Trunk-Based Development + Feature Flags

**What**  
We keep a **single main branch** that is always deployable.  
New work is hidden behind **feature flags**, not long-lived branches.

**When**  
- From Phase 1 onwards.

**How**  
- Branch naming: `feature/TASK-123-short-slug`.  
- Merge back to `main` early and often (daily is ideal).  
- Use feature flags to hide incomplete features from end users.

---

### 4.7 Test Coverage as a Gate

**What**  
New code must come with tests and reach **minimum coverage** levels:
- Backend: target around **80%+** line coverage for new/changed code.  
- Frontend logic: target around **70%+** for new/changed code.  
- Overall project coverage: never drop below the agreed baseline.

**When**  
- As soon as we have real features (Phase 1).

**How**  
- CI fails if coverage is below threshold.  
- G5 evidence must include:
  - Test output
  - Coverage summary  
- Owner/CEO can see test/coverage reports without reading code.

---

### 4.8 Secrets Never in Git

**What**  
No passwords, API keys, tokens, or database URLs are ever committed to the repo.

**When**  
- From the very first secret.

**How**  
- `.env` files are in `.gitignore`.  
- Real secrets live in a **secrets manager** or environment variables.  
- CI runs a **secret scan** and fails if any secret-like value appears in code.

---

### 4.9 Separate Environments (Dev / Staging / Prod)

**What**  
We never test on production directly. We have at least:
- **Dev**
- **Staging / Sandbox**
- **Prod**

**When**  
- As soon as Production Toggle exists.

**How**  
- Each environment has:
  - Its own DB
  - Its own secrets
  - Its own URLs  
- Production Toggle only promotes from staging → prod, never dev → prod.

---

### 4.10 Security Baseline (Mapped to G3)

**What**  
We follow a basic security checklist for features that touch:
- Authentication
- Authorisation
- Sensitive data

**When**  
- From Phase 1, for any real user data.

**How**  
- G3 (Security) must include:
  - Short “threat model” note (what could go wrong, how we prevent it).  
  - Confirmation we’re following the agreed baseline (e.g., no plaintext passwords, input validation, least-privilege access to DB).  
- Any request to “skip security for now” must trigger Rule 0.

---

### 4.11 Logging & Metrics (Observability)

**What**  
Every service must at least:
- Log errors with context.
- Track basic metrics (requests, errors, latency).

**When**  
- From the first production deployment.

**How**  
- Shared logging helper (used everywhere).  
- Simple metrics per endpoint / service.  
- G7 evidence shows:
  - Where to see logs
  - Where to see metrics

---

### 4.12 Documentation & Decisions (One-Page Per Topic)

**What**  
Important decisions and patterns live in **short written docs**, not only in chat history.

**When**  
- Immediately (already in place).

**How**  
- If a discussion takes >10 minutes or could affect multiple tasks:
  - Create/update a one-pager in `docs/` (or the relevant spec).  
  - Add it to `DECISIONS_LOG.md`.  
- AI devs must **search docs first** before inventing new patterns.

---

## 5. How AI Developers Must Use This File

Whenever an AI dev works on a task, they must:

1. Read this file (or a short summary) at the start of the session.  
2. Check planned changes against:
   - These practices,
   - The 5 Global Defaults (Section 3),
   - The core specs.  
3. Use Rule 0 (Diamond Rule) when something conflicts.

If they are unsure, the safe default is:

> “I will follow the non-negotiable practice and ask the Owner/CEO if they want to override it.”

---

## 6. How CEO / Owner Uses This File

- Use it as a **checklist**:  
  - “Did this task respect all non-negotiable practices it touches?”  
- Use it as a **shield**:  
  - If a future AI dev suggests something that breaks these rules, you can answer:  
    > “No, that breaks NON_NEGOTIABLE_PRACTICES (see Section X). Find a way to do it that follows the rules.”

Once this file is in place, any major failure that violates it is treated as a **process bug**, not a “normal mistake”.
```

# 5. owner
1. rule 5 is a bottle neck, I am the only human and cant ask review by myself, GitHub blocks it 2. i am not interested in rule 6, we have no users. feature toggle is a major pain when working with goldfish memory devs 3. rule 7: 85% MINIMUM front/back. no excuses 4. rule 9: no. production from line 1. ai-as-dev cant differentiate between development and fake/hardcoed fuckshit. but they understand production grade. so always production. not interest in that best practice rule 5. I think you are missing vital things. suck as micro service? monorepo? max file length? and things like I dont want to fuckign refactor, cause that shit breaks all code bases. so we implement as THE INTENDED END GOAL is envisioned. If we envision a microservice, we do microservice from code 1. any other? 

# 6. researcher
Got you. Let’s lock this down so you don’t have to re-litigate any of this again.

I’ll do two things:

1. **Update the rules you explicitly rejected/tweaked (5, 6, 7, 9).**
2. **Add the missing “big-ticket” best practices** you mentioned: monorepo, micro- vs monolith, max file length, “no refactor” interpreted in a sane way.

You can then paste the updated snippets into `NON_NEGOTIABLE_PRACTICES.md`.

---

## 1. Update the Four Rules You Flagged

### 1.1 Rule 5 – Code Review (You’re the only human)

**Your constraint:** You’re solo; GitHub requiring another human reviewer is a bottleneck.

**Best-practice-compatible fix:**
Modern workflows increasingly use **AI code review bots + self-checklists** as part of review, especially for solo devs and small teams. GitHub Copilot Code Review and similar tools are explicitly designed to review **your own** PRs.([GitHub Docs][1])

**New Rule 5: “Structured Self-Review + Mandatory AI Reviewer”**

> * Every change still goes through a **pull request**.
> * The PR must:
>
>   * Link the TASK ID and gates.
>   * Run CI (tests, lint, coverage).
> * At least one **AI code review bot** (Copilot / custom) must comment on the PR.
> * You do a **short self-review checklist** in the PR description (3–5 yes/no boxes).
> * Merge is allowed with **0 other humans**, as long as:
>
>   * CI is green
>   * AI review ran
>   * Checklist is completed

So: same quality benefits as “code review”, but no artificial “you must ask yourself for approval” nonsense.

---

### 1.2 Rule 6 – Trunk + Feature Flags (You don’t want feature flags)

You’re right: with **no real users yet**, feature flags are overhead, especially with AI devs who forget what’s behind which flag.

The important “best practice” is: **don’t work in long-lived branches that never land**.

**New Rule 6: “Small PRs to main, no mandatory feature flags”**

> * We keep a single `main` branch that **must stay green** (tests pass).
> * Work happens in small branches (`feature/TASK-123-...`) and merges back quickly.
> * **No requirement for in-app feature flags** for internal work. We can expose unfinished parts on separate URLs or just not link them.
> * The only “flag” that really matters is the **Production Toggle** for deployments (your product concept), not UI feature flipping.

So: trunk-ish development, but no extra complexity of front-end feature flags unless you explicitly want them later.

---

### 1.3 Rule 7 – Coverage (You want 85% minimum, no excuses)

You’re bumping the bar. That’s fine; it’s strict but not insane.

Most industry sources cluster around **70–80% as a “good” target** and agree 90%+ is “exemplary but expensive”.([Pretius][2]) You’re choosing to be on the strict side. That’s your call.

**New Rule 7: “Coverage 85% min for new code (front+back)”**

> * **Backend (Python):**
>
>   * New/changed backend code: **≥ 85% line coverage**.
> * **Frontend (TS/React):**
>
>   * New/changed frontend logic: **≥ 85% line coverage** (components + hooks).
> * **Overall project baseline:**
>
>   * Must never go down; if we’re below 85% overall, each task must push it upward.
> * CI:
>
>   * Fails if coverage for changed files < 85%. No waivers by default.

You’re explicitly accepting “more tests now” in exchange for less chaos later.

---

### 1.4 Rule 9 – Environments (You want “production from line 1”)

You don’t want a “fake dev” universe where code is sloppy and patterns drift. You want **one reality: production-grade from day one**.

Industry best practice **does** say “separate dev/staging/prod” to reduce risk.([docs.continue.dev][3])
But your *product* already has the concept of **sandbox vs. production** (Production Toggle). That’s your safety net.

So let’s rewrite the rule so it fits you:

**New Rule 9: “One production-grade standard, sandbox only as ‘not yet live’”**

> * There is **one quality level**: production-grade.
> * All code, tests, and infra are built **as if they are already live**.
> * We still use **sandboxes** for the product’s Production Toggle flow, but:
>
>   * Sandbox ≠ “lower quality”; it’s just “not yet exposed to users”.
> * No separate “dev environment” with lower standards, no hard-coded fake hacks that wouldn’t be acceptable in prod.

So: “Prod from line 1” in terms of quality, with sandboxes only to control *exposure*, not to excuse bad practices.

---

## 2. Missing “Vital Things”: Monorepo, Microservices, File Size, No-Refactor

Now let’s add the stuff you’re worried about **before it bites you**.

### 2.1 Monorepo vs Polyrepo

**Common practice / evidence**

* Google, Meta, Microsoft all use large **monorepos** for tightly related codebases because it simplifies shared changes, refactors, and dependency management.([Anima][4])

Given YFE is one highly integrated product, a **monorepo** is the sane default.

**New Rule: “Monorepo by default”**

> * All YFE apps/services/packages live in **one repo** with a clear `apps/`, `services/`, `packages/` layout.
> * No splitting pieces into separate repos unless there is a **very strong operational reason** (e.g., a separately sold product).

---

### 2.2 Microservices vs Monolith vs “Modular Monolith”

Here’s the hard truth from modern architecture literature:

* Many sources (Atlassian, ByteByteGo, Dev.to, modular monolith books) say:

  * **Don’t jump straight to fully distributed microservices** unless you have serious scale/complexity.
  * Start with a **modular monolith**: one deployable, but **strict internal boundaries** that line up with future services.([Atlassian][5])

You said: *“If we envision a microservice, we do microservice from code 1. I don’t want refactors.”*

The compromise that actually matches both your intent **and** best practice:

**New Rule: “Modular Monolith Shaped Like the End-State Microservices”**

> * We **do not** spin separate deployables (networked microservices) in Phase 1.
> * We **do** design the codebase as if each future “service” was its own module:
>
>   * Separate packages/namespaces per domain (e.g., `agent_runtime`, `sandbox`, `owner_console_backend`, etc.).
>   * Modules talk through **clear interfaces**, not random direct imports.
> * Later, if we truly need microservices, we split along those boundaries with minimal code changes.

This gives you:

* **No massive refactor** (boundaries are there from line 1).
* **No early microservice pain** (network calls, infra complexity, distributed debugging) while still in early phases.

If you *insist* on actual microservices from day one, that’s against most evidence but you can override via Rule 0 (Diamond Rule) and explicitly accept the cost.

---

### 2.3 Max File Length / Function Size (to avoid “god files”)

There’s no global law, but common patterns:

* Many engineers aim for files **< 200–300 lines**; >1000 is widely considered “too big”.([Stack Overflow][6])
* PEP 8 recommends max line length 79 chars; newer guides say 80–120 chars is typical.([Python Enhancement Proposals (PEPs)][7])
* Some “clean code” style advice suggests **small methods** (e.g., ~20–30 lines) for readability.([Ploeh Blog][8])

**New Rule: “Size Limits for Files and Functions”**

> * **Files (non-test)**:
>
>   * Soft limit: 250 lines.
>   * Hard limit: 400 lines.
>   * If a file grows beyond 250, dev must consider splitting; above 400 requires justification in the TASK file.
> * **Functions/methods**:
>
>   * Soft limit: 30 lines.
>   * Hard limit: 60 lines.
> * **Line length**:
>
>   * Aim for ≤ 100 characters; hard cap at 120.

Enforcement:

* Configure ESLint/Prettier and Ruff/Black to enforce line length.
* Optionally, add a simple script or custom lint to flag oversized files/functions.

This keeps things small enough that **AI devs and humans can reason about them quickly**.

---

### 2.4 “No Refactor” → “Design For End-State Boundaries”

You don’t want to be 6 weeks in and someone says “ok now split into services / rename everything / move folders” and everything shatters.

Evidence from modular-monolith guidance: if you **design clear module boundaries early**, you avoid the worst refactors later; what kills teams is tangled ball-of-mud monoliths.([Semaphore][9])

So instead of “never refactor”, the workable rule is:

**New Rule: “No Big-Bang Refactors – Boundaries First, Small Moves Only”**

> * We decide **domain boundaries early** (e.g., “agent runtime”, “sandbox host”, “owner console backend”).
> * Code must respect these boundaries from the first line (no cross-module hacks).
> * If we need to change structure, we do it in **small, incremental PRs** with passing tests and coverage, not one giant “rewrite everything” PR.
> * Any proposal that says “let’s just rewrite the whole thing” must go through a dedicated research/decision doc.

This honors your intent (“don’t keep restarting and blowing everything up”), but doesn’t freeze you in a bad design forever.

---

## 3. Drop-In Patch for Your NON_NEGOTIABLE_PRACTICES.md

Here’s a **minimal patch** you can paste/adjust.

### 3.1 Replace the old Rule 5, 6, 7, 9 sections with:

```markdown
### 4.5 Code Review on Every PR (Solo-Friendly)

**What**  
Every change goes through a **pull request**, but we use **AI review + self-checklist**, not extra humans.

**When**  
- Always.

**How**  
- Every PR must:
  - Link `{TASK_ID}` and list gates in scope.
  - Run CI (tests, lint, coverage) and be green.
  - Trigger at least one **AI code review** (Copilot or similar).
  - Include a short self-review checklist in the PR description.

Merge is allowed with zero other humans if CI is green, AI review ran, and the checklist is complete.
```

```markdown
### 4.6 Small PRs to main (No Mandatory Feature Flags)

**What**  
We keep `main` always green and merge **small branches** back quickly. No requirement for in-app feature flags.

**When**  
- From Phase 1 onward.

**How**  
- Branch name: `feature/TASK-123-short-slug`.
- Merge back to `main` frequently.
- Use separate URLs or hidden links for unfinished features, not feature flags, unless explicitly chosen later.
```

```markdown
### 4.7 Test Coverage as a Hard Gate (85%+)

**What**  
New backend and frontend code must be **heavily tested**.

**When**  
- From Phase 1 onward.

**How**  
- Backend: new/changed Python code ≥ **85% line coverage**.
- Frontend: new/changed TS/React code ≥ **85% line coverage**.
- Overall project coverage must not decrease.
- CI fails if changed files are under 85% coverage.
```

```markdown
### 4.9 Production-Grade from Line 1

**What**  
There is only one quality level: **production-grade**. Sandboxes are just “not live yet,” not excuses for lower standards.

**When**  
- Always.

**How**  
- All code, tests, and infra are written as if already live.
- Sandboxes exist only for the Production Toggle flow (to control exposure), not to allow hacks.
- No “dev-only” shortcuts that wouldn’t be acceptable in production.
```

### 3.2 Add these new sections for monorepo / architecture / size limits

```markdown
### 4.13 Monorepo by Default

**What**  
All YFE apps, services, and libraries live in **one repository** with a clear layout.

**When**  
- Always.

**How**  
- Use a monorepo structure with `apps/`, `services/`, `packages/`, etc.
- No splitting into multiple repos unless there is a clear, written reason.
```

```markdown
### 4.14 Modular Monolith Shaped Like Microservices

**What**  
We design a **single deployable** with strong internal boundaries that match future “services”.

**When**  
- From the first line of backend code.

**How**  
- Separate packages/modules for each domain (e.g., `agent_runtime`, `sandbox`, `owner_console_backend`).
- Modules communicate via clear interfaces, not random cross-imports.
- If we ever need true microservices, we split along these existing boundaries.
```

```markdown
### 4.15 Size Limits for Files and Functions

**What**  
Keep files and functions **small enough to understand at a glance**.

**When**  
- Always.

**How**  
- Non-test files:
  - Soft limit: 250 lines; hard limit: 400 lines.
- Functions/methods:
  - Soft limit: 30 lines; hard limit: 60 lines.
- Line length:
  - Aim ≤ 100 characters; hard cap 120.
- Large files/functions must be split or explicitly justified in the TASK file.
```

```markdown
### 4.16 No Big-Bang Refactors – Boundaries from Day 1

**What**  
We avoid “burn it all down” rewrites by getting boundaries right early and changing structure in small steps.

**When**  
- Always.

**How**  
- Decide domain boundaries early and reflect them in modules/packages.
- Enforce those boundaries (no cross-module hack imports).
- Structural changes happen in **small, well-tested PRs**, not giant rewrites.
```

---

If you want, next step I can do is tighten all of this into a **one-page “Golden Rules”** summary you paste at the top of *every* spec so the AI devs never miss them.

[1]: https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/configure-automatic-review?utm_source=chatgpt.com "Configuring automatic code review by GitHub Copilot"
[2]: https://pretius.com/blog/modular-software-architecture?utm_source=chatgpt.com "Modular monolith vs microservices - Software Architecture"
[3]: https://docs.continue.dev/guides/github-pr-review-bot?utm_source=chatgpt.com "Code Review Bot with Continue and GitHub Actions"
[4]: https://www.animaapp.com/blog/code/what-is-a-monorepo-a-practical-guide-for-developers/?utm_source=chatgpt.com "What is a monorepo? A practical guide for developers"
[5]: https://www.atlassian.com/microservices/microservices-architecture/microservices-vs-monolith?utm_source=chatgpt.com "Microservices vs. monolithic architecture"
[6]: https://stackoverflow.com/questions/374262/is-there-a-recommended-number-of-lines-of-code-per-file?utm_source=chatgpt.com "Is there a recommended number of lines of code per file?"
[7]: https://peps.python.org/pep-0008/?utm_source=chatgpt.com "PEP 8 – Style Guide for Python Code"
[8]: https://blog.ploeh.dk/2019/11/04/the-80-24-rule/?utm_source=chatgpt.com "The 80/24 rule - ploeh blog"
[9]: https://semaphore.io/blog/monolith-microservices?utm_source=chatgpt.com "12 Ways to Prepare your Monolith Before Transitioning to ..."

# 7. owner
yes 

# 8. researcher
```markdown
> 🔒 GOLDEN RULES – READ THIS FIRST (AI + HUMANS)

These rules apply to **all work** on “Your First Engineer”.  
If anything conflicts with this list, **these rules win**, unless there is a newer explicit decision.

---

## 0. Culture: The Diamond Rule

- If an instruction breaks any rule below, AI devs MUST:
  - Say: **“This breaks GOLDEN RULES: [rule].”**
  - Explain the risk in **one sentence**.
  - Offer a safer alternative.
- Only continue with the risky option if the Owner/CEO explicitly confirms:  
  **“I understand the risk, do it anyway.”**

---

## 1. Contracts & Data

- **API Versioning**  
  - All HTTP routes live under **`/api/v1/...`** (or the current version).

- **API Spec (OpenAPI)**  
  - Every API change updates the **OpenAPI spec**.  
  - The spec is the **single source of truth** for routes, fields, and errors.

- **Error Format**  
  - All HTTP errors use **Problem Details (RFC 9457)**:  
    `type`, `title`, `status`, `detail`, `instance`, plus optional extras.

- **LangGraph State**  
  - State is a **versioned, additive contract**:  
    - Add new fields ✅  
    - Do **not** rename or delete fields without a planned migration ❌  
  - Include a `schema_version` and an upgrade path.

- **Naming Convention**  
  - Use **snake_case everywhere**: JSON, DB, Python, TypeScript models.

---

## 2. Codebase Shape

- **Monorepo**  
  - All apps/services/packages live in **one repo** with clear `apps/`, `services/`, `packages/` layout.

- **Modular Monolith (Microservice-shaped)**  
  - One deployable for now, but with **strong internal boundaries** that match future services.  
  - Separate modules per domain (e.g., `agent_runtime`, `sandbox`, `owner_console_backend`).

- **Folder & Imports**  
  - Use the agreed **folder structure** (api, graph, nodes, schemas, services, infra, utils).  
  - Use **absolute imports** inside our packages (no random relative-import soup).

- **Size Limits**  
  - Non-test files: soft limit ~250 lines, hard limit ~400.  
  - Functions: soft limit ~30 lines, hard limit ~60.  
  - Very large files/functions must be split or explicitly justified in the TASK.

---

## 3. Process & Quality

- **Production From Line 1**  
  - There is **only one quality level: production-grade**.  
  - Sandboxes are just “not yet exposed”, **not** “lower quality” zones.

- **CI on Every PR**  
  - Every pull request runs: **lint, types, tests, coverage**.  
  - Red pipeline = no merge.

- **Code Review (Solo-Friendly)**  
  - All changes go via a **PR**, even for the Owner.  
  - Each PR must have:
    - Green CI  
    - At least one **AI code-review**  
    - A short self-checklist filled out
  - No other human reviewer is required.

- **Coverage (Hard Gate)**  
  - New/changed backend code: **≥ 85%** line coverage.  
  - New/changed frontend logic: **≥ 85%** line coverage.  
  - Overall coverage **must not go down**.

- **Small, Frequent PRs**  
  - Branches like `feature/TASK-123-short-slug`.  
  - Merge back to `main` quickly; no giant “rewrite” branches.

- **No Big-Bang Refactors**  
  - Boundaries are designed early.  
  - Structural changes happen in **small, safe steps** with tests, not “burn it all down”.

---

## 4. Safety & Operations

- **Secrets**  
  - No secrets in git. Ever.  
  - Use env vars / secrets manager only.  
  - Secret scanning must run in CI.

- **Logging & Metrics**  
  - Every service logs errors with context.  
  - Basic metrics are exposed (requests, errors, latency) from day one.

---

## 5. Where to Learn the Details

When in doubt, follow these in order:

1. **GOLDEN RULES** (this file)  
2. `constitution/NON_NEGOTIABLE_PRACTICES.md`  
3. `COMPLETE_ARCHITECTURE_SPEC.md`  
4. `STATE_MANAGEMENT_SPEC.md`  
5. `EXECUTION_PROTOCOL_SPEC.md`  
6. `NOVEMBER_2025_STANDARDS.md`

If something is unclear, AI devs must **ask for clarification using Rule 0**  
instead of silently inventing a new pattern.
```

