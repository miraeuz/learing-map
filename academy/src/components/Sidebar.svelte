<script lang="ts">
  import { untrack } from 'svelte';
  import { sections, sectionOf } from '../lib/course';
  import { app, topicProgress, levelOf } from '../lib/store.svelte';
  import { nav, go, openTopic } from '../lib/nav.svelte';
  import BrandMark from './BrandMark.svelte';
  import Ring from './Ring.svelte';

  let { onSearch }: { onSearch: () => void } = $props();

  const current = $derived(nav.route.name === 'topic' ? nav.route.id : null);
  let open = $state<Record<number, boolean>>({});
  // Open the section that holds the current topic.
  // Accordion: navigating to a topic opens its section, closes the others and reveals the topic.
  $effect(() => {
    if (!current) return;
    const num = sectionOf(current).num;
    untrack(() => {
      for (const k of Object.keys(open)) if (Number(k) !== num) open[Number(k)] = false;
      open[num] = true;
    });
    requestAnimationFrame(() => document.querySelector('.tree .topic.on')?.scrollIntoView({ block: 'nearest' }));
  });
  {
    const last = untrack(() => app.saved.last?.topic);
    open[last ? sectionOf(last).num : sections[0].num] = true;
  }

  function secPct(num: number) {
    const s = sections.find((x) => x.num === num)!;
    let d = 0, t = 0;
    for (const tp of s.topics) {
      const p = topicProgress(tp.id);
      d += p.done;
      t += p.total;
    }
    return t ? d / t : 0;
  }

  const lv = $derived(levelOf(app.saved.xp));
  const initials = $derived(
    (app.saved.name || 'M').split(' ').filter(Boolean).slice(0, 2).map((w) => w[0]?.toUpperCase()).join(''),
  );
  const items = [
    { name: 'home', label: 'Bosh sahifa', icon: 'M3 11.5 12 4l9 7.5V20a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z' },
    { name: 'playground', label: 'Kod maydoni', icon: 'M8 7 3 12l5 5M16 7l5 5-5 5M14 4l-4 16' },
    { name: 'exams', label: 'Imtihonlar', icon: 'M9 4h6l1 2h3v15H5V6h3zM9 12l2 2 4-4' },
    { name: 'settings', label: 'Sozlamalar', icon: 'M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zM19.4 13a7.6 7.6 0 0 0 0-2l2-1.6-2-3.4-2.4 1a7.4 7.4 0 0 0-1.7-1L15 3.5h-4l-.4 2.5a7.4 7.4 0 0 0-1.7 1l-2.4-1-2 3.4L4.6 11a7.6 7.6 0 0 0 0 2l-2 1.6 2 3.4 2.4-1a7.4 7.4 0 0 0 1.7 1l.3 2.5h4l.4-2.5a7.4 7.4 0 0 0 1.7-1l2.4 1 2-3.4z' },
  ] as const;
  const active = (n: string) => nav.route.name === n || (n === 'exams' && nav.route.name === 'exam');
</script>

<aside class="side">
  <button class="brand" onclick={() => go({ name: 'home' })} title="Bosh sahifa">
    <BrandMark size="2.2rem" />
    <span class="bt">Mirae <b>Academy</b></span>
  </button>

  <button class="search" onclick={onSearch}>
    <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5" /><path d="m16 16 4.5 4.5" /></svg>
    <span>Mavzu qidirish…</span>
    <kbd>Ctrl K</kbd>
  </button>

  <nav class="main-nav" aria-label="Asosiy">
    {#each items as it}
      <button class:on={active(it.name)} onclick={() => go({ name: it.name } as any)}>
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d={it.icon} /></svg>
        {it.label}
      </button>
    {/each}
  </nav>

  <div class="label">Kurs</div>
  <nav class="tree" aria-label="Kurs mavzulari">
    {#each sections as s}
      {@const pct = secPct(s.num)}
      <div class="sec" class:open={open[s.num]}>
        <button class="sec-head" aria-expanded={!!open[s.num]} onclick={() => (open[s.num] = !open[s.num])}>
          <span class="emo" aria-hidden="true">{s.emoji}</span>
          <span class="st"><small>{s.num}-boʻlim</small>{s.title}</span>
          <Ring {pct} size="1.55rem" tone="lapis"><span class="pct">{Math.round(pct * 100)}</span></Ring>
        </button>
        {#if open[s.num]}
          <ul>
            {#each s.topics as t}
              {@const p = topicProgress(t.id)}
              <li>
                <button class="topic" class:on={current === t.id} onclick={() => openTopic(t.id)}>
                  <span class="dot" class:read={p.read} class:full={p.pct >= 1}>
                    {#if p.pct >= 1}✓{:else}{t.id.split('.')[1]}{/if}
                  </span>
                  <span class="tt">{t.title}</span>
                  {#if p.done > 0 && p.pct < 1}<span class="cnt">{p.done}/{p.total}</span>{/if}
                </button>
              </li>
            {/each}
          </ul>
        {/if}
      </div>
    {/each}
  </nav>

  <button class="me" onclick={() => go({ name: 'settings' })} title="Profil va sozlamalar">
    <span class="av">{initials}</span>
    <span class="who">
      <b>{app.saved.name || 'Oʻquvchi'}</b>
      <small>{lv.level}-daraja · {lv.rank}</small>
      <span class="xpbar"><i style:width={`${(lv.into / lv.need) * 100}%`}></i></span>
    </span>
  </button>
</aside>

<style>
  .side {
    display: flex; flex-direction: column; gap: 0.7rem;
    height: 100vh; padding: 1rem 0.8rem 0.8rem;
    background: linear-gradient(180deg, var(--bg-2), var(--bg));
    border-right: 1px solid var(--line);
    overflow: hidden;
  }
  button { border: 0; background: none; text-align: left; }
  .brand { display: flex; align-items: center; gap: 0.7rem; padding: 0.2rem 0.5rem 0.5rem; }
  .bt { font-family: var(--display); font-size: 1.02rem; font-weight: 500; letter-spacing: 0.01em; }
  .bt b { color: var(--gold); font-weight: 700; }

  .search {
    display: flex; align-items: center; gap: 0.6rem;
    padding: 0.6rem 0.7rem; border-radius: var(--r-s);
    border: 1px solid var(--line); background: var(--surface); color: var(--text-3);
    font-size: 0.9rem;
  }
  .search:hover { border-color: var(--line-2); color: var(--text-2); }
  .search svg { width: 1.05rem; height: 1.05rem; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; }
  .search span { flex: 1; }

  .main-nav { display: grid; gap: 0.15rem; }
  .main-nav button {
    display: flex; align-items: center; gap: 0.75rem;
    padding: 0.58rem 0.7rem; border-radius: var(--r-s);
    color: var(--text-2); font-weight: 500;
    transition: background 0.15s, color 0.15s;
  }
  .main-nav button:hover { background: var(--surface); color: var(--text); }
  .main-nav button.on { background: linear-gradient(90deg, rgb(74 116 255 / 0.22), rgb(74 116 255 / 0.04)); color: var(--text); box-shadow: inset 2px 0 0 var(--lapis); }
  .main-nav svg { width: 1.15rem; height: 1.15rem; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }

  .label { margin: 0.4rem 0.7rem -0.2rem; font-size: 0.72rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-3); }
  .tree { flex: 1; overflow-y: auto; overflow-x: hidden; margin: 0 -0.3rem; padding: 0 0.3rem; display: grid; grid-template-columns: minmax(0, 1fr); align-content: start; gap: 0.25rem; }
  .sec { min-width: 0; }
  .sec-head {
    width: 100%; display: flex; align-items: center; gap: 0.65rem;
    padding: 0.55rem 0.6rem; border-radius: var(--r-s);
  }
  .sec-head:hover { background: var(--surface); }
  .sec.open .sec-head { background: var(--surface); }
  .emo { font-size: 1.15rem; width: 1.6rem; text-align: center; }
  .st { flex: 1; min-width: 0; display: grid; font-weight: 600; font-size: 0.92rem; line-height: 1.25; }
  .st small { font-size: 0.72rem; color: var(--text-3); font-weight: 500; }
  .pct { font-size: 0.82rem; color: var(--text-2); }
  ul { list-style: none; margin: 0.15rem 0 0.4rem; padding: 0 0 0 1.05rem; border-left: 1px solid var(--line); margin-left: 1.35rem; }
  .topic {
    width: 100%; display: flex; align-items: center; gap: 0.55rem;
    padding: 0.38rem 0.5rem; border-radius: 0.5rem;
    color: var(--text-2); font-size: 0.88rem;
  }
  .topic:hover { background: var(--surface); color: var(--text); }
  .topic.on { background: rgb(74 116 255 / 0.18); color: var(--text); }
  .dot {
    flex: none; display: grid; place-items: center; width: 1.35rem; height: 1.35rem; border-radius: 0.4rem;
    border: 1px solid var(--line-2); font-size: 0.7rem; font-weight: 700; color: var(--text-3);
  }
  .dot.read { border-color: var(--turq); color: var(--turq); }
  .dot.full { background: var(--gold); border-color: var(--gold); color: #3a2600; }
  .tt { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .cnt { font-size: 0.72rem; color: var(--text-3); font-variant-numeric: tabular-nums; }

  .me {
    display: flex; align-items: center; gap: 0.7rem;
    padding: 0.65rem; border-radius: var(--r-m);
    background: var(--surface); border: 1px solid var(--line);
  }
  .me:hover { border-color: var(--line-2); }
  .av {
    flex: none; display: grid; place-items: center; width: 2.4rem; height: 2.4rem; border-radius: 0.8rem;
    background: linear-gradient(135deg, var(--lapis), var(--turq-2)); color: #fff;
    font-family: var(--display); font-weight: 700; font-size: 0.9rem;
  }
  .who { flex: 1; min-width: 0; display: grid; gap: 0.1rem; }
  .who b { font-size: 0.92rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .who small { font-size: 0.76rem; color: var(--text-3); }
  .xpbar { height: 0.3rem; margin-top: 0.25rem; border-radius: 1rem; background: var(--line); overflow: hidden; }
  .xpbar i { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, var(--gold-2), var(--gold)); transition: width 0.6s; }
</style>
