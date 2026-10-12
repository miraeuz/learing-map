<script lang="ts">
  import { onMount } from 'svelte';
  import { stages, stageStart, topics } from '../lib/data';
  import { app, totals, stageTotals, select, currentIndex, exportJson, importJson, activity } from '../lib/store.svelte';
  import { showToast } from '../lib/ui.svelte';
  import BrandMark from './BrandMark.svelte';
  import Ring from './Ring.svelte';

  let { onJump }: { onJump: (i: number) => void } = $props();

  const t = $derived(totals());
  const activeStage = $derived(topics[app.selected].stage);
  const perStage = $derived(stages.map((s) => stageTotals(s.id)));
  const act = $derived(activity());
  const weekMax = $derived(Math.max(1, ...act.week));
  const firstName = $derived(app.saved.name.trim().split(/\s+/)[0] ?? '');
  let fileInput: HTMLInputElement;

  // Full screen toggle (desktop app only).
  const winApi = typeof window !== 'undefined' ? window.icpc?.window : undefined;
  let fullscreen = $state(false);
  onMount(() => {
    if (!winApi) return;
    winApi.isFullscreen().then((v) => (fullscreen = v));
    return winApi.onFullscreen((v) => (fullscreen = v));
  });

  function goStage(id: number) {
    select(stageStart[id]);
    onJump(stageStart[id]);
  }

  function goCurrent() {
    const i = currentIndex();
    select(i);
    onJump(i);
  }

  function doExport() {
    const blob = new Blob([exportJson()], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `icpc-yoli-zaxira-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
    showToast('Zaxira nusxa saqlandi', 'teal');
  }

  async function doImport(e: Event) {
    const file = (e.target as HTMLInputElement).files?.[0];
    if (!file) return;
    const ok = importJson(await file.text());
    showToast(ok ? 'Natijalar tiklandi' : 'Fayl notoʻgʻri: ICPC yoʻli zaxira faylini tanlang', ok ? 'teal' : 'ink');
    (e.target as HTMLInputElement).value = '';
  }

  function doReset() {
    app.resetOpen = true;
  }
</script>

<aside class="side">
  <header class="brand">
    <BrandMark />
    <div class="brand-text">
      <h1>ICPC yoʻli</h1>
      {#if firstName}
        <button class="hello" onclick={() => (app.profileOpen = true)} title="Ismni oʻzgartirish">
          Salom, {firstName}
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h4L19 9l-4-4L4 16v4Zm10-14 4 4" /></svg>
        </button>
      {:else}
        <p>Asoslardan finalgacha</p>
      {/if}
    </div>
  </header>

  <section class="stats" aria-label="Umumiy natija">
    <div class="stats-top">
      <Ring value={t.done / t.levels} size="3.6rem" label={`${Math.round((t.done / t.levels) * 100)}%`} />
      <div class="label stats-head">
        <b>{t.done} / {t.levels}</b>
        <span>daraja oʻzlashtirildi</span>
      </div>
    </div>
    <dl class="label">
      <div><dd>{t.solved}</dd><dt>masala</dt></div>
      <div class:hot={act.streak > 0}><dd>{act.streak > 0 ? "🔥" : ""}{act.streak}</dd><dt title="Ketma-ket kunlar">seriya</dt></div>
      <div><dd>{act.today}</dd><dt>bugun</dt></div>
    </dl>
    <div class="label week" aria-label="Oxirgi 7 kunda yechilgan masalalar">
      {#each act.week as n, k}
        <span class:today={k === 6} style:height={`${Math.max(8, (n / weekMax) * 100)}%`} class:zero={n === 0} title={`${n} ta masala`}></span>
      {/each}
    </div>
  </section>

  <div class="quick">
    <button class="search" onclick={() => (app.searchOpen = true)} title="Mavzu qidirish (Ctrl+K)">
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" /><path d="m20 20-4-4" /></svg>
      <span class="label">Mavzu qidirish</span>
      <kbd class="label">Ctrl K</kbd>
    </button>
    <button class="current" onclick={goCurrent} title="Joriy darajaga oʻtish (C)">
      <span aria-hidden="true">⛵</span><span class="label">Joriy daraja: {currentIndex() + 1}</span>
    </button>
  </div>

  <nav class="stages" aria-label="Bosqichlar">
    {#each stages as s, i (s.id)}
      {@const st = perStage[i]}
      <button
        class="stage"
        class:active={activeStage === s.id}
        style:--c={s.color}
        onclick={() => goStage(s.id)}
        title={`${s.id}-bosqich: ${s.name}`}
      >
        <span class="emoji" aria-hidden="true">{st.done === st.total ? '⭐' : s.emoji}</span>
        <span class="label stage-body">
          <span class="stage-name">{s.name}</span>
          <span class="bar"><span style:width={`${(st.done / st.total) * 100}%`}></span></span>
        </span>
        <span class="label count">{st.done}/{st.total}</span>
      </button>
    {/each}
  </nav>

  <footer class="tools">
    <button onclick={doExport} title="Natijalarni faylga saqlash">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11m0 0-4-4m4 4 4-4M5 19h14" /></svg>
      <span class="label">Zaxira</span>
    </button>
    <button onclick={() => fileInput.click()} title="Zaxira fayldan tiklash">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 15V4m0 0L8 8m4-4 4 4M5 19h14" /></svg>
      <span class="label">Tiklash</span>
    </button>
    <button onclick={() => (app.helpOpen = true)} title="Tugmalar va yordam (?)">
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" /><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6v.6M12 17h.01" /></svg>
      <span class="label">Yordam</span>
    </button>
    {#if winApi}
      <button onclick={() => winApi.toggleFullscreen()} title="Toʻliq ekran (F11)">
        {#if fullscreen}
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 4v5H4M15 4v5h5M9 20v-5H4M15 20v-5h5" /></svg>
          <span class="label">Oyna</span>
        {:else}
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5" /></svg>
          <span class="label">Ekran</span>
        {/if}
      </button>
    {/if}
    <button onclick={doReset} title="Barcha natijalarni tozalash">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M9 7V4h6v3m-8 0 1 13h8l1-13" /></svg>
      <span class="label">Tozalash</span>
    </button>
    <input bind:this={fileInput} type="file" accept="application/json,.json" class="sr-only" onchange={doImport} />
  </footer>
</aside>

<style>
  .side {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    height: 100vh;
    padding: 1.25rem 1rem 1rem;
    background: var(--paper);
    border-right: 2px solid var(--sand);
    overflow: hidden;
  }

  .brand { display: flex; align-items: center; gap: 0.75rem; padding: 0 0.25rem; }
  h1 { margin: 0; font-size: 1.35rem; font-weight: 900; line-height: 1.1; letter-spacing: -0.01em; }
  .brand p { margin: 0.1rem 0 0; font-size: 0.82rem; color: var(--ink-2); font-weight: 700; }

  .stats {
    display: grid;
    gap: 0.75rem;
    padding: 0.9rem;
    background: #fff;
    border: 1.5px solid var(--line);
    border-radius: var(--radius-l);
  }
  .stats-top { display: flex; align-items: center; gap: 0.8rem; }
  .stats-head { display: grid; line-height: 1.2; }
  .stats-head b { font-size: 1.2rem; font-weight: 900; font-variant-numeric: tabular-nums; }
  .stats-head span { font-size: 0.82rem; color: var(--ink-2); }
  dl { margin: 0; display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.4rem; }
  dl div.hot { background: #fff1e0; }
  .week { display: grid; grid-template-columns: repeat(7, 1fr); gap: 0.25rem; align-items: end; height: 1.6rem; }
  .week span { display: block; border-radius: 0.25rem; background: var(--teal); }
  .week span.zero { background: var(--paper-2); }
  .week span.today { box-shadow: inset 0 0 0 2px var(--teal-2); }
  .hello {
    display: inline-flex; align-items: center; gap: 0.3rem;
    margin-top: 0.1rem; padding: 0; border: 0; background: none;
    font-size: 0.85rem; font-weight: 800; color: var(--ink-2);
  }
  .hello svg { width: 0.85rem; height: 0.85rem; fill: none; stroke: currentColor; stroke-width: 2.2; stroke-linejoin: round; opacity: 0; transition: opacity 0.15s; }
  .hello:hover { color: var(--ink); }
  .hello:hover svg { opacity: 1; }
  dl div { padding: 0.45rem 0.5rem; border-radius: var(--radius-s); background: var(--paper); min-width: 0; }
  dd { margin: 0; font-weight: 900; font-size: 1.1rem; font-variant-numeric: tabular-nums; }
  dt { font-size: 0.72rem; color: var(--ink-2); font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

  .quick { display: grid; gap: 0.5rem; }
  .quick button {
    display: flex; align-items: center; gap: 0.6rem;
    width: 100%; padding: 0.65rem 0.8rem;
    border-radius: var(--radius-m);
    border: 1.5px solid var(--line);
    background: #fff;
    text-align: left;
    font-weight: 800;
    font-size: 0.92rem;
  }
  .quick button:hover { border-color: var(--sand-2); }
  .search svg { width: 1.1rem; height: 1.1rem; fill: none; stroke: var(--ink-2); stroke-width: 2.4; stroke-linecap: round; flex: none; }
  .search span { flex: 1; color: var(--ink-2); }
  .current { background: var(--deep) !important; border-color: var(--deep) !important; color: #fff; }
  .current:hover { filter: brightness(1.1); }

  .stages {
    flex: 1;
    min-height: 0;
    overflow-y: auto;
    display: grid;
    align-content: start;
    gap: 0.3rem;
    margin: 0 -0.25rem;
    padding: 0 0.25rem;
  }
  .stage {
    display: grid;
    grid-template-columns: 2rem 1fr auto;
    align-items: center;
    gap: 0.6rem;
    padding: 0.55rem 0.65rem;
    border: 0;
    border-radius: var(--radius-m);
    background: transparent;
    text-align: left;
  }
  .stage:hover { background: var(--paper-2); }
  .stage.active { background: var(--c); color: #fff; }
  .emoji { font-size: 1.3rem; text-align: center; }
  .stage-body { display: grid; gap: 0.3rem; min-width: 0; }
  .stage-name { font-size: 0.92rem; font-weight: 800; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .bar { height: 0.32rem; border-radius: 1rem; background: var(--paper-2); overflow: hidden; }
  .bar span { display: block; height: 100%; background: var(--c); border-radius: inherit; transition: width 0.5s; }
  .stage.active .bar { background: rgb(255 255 255 / 0.3); }
  .stage.active .bar span { background: #fff; }
  .count { font-size: 0.78rem; font-weight: 800; color: var(--ink-2); font-variant-numeric: tabular-nums; }
  .stage.active .count { color: rgb(255 255 255 / 0.9); }

  .tools { display: grid; grid-template-columns: repeat(auto-fit, minmax(3.4rem, 1fr)); gap: 0.3rem; }
  .tools button {
    display: grid; justify-items: center; gap: 0.2rem;
    padding: 0.5rem 0.2rem;
    border: 0; border-radius: var(--radius-s);
    background: transparent;
    font-size: 0.72rem; font-weight: 800; color: var(--ink-2);
  }
  .tools button:hover { background: var(--paper-2); color: var(--ink); }
  .tools svg { width: 1.25rem; height: 1.25rem; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }

  /* Rail: medium windows keep only icons */
  @media (max-width: 75em) {
    .side { padding: 1rem 0.6rem; align-items: center; }
    .label, .brand-text { display: none !important; }
    .stats { padding: 0.4rem; border: 0; background: transparent; }
    .quick button { justify-content: center; padding: 0.6rem; }
    .stage { grid-template-columns: 1fr; padding: 0.45rem; }
    .tools { grid-template-columns: 1fr; }
  }
</style>
