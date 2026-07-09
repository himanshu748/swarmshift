---
format: 1920x1080
message: "SwarmShift turns an agent task graph into a deterministic schedule, then recovers visibly when an agent fails."
arc: "Demo Loop — outcome hook → product promise → constraints → plan proof → recovery proof → CTA"
audience: "hackathon judges evaluating agent infrastructure"
mode: autonomous
music: "restrained technical pulse, precise and optimistic, no vocals"
destination: YouTube / hackathon submission embed
language: English
---

## Video direction

- palette system: Use the normative `frame.md` roles exactly: white canvas (`bg`), near-black display (`text`), muted gray body (`text-muted`), orange proof/critical-path accent (`primary`), softly orange-tinted cards (`card-bg`/`border`), and green only for a real positive deadline/cost state. UI screenshots retain their source colors inside the product surface.
- type system: Use the `frame.md` display, body, eyebrow, metric, and mono/data roles; one dominant near-black headline or orange numeral per frame, with the caption band kept clear in the bottom 17%.
- motion grammar: Every entrance uses an explicit seek-safe from-state and a smooth long-tail settle. Reveal each phrase, constraint, metric, and state on its spoken cue, with meaningful development continuing through the back half; use only deterministic GSAP-timeline motion.
- rhythm: Frames 1 and 3 are sequential and active; Frame 2 briefly holds the first clean product read; Frame 4 holds the deterministic hash proof; Frame 5 is the recovery climax and settles completely on the met deadline; Frame 6 is a quiet, focused close.
- idle budget: Settled content stays still. A finite low-amplitude jitter may keep one hero alive; no breathing cards, no back-half camera drift, no repeats or yoyo motion.
- negative list: No shadows, bouncy entrances, neon AI gradients, decorative particle fog, fake browser chrome, front-loaded slideshow animation, or independently floating screensaver elements.

## Frame 1 — The deadline survives

- scene: A stark deadline statement changes one phrase at a time, ending on “your deadline should not.”
- voiceover: "When one agent goes down, your delivery deadline should not go down with it."
- duration: 4.8s
- transition_in: cut
- status: animated
- src: compositions/frames/01-deadline-survives.html
- type: hook
- persuasion: Risk reversal
- beat: tension → control
- blueprint: kinetic-type-beats (Adapt) — escalating word swaps land the outcome promise before product vocabulary appears
- asset_candidates:
- focal: display typography — the changing deadline statement is the hero
- roles: no captured candidates; typography is the foreground subject
- sfx: soft impact

narrativeRole: Turn agent failure into an urgent human outcome and promise that the deadline can survive it.
keyMessage: An agent failure does not have to become a delivery failure.

Adapt: Keep the fixed-center token-swap signature; replace the playful escalation with restrained deadline-language swaps and one orange critical-path underline.
Scene 1 (0.0–1.1s): On the white canvas, “WHEN ONE AGENT” assembles phrase-by-phrase in the upper-center via **per-word staggered reveal** (`dynamic-content-sequencing`), Centered framing, low density, display type dominant; nothing else is present.
Scene 2 (1.1–2.4s): As “goes down” is spoken, only the variable slot hard-cuts from “is ready” to “GOES DOWN” using an **in-place token cycle** (`discrete-text-sequence`); the orange token carries the contrast while the camera stays locked.
Scene 3 (2.4–3.8s): “YOUR DELIVERY DEADLINE” arrives below as a full-width upper-third strip through a **kinetic beat-slam** (`kinetic-beat-slam`), creating a 3:1 hierarchy over the setup while leaving the caption band empty.
Scene 4 (3.8–4.8s): “SHOULD NOT” replaces the failure token at center on a hard cut, then an orange underline draws once with **marker highlight** (`css-marker-patterns`); the final read holds completely still.

## Frame 2 — Meet SwarmShift

- scene: The SwarmShift wordmark resolves above a restrained product window and one-line deterministic recovery promise.
- voiceover: "Meet SwarmShift: a deterministic planner for multi-agent work, built to schedule the mission and recover when reality changes."
- duration: 8.96s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/02-meet-swarmshift.html
- type: product_intro
- persuasion: Mechanism naming
- beat: relief + curiosity
- blueprint: cursor-ui-demo (Adapt) — a first cursor-led look introduces the real planner surface
- asset_candidates: assets/swarmshift-atlas.png — desktop planner with mission controls and initial execution timeline
- focal: assets/swarmshift-atlas.png
- roles: swarmshift-atlas = background product surface, cropped to the planner and dimmed only behind overlay copy
- sfx: ui whoosh, soft click

narrativeRole: Name the product and land the full value claim by the second beat.
keyMessage: SwarmShift schedules agent work deterministically and can recover from change.

Adapt: Keep the cursor-led product introduction and camera chase; use the captured planner as the stable surface, with restrained overlay labels rather than rebuilding every control.
Scene 1 (0.0–2.0s): “SwarmShift” and the first cropped product surface enter in an asymmetric 30/70 composition; the wordmark resolves via **per-word staggered reveal** (`dynamic-content-sequencing`) while the surface settles from a shallow perspective, filling more than half the frame.
Scene 2 (2.0–4.8s): On “deterministic planner,” a custom orange cursor sweeps to Run plan and lands a **cursor click + ripple** (`cursor-click-ripple`); the camera performs one **zoom-to-target** (`coordinate-target-zoom`) while a small “same input → same plan” label reveals on cue.
Scene 3 (4.8–6.6s): On “schedule the mission,” the camera servo shifts from the mission panel to the execution timeline via **pan / focus-lock** (`viewport-change`); timeline rows sharpen sequentially while off-focus regions soften with **selective blur** (`depth-of-field-blur`).
Scene 4 (6.6–8.96s): On “recover when reality changes,” a compact orange “REPLAN” proof pill lands beside the timeline with a smooth **spring-pop entrance** (`spring-pop-entrance`); the cursor and camera stop, and the first full product read holds.

## Frame 3 — Give it the constraints

- scene: A cursor travels down the mission panel as task dependencies, capabilities, costs, optimization mode, and deadline illuminate in sequence.
- voiceover: "Start with the actual constraints: tasks, dependencies, required capabilities, hourly costs, the optimization mode, and one deadline the whole swarm must respect."
- duration: 11.285s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/03-constraints.html
- type: feature_showcase
- persuasion: Concrete workflow proof
- beat: clarity + control
- blueprint: cursor-ui-demo (Reproduce) — one specific input workflow is demonstrated end to end
- asset_candidates: assets/swarmshift-atlas.png — desktop planner with task, agent, objective, and timeline regions
- focal: assets/swarmshift-atlas.png
- roles: swarmshift-atlas = background product surface with the mission panel as the active foreground region
- sfx: subtle tick, soft click

narrativeRole: Prove that the plan is grounded in explicit operational constraints rather than a vague prompt.
keyMessage: Real task and agent constraints are first-class inputs.

Reproduce: Use the cursor-ui workflow engine directly: the custom cursor advances through the real mission regions, and each spoken constraint receives a distinct live highlight before the final deadline selection.
Scene 1 (0.0–2.0s): The cropped mission panel dominates an asymmetric 60/40 composition; on “tasks,” the cursor taps the task list and four rows reveal sequentially using **dynamic content sequencing** (`dynamic-content-sequencing`).
Scene 2 (2.0–4.0s): On “dependencies,” orange connector strokes self-draw between the task labels with **SVG self-draw** (`svg-path-draw`), while the helper line “Dependencies are enforced” glows once on its spoken cue (`asr-keyword-glow`).
Scene 3 (4.0–6.5s): On “capabilities” and “hourly costs,” the camera pans down to the agent list via **camera-cursor tracking** (`camera-cursor-tracking`); capability chips and their source-backed prices reveal one row at a time.
Scene 4 (6.5–8.6s): On “optimization mode,” the cursor selects Balanced; on “one deadline,” it moves to the 90-minute control and lands a tactile **button press** (`press-release-spring`). The input surface remains large and readable in the top 83%.
Scene 5 (8.6–11.285s): The complete constraint set holds; a small line “EXPLICIT INPUTS · DETERMINISTIC OUTPUT” appears last via **per-word staggered reveal** (`dynamic-content-sequencing`), with no continuing camera motion.

## Frame 4 — A plan you can verify

- scene: The timeline assembles task by task; 80 min, $1.04, the critical path, explanation, and plan hash arrive as separate proof cues.
- voiceover: "Run the plan. SwarmShift assigns every task to a capable agent, maps the critical path, explains the choice, and returns the same plan hash for the same input."
- duration: 11.755s
- transition_in: push-slide LEFT
- status: animated
- src: compositions/frames/04-verifiable-plan.html
- type: feature_showcase
- persuasion: Show-don't-tell proof
- beat: confidence + trust
- blueprint: video-text-pivot (Adapt) — the product surface yields to verified metrics and the deterministic hash claim
- asset_candidates: assets/swarmshift-atlas.png — initial scheduled timeline with color-coded assignments and metrics
- focal: assets/swarmshift-atlas.png
- roles: swarmshift-atlas = foreground product surface that hands visual weight to the verified metrics
- sfx: run click, metric impact

narrativeRole: Turn the deterministic scheduling claim into inspectable visual evidence.
keyMessage: The output is capable, explainable, repeatable, and deadline-aware.

Adapt: Keep the signature same-anchor weight transfer from product surface to hero metrics; substitute the captured scheduled state for the blueprint's video clip, then pivot to the explanation and plan hash.
Scene 1 (0.0–2.8s): On “Run the plan,” the captured planner seats centered as a large tilted card; a custom cursor depresses the Run plan control using **cursor click + ripple** (`cursor-click-ripple`) and the timeline rows assemble in dependency order (`dynamic-content-sequencing`).
Scene 2 (2.8–6.2s): As “assigns every task” and “critical path” are spoken, the surface slides left and scales down while “80 MIN” and “$1.04” take the vacated right anchor in frame-filling data type—the blueprint's signature weight transfer—using **scale-swap** (`scale-swap-transition`) and **value-scaled counters** (`counting-dynamic-scale`).
Scene 3 (6.2–9.6s): On “explains the choice,” the surface and metrics clear from the center; three explanation lines type in one cue at a time via **dynamic content sequencing** (`dynamic-content-sequencing`), with the critical-path phrase receiving one synced orange **keyword glow** (`asr-keyword-glow`).
Scene 4 (9.6–11.755s): On “same plan hash,” a mono hash rail resolves at center character-group by character-group (`discrete-text-sequence`), and an orange “DETERMINISTIC” pill stamps beneath it with a bounded **ambient glow bloom** (`ambient-glow-bloom`); both hold still for verification.

## Frame 5 — Failure, replanned

- scene: “Builder failed · minute 22” interrupts the schedule; completed research locks, Reviewer takes build, and the revised timeline settles with the deadline still met.
- voiceover: "Now Builder fails at minute twenty-two. Completed research stays fixed. Reviewer takes the code, the remaining work is rescheduled, and the ninety-minute deadline is still met."
- duration: 11.776s
- transition_in: squeeze
- status: animated
- src: compositions/frames/05-failure-replanned.html
- type: benefit_highlight
- persuasion: Risk reversal through live proof
- beat: disruption → recovery → relief
- blueprint: device-surface-showcase (Adapt) — the real planner window advances through failure and recovered states
- asset_candidates: assets/swarmshift-incident.png — incident state with Builder removed, Reviewer reassigned, and updated metrics
- focal: assets/swarmshift-incident.png
- roles: swarmshift-incident = foreground product surface; reconstructed failure badges and locked-state labels are supporting overlays
- sfx: alert soft, mechanical replan, success tick

narrativeRole: Deliver the decisive recovery proof that pays off the opening promise.
keyMessage: SwarmShift preserves completed work and reschedules the remainder around a failed agent.

Adapt: Keep the static-tour surface and discrete screen-state advances; use one captured recovered state plus reconstructed, source-backed overlays to show the failure-to-recovery progression without inventing extra product screens.
Scene 1 (0.0–2.2s): The incident planner surface establishes as a large floating window in a rule-of-thirds composition; “MINUTE 22” counts into the upper corner with a **value-scaled counter** (`counting-dynamic-scale`) while the camera remains static.
Scene 2 (2.2–4.2s): On “Builder fails,” a red inline “BUILDER FAILED” state stamps over the Builder row and the row dims using a discrete UI-state swap (`discrete-text-sequence`); a narrow orange alert rule draws once, with no decorative alarm effects.
Scene 3 (4.2–6.3s): On “Completed research stays fixed,” the Research bar receives a green lock/check label through **keyword glow** (`asr-keyword-glow`); the rest of the surface selectively blurs (`depth-of-field-blur`) so the preserved work is unmistakable.
Scene 4 (6.3–9.0s): On “Reviewer takes the code,” the focus racks to the recovered timeline; Reviewer slides into the Build assignment via a coordinated **screen-state scale swap** (`scale-swap-transition`), then the remaining bars advance in dependency order (`dynamic-content-sequencing`).
Scene 5 (9.0–11.776s): On “deadline is still met,” the full incident screenshot sharpens, “58 MIN REMAINING · $1.05” and a green “90 MIN DEADLINE MET” proof card reveal sequentially, then hold absolutely still—the recovery climax and deliberate breather.

## Frame 6 — Plan the swarm

- scene: Browser, API, and SKILL.md choices condense into the SwarmShift lockup and GitHub URL.
- voiceover: "Use the browser, call the API, or install the skill. SwarmShift: plan the swarm, keep the deadline."
- duration: 7.381s
- transition_in: zoom-through
- status: animated
- src: compositions/frames/06-plan-the-swarm.html
- type: cta
- persuasion: Friction reduction
- beat: motivation + urgency-to-act
- blueprint: cta-morph-press (Adapt) — three access paths condense into one focused GitHub action
- asset_candidates:
- focal: SwarmShift wordmark and CTA typography
- roles: no captured candidates; brand lockup is the foreground subject and access-path labels are supporting
- sfx: soft morph, click confirmation

narrativeRole: Make the next step obvious and leave the viewer with the product's memorable promise.
keyMessage: Try SwarmShift from the UI, API, or skill at github.com/himanshu748/swarmshift.

Adapt: Keep the same-center identity-to-action morph and human-aimed click; let the three source-backed access paths condense into the single GitHub CTA before the final tagline.
Scene 1 (0.0–1.6s): “BROWSER · API · SKILL.md” reveals one label per spoken cue around a centered SwarmShift lockup, a low-density layered composition; the lockup stays rock-stable while only the labels enter (`dynamic-content-sequencing`).
Scene 2 (1.6–3.3s): The three labels converge and the wordmark condenses at the same center into an orange “OPEN ON GITHUB” pill using the blueprint's signature **scale-swap morph** (`scale-swap-transition`); the shared center makes it read as one object transforming.
Scene 3 (3.3–5.2s): A custom cursor enters from off-stage on a smooth decelerating path and aims slightly off-center; it lands a physical **cursor click + ripple** (`cursor-click-ripple`) with cursor and CTA compressing together (`physics-press-reaction`).
Scene 4 (5.2–7.381s): The clicked pill resolves into `github.com/himanshu748/swarmshift`; “PLAN THE SWARM. KEEP THE DEADLINE.” assembles beneath it phrase-by-phrase, then holds on the white canvas with one orange accent line and no further motion.
