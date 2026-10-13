<script lang="ts">
  import { topicById, sectionOf, neighbours, bandOf, KIND_LABEL, exTitle } from '../lib/course';
  import { app, topicProgress, markRead, save } from '../lib/store.svelte';
  import { nav, openTopic, go } from '../lib/nav.svelte';
  import Lesson from './Lesson.svelte';
  import ExQuiz from './ExQuiz.svelte';
  import ExCode from './ExCode.svelte';
  import ExLink from './ExLink.svelte';
  import Ring from './Ring.svelte';

  let { id, tab, ex }: { id: string; tab: 'dars' | 'mashq'; ex: number } = $props();

  const topic = $derived(topicById.get(id)!);
  const sec = $derived(sectionOf(id));
  const nb = $derived(neighbours(id));
  const prog = $derived(topicProgress(id));
  const band = $derived(bandOf(sec.num));
  const cur = $derived(topic.ex[Math.min(ex, topic.ex.length - 1)]);
  const headings = $derived(topic.blocks.map((b, i) => ({ b, i })).filter((x) => x.b.t === 'h') as { b: { t: 'h'; text: string }; i: number }[]);

  function setTab(t: 'dars' | 'mashq', i = ex) {
    nav.route = { name: 'topic', id, tab: t, ex: i };
    app.saved.last = { topic: id, tab: t, ex: i };
    document.querySelector('main')?.scrollTo({ top: 0 });
  }
  function setEx(i: number) {
    setTab('mashq', Math.max(0, Math.min(topic.ex.length - 1, i)));
  }
  function nextEx() {
    // Next unsolved exercise after this one; otherwise the next one.
    const n = topic.ex.length;
    for (let k = 1; k <= n; k++) {
      const j = (ex + k) % n;
      if (!app.saved.solved[topic.ex[j].id]) return setEx(j);
    }
    if (ex < n - 1) setEx(ex + 1);
  }
  function finishLesson() {
    markRead(id);
    setTab('mashq', topic.ex.findIndex((e) => !app.saved.solved[e.id]) >= 0 ? topic.ex.findIndex((e) => !app.saved.solved[e.id]) : 0);
  }
  function jump(i: number) {
    document.getElementById(`blk-${i}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function onKey(e: KeyboardEvent) {
    if (tab !== 'mashq') return;
    const t = e.target as HTMLElement;
    if (t.closest('input, textarea, .cm-editor')) return;
    if (e.key === 'ArrowRight' && !e.altKey) setEx(ex + 1);
    else if (e.key === 'ArrowLeft' && !e.altKey) setEx(ex - 1);
  }

  const ICON: Record<string, string> = { quiz: '?', func: 'ƒ', prog: '▤', link: '↗' };
  const allDone = $derived(prog.pct >= 1);
</script>

<svelte:window onkeydown={onKey} />

<div class="page">
  <header class="head">
    <div class="crumbs">
      <button onclick={() => go({ name: 'home' })}>Bosh sahifa</button><span>/</span>
      <span>{sec.emoji} {sec.num}-boʻlim · {sec.title}</span><span>/</span>
      <span class="here">{topic.id}</span>
    </div>
    <div class="title-row">
      <div class="tt">
        <h1>{topic.title}</h1>
        <p>{topic.short}</p>
        <div class="chips">
          <span class="band {band.tone}">{band.label}</span>
          <span class="chip">⏱ ~{topic.mins} daqiqa</span>
          <span class="chip">🎯 {topic.ex.length} mashq</span>
          {#if prog.read}<span class="chip ok">✓ Dars oʻqilgan</span>{/if}
        </div>
      </div>
      <div class="ring-box">
        <Ring pct={prog.pct} size="4.6rem" stroke={3}><b class="rp">{prog.done}<small>/{prog.total}</small></b></Ring>
      </div>
    </div>
    <div class="tabs" role="tablist">
      <button role="tab" aria-selected={tab === 'dars'} class:on={tab === 'dars'} onclick={() => setTab('dars')}>📖 Dars</button>
      <button role="tab" aria-selected={tab === 'mashq'} class:on={tab === 'mashq'} onclick={() => setTab('mashq')}>
        🎯 Mashqlar <span class="cnt">{prog.done}/{prog.total}</span>
      </button>
    </div>
  </header>

  {#if tab === 'dars'}
    <div class="lesson-grid">
      <div class="lesson-col">
        {#key topic.id}
          <Lesson {topic} />
        {/key}
        <div class="finish">
          <div>
            <b>{prog.read ? 'Dars oʻqilgan ✓' : 'Darsni tugatdingizmi?'}</b>
            <p>Endi bilimni mustahkamlash vaqti: {topic.ex.length} ta mashq — savollar, kod yozish va online masalalar.</p>
          </div>
          <button class="btn-primary" onclick={finishLesson}>{prog.read ? 'Mashqlarga oʻtish' : 'Tugatdim — mashqlarga'} →</button>
        </div>
      </div>
      <aside class="rail">
        <div class="rail-card">
          <h4>Bu darsda</h4>
          <ol>
            {#each headings as h}
              <li><button onclick={() => jump(h.i)}>{h.b.text}</button></li>
            {/each}
          </ol>
        </div>
        <div class="rail-card notes">
          <h4>📝 Mening qaydlarim</h4>
          <textarea
            rows="5"
            placeholder="Muhim fikrlar, savollar, eslatmalar… Faqat shu kompyuterda saqlanadi."
            value={app.saved.notes[id] ?? ''}
            oninput={(e) => {
              const v = (e.currentTarget as HTMLTextAreaElement).value;
              if (v.trim()) app.saved.notes[id] = v;
              else delete app.saved.notes[id];
              save();
            }}
          ></textarea>
          {#if app.saved.notes[id]}<small>✓ Saqlandi</small>{/if}
        </div>
        <div class="rail-card tipc">
          <h4>⌨️ Maslahat</h4>
          <p>Har bir kod blokini <b>oʻzgartirib</b>, <kbd>Ctrl</kbd>+<kbd>↵</kbd> bilan qayta ishga tushiring. Eng yaxshi oʻrganish — tajriba!</p>
        </div>
      </aside>
    </div>
  {:else}
    <div class="practice">
      <div class="tiles" role="tablist" aria-label="Mashqlar">
        {#each topic.ex as e, i}
          {@const done = !!app.saved.solved[e.id]}
          {@const tried = !done && (app.saved.attempts[e.id] ?? 0) > 0}
          <button class="tile {e.kind}" class:on={i === ex} class:done class:tried role="tab" aria-selected={i === ex}
            title={`${i + 1}. ${KIND_LABEL[e.kind]} — ${exTitle(e)}`} onclick={() => setEx(i)}>
            <span class="n">{i + 1}</span><span class="ic">{done ? '✓' : ICON[e.kind]}</span>
          </button>
        {/each}
      </div>
      <div class="legend">
        <span><i class="q"></i>Savol</span><span><i class="f"></i>Kod yozish</span><span><i class="l"></i>Online masala</span>
        <span class="sp"></span>
        <span class="nav-hint"><kbd>←</kbd> <kbd>→</kbd> mashqlar orasida</span>
      </div>

      {#if allDone}
        <div class="celebrate">
          <span class="big">🏆</span>
          <div><b>Mavzu toʻliq yakunlandi!</b><p>Barcha {topic.ex.length} ta mashq yechildi. Ajoyib natija!</p></div>
          {#if nb.next}<button class="btn-primary" onclick={() => openTopic(nb.next!.id)}>Keyingi mavzu: {nb.next.title} →</button>{/if}
        </div>
      {/if}

      <div class="ex-card">
        <div class="ex-top">
          <span class="ex-n">{ex + 1}<small>/{topic.ex.length}</small></span>
          <span class="ex-k">{KIND_LABEL[cur.kind]}</span>
          <span class="sp"></span>
          <button class="nb" onclick={() => setEx(ex - 1)} disabled={ex === 0} aria-label="Oldingi">‹</button>
          <button class="nb" onclick={() => setEx(ex + 1)} disabled={ex === topic.ex.length - 1} aria-label="Keyingi">›</button>
        </div>
        {#key cur.id}
          <div class="ex-body">
            {#if cur.kind === 'quiz'}
              <ExQuiz ex={cur} onNext={nextEx} />
            {:else if cur.kind === 'link'}
              <ExLink ex={cur} onNext={nextEx} />
            {:else}
              <ExCode ex={cur} onNext={nextEx} />
            {/if}
          </div>
        {/key}
      </div>
    </div>
  {/if}

  <footer class="pn">
    {#if nb.prev}
      <button onclick={() => openTopic(nb.prev!.id)}><small>← Oldingi mavzu</small><b>{nb.prev.title}</b></button>
    {:else}<span></span>{/if}
    {#if nb.next}
      <button class="r" onclick={() => openTopic(nb.next!.id)}><small>Keyingi mavzu →</small><b>{nb.next.title}</b></button>
    {/if}
  </footer>
</div>

<style>
  .page { display: grid; gap: 1.4rem; padding: 1.6rem clamp(1.5rem, 3vw, 3rem) 3rem; max-width: 96rem; margin: 0 auto; }
  .crumbs { display: flex; gap: 0.5rem; align-items: center; font-size: 0.85rem; color: var(--text-3); flex-wrap: wrap; }
  .crumbs button { border: 0; background: none; padding: 0; color: var(--text-3); }
  .crumbs button:hover { color: var(--text); }
  .here { color: var(--text-2); font-family: var(--mono); }
  .title-row { display: flex; justify-content: space-between; gap: 2rem; align-items: center; margin-top: 0.6rem; }
  .tt { display: grid; gap: 0.5rem; }
  h1 { margin: 0; font-family: var(--display); font-size: clamp(1.7rem, 2.6vw, 2.5rem); font-weight: 700; letter-spacing: -0.015em; line-height: 1.12; }
  .tt p { margin: 0; color: var(--text-2); font-size: 1.08rem; }
  .chips { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 0.3rem; }
  .chip { font-size: 0.8rem; padding: 0.28rem 0.7rem; border-radius: 2rem; border: 1px solid var(--line); color: var(--text-2); }
  .chip.ok { border-color: rgb(57 220 200 / 0.4); color: var(--turq); }
  .band { font-size: 0.78rem; font-weight: 700; padding: 0.28rem 0.7rem; border-radius: 2rem; }
  .band.turq { background: rgb(57 220 200 / 0.14); color: var(--turq); }
  .band.lapis { background: rgb(74 116 255 / 0.16); color: #8fb0ff; }
  .band.gold { background: rgb(247 189 70 / 0.15); color: var(--gold); }
  .band.rose { background: var(--rose-bg); color: var(--rose); }
  .rp { font-family: var(--display); font-size: 1.6rem; }
  .rp small { font-size: 0.75rem; color: var(--text-3); }
  .tabs { display: flex; gap: 0.3rem; margin-top: 1.2rem; border-bottom: 1px solid var(--line); }
  .tabs button {
    position: relative; border: 0; background: none; padding: 0.8rem 1.2rem; color: var(--text-3);
    font-weight: 600; font-size: 1rem; display: flex; align-items: center; gap: 0.5rem;
  }
  .tabs button:hover { color: var(--text); }
  .tabs button.on { color: var(--text); }
  .tabs button.on::after { content: ''; position: absolute; left: 0.6rem; right: 0.6rem; bottom: -1px; height: 3px; border-radius: 3px 3px 0 0; background: linear-gradient(90deg, var(--lapis), var(--turq)); }
  .cnt { font-size: 0.78rem; padding: 0.1rem 0.5rem; border-radius: 1rem; background: var(--surface-2); color: var(--text-2); font-variant-numeric: tabular-nums; }

  .lesson-grid { display: grid; grid-template-columns: minmax(0, 52rem) minmax(14rem, 17rem); gap: 2.5rem; justify-content: center; }
  .lesson-col { display: grid; gap: 2rem; align-content: start; min-width: 0; }
  .finish { display: flex; align-items: center; justify-content: space-between; gap: 1.5rem; padding: 1.4rem 1.6rem; border-radius: var(--r-l); background: linear-gradient(135deg, rgb(74 116 255 / 0.16), rgb(57 220 200 / 0.08)); border: 1px solid rgb(74 116 255 / 0.3); }
  .finish b { font-size: 1.1rem; }
  .finish p { margin: 0.3rem 0 0; color: var(--text-2); font-size: 0.95rem; line-height: 1.5; }
  .rail { position: sticky; top: 1.4rem; align-self: start; display: grid; gap: 1rem; }
  .rail-card { padding: 1.1rem 1.2rem; border-radius: var(--r-l); background: var(--surface); border: 1px solid var(--line); display: grid; gap: 0.6rem; }
  .rail-card h4 { margin: 0; font-size: 0.78rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-3); }
  .rail-card ol { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.15rem; counter-reset: h; }
  .rail-card li button { width: 100%; text-align: left; border: 0; background: none; padding: 0.35rem 0.5rem; border-radius: 0.45rem; color: var(--text-2); font-size: 0.9rem; line-height: 1.35; }
  .rail-card li button:hover { background: var(--surface-2); color: var(--text); }
  .notes textarea { width: 100%; resize: vertical; min-height: 6.5rem; padding: 0.6rem 0.7rem; border-radius: var(--r-s); border: 1px solid var(--line); background: var(--bg-2); color: var(--text); font: 0.9rem/1.5 var(--body, inherit); }
  .notes textarea:focus { outline: none; border-color: var(--lapis); box-shadow: 0 0 0 3px rgb(74 116 255 / 0.15); }
  .notes small { font-size: 0.75rem; color: var(--turq); }
  .tipc p { margin: 0; font-size: 0.88rem; color: var(--text-2); line-height: 1.55; }

  .practice { display: grid; gap: 1rem; }
  .tiles { display: grid; grid-template-columns: repeat(20, minmax(0, 1fr)); gap: 0.35rem; }
  .tile {
    display: grid; justify-items: center; gap: 0.05rem; padding: 0.45rem 0 0.4rem;
    border-radius: 0.6rem; border: 1px solid var(--line); background: var(--surface);
    color: var(--text-3); transition: transform 0.12s, border-color 0.12s;
    border-bottom: 3px solid var(--kc);
  }
  .tile.quiz { --kc: #8fb0ff; } .tile.func, .tile.prog { --kc: var(--gold); } .tile.link { --kc: #b48cff; }
  .tile:hover { transform: translateY(-2px); border-color: var(--line-2); border-bottom-color: var(--kc); }
  .tile .n { font-size: 0.68rem; font-weight: 600; }
  .tile .ic { font-size: 0.95rem; font-weight: 700; color: var(--text-2); line-height: 1.1; }
  .tile.done { background: var(--ok-bg); border-color: rgb(57 220 200 / 0.4); border-bottom-color: var(--turq); }
  .tile.done .ic { color: var(--turq); }
  .tile.tried { border-color: rgb(255 122 138 / 0.4); }
  .tile.on { border-color: var(--lapis); background: rgb(74 116 255 / 0.18); box-shadow: 0 0 0 3px rgb(74 116 255 / 0.2); color: var(--text); }
  .legend { display: flex; gap: 1.1rem; font-size: 0.8rem; color: var(--text-3); align-items: center; flex-wrap: wrap; }
  .legend i { display: inline-block; width: 0.8rem; height: 0.25rem; border-radius: 1rem; margin-right: 0.4rem; vertical-align: middle; }
  .legend .q { background: #8fb0ff; } .legend .f { background: var(--gold); } .legend .l { background: #b48cff; }
  .legend .sp, .ex-top .sp { flex: 1; }
  .celebrate { display: flex; align-items: center; gap: 1.1rem; padding: 1.1rem 1.4rem; border-radius: var(--r-l); background: linear-gradient(135deg, rgb(247 189 70 / 0.18), rgb(247 189 70 / 0.05)); border: 1px solid rgb(247 189 70 / 0.4); flex-wrap: wrap; }
  .celebrate .big { font-size: 2.2rem; }
  .celebrate div { flex: 1; min-width: 14rem; }
  .celebrate b { color: var(--gold); font-size: 1.08rem; }
  .celebrate p { margin: 0.2rem 0 0; color: var(--text-2); }
  .ex-card { border-radius: var(--r-l); background: var(--bg-2); border: 1px solid var(--line); overflow: hidden; }
  .ex-top { display: flex; align-items: center; gap: 0.8rem; padding: 0.7rem 1rem 0.7rem 1.4rem; border-bottom: 1px solid var(--line); background: var(--surface); }
  .ex-n { font-family: var(--display); font-weight: 700; font-size: 1.15rem; }
  .ex-n small { font-size: 0.75rem; color: var(--text-3); font-weight: 500; }
  .ex-k { font-size: 0.82rem; color: var(--text-3); }
  .nb { width: 2.2rem; height: 2.2rem; border-radius: 0.6rem; border: 1px solid var(--line); background: var(--surface-2); font-size: 1.3rem; line-height: 1; color: var(--text-2); }
  .nb:hover:not(:disabled) { border-color: var(--lapis); color: var(--text); }
  .nb:disabled { opacity: 0.35; cursor: default; }
  .ex-body { padding: 1.5rem 1.6rem 1.7rem; }

  .pn { display: flex; justify-content: space-between; gap: 1rem; padding-top: 1rem; border-top: 1px solid var(--line); }
  .pn button { display: grid; gap: 0.2rem; text-align: left; border: 1px solid var(--line); background: var(--surface); padding: 0.8rem 1.1rem; border-radius: var(--r-m); max-width: 48%; }
  .pn button:hover { border-color: var(--lapis); }
  .pn .r { text-align: right; margin-left: auto; }
  .pn small { color: var(--text-3); font-size: 0.8rem; }
  .pn b { font-weight: 600; }

  @media (max-width: 80em) {
    .lesson-grid { grid-template-columns: minmax(0, 1fr); }
    .rail { display: none; }
    .tiles { grid-template-columns: repeat(10, minmax(0, 1fr)); }
  }
</style>
