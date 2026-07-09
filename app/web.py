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
      --ink: #0b0d10;
      --muted: #56606f;
      --line: #c8d1dc;
      --soft-line: #e7ebf0;
      --blue: #0e5ee8;
      --blue-soft: #edf4ff;
      --orange: #f45b0b;
      --green: #19883b;
      --green-soft: #eef9f0;
      --purple: #672dc4;
      --white: #ffffff;
      --radius: 10px;
      --mono: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      --sans: Inter, ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    * { box-sizing: border-box; }
    body { margin: 0; color: var(--ink); background: var(--white); font-family: var(--sans); }
    button, textarea, input, select { font: inherit; }
    a { color: inherit; }
    header { height: 68px; display: flex; align-items: center; justify-content: space-between; padding: 0 30px; border-bottom: 1px solid var(--line); }
    .brand { font-weight: 800; font-size: 28px; letter-spacing: -1px; text-decoration: none; }
    nav { display: flex; align-items: center; gap: 34px; font-weight: 650; }
    nav a { text-decoration: none; border-bottom: 2px solid transparent; padding: 8px 0; }
    nav a:hover, nav a:focus-visible { border-color: var(--blue); outline: none; }
    main { padding: 24px 28px 0; }
    h1 { font-size: clamp(38px, 4vw, 58px); line-height: 1.03; letter-spacing: -2.6px; margin: 0; max-width: 1000px; }
    .lede { margin: 12px 0 20px; color: var(--muted); font-size: clamp(17px, 1.55vw, 23px); }
    .actions { display: flex; gap: 14px; margin-bottom: 20px; }
    .button { min-height: 48px; padding: 0 22px; border: 1px solid #667384; border-radius: 8px; background: var(--white); color: var(--ink); font-weight: 700; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; gap: 10px; }
    .button.primary { border-color: var(--blue); background: var(--blue); color: var(--white); box-shadow: 0 0 0 3px #bdd3ff; }
    .button:hover { transform: translateY(-1px); }
    .button:focus-visible, textarea:focus-visible, select:focus-visible { outline: 3px solid #a9c8ff; outline-offset: 2px; }
    .workspace { display: grid; grid-template-columns: minmax(320px, .88fr) minmax(620px, 2fr); gap: 4%; align-items: stretch; min-height: 610px; }
    .mission, .plan { border: 1px solid var(--line); border-radius: var(--radius); background: var(--white); overflow: hidden; }
    .mission { padding: 18px 14px 14px; }
    .section-title { font-size: 21px; font-weight: 800; letter-spacing: -.45px; margin: 0 0 14px; }
    .field-label { display: flex; justify-content: space-between; align-items: center; font-weight: 750; margin: 12px 0 7px; }
    .add-inline { border: 0; background: none; color: var(--blue); font-weight: 750; cursor: pointer; padding: 4px; }
    .add-inline:hover, .add-inline:focus-visible { text-decoration: underline; outline: 2px solid #a9c8ff; outline-offset: 2px; }
    .task-list, .agent-list { border: 1px solid var(--line); border-radius: 7px; overflow: hidden; }
    .task-row, .agent-row { display: grid; grid-template-columns: 28px 1fr auto 24px; gap: 8px; align-items: center; min-height: 42px; padding: 0 7px 0 9px; border-bottom: 1px solid var(--soft-line); font-size: 13px; }
    .task-row:last-child, .agent-row:last-child { border-bottom: 0; }
    .task-row span:first-child { font-family: var(--mono); color: var(--muted); }
    .capability { padding: 3px 7px; border: 1px solid var(--line); border-radius: 5px; background: #f7f9fb; color: var(--muted); font-family: var(--mono); font-size: 11px; }
    .dot { width: 10px; height: 10px; border-radius: 50%; }
    .agent-row { grid-template-columns: 15px 1fr auto 24px; }
    .row-remove { width: 24px; height: 24px; border: 0; background: none; color: var(--muted); cursor: pointer; border-radius: 4px; }
    .row-remove:hover, .row-remove:focus-visible { color: var(--ink); background: #eef2f6; outline: none; }
    .helper { color: var(--muted); font-family: var(--mono); font-size: 11px; margin: 7px 2px 0; }
    textarea { width: 100%; min-height: 112px; resize: vertical; border: 1px solid var(--blue); border-radius: 7px; padding: 11px; color: var(--ink); background: var(--white); font-family: var(--mono); font-size: 12px; line-height: 1.45; }
    .objective-row { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
    select { min-height: 40px; border: 1px solid var(--line); border-radius: 7px; padding: 0 9px; background: var(--white); }
    .plan { display: flex; flex-direction: column; }
    .plan-head { min-height: 84px; padding: 0 26px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid var(--line); }
    .metrics { display: flex; align-items: center; gap: 42px; }
    .metric strong { display: block; font-family: var(--mono); font-size: 29px; font-weight: 500; color: var(--orange); }
    .metric.cost strong { color: var(--green); }
    .metric span { display: block; margin-top: 3px; font-family: var(--mono); font-size: 11px; color: var(--muted); }
    .timeline { position: relative; flex: 1; min-height: 415px; background: linear-gradient(to right, transparent calc(100% - 1px), var(--soft-line) calc(100% - 1px)); background-size: 12.5% 100%; }
    .axis { height: 48px; margin-left: 116px; border-bottom: 1px solid var(--line); position: relative; display: flex; justify-content: space-between; align-items: end; padding: 0 10px 9px; font-family: var(--mono); font-size: 11px; }
    .time-label { position: absolute; left: -102px; bottom: 9px; color: var(--muted); }
    .timeline-row { min-height: 86px; display: grid; grid-template-columns: 116px 1fr; border-bottom: 1px solid var(--soft-line); }
    .row-label { padding: 22px 15px; font-weight: 750; }
    .row-label small { display: block; margin-top: 5px; color: var(--muted); font-family: var(--mono); font-weight: 400; }
    .track { position: relative; padding: 18px 8px; }
    .bar { position: absolute; top: 18px; min-width: 94px; min-height: 51px; padding: 7px 11px; border: 2px solid var(--blue); border-radius: 7px; background: var(--blue-soft); overflow: hidden; }
    .bar.green { border-color: var(--green); background: var(--green-soft); }
    .bar.purple { border-color: var(--purple); background: #f5efff; }
    .bar strong { display: block; font-size: 13px; white-space: nowrap; }
    .bar small { display: block; font-family: var(--mono); color: #354052; white-space: nowrap; margin-top: 3px; }
    .critical .row-label { color: var(--orange); }
    .critical .bar { box-shadow: inset 0 -3px 0 var(--orange); }
    .legend { min-height: 46px; padding: 0 18px 0 132px; display: flex; align-items: center; gap: 26px; border-top: 1px solid var(--soft-line); font-family: var(--mono); font-size: 11px; color: #354052; }
    .legend-item { display: inline-flex; align-items: center; gap: 7px; }
    .legend-swatch { width: 12px; height: 12px; border-radius: 3px; background: var(--blue); }
    .legend-swatch.green { background: var(--green); }
    .legend-swatch.purple { background: var(--purple); }
    .legend-swatch.critical-line { width: 28px; height: 2px; border-radius: 0; background: var(--orange); }
    .empty { display: grid; place-items: center; height: 100%; color: var(--muted); font-family: var(--mono); }
    .explain { min-height: 76px; display: grid; grid-template-columns: 122px 1fr auto; align-items: center; gap: 18px; padding: 12px 18px; border-top: 1px solid var(--line); }
    .explain strong { border-right: 1px solid var(--line); padding-right: 18px; }
    .explain p { margin: 0; color: #354052; font-family: var(--mono); font-size: 11px; line-height: 1.55; }
    .json-button { min-height: 38px; padding: 0 13px; border: 1px solid #667384; border-radius: 6px; background: white; cursor: pointer; }
    footer { min-height: 72px; margin: 24px -28px 0; padding: 0 34px; border-top: 1px solid var(--line); display: flex; align-items: center; gap: 30px; color: #354052; font-family: var(--mono); font-size: 12px; }
    .status-good { color: var(--green); }
    dialog { width: min(900px, 92vw); max-height: 82vh; border: 1px solid var(--line); border-radius: 10px; padding: 0; }
    dialog::backdrop { background: rgba(16, 24, 40, .35); }
    dialog pre { margin: 0; padding: 22px; overflow: auto; font-size: 12px; }
    .dialog-head { display: flex; justify-content: space-between; align-items: center; padding: 12px 18px; border-bottom: 1px solid var(--line); }
    .dialog-head button { border: 0; background: none; font-size: 24px; cursor: pointer; }
    .sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
    @media (max-width: 980px) {
      header { padding: 0 18px; }
      nav { gap: 16px; font-size: 14px; }
      main { padding: 20px 16px 0; }
      .workspace { grid-template-columns: 1fr; }
      .mission { max-width: none; }
      .plan { min-height: 600px; }
      footer { margin-left: -16px; margin-right: -16px; }
    }
    @media (max-width: 620px) {
      .brand { font-size: 23px; }
      nav a:last-child { display: none; }
      h1 { font-size: 40px; letter-spacing: -1.8px; }
      .actions { flex-direction: column; }
      .metrics { gap: 16px; }
      .plan-head { padding: 12px 16px; align-items: flex-start; gap: 16px; flex-direction: column; }
      .timeline { overflow-x: auto; }
      .timeline-inner { min-width: 680px; }
      .explain { grid-template-columns: 1fr; }
      .explain strong { border: 0; }
      .legend { padding-left: 18px; flex-wrap: wrap; gap: 12px; }
      footer { align-items: flex-start; flex-direction: column; padding: 18px; gap: 8px; }
    }
    @media (prefers-reduced-motion: reduce) { * { scroll-behavior: auto !important; transition: none !important; } }
  </style>
</head>
<body>
  <header>
    <a class="brand" href="/">SwarmShift</a>
    <nav aria-label="Primary navigation">
      <a href="/docs">API docs</a>
      <a href="/skill.md">SKILL.md</a>
      <a href="https://github.com/himanshu748/swarmshift">GitHub</a>
    </nav>
  </header>
  <main>
    <h1>Plan the swarm. Keep the deadline.</h1>
    <p class="lede">Turn tasks, dependencies, and agent capabilities into a deterministic execution plan.</p>
    <div class="actions">
      <button id="run" class="button primary" type="button"><span aria-hidden="true">▶</span> Run plan</button>
      <button id="incident" class="button" type="button">Load incident demo</button>
    </div>
    <section class="workspace" aria-label="Planner workspace">
      <form class="mission" id="mission-form">
        <h2 class="section-title">Mission</h2>
        <div class="field-label"><span>Tasks</span><button id="add-task" class="add-inline" type="button">⊕ Add task</button></div>
        <div class="task-list" id="task-list"></div>
        <p class="helper">Dependencies are enforced by the planner</p>
        <div class="field-label"><span>Agents</span><button id="add-agent" class="add-inline" type="button">⊕ Add agent</button></div>
        <div class="agent-list" id="agent-list"></div>
        <label class="field-label" for="objective-copy">Objective</label>
        <textarea id="objective-copy">Deliver a production-ready integration that meets all constraints with tests and docs. Deadline: 90 minutes. Minimize cost.</textarea>
        <div class="objective-row">
          <label><span class="sr-only">Optimization mode</span><select id="mode"><option value="balanced">Balanced</option><option value="fastest">Fastest</option><option value="cheapest">Cheapest</option></select></label>
          <label><span class="sr-only">Deadline in minutes</span><select id="deadline"><option value="90">90 minute deadline</option><option value="75">75 minute deadline</option><option value="120">120 minute deadline</option></select></label>
        </div>
      </form>
      <section class="plan" aria-live="polite">
        <div class="plan-head">
          <h2 class="section-title">Execution plan</h2>
          <div class="metrics">
            <div class="metric"><strong id="makespan">—</strong><span>Critical path</span></div>
            <div class="metric cost"><strong id="cost">—</strong><span>Total cost</span></div>
          </div>
        </div>
        <div class="timeline"><div class="timeline-inner" id="timeline"><div class="empty">Run the plan to schedule this mission.</div></div></div>
        <div class="legend" aria-label="Timeline legend">
          <span class="legend-item"><span class="legend-swatch green"></span>Scout</span>
          <span class="legend-item"><span class="legend-swatch"></span>Builder</span>
          <span class="legend-item"><span class="legend-swatch purple"></span>Reviewer</span>
          <span class="legend-item"><span class="legend-swatch critical-line"></span>Critical path</span>
        </div>
        <div class="explain">
          <strong>Explanation</strong>
          <p id="explanation">The planner will show why each agent was selected and where dependencies constrain the schedule.</p>
          <button id="view-json" class="json-button" type="button">&lt;/&gt; View as JSON</button>
        </div>
      </section>
    </section>
    <footer>
      <span>Plan hash <strong id="hash">pending</strong></span>
      <span class="status-good">✓ Deterministic · No API key required</span>
    </footer>
  </main>
  <dialog id="json-dialog">
    <div class="dialog-head"><strong>Plan JSON</strong><button id="close-dialog" aria-label="Close">×</button></div>
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
    let lastResult = null;
    const byId = id => document.getElementById(id);
    function renderMission() {
      byId('task-list').innerHTML = demo.tasks.map((task, i) => `<div class="task-row"><span>${i+1}</span><span>${task.label}</span><span class="capability">${task.requires.join(', ')}</span><button class="row-remove" data-remove-task="${task.id}" aria-label="Remove ${task.id}">×</button></div>`).join('');
      byId('agent-list').innerHTML = demo.agents.map(agent => `<div class="agent-row"><span class="dot" style="background:${agent.color==='green'?'#19883b':agent.color==='purple'?'#672dc4':'#0e5ee8'}"></span><span><strong>${agent.id}</strong> <span class="capability">${agent.capabilities.join(' · ')}</span></span><span class="helper">$${agent.cost_per_hour.toFixed(2)} / hr</span><button class="row-remove" data-remove-agent="${agent.id}" aria-label="Remove ${agent.id}">×</button></div>`).join('');
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
    function renderTimeline(result) {
      const max = Math.max(result.metrics.makespan_minutes, Number(byId('deadline').value));
      const ticks = [0,.2,.4,.6,.8,1].map(v => Math.round(max*v));
      const assignmentByTask = Object.fromEntries(result.assignments.map(item => [item.task_id,item]));
      const colorByAgent = Object.fromEntries(demo.agents.map(agent => [agent.id,agent.color]));
      const rows = demo.tasks.filter(task => assignmentByTask[task.id]).map(task => {
        const item = assignmentByTask[task.id];
        const left = item.start_minute / max * 100;
        const width = Math.max(item.duration_minutes / max * 100, 12);
        return `<div class="timeline-row ${item.critical?'critical':''}"><div class="row-label">${task.id[0].toUpperCase()+task.id.slice(1)}<small>${item.duration_minutes} min</small></div><div class="track"><div class="bar ${colorByAgent[item.agent_id]||''}" style="left:${left}%;width:min(${width}%,calc(100% - ${left}% - 8px))"><strong>${item.agent_id}</strong><small>${item.start_minute}–${item.end_minute} min · $${item.cost.toFixed(2)}</small></div></div></div>`;
      }).join('');
      byId('timeline').innerHTML = `<div class="axis"><span class="time-label">Time (min)</span>${ticks.map(t=>`<span>${t}</span>`).join('')}</div>${rows}`;
      byId('makespan').textContent = `${result.metrics.makespan_minutes} min`;
      byId('cost').textContent = `$${result.metrics.total_cost.toFixed(2)}`;
      byId('hash').textContent = `${result.plan_hash.slice(0,4)}…${result.plan_hash.slice(-4)}`;
      byId('explanation').textContent = result.explanation.join(' ');
      byId('json-output').textContent = JSON.stringify(result,null,2);
    }
    async function runPlan() {
      const button = byId('run');
      button.disabled = true; button.textContent = 'Planning…';
      try {
        const response = await fetch('/v1/plan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload())});
        const data = await response.json();
        if (!response.ok) throw new Error(data.error?.message || 'Planning failed');
        lastResult = data; renderTimeline(data);
      } catch (error) {
        byId('explanation').textContent = error.message;
      } finally {
        button.disabled = false; button.innerHTML = '<span aria-hidden="true">▶</span> Run plan';
      }
    }
    async function runIncident() {
      if (!lastResult) await runPlan();
      const mission = payload();
      const response = await fetch('/v1/replan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({mission,current_minute:22,completed:[{task_id:'research',agent_id:'Scout',ended_at_minute:22}],failed_agent_ids:['Builder']})});
      const data = await response.json();
      if (!response.ok) { byId('explanation').textContent = data.error?.message || 'Replanning failed'; return; }
      lastResult = data; renderTimeline(data.plan); byId('explanation').textContent = data.changes.join(' ');
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
    byId('run').addEventListener('click',runPlan);
    byId('incident').addEventListener('click',runIncident);
    byId('view-json').addEventListener('click',()=>byId('json-dialog').showModal());
    byId('close-dialog').addEventListener('click',()=>byId('json-dialog').close());
    runPlan();
  </script>
</body>
</html>
"""
