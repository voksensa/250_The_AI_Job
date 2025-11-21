---
trigger: always_on
---

# PROJECT STATE INDEX

## Snapshot (Living)

- **Phase**: Phase 1 – MVP (Production Toggle Proof)
- **Active Epic**: E001 – Foundation
- **Current Task ID**: TASK-003_production-toggle-mvp
- **Current Owner**: Developer
- **Gate Focus**: G1 (Research), G2 (Architecture)
- **Last Updated**: 2025-11-21 by CEO

## Quick Links

- **Current Task**: [docs/state/CURRENT_TASK.md](./CURRENT_TASK.md)
- **Blockers**: [docs/state/BLOCKERS.md](./BLOCKERS.md)
- **Progress Log**: [docs/state/PROGRESS.md](./PROGRESS.md)
- **Decisions**: [docs/state/DECISIONS_LOG.md](./DECISIONS_LOG.md)
- **Key Specs**:
  - [Complete Architecture](../research/COMPLETE_ARCHITECTURE_SPEC.md)
  - [State Management](../../constitution/STATE_MANAGEMENT.md)
  - [Quality Gates](../../constitution/CLAUDE.md)

# 

```markdown
# VISION.md  
**Working title:** Your First Engineer

---

## 1. The One-Line Vision

> **Tell us your idea. We give you a real, working app.**

Not a demo. Not a toy.  
A **real** app your customers can use, pay through, and trust.

---

## 2. What We’re Building

We are building **“your first engineer”** for people who can’t code.

- You type: **“Build me an Airbnb-style site for my guesthouse.”**
- Our system:
  - Understands what you want
  - Plans the app
  - Builds it
  - Tests it
  - Checks for security and basic performance issues
  - Puts it online
- You end with **a live product**, not a pile of files.

### In plain words

- **For:** Non-technical founders, solo entrepreneurs, small business owners.  
- **Input:** A simple description of the business you want to build.  
- **Output:** A production-ready web app, live on a URL, that real customers can use.

### What this is NOT

- Not “yet another code assistant” for professional developers.
- Not just a website or landing page generator.
- Not a sandbox demo that breaks under real use.
- Not a marketplace of templates that you must wire together yourself.

We are building **the first consumer product** that behaves like a **full engineering team in a box.**

---

## 3. Why It Matters

### Today’s reality

- Millions of people have business ideas but **can’t code**.
- Current AI tools can:
  - Generate bits of code  
  - Create prototypes  
  - Deploy quick demos  
- But they **do not give non-technical people**:
  - Confidence that the app is reliable  
  - Confidence that payments will work  
  - Confidence that it won’t fall apart when real users show up  

So most people still need to:

- Hire developers, or  
- Give up, or  
- Ship something fragile and hope it doesn’t break.

### What we change

We make it possible to go from:

> “I have an idea”  
> **to**  
> “My customers are already using it”

without needing to learn code, tools, or infrastructure.

**Why investors care:** This is a new category:  
> **“B2C-grade no-code, with true production quality.”**

**Why customers care:** They get to **skip the “find a developer” step** and just start their business.

---

## 4. The Three Killer Features

These are the **non-negotiable** pillars of the product.  
If something doesn’t support these, we cut it.

### 4.1 Killer Feature #1 — The Production Switch

**Name:** *Prototype ↔ Production* switch

- One simple toggle:
  - **Prototype mode:**
    - Fast
    - Cheap
    - Good for trying ideas
  - **Production mode:**
    - Runs deep automatic checks
    - Fixes obvious bugs
    - Checks basic security issues
    - Checks basic performance issues
    - Only then puts the app live

**Why this matters:**

- Normal people understand **“draft vs final”**, **“test vs live”**.  
- They do **not** understand “CI pipelines”, “coverage”, or “security scans”.
- This switch turns lots of hidden engineering work into **one clear decision**.

> **North Star:**  
> If the app is in **Production** mode and marked **“Ready”**, the founder trusts it enough to invite paying customers.

---

### 4.2 Killer Feature #2 — AI Test Users (“Synthetic QA Crowd”)

**Name:** *AI Test Users*

- Before the app goes live, a swarm of **AI test users**:
  - Try to sign up  
  - Try to log in  
  - Try to buy or book something  
  - Try to break the forms  
  - Try with a screen reader or keyboard only  

- The system:
  - Watches where these test users get stuck  
  - Fixes problems automatically where it can  
  - Reports clearly what it fixed and what still needs a human decision

**Why this matters:**

- Non-technical founders normally ship blind. They don’t know what’s broken until customers complain.
- AI test users give them **confidence**:  
  - “Someone has already walked through the flows.”  
  - “At least the basics have been tested.”

> **North Star:**  
> Every app has been “test-driven” by AI users before real people see it.

---

### 4.3 Killer Feature #3 — The Build Story (Explainable Timeline)

**Name:** *Build Story*

- A simple timeline that tells the story of what happened:
  1. We understood your idea.
  2. We chose an overall structure.
  3. We created pages and data.
  4. We wrote tests for key flows.
  5. We found and fixed X problems.
  6. We ran speed and basic security checks.
  7. We put it live at this URL.

- Each step:
  - Is written in plain language.
  - Has a short explanation of **why** we did it.
  - Can be expanded to show more detail (for power users and developers).

**Why this matters:**

- Long-running AI that works for hours is scary if you don’t know what it’s doing.
- The Build Story:
  - Builds **trust** (“it’s not a black box”).  
  - Helps with investors and partners (“here is what the system actually does”).  
  - Gives developers a clear overview when they later join the project.

> **North Star:**  
> A non-technical founder can explain to someone else, in their own words, what the AI did for them.

---

## 5. How It Should Feel to Use

Imagine the ideal first-time experience:

1. You type your idea:
   > “Build me an Airbnb-style site for my guesthouse in Copenhagen. It should handle bookings, clean calendars, Stripe payments in EUR, and emails in Danish and English.”

2. The system replies with a **one-page plan**:
   - “Here’s what we’ll build: pages, roles, payments, emails.”
   - “This will take about 15–20 minutes in Production mode.”

3. You press **“Start in Production mode”**.

4. While it works, you see a **calm progress view**, not spam:
   - “Designing your booking flow…”
   - “AI test users are trying bookings…”
   - “We fixed 5 issues in checkout.”

5. At the end, you see:

   - A **live link** to your new app.  
   - A short summary:
     - “Bookings work end-to-end.”
     - “Payments have been test-charged.”
     - “Test users completed 42 scenarios successfully.”

6. You open the link on your phone, book a test stay, and it just **works**.

That’s the bar.

---

## 6. Clear Success Criteria

These are the **simple, plain-language goals** everyone can remember.

### 6.1 User Success

- A non-technical founder can:
  - Go from idea → live app in **under one hour**.  
  - Invite real users **without a developer** touching the app first.
- At least **80%** of first-time builds in Production mode:
  - Work end-to-end for the main flow (signup, main action, payment).
  - Need **no code edits** before first real users arrive.

### 6.2 Product Success

Within the first 12–18 months after launch:

- Users build **thousands** of apps.
- At least **70%** of apps that go to Production:
  - Stay online
  - Handle real usage
  - Do not get rolled back due to basic bugs

- For users, the product becomes:
  - “The default way I start a new online business.”

### 6.3 Brand Success

When someone asks:

> “I have an idea but no developer. What should I use?”

We want the default answer to be:

> “Use **[Product Name]**. You tell it your idea and it gives you a real app.”

---

## 7. What We Are Building (and Not Building), In One Sentence

- **We are building:**  
  > *The first consumer product that turns plain-language ideas into production-ready apps, with a simple Production switch, built-in AI test users, and a clear story of what the AI did.*

- **We are not building:**  
  > *Another dev tool, another code editor, or another prototype-only toy.*

This is the **North Star**.  
Every roadmap, feature, and process should either support this vision — or be cut.

---
```


