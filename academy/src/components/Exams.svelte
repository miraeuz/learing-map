<script lang="ts">
  import { sections, BANDS } from '../lib/course';
  import { app, topicProgress } from '../lib/store.svelte';
  import { go } from '../lib/nav.svelte';
  import Ring from './Ring.svelte';

  const passed = $derived(sections.filter((s) => app.saved.exams[s.num]?.passed).length);
  function ready(num: number) {
    const s = sections.find((x) => x.num === num)!;
    return s.topics.filter((t) => topicProgress(t.id).read).length / s.topics.length;
  }
</script>

<div class="page">
  <header>
    <h1>Imtihonlar</h1>
    <p>Har bir boʻlim oxirida — imtihon: {14} ta test va 2 ta kod topshirigʻi, 30 daqiqa. Oʻtish bali — 70%.</p>
    <div class="cups">
      {#each sections as s}<span class:on={app.saved.exams[s.num]?.passed} title={s.title}>🏆</span>{/each}
      <b>{passed} / {sections.length} kubok</b>
    </div>
  </header>

  <div class="list">
    {#each sections as s}
      {@const r = app.saved.exams[s.num]}
      {@const rd = ready(s.num)}
      <article class:passed={r?.passed}>
        <span class="emo">{s.emoji}</span>
        <div class="info">
          <small>{s.num}-boʻlim · {BANDS[s.num].label}</small>
          <h3>{s.title}</h3>
          <p>{rd < 0.5 ? `Tavsiya: avval darslarni oʻqing (${Math.round(rd * 100)}% oʻqilgan)` : `${Math.round(rd * 100)}% darslar oʻqilgan — tayyorsiz!`}</p>
        </div>
        <div class="res">
          {#if r}
            <Ring pct={r.best / 100} size="3.4rem" stroke={3} tone={r.passed ? 'gold' : 'rose'}><b>{r.best}%</b></Ring>
            <small>{r.tries} urinish</small>
          {:else}
            <small class="none">Hali topshirilmagan</small>
          {/if}
        </div>
        <button class={r?.passed ? 'btn-ghost' : 'btn-primary'} onclick={() => go({ name: 'exam', sec: s.num })}>
          {r ? 'Qayta topshirish' : 'Boshlash'}
        </button>
      </article>
    {/each}
  </div>
</div>

<style>
  .page { display: grid; gap: 1.6rem; padding: 2rem clamp(1.5rem, 3vw, 3rem) 3rem; max-width: 70rem; margin: 0 auto; }
  h1 { margin: 0; font-family: var(--display); font-size: 2rem; font-weight: 700; }
  header p { margin: 0.5rem 0 0; color: var(--text-2); }
  .cups { display: flex; align-items: center; gap: 0.3rem; margin-top: 1rem; font-size: 1.5rem; }
  .cups span { filter: grayscale(1); opacity: 0.25; }
  .cups span.on { filter: none; opacity: 1; }
  .cups b { margin-left: 0.8rem; font-size: 0.95rem; color: var(--gold); }
  .list { display: grid; gap: 0.8rem; }
  article { display: flex; align-items: center; gap: 1.2rem; padding: 1.1rem 1.4rem; border-radius: var(--r-l); background: var(--surface); border: 1px solid var(--line); }
  article.passed { border-color: rgb(247 189 70 / 0.4); background: linear-gradient(90deg, rgb(247 189 70 / 0.08), var(--surface) 50%); }
  .emo { font-size: 1.8rem; display: grid; place-items: center; width: 3.4rem; height: 3.4rem; border-radius: 1rem; background: var(--surface-2); flex: none; }
  .info { flex: 1; min-width: 0; display: grid; gap: 0.15rem; }
  .info small { color: var(--text-3); font-size: 0.8rem; }
  h3 { margin: 0; font-size: 1.12rem; font-weight: 650; }
  .info p { margin: 0; color: var(--text-2); font-size: 0.88rem; }
  .res { display: grid; justify-items: center; gap: 0.2rem; min-width: 6rem; }
  .res b { font-size: 1.15rem; }
  .res small { color: var(--text-3); font-size: 0.78rem; }
  .res .none { font-size: 0.82rem; text-align: center; }
</style>
