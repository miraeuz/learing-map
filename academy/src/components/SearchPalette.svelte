<script lang="ts">
  import { allTopics, sectionOf, plain } from '../lib/course';
  import { topicProgress } from '../lib/store.svelte';
  import { openTopic, go } from '../lib/nav.svelte';

  let { onClose }: { onClose: () => void } = $props();
  let q = $state('');
  let sel = $state(0);
  let input: HTMLInputElement;
  $effect(() => { input?.focus(); });

  const norm = (s: string) => s.toLowerCase().replace(/[ʻʼ'`‘’]/g, '');
  // Search titles, summaries and the lesson text (headings and paragraphs).
  const index = allTopics.map((t) => ({
    t,
    head: norm(`${t.id} ${t.title} ${t.short}`),
    body: norm(t.blocks.map((b) => (b.t === 'h' ? b.text : b.t === 'p' || b.t === 'tip' || b.t === 'warn' ? plain(b.html) : b.t === 'code' ? b.code : '')).join(' ')),
  }));
  const pages = [
    { label: '🏠 Bosh sahifa', run: () => go({ name: 'home' }) },
    { label: '⌨ Kod maydoni', run: () => go({ name: 'playground' }) },
    { label: '📝 Imtihonlar', run: () => go({ name: 'exams' }) },
    { label: '⚙ Sozlamalar', run: () => go({ name: 'settings' }) },
  ];

  const results = $derived.by(() => {
    const s = norm(q.trim());
    if (!s) return index.slice(0, 8).map((x) => ({ t: x.t, where: '' }));
    const words = s.split(/\s+/);
    return index
      .map((x) => {
        const inHead = words.every((w) => x.head.includes(w));
        const inBody = !inHead && words.every((w) => x.head.includes(w) || x.body.includes(w));
        return { x, score: inHead ? 2 : inBody ? 1 : 0 };
      })
      .filter((r) => r.score)
      .sort((a, b) => b.score - a.score)
      .slice(0, 10)
      .map((r) => ({ t: r.x.t, where: r.score === 1 ? 'dars matnida' : '' }));
  });
  $effect(() => { void q; sel = 0; });

  function choose(i: number) {
    const r = results[i];
    if (!r) return;
    onClose();
    openTopic(r.t.id);
  }

  function onKey(e: KeyboardEvent) {
    if (e.key === 'Escape') onClose();
    else if (e.key === 'ArrowDown') { sel = Math.min(results.length - 1, sel + 1); e.preventDefault(); }
    else if (e.key === 'ArrowUp') { sel = Math.max(0, sel - 1); e.preventDefault(); }
    else if (e.key === 'Enter') choose(sel);
  }
</script>

<!-- svelte-ignore a11y_click_events_have_key_events -->
<!-- svelte-ignore a11y_no_static_element_interactions -->
<div class="scrim" onclick={(e) => e.target === e.currentTarget && onClose()}>
  <div class="pal" role="dialog" aria-modal="true" aria-label="Qidiruv">
    <div class="in">
      <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5" /><path d="m16 16 4.5 4.5" /></svg>
      <input bind:this={input} bind:value={q} onkeydown={onKey} placeholder="Mavzu, tushuncha yoki funksiya: lugʻat, try, append…" />
      <kbd>Esc</kbd>
    </div>
    {#if !q.trim()}
      <div class="pages">{#each pages as p}<button onclick={() => { onClose(); p.run(); }}>{p.label}</button>{/each}</div>
    {/if}
    <ul>
      {#each results as r, i}
        {@const s = sectionOf(r.t.id)}
        {@const p = topicProgress(r.t.id)}
        <li>
          <button class:on={i === sel} onmouseenter={() => (sel = i)} onclick={() => choose(i)}>
            <span class="id">{r.t.id}</span>
            <span class="tx"><b>{r.t.title}</b><small>{s.emoji} {s.title}{r.where ? ` · ${r.where}` : ''}</small></span>
            <span class="pr">{p.done}/{p.total}</span>
          </button>
        </li>
      {:else}
        <li class="none">Hech narsa topilmadi</li>
      {/each}
    </ul>
  </div>
</div>

<style>
  .scrim { position: fixed; inset: 0; z-index: 60; background: var(--scrim); backdrop-filter: blur(6px); display: grid; justify-items: center; align-items: start; padding-top: 12vh; animation: fade 0.15s; }
  @keyframes fade { from { opacity: 0; } }
  .pal { width: min(40rem, 92vw); border-radius: var(--r-l); background: var(--surface); border: 1px solid var(--line-2); box-shadow: 0 2rem 5rem rgb(0 0 0 / 0.5); overflow: hidden; animation: drop 0.2s cubic-bezier(0.2, 1, 0.3, 1); }
  @keyframes drop { from { transform: translateY(-0.8rem); opacity: 0; } }
  .in { display: flex; align-items: center; gap: 0.7rem; padding: 0.9rem 1.1rem; border-bottom: 1px solid var(--line); }
  .in svg { width: 1.2rem; height: 1.2rem; fill: none; stroke: var(--text-3); stroke-width: 2; stroke-linecap: round; }
  .in input { flex: 1; border: 0; background: none; font-size: 1.08rem; }
  .in input:focus { outline: none; }
  .pages { display: flex; gap: 0.4rem; padding: 0.7rem 1rem 0; flex-wrap: wrap; }
  .pages button { padding: 0.35rem 0.75rem; border-radius: 2rem; border: 1px solid var(--line); background: var(--bg-2); font-size: 0.85rem; color: var(--text-2); }
  .pages button:hover { border-color: var(--lapis); color: var(--text); }
  ul { list-style: none; margin: 0; padding: 0.5rem; max-height: 55vh; overflow: auto; }
  li button { width: 100%; display: flex; align-items: center; gap: 0.9rem; padding: 0.6rem 0.8rem; border-radius: var(--r-s); border: 0; background: none; text-align: left; }
  li button.on { background: rgb(74 116 255 / 0.16); }
  .id { font: 0.8rem var(--mono); color: var(--text-3); width: 2.6rem; }
  .tx { flex: 1; display: grid; }
  .tx b { font-weight: 600; }
  .tx small { color: var(--text-3); font-size: 0.8rem; }
  .pr { font-size: 0.78rem; color: var(--text-3); font-variant-numeric: tabular-nums; }
  .none { padding: 1.5rem; text-align: center; color: var(--text-3); }
</style>
