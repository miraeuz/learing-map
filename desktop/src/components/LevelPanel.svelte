<script lang="ts">
  import { topics, stages, siteOf } from '../lib/data';
  import { app, statusOf, isLocked, isSolved, solvedCount, toggleSolved, answer, clearAnswer, setNote, select } from '../lib/store.svelte';
  import { burst, showToast } from '../lib/ui.svelte';

  let { onJump }: { onJump: (i: number) => void } = $props();

  const i = $derived(app.selected);
  const topic = $derived(topics[i]);
  const stage = $derived(stages[topic.stage]);
  const status = $derived(statusOf(i));
  const locked = $derived(isLocked(i));
  const solved = $derived(solvedCount(i));
  const total = $derived(topic.links.length);
  let filter = $state<'all' | 'open'>('all');
  const shown = $derived(
    topic.links.map((l, k) => ({ l, k })).filter(({ l }) => filter === 'all' || !isSolved(l.url)),
  );

  let noteText = $state('');
  let noteFor = -1;
  $effect(() => {
    if (noteFor !== i) {
      noteFor = i;
      noteText = app.saved.notes[i] ?? '';
    }
  });

  function go(delta: number) {
    const n = Math.max(0, Math.min(topics.length - 1, i + delta));
    select(n);
    onJump(n);
  }

  export function respond(ok: boolean, ev?: MouseEvent) {
    if (locked) return;
    answer(i, ok);
    if (ok) {
      const x = ev?.clientX ?? window.innerWidth - 200;
      const y = ev?.clientY ?? window.innerHeight - 80;
      burst(x, y);
      showToast(`${i + 1}-daraja oʻzlashtirildi ⭐`, 'gold');
    } else {
      showToast(`${i + 1}-daraja mashq roʻyxatiga qoʻshildi`, 'teal');
    }
    if (i < topics.length - 1) {
      setTimeout(() => go(1), 450);
    }
  }

  const statusText = $derived(
    locked ? 'Yopiq' : status === 'done' ? 'Oʻzlashtirilgan' : status === 'practice' ? 'Mashq kerak' : 'Yangi',
  );
</script>

<section class="panel" style:--c={stage.color} aria-label="Daraja tafsilotlari">
  <header class="head">
    <div class="nav">
      <button class="icon" onclick={() => go(-1)} disabled={i === 0} title="Oldingi daraja (←)" aria-label="Oldingi daraja">
        <svg viewBox="0 0 24 24"><path d="m15 5-7 7 7 7" /></svg>
      </button>
      <span class="crumb">{stage.emoji} {stage.id}-bosqich: {stage.name}</span>
      <button class="icon" onclick={() => go(1)} disabled={i === topics.length - 1} title="Keyingi daraja (→)" aria-label="Keyingi daraja">
        <svg viewBox="0 0 24 24"><path d="m9 5 7 7-7 7" /></svg>
      </button>
      <button class="icon close" onclick={() => (app.panelOpen = false)} title="Yopish (Esc)" aria-label="Panelni yopish">
        <svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18" /></svg>
      </button>
    </div>
    <h2>{topic.name}</h2>
    <div class="chips">
      <span class="chip level">{i + 1}-daraja</span>
      <span class="chip status {locked ? 'locked' : (status ?? 'new')}">{statusText}</span>
    </div>
  </header>

  <div class="body">
    <section>
      <h3>Nimani oʻrganish kerak</h3>
      <p class="info">{topic.info}</p>
    </section>

    <section class="progress">
      <div class="progress-head">
        <h3>Masalalar</h3>
        <span class="count"><b>{solved}</b>/{total} yechildi</span>
      </div>
      <div class="meter" role="progressbar" aria-valuemin="0" aria-valuemax={total} aria-valuenow={solved}>
        <span style:width={`${(solved / total) * 100}%`}></span>
        <i style:left={`${(10 / total) * 100}%`} title="10 ta masaladan keyin bu mavzu odatda oʻzlashtirilgan boʻladi"></i>
      </div>
      <div class="filters" role="group" aria-label="Filtr">
        <button class:on={filter === 'all'} onclick={() => (filter = 'all')}>Hammasi</button>
        <button class:on={filter === 'open'} onclick={() => (filter = 'open')}>Yechilmagan ({total - solved})</button>
      </div>

      <ul class="list">
        {#each shown as { l } (l.url)}
          {@const site = siteOf(l.site)}
          {@const done = isSolved(l.url)}
          <li class:done>
            <label class="check" title={done ? 'Belgini olib tashlash' : 'Yechildi deb belgilash'}>
              <input type="checkbox" checked={done} onchange={() => toggleSolved(l.url)} aria-label={`${l.title} — yechildi`} />
              <span class="box"><svg viewBox="0 0 24 24"><path d="m5 12.5 4.5 4.5L19 7.5" /></svg></span>
            </label>
            <span class="badge" style:background={site.color}>{site.badge}</span>
            <a href={l.url} target="_blank" rel="noopener noreferrer" class="title">
              <span class="t">{l.title.replace(/^Nazariya: /, '')}</span>
              <span class="s">{l.title.startsWith('Nazariya: ') ? 'Nazariya, cp-algorithms' : site.name}</span>
            </a>
            <svg class="ext" viewBox="0 0 24 24" aria-hidden="true"><path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5" /></svg>
          </li>
        {:else}
          <li class="empty">Hammasi yechildi. Endi "Ha, bilaman" ni bosing.</li>
        {/each}
      </ul>
    </section>

    <section>
      <h3><label for="note">Eslatmalar</label></h3>
      <textarea
        id="note"
        rows="3"
        placeholder="Masalan: segment tree shablonimda lazy push xatosi bor edi…"
        bind:value={noteText}
        oninput={() => setNote(i, noteText)}
      ></textarea>
    </section>
  </div>

  <footer class="answer">
    {#if locked}
      <p class="locked-msg">Bu darajani ochish uchun avval {i}-darajaga javob bering.</p>
    {:else if status}
      <p class="answered">
        {status === 'done' ? '⭐ Siz bu mavzuni oʻzlashtirdingiz.' : '↻ Bu mavzu mashq roʻyxatida.'}
        <button class="link" onclick={() => { clearAnswer(i); showToast('Javob bekor qilindi', 'ink'); }}>Javobni bekor qilish</button>
      </p>
      <div class="buttons">
        <button class="push soft" onclick={(e) => respond(false, e)}>Hali yoʻq <kbd>N</kbd></button>
        <button class="push primary" onclick={(e) => respond(true, e)}>Ha, bilaman <kbd>Y</kbd></button>
      </div>
    {:else}
      <p class="q">Buni kontestda yoddan, xatosiz yoza olasizmi?</p>
      <div class="buttons">
        <button class="push soft" onclick={(e) => respond(false, e)}>Hali yoʻq <kbd>N</kbd></button>
        <button class="push primary" onclick={(e) => respond(true, e)}>Ha, bilaman <kbd>Y</kbd></button>
      </div>
    {/if}
  </footer>
</section>

<style>
  .panel {
    display: grid;
    grid-template-rows: auto 1fr auto;
    height: 100vh;
    background: var(--paper);
    border-left: 2px solid var(--sand);
    min-width: 0;
  }

  .head { background: var(--c); color: #fff; padding: 0.9rem 1.25rem 1.1rem; }
  .nav { display: flex; align-items: center; gap: 0.25rem; margin: 0 -0.5rem 0.4rem; }
  .crumb { flex: 1; text-align: center; font-size: 0.85rem; font-weight: 800; opacity: 0.92; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .icon {
    display: grid; place-items: center;
    width: 2.2rem; height: 2.2rem;
    border: 0; border-radius: 50%;
    background: rgb(255 255 255 / 0.16);
    color: #fff;
  }
  .icon:hover:not(:disabled) { background: rgb(255 255 255 / 0.3); }
  .icon:disabled { opacity: 0.35; cursor: default; }
  .icon svg { width: 1.2rem; height: 1.2rem; fill: none; stroke: currentColor; stroke-width: 2.6; stroke-linecap: round; stroke-linejoin: round; }
  .close { display: none; }
  h2 { margin: 0.2rem 0 0.6rem; font-size: 1.65rem; font-weight: 900; line-height: 1.12; letter-spacing: -0.01em; }
  .chips { display: flex; gap: 0.4rem; flex-wrap: wrap; }
  .chip { padding: 0.2rem 0.7rem; border-radius: 1rem; font-size: 0.8rem; font-weight: 800; }
  .chip.level { background: #fff; color: var(--c); }
  .chip.status { background: rgb(0 0 0 / 0.18); color: #fff; }
  .chip.status.done { background: var(--gold); color: var(--ink); }
  .chip.status.practice { background: var(--teal-2); }
  .chip.status.new { background: var(--coral-2); }

  .body { overflow-y: auto; padding: 1.1rem 1.25rem 1.25rem; display: grid; align-content: start; gap: 1.4rem; }
  h3 { margin: 0 0 0.45rem; font-size: 1rem; font-weight: 900; }
  .info { margin: 0; font-size: 1.02rem; line-height: 1.55; font-weight: 600; max-width: 38rem; }

  .progress-head { display: flex; justify-content: space-between; align-items: baseline; }
  .count { font-size: 0.9rem; color: var(--ink-2); font-variant-numeric: tabular-nums; }
  .count b { color: var(--ink); font-weight: 900; font-size: 1.05rem; }
  .meter { position: relative; height: 0.6rem; margin: 0.2rem 0 0.75rem; border-radius: 1rem; background: var(--paper-2); }
  .meter span { display: block; height: 100%; border-radius: inherit; background: var(--teal); transition: width 0.35s; }
  .meter i { position: absolute; top: -0.25rem; bottom: -0.25rem; width: 2px; background: var(--sand-2); border-radius: 2px; }

  .filters { display: inline-flex; padding: 0.2rem; border-radius: 1rem; background: var(--paper-2); margin-bottom: 0.6rem; }
  .filters button { border: 0; background: transparent; padding: 0.3rem 0.85rem; border-radius: 0.8rem; font-size: 0.85rem; font-weight: 800; color: var(--ink-2); }
  .filters button.on { background: #fff; color: var(--ink); box-shadow: 0 1px 4px rgb(93 74 31 / 0.15); }

  .list { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.4rem; }
  .list li {
    display: grid;
    grid-template-columns: auto 3rem minmax(0, 1fr) auto;
    align-items: center;
    gap: 0.7rem;
    padding: 0.5rem 0.75rem 0.5rem 0.5rem;
    background: #fff;
    border: 1.5px solid var(--line);
    border-radius: var(--radius-m);
    transition: border-color 0.15s, background 0.15s;
  }
  .list li:hover { border-color: var(--sand-2); }
  .list li.done { background: #effaf6; border-color: #bfe7db; }
  .list li.empty { display: block; text-align: center; color: var(--ink-2); padding: 1rem; }

  .check { position: relative; display: grid; place-items: center; width: 2rem; height: 2rem; cursor: pointer; }
  .check input { position: absolute; opacity: 0; width: 100%; height: 100%; margin: 0; cursor: pointer; }
  .box {
    width: 1.45rem; height: 1.45rem;
    display: grid; place-items: center;
    border-radius: 0.45rem;
    border: 2.5px solid var(--stone);
    background: #fff;
    transition: background 0.12s, border-color 0.12s, transform 0.12s;
  }
  .box svg { width: 1rem; height: 1rem; fill: none; stroke: #fff; stroke-width: 3.4; stroke-linecap: round; stroke-linejoin: round; opacity: 0; }
  .check input:checked + .box { background: var(--teal); border-color: var(--teal); transform: scale(1.05); }
  .check input:checked + .box svg { opacity: 1; }
  .check input:focus-visible + .box { outline: 3px solid var(--deep); outline-offset: 2px; }
  .check:hover .box { border-color: var(--teal); }

  .badge { display: grid; place-items: center; height: 2rem; border-radius: 0.55rem; color: #fff; font-size: 0.72rem; font-weight: 900; letter-spacing: 0.02em; }
  .title { display: grid; min-width: 0; text-decoration: none; color: inherit; }
  .title .t { font-weight: 800; font-size: 0.98rem; line-height: 1.25; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .title .s { font-size: 0.78rem; color: var(--ink-2); font-weight: 700; }
  .title:hover .t { text-decoration: underline; text-decoration-color: var(--sand-2); text-underline-offset: 3px; }
  li.done .t { color: var(--ink-2); }
  .ext { width: 1.1rem; height: 1.1rem; fill: none; stroke: var(--stone-2); stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }

  textarea {
    width: 100%;
    resize: vertical;
    min-height: 4.5rem;
    padding: 0.7rem 0.85rem;
    border-radius: var(--radius-m);
    border: 1.5px solid var(--line);
    background: #fff;
    font-weight: 600;
    line-height: 1.45;
  }
  textarea:focus { outline: none; border-color: var(--c); }

  .answer { padding: 0.9rem 1.25rem 1.1rem; background: var(--paper-2); border-top: 1.5px solid var(--line); }
  .q, .answered, .locked-msg { margin: 0 0 0.7rem; text-align: center; font-weight: 900; font-size: 0.98rem; }
  .locked-msg { margin: 0.3rem 0; color: var(--ink-2); font-weight: 800; }
  .answered { font-weight: 800; color: var(--ink-2); }
  .link { border: 0; background: none; padding: 0 0 0 0.4rem; color: var(--deep); font-weight: 900; text-decoration: underline; text-underline-offset: 3px; }
  .buttons { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
  .push {
    position: relative;
    display: flex; align-items: center; justify-content: center; gap: 0.5rem;
    height: 3.2rem;
    border: 0;
    border-radius: 1.1rem;
    font-size: 1.05rem;
    font-weight: 900;
    transition: transform 0.06s, box-shadow 0.06s;
  }
  .push kbd { opacity: 0.8; }
  .push.soft { background: #fff; color: var(--teal-2); box-shadow: 0 0.3rem 0 #d9cba6; }
  .push.primary { background: var(--coral); color: #fff; box-shadow: 0 0.3rem 0 var(--coral-2); }
  .push.primary kbd { background: rgb(255 255 255 / 0.2); border-color: rgb(255 255 255 / 0.35); color: #fff; }
  .push:hover { filter: brightness(1.04); }
  .push:active { transform: translateY(0.25rem); box-shadow: 0 0.05rem 0 transparent; }

  @media (max-width: 56em) {
    .panel { border-left: 0; box-shadow: -1rem 0 2.5rem rgb(6 50 74 / 0.3); }
    .close { display: grid; }
  }
</style>
