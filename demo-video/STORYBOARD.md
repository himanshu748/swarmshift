---
format: 1920x1080
message: "SwarmShift turns an explicit task graph into a deterministic schedule, then preserves completed work and recovers when an agent fails."
arc: "Incident hook → one live product view → constraints → deterministic proof → recovery proof → live CTA"
audience: "hackathon judges evaluating agent infrastructure"
mode: autonomous
music: "restrained technical pulse, precise and optimistic, no vocals"
destination: "hackathon submission embed"
language: English
---

## Visual rule

The full product UI appears once, in Frame 2. Every other frame uses a purpose-built visual language—graph, data proof, incident timeline, or access cards—so the sequence never repeats the same dashboard. The bottom caption band remains clear. Orange marks critical work; green is reserved for preserved work and a met deadline; red appears only for the failure.

## Frame 1 — The deadline stays

- duration: 4.8s
- voiceover: "When one agent goes down, your delivery deadline should not go down with it."
- src: `compositions/frames/01-deadline-survives.html`
- visual: A dark 90-minute timeline establishes the problem immediately. Builder drops out at minute 22 in red while the green deadline marker stays fixed. The message resolves from `THE AGENT FAILS.` to `THE DEADLINE STAYS.`
- transition: hard cut

## Frame 2 — Meet SwarmShift

- duration: 8.96s
- voiceover: "Meet SwarmShift: a deterministic planner for multi-agent work, built to schedule the mission and recover when reality changes."
- src: `compositions/frames/02-meet-swarmshift.html`
- visual: The redesigned, browser-free SwarmShift interface is the single full product shot. Focus moves from the explicit mission, to the execution map, to verified metrics. The left-side mode stack changes from `schedule` to `recover`, ending on `WHEN REALITY CHANGES → REPLAN`.
- transition: controlled zoom-through

## Frame 3 — Constraints, not prompts

- duration: 11.285s
- voiceover: "Start with the actual constraints: tasks, dependencies, required capabilities, hourly costs, the optimization mode, and one deadline the whole swarm must respect."
- src: `compositions/frames/03-constraints.html`
- visual: A screenshot-free DAG draws `Research → Build → Verify → Ship`. Separate Scout, Builder, and Reviewer cards expose capabilities and hourly rates. Eligibility lines connect agents to work; Balanced and 90-minute controls lock last.
- transition: editorial push

## Frame 4 — Deterministic proof

- duration: 11.755s
- voiceover: "Run the plan. SwarmShift assigns every task to a capable agent, maps the critical path, explains the choice, and returns the same plan hash for the same input."
- src: `compositions/frames/04-verifiable-plan.html`
- visual: A full-width reconstructed schedule grows in dependency order. The proof rail resolves `80 MIN`, `$1.04`, and `DEADLINE MET`, followed by `RUN A` and `RUN B` producing the same SHA-256 hash.
- transition: data pivot

## Frame 5 — Failure, replanned

- duration: 11.776s
- voiceover: "Now Builder fails at minute twenty-two. Completed research stays fixed. Reviewer takes the code, the remaining work is rescheduled, and the ninety-minute deadline is still met."
- src: `compositions/frames/05-failure-replanned.html`
- visual: The sole dark incident scene. At minute 22, Research locks green, Builder fails red, and a before/after schedule merges into the recovery plan: Reviewer takes Build, then Verify, then Ship. The climax holds on `58 MIN REMAINING · $1.05 · 90 MIN DEADLINE MET`.
- transition: hard incident cut, split-to-merge recovery

## Frame 6 — Try it live

- duration: 7.381s
- voiceover: "Use the browser, call the API, or install the skill. SwarmShift: plan the swarm, keep the deadline."
- src: `compositions/frames/06-plan-the-swarm.html`
- visual: Browser, API, and SKILL.md access cards converge into `TRY LIVE DEMO`, resolving to `swarmshift.vercel.app` and the final promise.
- transition: focused CTA morph
