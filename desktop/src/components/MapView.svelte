<script lang="ts">
  import { onMount } from 'svelte';
  import { topics } from '../lib/data';
  import { MAP_W, MAP_H, nodes, islands, signs, trophy, routeD, blobD, palm, segPoint } from '../lib/layout';
  import { app, statusOf, isLocked, solvedCount, currentIndex, frontier, select } from '../lib/store.svelte';

  let scroller: HTMLDivElement;
  const route = routeD();
  const cur = $derived(currentIndex());
  const front = $derived(frontier());

  // Static decoration, computed once.
  function rand(seed: number) {
    let s = seed;
    return () => ((s = (s * 16807) % 2147483647) / 2147483647);
  }
  const r1 = rand(11);
  const swirls = Array.from({ length: Math.floor(MAP_H / 130) }, () => ({
    x: r1() * MAP_W, y: r1() * MAP_H, r: 20 + r1() * 40, a: r1() * Math.PI * 2,
  }));
  const r2 = rand(5);
  const fish = Array.from({ length: Math.floor(MAP_H / 180) }, () => ({
    x: r2() * MAP_W, y: r2() * MAP_H, s: 0.6 + r2() * 0.7, d: r2() > 0.5 ? 1 : -1,
  }));
  const arc = (x: number, y: number, r: number, a: number, len: number) => {
    const x1 = x + r * Math.cos(a), y1 = y + r * Math.sin(a);
    const x2 = x + r * Math.cos(a + len), y2 = y + r * Math.sin(a + len);
    return `M ${x1.toFixed(1)} ${y1.toFixed(1)} A ${r.toFixed(1)} ${r.toFixed(1)} 0 0 1 ${x2.toFixed(1)} ${y2.toFixed(1)}`;
  };
  const islandArt = [...islands, { c: trophy, r: 92, emoji: '🏆', seed: 99 }].map((s) => ({
    ...s,
    halo: blobD(s.c, s.r, s.seed, 1.2),
    foam: blobD(s.c, s.r, s.seed, 1.05),
    shadow: blobD({ x: s.c.x, y: s.c.y + 8 }, s.r, s.seed, 1),
    sand: blobD(s.c, s.r, s.seed, 1),
    grass: blobD({ x: s.c.x, y: s.c.y - s.r * 0.08 }, s.r, s.seed + 1, 0.62),
    grass2: blobD({ x: s.c.x, y: s.c.y - s.r * 0.12 }, s.r, s.seed + 2, 0.45),
    palms: [palm({ x: s.c.x - s.r * 0.75, y: s.c.y + s.r * 0.15 }, s.r * 0.72, -11), palm({ x: s.c.x + s.r * 0.7, y: s.c.y + s.r * 0.1 }, s.r * 0.62, 13)],
  }));
  const beachY = MAP_H - 90;
  const beach = (() => {
    let d = `M 0 ${beachY}`;
    const w = MAP_W / 6;
    for (let i = 0; i < 6; i++) d += ` Q ${w * i + w / 2} ${beachY + (i % 2 === 0 ? -16 : 12)} ${w * (i + 1)} ${beachY}`;
    return d + ` L ${MAP_W} ${MAP_H} L 0 ${MAP_H} Z`;
  })();

  // Wake (answered) and bubbles (ahead), per segment.
  const segs = Array.from({ length: nodes.length - 1 }, (_, i) => {
    const wake: string[] = [];
    for (let k = 0; k < 14; k += 2) {
      const a = segPoint(i, 0.18 + (0.64 * k) / 14);
      const b = segPoint(i, 0.18 + (0.64 * (k + 1)) / 14);
      wake.push(`M ${a.x.toFixed(1)} ${a.y.toFixed(1)} L ${b.x.toFixed(1)} ${b.y.toFixed(1)}`);
    }
    return { wake: wake.join(' '), bubbles: [0.33, 0.5, 0.67].map((t) => segPoint(i, t)) };
  });

  const pct = (v: number, of: number) => `${(v / of) * 100}%`;

  export function scrollToLevel(i: number, smooth = true) {
    const el = scroller?.querySelector<HTMLElement>(`[data-level="${i}"]`);
    el?.scrollIntoView({ block: 'center', behavior: smooth ? 'smooth' : 'auto' });
  }

  onMount(() => {
    requestAnimationFrame(() => scrollToLevel(app.selected, false));
  });

  function statusClass(i: number) {
    if (isLocked(i)) return 'locked';
    return statusOf(i) ?? 'new';
  }
</script>

<div class="map" bind:this={scroller}>
  <div class="canvas" style:aspect-ratio={`${MAP_W} / ${MAP_H}`}>
    <svg viewBox={`0 0 ${MAP_W} ${MAP_H}`} preserveAspectRatio="xMidYMid meet" aria-hidden="true">
      <g class="swirls">
        {#each swirls as s}
          <path d={arc(s.x, s.y, s.r, s.a, 1.1)} />
          <path d={arc(s.x, s.y + 7, s.r * 0.7, s.a + 0.2, 0.8)} />
        {/each}
      </g>
      <g class="fish">
        {#each fish as f}
          <g transform={`translate(${f.x.toFixed(1)} ${f.y.toFixed(1)}) scale(${(f.s * f.d).toFixed(2)} ${f.s.toFixed(2)})`}>
            <ellipse rx="14" ry="5" />
            <path d="M -12 0 L -22 -7 L -22 7 Z" />
          </g>
        {/each}
      </g>
      <path class="channel wide" d={route} />
      <path class="channel" d={route} />

      {#each islandArt as s}
        <g class="island">
          <path d={s.halo} class="halo" />
          <path d={s.foam} class="foam" />
          <path d={s.shadow} class="shadow" />
          <path d={s.sand} class="sand" />
          <path d={s.grass} class="grass" />
          <path d={s.grass2} class="grass2" />
          {#each s.palms as p}
            <path d={p.trunk} class="trunk" />
            {#each p.leaves as l}<path d={l} class="leaf" />{/each}
            <circle cx={p.top.x - 4} cy={p.top.y + 4} r="4" class="coco" />
            <circle cx={p.top.x + 4} cy={p.top.y + 5} r="4" class="coco" />
          {/each}
          <text x={s.c.x} y={s.c.y + s.r * 0.12} font-size={s.r * 0.72} text-anchor="middle">{s.emoji}</text>
        </g>
      {/each}

      <path d={beach} class="beach-foam" transform="translate(0 -10)" />
      <path d={beach} class="beach" />

      {#each segs as sg, i}
        {#if i < front}
          <path d={sg.wake} class="wake-glow" />
          <path d={sg.wake} class="wake" />
        {:else}
          {#each sg.bubbles as b}<circle cx={b.x} cy={b.y} r="5" class="bubble" />{/each}
        {/if}
      {/each}
    </svg>

    {#each signs as sg (sg.index)}
      <button
        class="sign"
        style:left={pct(sg.c.x, MAP_W)}
        style:top={pct(sg.c.y, MAP_H)}
        style:--c={sg.stage.color}
        onclick={() => select(sg.index)}
        title={sg.stage.tagline}
      >
        <span class="sign-emoji" aria-hidden="true">{sg.stage.emoji}</span>
        <span class="sign-text"><small>{sg.stage.id}-bosqich</small>{sg.stage.name}</span>
      </button>
    {/each}

    {#each topics as t, i (i)}
      {@const cls = statusClass(i)}
      {@const solved = solvedCount(i)}
      <button
        data-level={i}
        class="node {cls}"
        class:selected={app.selected === i}
        class:current={cur === i}
        style:left={pct(nodes[i].x, MAP_W)}
        style:top={pct(nodes[i].y, MAP_H)}
        onclick={() => select(i)}
        aria-label={`${i + 1}-daraja: ${t.name}`}
        title={`${i + 1}. ${t.name}`}
      >
        <span class="rim"></span>
        <span class="face">
          {#if cls === 'locked'}
            <svg viewBox="0 0 24 24" class="lock" aria-hidden="true"><rect x="5" y="11" width="14" height="10" rx="2.5" /><path d="M8 11V8a4 4 0 0 1 8 0v3" /></svg>
          {:else}
            {i + 1}
          {/if}
        </span>
        {#if solved > 0}
          <svg class="solved" viewBox="0 0 64 64" aria-hidden="true">
            <circle cx="32" cy="32" r="30" pathLength="15" stroke-dasharray={`${solved} 15`} transform="rotate(-90 32 32)" />
          </svg>
        {/if}
        {#if cls === 'done'}
          <span class="stars" aria-hidden="true"><i>★</i><i>★</i><i>★</i></span>
        {:else if cls === 'practice'}
          <span class="badge" aria-hidden="true">↻</span>
        {/if}
      </button>
    {/each}

    <div
      class="ship"
      class:left={nodes[cur].x > MAP_W / 2}
      style:left={pct(nodes[cur].x + (nodes[cur].x > MAP_W / 2 ? -88 : 88), MAP_W)}
      style:top={pct(nodes[cur].y, MAP_H)}
      aria-hidden="true"
    >⛵</div>
  </div>
</div>

<style>
  .map {
    position: relative;
    height: 100vh;
    overflow-y: auto;
    overflow-x: hidden;
    background: var(--lagoon);
    scroll-behavior: smooth;
  }
  .canvas {
    position: relative;
    width: min(100%, 44rem);
    margin: 0 auto;
  }
  svg { display: block; width: 100%; height: 100%; }
  .canvas > svg { position: absolute; inset: 0; overflow: visible; }

  .swirls path { fill: none; stroke: rgb(255 255 255 / 0.3); stroke-width: 2.5; stroke-linecap: round; }
  .fish { fill: rgb(11 95 134 / 0.18); }
  .channel { fill: none; stroke: rgb(11 95 134 / 0.15); stroke-width: 70; stroke-linecap: round; stroke-linejoin: round; }
  .channel.wide { stroke: rgb(11 95 134 / 0.2); stroke-width: 120; }
  .halo { fill: rgb(128 227 242 / 0.33); }
  .foam { fill: none; stroke: rgb(255 255 255 / 0.85); stroke-width: 5; }
  .shadow { fill: var(--sand-2); }
  .sand { fill: var(--sand); }
  .grass { fill: #8cc152; }
  .grass2 { fill: #a0d468; }
  .trunk { fill: none; stroke: #9c6b3c; stroke-width: 7; stroke-linecap: round; }
  .leaf { fill: #5cb85c; stroke: #2e7d32; stroke-width: 1.2; }
  .coco { fill: #8d6e2f; }
  .beach { fill: var(--sand); }
  .beach-foam { fill: rgb(255 255 255 / 0.85); }
  .wake-glow { fill: none; stroke: rgb(255 224 138 / 0.45); stroke-width: 14; stroke-linecap: round; }
  .wake { fill: none; stroke: var(--gold); stroke-width: 6; stroke-linecap: round; }
  .bubble { fill: #fff; stroke: #7fd3ee; stroke-width: 2; }

  /* Stage signs */
  .sign {
    position: absolute;
    transform: translate(-50%, -50%) rotate(-2deg);
    display: flex; align-items: center; gap: 0.55rem;
    width: 11.5rem;
    padding: 0.45rem 0.8rem 0.45rem 0.6rem;
    border: 2.5px solid #7a4a22;
    border-radius: 0.9rem;
    background: #b57a45;
    color: #fff;
    text-align: left;
    box-shadow: 0 0.3rem 0 #7a4a22, 0 0.6rem 1rem rgb(6 50 74 / 0.25);
    transition: transform 0.15s;
  }
  .sign:nth-of-type(even) { transform: translate(-50%, -50%) rotate(2deg); }
  .sign:hover { transform: translate(-50%, -52%) rotate(0deg); }
  .sign-emoji { font-size: 1.4rem; }
  .sign-text { display: grid; font-size: 0.95rem; font-weight: 900; line-height: 1.15; min-width: 0; }
  .sign-text small { font-size: 0.75rem; font-weight: 800; color: #ffe3bf; }

  /* Level nodes: chunky 3D buttons */
  .node {
    --face: var(--coral); --light: #ff9a80; --rim: var(--coral-2);
    position: absolute;
    width: 3.7rem; height: 3.7rem;
    transform: translate(-50%, -50%);
    border: 0; padding: 0; background: none;
    border-radius: 50%;
  }
  .node.done { --face: var(--gold); --light: #ffdc7a; --rim: var(--gold-2); }
  .node.practice { --face: var(--teal); --light: #5ed3be; --rim: var(--teal-2); }
  .node.locked { --face: var(--stone); --light: #d5dce2; --rim: var(--stone-2); }
  .rim { position: absolute; inset: 0.4rem 0 -0.4rem; border-radius: 50%; background: var(--rim); box-shadow: 0 0.6rem 0.8rem rgb(6 50 74 / 0.25); }
  .face {
    position: absolute; inset: 0;
    display: grid; place-items: center;
    border-radius: 50%;
    border: 3px solid #fff;
    background: radial-gradient(circle at 32% 28%, var(--light), var(--face) 70%);
    color: #fff; font-weight: 900; font-size: 1.35rem;
    text-shadow: 0 2px 0 var(--rim);
    transition: transform 0.08s;
  }
  .node:hover .face { transform: translateY(-2px); }
  .node:active .face { transform: translateY(0.3rem); }
  .lock { width: 1.4rem; height: 1.4rem; fill: none; stroke: #fff; stroke-width: 2.4; stroke-linecap: round; }
  .solved { position: absolute; inset: -0.45rem; width: calc(100% + 0.9rem); height: calc(100% + 0.9rem); pointer-events: none; }
  .solved circle { fill: none; stroke: #fff; stroke-width: 4; stroke-linecap: round; }
  .node.selected::after {
    content: ''; position: absolute; inset: -0.75rem;
    border-radius: 50%;
    border: 3px dashed var(--deep);
    animation: spin 14s linear infinite;
    pointer-events: none;
  }
  .node.current:not(.locked)::before {
    content: ''; position: absolute; inset: 0;
    border-radius: 50%;
    box-shadow: 0 0 0 0 rgb(255 255 255 / 0.7);
    animation: pulse 1.8s ease-out infinite;
    pointer-events: none;
  }
  .stars { position: absolute; left: 50%; top: -1.35rem; transform: translateX(-50%); display: flex; gap: 0.05rem; pointer-events: none; }
  .stars i { font-style: normal; color: var(--gold); font-size: 1.05rem; text-shadow: 0 1.5px 0 #b36200; }
  .stars i:nth-child(2) { font-size: 1.35rem; transform: translateY(-0.3rem); }
  .badge {
    position: absolute; right: -0.35rem; top: -0.35rem;
    width: 1.5rem; height: 1.5rem; border-radius: 50%;
    display: grid; place-items: center;
    background: var(--coral); color: #fff; border: 2px solid #fff;
    font-size: 0.85rem; font-weight: 900;
  }

  .ship {
    position: absolute;
    transform: translate(-50%, -60%);
    font-size: 2.3rem;
    pointer-events: none;
    transition: left 0.9s cubic-bezier(0.6, 0, 0.3, 1), top 0.9s cubic-bezier(0.6, 0, 0.3, 1);
    animation: bob 2.4s ease-in-out infinite;
  }
  .ship.left { scale: -1 1; }

  @keyframes spin { to { rotate: 360deg; } }
  @keyframes pulse { to { box-shadow: 0 0 0 1.4rem rgb(255 255 255 / 0); } }
  @keyframes bob { 50% { translate: 0 -0.25rem; rotate: 3deg; } }
</style>
