<script lang="ts">
  import { topics, stages } from '../lib/data';
  import details from '../data/details.json';
  import { app, isLearned, toggleLearned, learnedCount } from '../lib/store.svelte';
  import Modal from './Modal.svelte';

  const i = $derived(app.selected);
  const topic = $derived(topics[i]);
  const stage = $derived(stages[topic.stage]);
  const d = $derived(details[i] as { k: string[]; c: string; p: string[] });
  const done = $derived(learnedCount(i, d.k.length));
  const theory = $derived(topic.links.find((l) => l.title.startsWith('Nazariya: ')));

  const close = () => (app.studyOpen = false);
</script>

<Modal open={app.studyOpen} onClose={close} label={`${topic.name}: batafsil`} width="44rem" closable flush>
  <div class="study" style:--c={stage.color}>
    <header>
      <span class="eyebrow">{stage.emoji} {i + 1}-daraja, {stage.name}</span>
      <h2>{topic.name}</h2>
      <p>{topic.info}</p>
      <div class="meter" aria-label={`${done} / ${d.k.length} oʻrganildi`}>
        <span style:width={`${(done / d.k.length) * 100}%`}></span>
      </div>
      <span class="count">{done} / {d.k.length} oʻrganildi</span>
    </header>

    <div class="body">
      <section>
        <h3>Nimalarni oʻrganishingiz kerak</h3>
        <ul class="learn">
          {#each d.k as item, j}
            {@const on = isLearned(i, j)}
            <li>
              <label class:on>
                <input type="checkbox" checked={on} onchange={() => toggleLearned(i, j)} />
                <span class="box"><svg viewBox="0 0 24 24"><path d="m5 12.5 4.5 4.5L19 7.5" /></svg></span>
                <span class="txt">{item}</span>
              </label>
            </li>
          {/each}
        </ul>
      </section>

      <div class="grid">
        <section class="box-c">
          <h3>Murakkablik</h3>
          <p class="mono">{d.c}</p>
        </section>
        <section class="box-p">
          <h3>Koʻp uchraydigan xatolar</h3>
          <ul class="pit">
            {#each d.p as item}<li>{item}</li>{/each}
          </ul>
        </section>
      </div>
    </div>

    <footer>
      {#if theory}
        <a class="ghost" href={theory.url} target="_blank" rel="noopener noreferrer">Nazariyani oʻqish (cp-algorithms)</a>
      {/if}
      <button class="primary" onclick={close}>Masalalarga oʻtish</button>
    </footer>
  </div>
</Modal>

<style>
  header { padding: 1.6rem 4rem 1.3rem 1.75rem; background: var(--c); color: #fff; }
  .eyebrow { font-size: 0.85rem; font-weight: 800; opacity: 0.92; }
  h2 { margin: 0.25rem 0 0.5rem; font-size: 1.9rem; font-weight: 900; line-height: 1.1; }
  header p { margin: 0 0 1rem; font-size: 1rem; line-height: 1.5; font-weight: 600; color: rgb(255 255 255 / 0.95); max-width: 36rem; }
  .meter { height: 0.5rem; border-radius: 1rem; background: rgb(255 255 255 / 0.28); overflow: hidden; }
  .meter span { display: block; height: 100%; background: #fff; border-radius: inherit; transition: width 0.3s; }
  .count { display: block; margin-top: 0.35rem; font-size: 0.85rem; font-weight: 800; }

  .body { padding: 1.4rem 1.75rem; display: grid; gap: 1.4rem; }
  h3 { margin: 0 0 0.6rem; font-size: 1.02rem; font-weight: 900; }
  .learn { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.45rem; }
  .learn label {
    position: relative;
    display: grid; grid-template-columns: 1.6rem 1fr; gap: 0.75rem; align-items: start;
    padding: 0.7rem 0.85rem;
    background: #fff; border: 1.5px solid var(--line); border-radius: var(--radius-m);
    cursor: pointer; transition: background 0.15s, border-color 0.15s;
  }
  .learn label:hover { border-color: var(--sand-2); }
  .learn label.on { background: #effaf6; border-color: #bfe7db; }
  .learn input { position: absolute; opacity: 0; pointer-events: none; }
  .box {
    width: 1.45rem; height: 1.45rem; margin-top: 0.05rem;
    display: grid; place-items: center;
    border-radius: 0.45rem; border: 2.5px solid var(--stone); background: #fff;
  }
  .box svg { width: 1rem; height: 1rem; fill: none; stroke: #fff; stroke-width: 3.4; stroke-linecap: round; stroke-linejoin: round; opacity: 0; }
  label.on .box { background: var(--teal); border-color: var(--teal); }
  label.on .box svg { opacity: 1; }
  .learn input:focus-visible + .box { outline: 3px solid var(--deep); outline-offset: 2px; }
  .txt { font-weight: 700; line-height: 1.45; }
  label.on .txt { color: var(--ink-2); }

  .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); gap: 1rem; }
  .box-c, .box-p { padding: 1rem 1.1rem; border-radius: var(--radius-m); }
  .box-c { background: #eaf6fb; }
  .box-p { background: #fff3e6; }
  .mono { margin: 0; font-weight: 800; line-height: 1.5; color: var(--deep); }
  .pit { margin: 0; padding: 0; list-style: none; display: grid; gap: 0.5rem; }
  .pit li { position: relative; padding-left: 1.5rem; font-weight: 700; line-height: 1.45; }
  .pit li::before { content: '⚠'; position: absolute; left: 0; color: var(--gold-2); }

  footer {
    position: sticky; bottom: 0;
    display: flex; justify-content: flex-end; gap: 0.75rem; flex-wrap: wrap;
    padding: 1rem 1.75rem 1.25rem;
    background: var(--paper-2); border-top: 1.5px solid var(--line);
  }
  .ghost, .primary {
    display: inline-flex; align-items: center; height: 2.9rem; padding: 0 1.2rem;
    border-radius: 0.9rem; font-weight: 900; font-size: 0.98rem; text-decoration: none;
  }
  .ghost { background: #fff; color: var(--deep); border: 1.5px solid var(--line); }
  .ghost:hover { border-color: var(--sand-2); }
  .primary { border: 0; background: var(--coral); color: #fff; box-shadow: 0 0.25rem 0 var(--coral-2); }
  .primary:active { transform: translateY(0.2rem); box-shadow: none; }
</style>
