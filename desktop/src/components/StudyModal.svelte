<script lang="ts">
  import { topics, stages } from '../lib/data';
  import { app, isLearned, toggleLearned, learnedCount, markOpened, select, solvedCount } from '../lib/store.svelte';
  import { detailOf, lessonSteps, hoursText } from '../lib/lesson';
  import Modal from './Modal.svelte';
  import Ring from './Ring.svelte';

  let { onJump }: { onJump: (i: number) => void } = $props();

  const i = $derived(app.selected);
  const topic = $derived(topics[i]);
  const stage = $derived(stages[topic.stage]);
  const d = $derived(detailOf(i));
  const learned = $derived(learnedCount(i, d.k.length));
  const steps = $derived(lessonSteps(i));
  const done = $derived(steps.filter((s) => s.done).length);
  const nextStep = $derived(steps.findIndex((s) => !s.done));
  const solved = $derived(solvedCount(i));

  const close = () => (app.studyOpen = false);
  function go(delta: number) {
    const n = Math.max(0, Math.min(topics.length - 1, i + delta));
    select(n);
    onJump(n);
  }
</script>

<Modal open={app.studyOpen} onClose={close} label={`${topic.name}: dars rejasi`} width="62rem" closable flush>
  <article class="lesson" style:--c={stage.color}>
    <header>
      <div class="head-text">
        <span class="eyebrow">{stage.emoji} {stage.id}-bosqich: {stage.name}, {i + 1}-daraja</span>
        <h2>{topic.name}</h2>
        <p>{topic.info}</p>
        <div class="chips">
          <span>⏱ {hoursText(d.h)} oʻrganish</span>
          <span>📚 {d.k.length} ta asosiy gʻoya</span>
          <span>✅ {solved}/15 masala yechilgan</span>
        </div>
      </div>
      <div class="head-ring">
        <Ring value={done / steps.length} size="5.5rem" stroke={8} color="#fff" track="rgb(255 255 255 / 0.25)" label="" />
        <span class="ring-num">{done}<small>/{steps.length}</small></span>
        <span class="ring-cap">qadam</span>
      </div>
    </header>

    <div class="cols">
      <div class="main">
        <section class="signal">
          <h3><span aria-hidden="true">💡</span> Qachon kerak boʻladi?</h3>
          <p>{d.w}</p>
        </section>

        <section>
          <div class="sec-head">
            <h3>Nimalarni oʻrganishingiz kerak</h3>
            <span class="muted">{learned}/{d.k.length} belgilandi</span>
          </div>
          <p class="hint">Tartib bilan oʻrganing. Har bir gʻoyani oʻzingiz tushuntira olsangiz — belgilang.</p>
          <ol class="learn">
            {#each d.k as item, j}
              {@const on = isLearned(i, j)}
              <li>
                <label class:on>
                  <input type="checkbox" checked={on} onchange={() => toggleLearned(i, j)} />
                  <span class="num">{#if on}✓{:else}{j + 1}{/if}</span>
                  <span class="txt">{item}</span>
                </label>
              </li>
            {/each}
          </ol>
        </section>

        <div class="duo">
          <section class="box complexity">
            <h3>Murakkablik</h3>
            <p>{d.c}</p>
          </section>
          <section class="box pitfalls">
            <h3>Koʻp uchraydigan xatolar</h3>
            <ul>{#each d.p as item}<li>{item}</li>{/each}</ul>
          </section>
        </div>
      </div>

      <aside class="plan" aria-label="Dars rejasi">
        <h3>Dars rejasi</h3>
        <ol class="steps">
          {#each steps as st, k}
            <li class:done={st.done} class:next={k === nextStep}>
              <span class="dot">{#if st.done}✓{:else}{k + 1}{/if}</span>
              <div class="step-body">
                <b>{st.title}</b>
                <span>{st.hint}</span>
                {#if st.progress && !st.done}
                  <span class="bar"><span style:width={`${(st.progress[0] / st.progress[1]) * 100}%`}></span></span>
                {/if}
                {#if st.url && !st.done}
                  <a href={st.url} target="_blank" rel="noopener noreferrer" onclick={() => markOpened(st.url!)}>Maqolani ochish</a>
                {/if}
                {#if k === 2 && !st.done}
                  <button class="link" onclick={close}>Masalalar roʻyxatiga</button>
                {/if}
              </div>
            </li>
          {/each}
        </ol>
        {#if done === steps.length}
          <p class="cheer">Ajoyib! Bu mavzu toʻliq oʻzlashtirildi.</p>
        {/if}
      </aside>
    </div>

    <footer>
      <button class="nav" onclick={() => go(-1)} disabled={i === 0}>← Oldingi mavzu</button>
      <span class="spacer"></span>
      <button class="nav" onclick={() => go(1)} disabled={i === topics.length - 1}>Keyingi mavzu →</button>
      <button class="primary" onclick={close}>Masalalarga oʻtish</button>
    </footer>
  </article>
</Modal>

<style>
  header {
    display: grid; grid-template-columns: 1fr auto; gap: 1.5rem; align-items: center;
    padding: 1.6rem 4.25rem 1.4rem 1.9rem;
    background: var(--c); color: #fff;
  }
  .eyebrow { font-size: 0.86rem; font-weight: 800; opacity: 0.92; }
  h2 { margin: 0.25rem 0 0.45rem; font-size: 2rem; font-weight: 900; line-height: 1.08; letter-spacing: -0.01em; }
  header p { margin: 0 0 0.9rem; font-size: 1.02rem; line-height: 1.5; font-weight: 600; color: rgb(255 255 255 / 0.95); max-width: 40rem; }
  .chips { display: flex; flex-wrap: wrap; gap: 0.4rem; }
  .chips span { padding: 0.22rem 0.7rem; border-radius: 1rem; background: rgb(0 0 0 / 0.16); font-size: 0.84rem; font-weight: 800; }
  .head-ring { position: relative; display: grid; justify-items: center; }
  .ring-num { position: absolute; top: 1.55rem; font-size: 1.6rem; font-weight: 900; line-height: 1; }
  .ring-num small { font-size: 0.95rem; opacity: 0.85; }
  .ring-cap { margin-top: 0.3rem; font-size: 0.8rem; font-weight: 800; opacity: 0.9; }

  .cols { display: grid; grid-template-columns: minmax(0, 1fr) 18.5rem; gap: 1.5rem; padding: 1.5rem 1.9rem; align-items: start; }
  .main { display: grid; gap: 1.4rem; min-width: 0; }
  h3 { margin: 0 0 0.55rem; font-size: 1.05rem; font-weight: 900; }
  .sec-head { display: flex; justify-content: space-between; align-items: baseline; gap: 1rem; }
  .sec-head h3 { margin-bottom: 0.2rem; }
  .muted { color: var(--ink-2); font-size: 0.86rem; font-weight: 800; }
  .hint { margin: 0 0 0.7rem; color: var(--ink-2); font-size: 0.9rem; font-weight: 700; }

  .signal { padding: 1rem 1.15rem; border-radius: var(--radius-m); background: #fff7dc; border: 1.5px solid #f4e2a8; }
  .signal h3 { margin-bottom: 0.3rem; }
  .signal p { margin: 0; line-height: 1.55; font-weight: 700; }

  .learn { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.45rem; }
  .learn label {
    position: relative;
    display: grid; grid-template-columns: 2rem 1fr; gap: 0.8rem; align-items: center;
    padding: 0.65rem 0.9rem 0.65rem 0.65rem;
    background: #fff; border: 1.5px solid var(--line); border-radius: var(--radius-m);
    cursor: pointer; transition: background 0.15s, border-color 0.15s;
  }
  .learn label:hover { border-color: var(--c); }
  .learn label.on { background: #effaf6; border-color: #bfe7db; }
  .learn input { position: absolute; opacity: 0; pointer-events: none; }
  .learn input:focus-visible ~ .num { outline: 3px solid var(--deep); outline-offset: 2px; }
  .num {
    display: grid; place-items: center; width: 2rem; height: 2rem; border-radius: 50%;
    border: 2px solid var(--c); color: var(--c); font-weight: 900; font-size: 0.95rem;
  }
  label.on .num { background: var(--teal); border-color: var(--teal); color: #fff; }
  .txt { font-weight: 700; line-height: 1.45; }
  label.on .txt { color: var(--ink-2); }

  .duo { display: grid; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); gap: 1rem; }
  .box { padding: 1rem 1.1rem; border-radius: var(--radius-m); }
  .complexity { background: #eaf6fb; }
  .complexity p { margin: 0; font-weight: 800; line-height: 1.5; color: var(--deep); }
  .pitfalls { background: #fff1e8; }
  .pitfalls ul { margin: 0; padding: 0; list-style: none; display: grid; gap: 0.5rem; }
  .pitfalls li { position: relative; padding-left: 1.5rem; font-weight: 700; line-height: 1.45; }
  .pitfalls li::before { content: '⚠'; position: absolute; left: 0; color: var(--gold-2); }

  .plan {
    position: sticky; top: 1rem;
    padding: 1.1rem 1.1rem 1.2rem;
    background: #fff; border: 1.5px solid var(--line); border-radius: var(--radius-l);
  }
  .steps { list-style: none; margin: 0; padding: 0; display: grid; gap: 0; }
  .steps li { position: relative; display: grid; grid-template-columns: 2rem 1fr; gap: 0.7rem; padding-bottom: 1rem; }
  .steps li:not(:last-child)::after {
    content: ''; position: absolute; left: 0.95rem; top: 2.1rem; bottom: 0.15rem;
    width: 2px; background: var(--line);
  }
  .steps li.done:not(:last-child)::after { background: var(--teal); }
  .dot {
    display: grid; place-items: center; width: 2rem; height: 2rem; border-radius: 50%;
    background: var(--paper-2); color: var(--ink-2); font-weight: 900; font-size: 0.9rem;
  }
  li.done .dot { background: var(--teal); color: #fff; }
  li.next .dot { background: var(--coral); color: #fff; box-shadow: 0 0 0 4px rgb(255 107 74 / 0.2); }
  .step-body { display: grid; gap: 0.15rem; padding-top: 0.2rem; min-width: 0; }
  .step-body b { font-weight: 900; font-size: 0.96rem; }
  li.done .step-body b { color: var(--ink-2); text-decoration: line-through; text-decoration-color: var(--teal); }
  .step-body > span { font-size: 0.82rem; color: var(--ink-2); font-weight: 700; }
  .bar { display: block; height: 0.35rem; margin-top: 0.3rem; border-radius: 1rem; background: var(--paper-2); overflow: hidden; }
  .bar span { display: block; height: 100%; background: var(--coral); border-radius: inherit; }
  .step-body a, .link {
    justify-self: start; margin-top: 0.25rem; padding: 0; border: 0; background: none;
    color: var(--deep); font-weight: 900; font-size: 0.88rem; text-decoration: underline; text-underline-offset: 3px;
  }
  .cheer { margin: 0.2rem 0 0; padding: 0.6rem 0.75rem; border-radius: 0.8rem; background: #effaf6; color: var(--teal-2); font-weight: 900; text-align: center; }

  footer {
    position: sticky; bottom: 0;
    display: flex; align-items: center; gap: 0.6rem; flex-wrap: wrap;
    padding: 0.9rem 1.9rem 1.1rem;
    background: var(--paper-2); border-top: 1.5px solid var(--line);
  }
  .spacer { flex: 1; }
  .nav, .primary { height: 2.8rem; padding: 0 1.1rem; border-radius: 0.9rem; font-weight: 900; font-size: 0.95rem; }
  .nav { border: 1.5px solid var(--line); background: #fff; }
  .nav:hover:not(:disabled) { border-color: var(--sand-2); }
  .nav:disabled { opacity: 0.45; cursor: default; }
  .primary { border: 0; background: var(--coral); color: #fff; box-shadow: 0 0.25rem 0 var(--coral-2); }
  .primary:active { transform: translateY(0.2rem); box-shadow: none; }

  @media (max-width: 62em) {
    .cols { grid-template-columns: 1fr; }
    .plan { position: static; }
  }
</style>
