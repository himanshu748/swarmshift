from __future__ import annotations

PAGE = r"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Deterministic multi-agent task scheduling and failure replanning.">
  <link rel="icon" href="data:,">
  <title>SwarmShift — deterministic agent scheduling</title>
  <style>
    :root {
      --ink: #11110f;
      --ink-2: #2e302c;
      --muted: #676b63;
      --canvas: #f4f3ef;
      --paper: #fffefa;
      --line: #d8d6cf;
      --soft-line: #ebe9e2;
      --orange: #f05a18;
      --orange-dark: #c63d06;
      --orange-soft: #fff0e8;
      --blue: #2467df;
      --blue-soft: #edf3ff;
      --green: #137a45;
      --green-soft: #eaf7ef;
      --red: #c72f3a;
      --red-soft: #fff0f1;
      --purple: #6f42c1;
      --purple-soft: #f3edff;
      --shadow: 0 18px 50px rgba(35, 31, 24, .08);
      --radius-lg: 22px;
      --radius-md: 14px;
      --radius-sm: 9px;
      --mono: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      --sans: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body { margin: 0; color: var(--ink); background: var(--canvas); font-family: var(--sans); }
    button, textarea, input, select { font: inherit; }
    button { color: inherit; }
    a { color: inherit; }
    [hidden] { display: none !important; }
    .topbar { min-height: 66px; display: flex; align-items: center; justify-content: space-between; gap: 24px; padding: 0 34px; border-bottom: 1px solid var(--line); background: rgba(244, 243, 239, .96); position: sticky; top: 0; z-index: 50; }
    .brand { display: inline-flex; align-items: center; gap: 11px; font-weight: 850; font-size: 22px; letter-spacing: -.8px; text-decoration: none; }
    .brand-mark { position: relative; width: 27px; height: 23px; flex: 0 0 auto; }
    .brand-mark::before, .brand-mark::after { content: ""; position: absolute; top: 10px; left: 5px; width: 18px; height: 2px; background: #f2a07b; transform-origin: center; }
    .brand-mark::before { transform: rotate(31deg); }
    .brand-mark::after { transform: rotate(-31deg); }
    .brand-mark i { position: absolute; width: 8px; height: 8px; border-radius: 50%; background: var(--orange); z-index: 1; }
    .brand-mark i:nth-child(1) { left: 10px; top: 0; }
    .brand-mark i:nth-child(2) { left: 0; bottom: 0; }
    .brand-mark i:nth-child(3) { right: 0; bottom: 0; }
    nav { display: flex; align-items: center; gap: 25px; font-size: 14px; font-weight: 700; }
    nav a { text-decoration: none; color: var(--ink-2); padding: 9px 0; border-bottom: 2px solid transparent; }
    nav a:hover, nav a:focus-visible { color: var(--ink); border-color: var(--orange); outline: none; }
    .nav-cta { border: 1px solid var(--ink) !important; border-radius: 999px; padding: 9px 15px !important; }
    main { width: min(1540px, calc(100% - 44px)); margin: 0 auto; padding: 54px 0 0; }
    .hero { display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(300px, .65fr); gap: 54px; align-items: end; margin-bottom: 36px; }
    .eyebrow { display: inline-flex; align-items: center; gap: 9px; margin: 0 0 17px; color: var(--orange-dark); font-family: var(--mono); font-size: 12px; font-weight: 800; letter-spacing: .08em; text-transform: uppercase; }
    .eyebrow::before { content: ""; width: 25px; height: 2px; background: var(--orange); }
    h1 { margin: 0; max-width: 930px; font-size: clamp(48px, 5.5vw, 88px); line-height: .94; letter-spacing: clamp(-4.8px, -.055em, -2px); font-weight: 850; }
    h1 em { color: var(--orange); font-style: normal; }
    .hero-side { padding-bottom: 5px; }
    .lede { margin: 0 0 23px; color: var(--muted); font-size: clamp(17px, 1.55vw, 22px); line-height: 1.48; max-width: 580px; }
    .proof-row { display: flex; flex-wrap: wrap; gap: 9px; }
    .proof-chip { display: inline-flex; align-items: center; gap: 7px; min-height: 34px; padding: 0 11px; border: 1px solid var(--line); border-radius: 999px; background: rgba(255, 254, 250, .65); color: var(--ink-2); font-family: var(--mono); font-size: 11px; }
    .proof-chip::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: var(--green); }
    .command-bar { display: flex; align-items: center; justify-content: space-between; gap: 18px; margin-bottom: 18px; }
    .actions { display: flex; gap: 11px; }
    .button { min-height: 49px; padding: 0 18px; border: 1px solid #aaa79e; border-radius: 10px; background: var(--paper); color: var(--ink); font-weight: 800; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 9px; transition: transform .16s ease, border-color .16s ease, background .16s ease; }
    .button:hover:not(:disabled) { transform: translateY(-2px); border-color: var(--ink); }
    .button:disabled { opacity: .6; cursor: wait; }
    .button.primary { border-color: var(--ink); background: var(--ink); color: var(--paper); box-shadow: 0 4px 0 var(--orange); }
    .button.incident { color: var(--red); border-color: #e2aeb3; background: #fffafa; }
    .button.restore { color: var(--ink); border-color: var(--green); background: var(--green-soft); }
    .button:focus-visible, textarea:focus-visible, select:focus-visible { outline: 3px solid rgba(36, 103, 223, .28); outline-offset: 2px; }
    .keyboard-note { color: var(--muted); font-family: var(--mono); font-size: 11px; }
    .keyboard-note kbd { padding: 3px 6px; border: 1px solid var(--line); border-bottom-width: 2px; border-radius: 5px; background: var(--paper); font-family: inherit; color: var(--ink-2); }
    .incident-banner { min-height: 62px; margin-bottom: 18px; padding: 11px 16px; display: grid; grid-template-columns: auto 1fr auto; align-items: center; gap: 14px; border: 1px solid #e7aeb3; border-radius: var(--radius-md); background: var(--red-soft); }
    .incident-icon { width: 36px; height: 36px; display: grid; place-items: center; border-radius: 50%; background: var(--red); color: white; font-weight: 900; }
    .incident-banner strong { display: block; font-size: 14px; }
    .incident-banner p { margin: 3px 0 0; color: #6e3a3e; font-size: 13px; }
    .incident-proof { display: flex; gap: 8px; }
    .incident-proof span { padding: 7px 10px; border: 1px solid #dfbcc0; border-radius: 999px; background: rgba(255,255,255,.7); font-family: var(--mono); font-size: 10px; font-weight: 700; white-space: nowrap; }
    .incident-proof .kept { color: var(--green); border-color: #acd0bb; background: var(--green-soft); }
    .workspace { display: grid; grid-template-columns: minmax(330px, .76fr) minmax(660px, 1.64fr); gap: 18px; align-items: start; }
    .panel { border: 1px solid var(--line); border-radius: var(--radius-lg); background: var(--paper); box-shadow: var(--shadow); overflow: hidden; }
    .mission { padding: 23px; position: sticky; top: 84px; }
    .panel-kicker { margin: 0 0 5px; color: var(--muted); font-family: var(--mono); font-size: 10px; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }
    .section-title { font-size: 22px; font-weight: 850; letter-spacing: -.55px; margin: 0; }
    .mission-head { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
    .mission-count { padding: 6px 9px; border-radius: 7px; background: var(--orange-soft); color: var(--orange-dark); font-family: var(--mono); font-size: 10px; font-weight: 800; }
    .field-group { margin-top: 18px; }
    .field-label { display: flex; justify-content: space-between; align-items: center; font-size: 13px; font-weight: 800; margin: 0 0 8px; }
    .field-label > span:first-child { display: inline-flex; align-items: center; gap: 8px; }
    .step { width: 21px; height: 21px; display: inline-grid; place-items: center; border-radius: 50%; background: var(--ink); color: white; font-family: var(--mono); font-size: 10px; }
    .add-inline { border: 0; background: none; color: var(--blue); font-size: 12px; font-weight: 800; cursor: pointer; padding: 5px; }
    .add-inline:hover, .add-inline:focus-visible { text-decoration: underline; outline: 2px solid rgba(36, 103, 223, .25); outline-offset: 2px; }
    .task-list, .agent-list { display: grid; gap: 7px; }
    .task-row, .agent-row { display: grid; align-items: center; min-height: 48px; padding: 7px 8px 7px 10px; border: 1px solid var(--soft-line); border-radius: var(--radius-sm); background: #fff; font-size: 12px; transition: border-color .16s ease, background .16s ease; }
    .task-row { grid-template-columns: 27px minmax(0, 1fr) auto 24px; gap: 8px; }
    .task-row:hover, .agent-row:hover { border-color: #bbb8ae; }
    .task-index { width: 25px; height: 25px; display: grid; place-items: center; border-radius: 6px; background: #f0efe9; color: var(--muted); font-family: var(--mono); font-size: 10px; }
    .task-copy { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-weight: 700; }
    .capability { padding: 4px 7px; border: 1px solid var(--line); border-radius: 5px; background: #f7f7f4; color: var(--muted); font-family: var(--mono); font-size: 9px; white-space: nowrap; }
    .agent-row { grid-template-columns: 13px minmax(0, 1fr) auto 24px; gap: 9px; }
    .agent-meta { min-width: 0; display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
    .agent-rate { color: var(--muted); font-family: var(--mono); font-size: 9px; white-space: nowrap; }
    .agent-row.offline { border-color: #e2aeb3; background: var(--red-soft); }
    .agent-row.offline .agent-meta strong { text-decoration: line-through; color: var(--red); }
    .offline-pill { padding: 3px 6px; border-radius: 5px; background: var(--red); color: white; font-family: var(--mono); font-size: 8px; font-weight: 900; letter-spacing: .05em; }
    .dot { width: 9px; height: 9px; border-radius: 50%; }
    .row-remove { width: 34px; height: 34px; margin: -5px; border: 0; background: none; color: #8a8e86; cursor: pointer; border-radius: 7px; }
    .row-remove:hover { color: var(--ink); background: #ecebe5; }
    .row-remove:focus-visible { color: var(--ink); background: #ecebe5; outline: 3px solid rgba(36, 103, 223, .25); outline-offset: 1px; }
    .helper { margin: 7px 2px 0; color: var(--muted); font-family: var(--mono); font-size: 9px; line-height: 1.45; }
    textarea { width: 100%; min-height: 95px; resize: none; border: 1px solid var(--line); border-radius: var(--radius-sm); padding: 11px; color: var(--ink-2); background: #f8f7f3; font-size: 12px; line-height: 1.48; }
    .objective-row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 8px; }
    select { width: 100%; min-height: 41px; border: 1px solid var(--line); border-radius: var(--radius-sm); padding: 0 9px; background: #fff; color: var(--ink); font-size: 12px; font-weight: 700; }
    .plan { min-height: 716px; }
    .plan-status { min-height: 47px; padding: 0 23px; display: flex; align-items: center; justify-content: space-between; gap: 15px; border-bottom: 1px solid var(--line); background: #f7f6f1; }
    .status-left { display: flex; align-items: center; gap: 9px; font-family: var(--mono); font-size: 10px; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; }
    .status-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--green); box-shadow: 0 0 0 4px rgba(19, 122, 69, .1); }
    .status-dot.incident { background: var(--orange); box-shadow: 0 0 0 4px rgba(240, 90, 24, .12); }
    .plan-hash { color: var(--muted); font-family: var(--mono); font-size: 10px; }
    .plan-head { min-height: 129px; padding: 21px 23px; display: grid; grid-template-columns: minmax(150px, .7fr) minmax(450px, 1.7fr); align-items: center; gap: 22px; border-bottom: 1px solid var(--line); }
    .plan-head-copy p { margin: 7px 0 0; color: var(--muted); font-size: 12px; line-height: 1.45; }
    .metrics { display: grid; grid-template-columns: repeat(4, 1fr); border: 1px solid var(--line); border-radius: 12px; overflow: hidden; background: #fff; }
    .metric { min-height: 77px; padding: 12px 14px; border-right: 1px solid var(--soft-line); }
    .metric:last-child { border-right: 0; }
    .metric span { display: block; color: var(--muted); font-family: var(--mono); font-size: 9px; font-weight: 800; letter-spacing: .07em; text-transform: uppercase; }
    .metric strong { display: block; margin-top: 7px; font-family: var(--mono); font-size: 24px; font-weight: 700; letter-spacing: -.8px; }
    .metric.cost strong { color: var(--ink); }
    .metric.slack strong, .metric.deadline strong { color: var(--green); }
    .timeline-shell { padding: 20px 23px 0; }
    .timeline-title-row { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
    .timeline-title-row strong { font-size: 13px; }
    .timeline-title-row span { color: var(--muted); font-family: var(--mono); font-size: 9px; }
    .timeline { position: relative; min-height: 397px; border: 1px solid var(--line); border-radius: 12px; overflow: hidden; background: #fff; }
    .timeline-inner { min-width: 650px; position: relative; }
    .axis { height: 43px; margin-left: 116px; border-bottom: 1px solid var(--line); position: relative; display: flex; justify-content: space-between; align-items: end; padding: 0 10px 8px; color: var(--muted); font-family: var(--mono); font-size: 9px; }
    .axis::after { content: "DEADLINE"; position: absolute; right: 8px; top: 7px; color: var(--green); font-size: 8px; font-weight: 900; letter-spacing: .08em; }
    .time-label { position: absolute; left: -102px; bottom: 8px; }
    .timeline-row { min-height: 83px; display: grid; grid-template-columns: 116px 1fr; border-bottom: 1px solid var(--soft-line); }
    .timeline-row:last-child { border-bottom: 0; }
    .row-label { padding: 19px 13px; font-size: 12px; font-weight: 800; }
    .row-label small { display: block; margin-top: 5px; color: var(--muted); font-family: var(--mono); font-size: 9px; font-weight: 500; }
    .track { position: relative; padding: 16px 8px; background-image: linear-gradient(to right, transparent calc(100% - 1px), #eeece6 calc(100% - 1px)); background-size: 20% 100%; }
    .track::after { content: ""; position: absolute; right: 0; top: 0; bottom: 0; width: 2px; background: rgba(19, 122, 69, .55); }
    .bar { position: absolute; top: 16px; min-width: 84px; min-height: 50px; padding: 7px 10px; border: 1.5px solid var(--blue); border-radius: 8px; background: var(--blue-soft); overflow: hidden; box-shadow: inset 0 -3px 0 var(--orange); }
    .bar.green { border-color: var(--green); background: var(--green-soft); }
    .bar.purple { border-color: var(--purple); background: var(--purple-soft); }
    .bar strong { display: block; font-size: 11px; white-space: nowrap; }
    .bar small { display: block; margin-top: 3px; color: #4f554d; font-family: var(--mono); font-size: 8px; white-space: nowrap; }
    .timeline-row.completed .bar { border-color: var(--green); background: var(--green-soft); box-shadow: none; }
    .timeline-row.completed .bar::after { content: "PRESERVED ✓"; position: absolute; right: 6px; top: 6px; color: var(--green); font-family: var(--mono); font-size: 7px; font-weight: 900; }
    .timeline-row.reassigned .bar { border-color: var(--purple); background: var(--purple-soft); box-shadow: inset 0 -3px 0 var(--orange); }
    .failure-line { position: absolute; top: 43px; bottom: 0; width: 2px; background: var(--red); z-index: 7; pointer-events: none; }
    .failure-line::before { content: "FAILURE · 22m"; position: absolute; top: 5px; left: 7px; padding: 4px 6px; border-radius: 5px; background: var(--red); color: white; font-family: var(--mono); font-size: 8px; font-weight: 900; white-space: nowrap; }
    .empty { display: grid; place-items: center; min-height: 350px; color: var(--muted); font-family: var(--mono); font-size: 11px; }
    .plan-footer { padding: 17px 23px 23px; display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 14px; align-items: stretch; }
    .explain { padding: 14px 15px; border: 1px solid var(--line); border-radius: 11px; background: #f7f6f1; }
    .explain strong { display: flex; align-items: center; gap: 7px; font-size: 12px; }
    .explain strong::before { content: "↳"; color: var(--orange); font-family: var(--mono); }
    .explain p { margin: 7px 0 0; color: var(--muted); font-family: var(--mono); font-size: 9px; line-height: 1.55; }
    .json-button { min-width: 112px; border: 1px solid var(--line); border-radius: 11px; background: #fff; cursor: pointer; font-family: var(--mono); font-size: 10px; font-weight: 800; }
    .json-button:hover { border-color: var(--ink); }
    .site-footer { min-height: 84px; margin-top: 31px; padding: 0 5px; border-top: 1px solid var(--line); display: flex; align-items: center; justify-content: space-between; gap: 24px; color: var(--muted); font-family: var(--mono); font-size: 10px; }
    .footer-proof { display: flex; gap: 17px; flex-wrap: wrap; }
    .footer-proof span::before { content: "✓"; color: var(--green); margin-right: 6px; font-weight: 900; }
    dialog { width: min(900px, 92vw); max-height: 82vh; border: 1px solid var(--line); border-radius: 15px; padding: 0; background: var(--paper); box-shadow: var(--shadow); }
    dialog::backdrop { background: rgba(17, 17, 15, .48); backdrop-filter: blur(3px); }
    dialog pre { margin: 0; padding: 22px; overflow: auto; font-size: 11px; line-height: 1.5; }
    .dialog-head { display: flex; justify-content: space-between; align-items: center; padding: 13px 18px; border-bottom: 1px solid var(--line); }
    .dialog-head button { border: 0; background: none; font-size: 24px; cursor: pointer; }
    .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
    @media (max-width: 1120px) {
      .hero { grid-template-columns: 1fr; gap: 22px; }
      .hero-side { display: grid; grid-template-columns: 1fr auto; align-items: end; gap: 25px; }
      .workspace { grid-template-columns: 1fr; }
      .mission { position: static; }
      .plan { min-height: 690px; }
    }
    @media (max-width: 760px) {
      .topbar { padding: 0 18px; }
      nav { gap: 14px; }
      nav a:first-child { display: none; }
      main { width: min(100% - 24px, 1540px); padding-top: 34px; }
      h1 { font-size: clamp(44px, 14vw, 68px); }
      .hero-side { display: block; }
      .proof-row { margin-top: 18px; }
      .command-bar { align-items: flex-start; }
      .actions { width: 100%; }
      .button { flex: 1; }
      .keyboard-note { display: none; }
      .incident-banner { grid-template-columns: auto 1fr; }
      .incident-proof { grid-column: 1 / -1; }
      .plan-head { grid-template-columns: 1fr; }
      .metrics { grid-template-columns: 1fr 1fr; }
      .metric:nth-child(2) { border-right: 0; }
      .metric:nth-child(-n+2) { border-bottom: 1px solid var(--soft-line); }
      .timeline { overflow-x: auto; }
      .plan-footer { grid-template-columns: 1fr; }
      .json-button { min-height: 43px; }
      .site-footer { align-items: flex-start; flex-direction: column; padding: 22px 5px; }
    }
    @media (max-width: 520px) {
      .brand { font-size: 19px; }
      .nav-cta { display: none; }
      .actions { flex-direction: column; }
      .button { width: 100%; }
      .objective-row { grid-template-columns: 1fr; }
      .mission { padding: 18px 14px; }
      .plan-status, .plan-head, .timeline-shell, .plan-footer { padding-left: 14px; padding-right: 14px; }
      .plan-hash { display: none; }
      .incident-proof { flex-wrap: wrap; }
    }
    @media (max-width: 620px) {
      .timeline { overflow: visible; }
      .timeline-inner { min-width: 0; padding: 10px; }
      .axis, .failure-line { display: none; }
      .timeline-row { min-height: 0; display: block; padding: 11px 5px 14px; border-bottom: 1px solid var(--soft-line); }
      .row-label { padding: 0 0 8px; }
      .row-label small { display: inline; margin-left: 7px; }
      .track { min-height: 52px; padding: 0; background: none; }
      .track::after { display: none; }
      .bar { position: relative; inset: auto !important; width: 100% !important; min-height: 52px; }
    }
    @media (prefers-reduced-motion: reduce) { * { scroll-behavior: auto !important; transition: none !important; } }
  </style>
</head>
<body>
  <header class="topbar">
    <a class="brand" href="/" aria-label="SwarmShift home"><span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span>SwarmShift</a>
    <nav aria-label="Primary navigation">
      <a href="/docs">API docs</a>
      <a href="/skill.md">SKILL.md</a>
      <a class="nav-cta" href="https://github.com/himanshu748/swarmshift">GitHub ↗</a>
    </nav>
  </header>
  <main>
    <section class="hero">
      <div>
        <p class="eyebrow">Deterministic agent operations</p>
        <h1 aria-label="Plan the swarm. Keep the deadline.">Plan the swarm.<br>Keep the <em>deadline.</em></h1>
      </div>
      <div class="hero-side">
        <p class="lede">Turn dependencies, capabilities, and cost into an execution plan that can recover when an agent goes offline.</p>
        <div class="proof-row" aria-label="Product proof points">
          <span class="proof-chip">Same input, same plan</span>
          <span class="proof-chip">No API key</span>
          <span class="proof-chip">Failure-aware</span>
        </div>
      </div>
    </section>
    <div class="command-bar">
      <div class="actions">
        <button id="run" class="button primary" type="button"><span aria-hidden="true">▶</span> Generate plan</button>
        <button id="incident" class="button incident" type="button"><span aria-hidden="true">⚡</span> Simulate Builder failure</button>
      </div>
      <span class="keyboard-note"><kbd>1</kbd> plan &nbsp; <kbd>2</kbd> incident</span>
    </div>
    <aside id="incident-banner" class="incident-banner" hidden aria-live="assertive">
      <span class="incident-icon" aria-hidden="true">!</span>
      <div><strong>Builder went offline at minute 22</strong><p>SwarmShift kept completed research and reassigned only the remaining work.</p></div>
      <div class="incident-proof"><span class="kept">Research preserved</span><span>Reviewer → Build · +$0.01</span><span>58m remaining</span><span class="kept">90m deadline met</span></div>
    </aside>
    <section class="workspace" aria-label="Planner workspace">
      <form class="mission panel" id="mission-form">
        <div class="mission-head"><div><p class="panel-kicker">Inputs</p><h2 class="section-title">Mission brief</h2></div><span class="mission-count">4 TASKS · 3 AGENTS</span></div>
        <div class="field-group">
          <div class="field-label"><span><span class="step">1</span>Tasks & dependencies</span><button id="add-task" class="add-inline" type="button">+ Add task</button></div>
          <div class="task-list" id="task-list"></div>
          <p class="helper">Each task starts only after its dependencies finish.</p>
        </div>
        <div class="field-group">
          <div class="field-label"><span><span class="step">2</span>Agent pool</span><button id="add-agent" class="add-inline" type="button">+ Add agent</button></div>
          <div class="agent-list" id="agent-list"></div>
        </div>
        <div class="field-group">
          <label class="field-label" for="objective-copy"><span><span class="step">3</span>Demo success criteria</span></label>
          <textarea id="objective-copy" readonly aria-readonly="true">Deliver a production-ready integration with tests and docs. Respect the 90-minute deadline and minimize cost.</textarea>
          <div class="objective-row">
            <label><span class="sr-only">Optimization mode</span><select id="mode"><option value="balanced">Balanced objective</option><option value="fastest">Fastest finish</option><option value="cheapest">Lowest cost</option></select></label>
            <label><span class="sr-only">Deadline in minutes</span><select id="deadline"><option value="90">90-minute deadline</option><option value="75">75-minute deadline</option><option value="120">120-minute deadline</option></select></label>
          </div>
        </div>
      </form>
      <section class="plan panel" aria-live="polite" aria-busy="false">
        <div class="plan-status">
          <div class="status-left"><span id="status-dot" class="status-dot"></span><span id="status-copy">Plan ready · deadline protected</span></div>
          <span class="plan-hash">plan <strong id="hash">pending</strong></span>
        </div>
        <div class="plan-head">
          <div class="plan-head-copy"><p class="panel-kicker">Output</p><h2 class="section-title">Execution map</h2><p id="plan-subtitle">Four dependent tasks assigned across three capable agents.</p></div>
          <div class="metrics" aria-label="Plan metrics">
            <div class="metric"><span>Finish</span><strong id="finish">—</strong></div>
            <div class="metric cost"><span>Total cost</span><strong id="cost">—</strong></div>
            <div class="metric slack"><span>Slack</span><strong id="slack">—</strong></div>
            <div class="metric deadline"><span>Deadline</span><strong id="deadline-state">—</strong></div>
          </div>
        </div>
        <div class="timeline-shell">
          <div class="timeline-title-row"><strong>Dependency-aware schedule</strong><span id="timeline-mode">BASELINE · 0–90 MIN</span></div>
          <div class="timeline"><div class="timeline-inner" id="timeline"><div class="empty">Generating deterministic schedule…</div></div></div>
        </div>
        <div class="plan-footer">
          <div class="explain"><strong id="explain-title">Why this plan</strong><p id="explanation">The planner will show why each agent was selected and where dependencies constrain the schedule.</p></div>
          <button id="view-json" class="json-button" type="button">&lt;/&gt; View JSON</button>
        </div>
      </section>
    </section>
    <footer class="site-footer">
      <span>SwarmShift v0.1 · stateless FastAPI service</span>
      <div class="footer-proof"><span>Deterministic SHA-256 plan hash</span><span>Completed work preserved</span><span>Open API + SKILL.md</span></div>
    </footer>
  </main>
  <dialog id="json-dialog">
    <div class="dialog-head"><strong>Current plan JSON</strong><button id="close-dialog" aria-label="Close">×</button></div>
    <pre id="json-output"></pre>
  </dialog>
  <script>
    const demo = {
      tasks: [
        {id:'research', label:'Research API surface and constraints', duration_minutes:22, requires:['research'], depends_on:[], priority:5},
        {id:'build', label:'Build integration and adapter', duration_minutes:36, requires:['code'], depends_on:['research'], priority:5},
        {id:'verify', label:'Verify behavior and edge cases', duration_minutes:12, requires:['qa'], depends_on:['build'], priority:4},
        {id:'ship', label:'Ship release and notes', duration_minutes:10, requires:['research'], depends_on:['verify'], priority:3}
      ],
      agents: [
        {id:'Scout', capabilities:['research'], cost_per_hour:.55, color:'green'},
        {id:'Builder', capabilities:['code'], cost_per_hour:.85, color:'blue'},
        {id:'Reviewer', capabilities:['qa','code'], cost_per_hour:1.20, color:'purple'}
      ]
    };
    let lastPlan = null;
    let lastJson = null;
    let incidentMode = false;
    const byId = id => document.getElementById(id);
    const colorHex = color => color === 'green' ? '#137a45' : color === 'purple' ? '#6f42c1' : '#2467df';
    function renderMission() {
      byId('task-list').innerHTML = demo.tasks.map((task, i) => `<div class="task-row"><span class="task-index">${i+1}</span><span class="task-copy">${task.label}</span><span class="capability">${task.requires.join(' + ')}</span><button class="row-remove" data-remove-task="${task.id}" aria-label="Remove ${task.id}">×</button></div>`).join('');
      byId('agent-list').innerHTML = demo.agents.map(agent => {
        const offline = incidentMode && agent.id === 'Builder';
        return `<div class="agent-row ${offline?'offline':''}"><span class="dot" style="background:${offline?'#c72f3a':colorHex(agent.color)}"></span><span class="agent-meta"><strong>${agent.id}</strong>${offline?'<span class="offline-pill">OFFLINE</span>':`<span class="capability">${agent.capabilities.join(' · ')}</span>`}</span><span class="agent-rate">$${agent.cost_per_hour.toFixed(2)}/hr</span><button class="row-remove" data-remove-agent="${agent.id}" aria-label="Remove ${agent.id}">×</button></div>`;
      }).join('');
      byId('mission-form').querySelector('.mission-count').textContent = `${demo.tasks.length} TASKS · ${demo.agents.length} AGENTS`;
      document.querySelectorAll('[data-remove-task]').forEach(button => button.addEventListener('click', () => {
        const id = button.dataset.removeTask;
        demo.tasks = demo.tasks.filter(task => task.id !== id).map(task => ({...task, depends_on:task.depends_on.filter(parent => parent !== id)}));
        renderMission(); runPlan();
      }));
      document.querySelectorAll('[data-remove-agent]').forEach(button => button.addEventListener('click', () => {
        demo.agents = demo.agents.filter(agent => agent.id !== button.dataset.removeAgent);
        renderMission(); runPlan();
      }));
    }
    function payload() {
      return {
        tasks: demo.tasks.map(({label, ...task}) => task),
        agents: demo.agents.map(({color, ...agent}) => agent),
        objective: {mode: byId('mode').value, cost_weight:.35, deadline_minutes:Number(byId('deadline').value)}
      };
    }
    function setBusy(isBusy) {
      document.querySelector('.plan').setAttribute('aria-busy', String(isBusy));
      byId('run').disabled = isBusy;
      byId('incident').disabled = isBusy;
    }
    function renderTimeline(result, context = {}) {
      const deadline = Number(byId('deadline').value);
      const ticks = [0,.2,.4,.6,.8,1].map(v => Math.round(deadline*v));
      const assignmentByTask = Object.fromEntries(result.assignments.map(item => [item.task_id,item]));
      if (context.incident) assignmentByTask.research = {task_id:'research',agent_id:'Scout',start_minute:0,end_minute:22,duration_minutes:22,cost:.2017,critical:true,preserved:true};
      const colorByAgent = Object.fromEntries(demo.agents.map(agent => [agent.id,agent.color]));
      const rows = demo.tasks.filter(task => assignmentByTask[task.id]).map(task => {
        const item = assignmentByTask[task.id];
        const left = item.start_minute / deadline * 100;
        const width = Math.max(item.duration_minutes / deadline * 100, 11);
        const classes = [item.preserved?'completed':'', context.incident && task.id === 'build'?'reassigned':''].filter(Boolean).join(' ');
        const state = item.preserved ? 'completed · kept' : context.incident && task.id === 'build' ? 'reassigned' : item.critical ? 'critical path' : 'scheduled';
        return `<div class="timeline-row ${classes}"><div class="row-label">${task.id[0].toUpperCase()+task.id.slice(1)}<small>${item.duration_minutes}m · ${state}</small></div><div class="track"><div class="bar ${colorByAgent[item.agent_id]||''}" style="left:${left}%;width:min(${width}%,calc(100% - ${left}% - 8px))"><strong>${item.agent_id}</strong><small>${item.start_minute}–${item.end_minute}m · $${item.cost.toFixed(2)}</small></div></div></div>`;
      }).join('');
      const failure = context.incident ? `<span class="failure-line" style="left:calc(116px + (100% - 116px) * ${22/deadline})"></span>` : '';
      byId('timeline').innerHTML = `<div class="axis"><span class="time-label">TIME / MIN</span>${ticks.map(t=>`<span>${t}</span>`).join('')}</div>${rows}${failure}`;
      const finish = Math.max(0, ...Object.values(assignmentByTask).map(item => item.end_minute));
      const slack = deadline - finish;
      byId('finish').textContent = `${finish}m`;
      byId('cost').textContent = `$${result.metrics.total_cost.toFixed(2)}`;
      byId('slack').textContent = `${slack >= 0 ? '+' : ''}${slack}m`;
      byId('deadline-state').textContent = result.metrics.deadline_met ? 'MET ✓' : 'MISSED';
      byId('deadline-state').style.color = result.metrics.deadline_met ? '#137a45' : '#c72f3a';
      byId('slack').style.color = slack >= 0 ? '#137a45' : '#c72f3a';
      byId('hash').textContent = `${result.plan_hash.slice(0,6)}…${result.plan_hash.slice(-6)}`;
      byId('json-output').textContent = JSON.stringify(lastJson || result,null,2);
      byId('explanation').textContent = context.incident ? context.changes.join(' ') : result.explanation.join(' ');
      byId('status-dot').className = `status-dot${context.incident?' incident':''}`;
      byId('status-copy').textContent = context.incident ? 'Recovered plan · no duplicated work' : 'Plan ready · deadline protected';
      byId('timeline-mode').textContent = context.incident ? 'RECOVERY · FAILURE AT 22 MIN' : `BASELINE · 0–${deadline} MIN`;
      byId('plan-subtitle').textContent = context.incident ? 'Builder removed. Research stays fixed; Reviewer takes the code.' : `${demo.tasks.length} dependent tasks assigned across ${demo.agents.length} capable agents.`;
      byId('explain-title').textContent = context.incident ? 'What changed' : 'Why this plan';
    }
    async function runPlan(focusResult = false) {
      const button = byId('run');
      incidentMode = false;
      renderMission();
      byId('incident-banner').hidden = true;
      byId('incident').className = 'button incident';
      byId('incident').innerHTML = '<span aria-hidden="true">⚡</span> Simulate Builder failure';
      setBusy(true); button.innerHTML = '<span aria-hidden="true">◌</span> Planning…';
      try {
        const response = await fetch('/v1/plan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload())});
        const data = await response.json();
        if (!response.ok) throw new Error(data.error?.message || 'Planning failed');
        lastPlan = data; lastJson = data; renderTimeline(data);
        if (focusResult && window.innerWidth <= 760) requestAnimationFrame(() => document.querySelector('.plan').scrollIntoView({behavior:'smooth',block:'start'}));
      } catch (error) {
        byId('explanation').textContent = error.message;
        byId('status-copy').textContent = 'Plan needs attention';
      } finally {
        setBusy(false); button.innerHTML = '<span aria-hidden="true">↻</span> Re-run baseline';
      }
    }
    async function runIncident() {
      if (incidentMode) { await runPlan(true); return; }
      if (!lastPlan) await runPlan();
      const button = byId('incident');
      setBusy(true); button.textContent = 'Replanning…';
      try {
        const mission = payload();
        const response = await fetch('/v1/replan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mission,current_minute:22,completed:[{task_id:'research',agent_id:'Scout',ended_at_minute:22}],failed_agent_ids:['Builder']})});
        const data = await response.json();
        if (!response.ok) throw new Error(data.error?.message || 'Replanning failed');
        incidentMode = true; lastPlan = data.plan; lastJson = data; renderMission();
        byId('incident-banner').hidden = false;
        renderTimeline(data.plan,{incident:true,changes:data.changes});
        button.className = 'button restore';
        button.innerHTML = '<span aria-hidden="true">↺</span> Restore baseline';
        if (window.innerWidth <= 760) requestAnimationFrame(() => document.querySelector('.plan').scrollIntoView({behavior:'smooth',block:'start'}));
      } catch (error) {
        byId('explanation').textContent = error.message;
      } finally { setBusy(false); }
    }
    renderMission();
    byId('add-task').addEventListener('click', () => {
      const number = demo.tasks.length + 1;
      const parent = demo.tasks.at(-1)?.id;
      demo.tasks.push({id:`task-${number}`, label:`Follow-up task ${number}`, duration_minutes:15, requires:['code'], depends_on:parent?[parent]:[], priority:3});
      renderMission(); runPlan();
    });
    byId('add-agent').addEventListener('click', () => {
      const number = demo.agents.length + 1;
      demo.agents.push({id:`Agent-${number}`, capabilities:['research','code','qa'], cost_per_hour:1, color:'blue'});
      renderMission(); runPlan();
    });
    byId('run').addEventListener('click',()=>runPlan(true));
    byId('incident').addEventListener('click',runIncident);
    byId('mode').addEventListener('change',runPlan);
    byId('deadline').addEventListener('change',runPlan);
    byId('view-json').addEventListener('click',()=>byId('json-dialog').showModal());
    byId('close-dialog').addEventListener('click',()=>byId('json-dialog').close());
    document.addEventListener('keydown', event => {
      if (event.target.matches('textarea, input, select')) return;
      if (event.key === '1') runPlan(true);
      if (event.key === '2') runIncident();
      if (event.key === 'Escape' && byId('json-dialog').open) byId('json-dialog').close();
    });
    runPlan();
  </script>
</body>
</html>
"""
