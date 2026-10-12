<script lang="ts">
  import { topics, stages, normalize } from '../lib/data';
  import { app, statusOf, isLocked, solvedCount, select } from '../lib/store.svelte';

  let { onJump }: { onJump: (i: number) => void } = $props();

  let q = $state('');
  let active = $state(0);
  let input = $state<HTMLInputElement>();

  const index = topics.map((t, i) => ({ i, hay: normalize(`${i + 1} ${t.name} ${t.info} ${stages[t.stage].name}`) }));
  const results = $derived.by(() => {
    const words = normalize(q).split(/\s+/).filter(Boolean);
    const list = words.length ? index.filter((e) => words.every((w) => e.hay.includes(w))) : index;
    return list.slice(0, 40).map((e) => e.i);
  });

  $effect(() => {
    results;
    active = 0;
  });

  $effect(() => {
    if (app.searchOpen) queueMicrotask(() => input?.focus());
  });

  function pick(i: number) {
    select(i);
    onJump(i);
    close();
  }

  function close() {
    app.searchOpen = false;
    q = '';
  }

  function onKey(e: KeyboardEvent) {
    if (e.key === 'ArrowDown') { active = Math.min(results.length - 1, active + 1); e.preventDefault(); }
    else if (e.key === 'ArrowUp') { active = Math.max(0, active - 1); e.preventDefault(); }
    else if (e.key === 'Enter' && results[active] !== undefined) pick(results[active]);
    else if (e.key === 'Escape') close();
  }

  const label = (i: number) => (isLocked(i) ? 'Yopiq' : statusOf(i) === 'done' ? '⭐' : statusOf(i) === 'practice' ? '↻' : '');
</script>

{#if app.searchOpen}
  <!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
  <div class="backdrop" onclick={close}>
    <!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
    <div class="palette" role="dialog" aria-modal="true" aria-label="Mavzu qidirish" tabindex="-1" onclick={(e) => e.stopPropagation()}>
      <div class="field">
        <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7" /><path d="m20 20-4-4" /></svg>
        <input
          bind:this={input}
          bind:value={q}
          onkeydown={onKey}
          placeholder="Mavzu, algoritm yoki daraja raqami…"
          aria-label="Qidiruv"
        />
        <kbd>Esc</kbd>
      </div>
      <ul>
        {#each results as i, k (i)}
          {@const s = stages[topics[i].stage]}
          <li>
            <button class:active={k === active} onmouseenter={() => (active = k)} onclick={() => pick(i)}>
              <span class="num" style:background={s.color}>{i + 1}</span>
              <span class="txt">
                <span class="name">{topics[i].name}</span>
                <span class="meta">{s.emoji} {s.name}, {solvedCount(i)}/15 masala</span>
              </span>
              <span class="st">{label(i)}</span>
            </button>
          </li>
        {:else}
          <li class="none">Hech narsa topilmadi. Boshqa soʻz bilan qidiring.</li>
        {/each}
      </ul>
    </div>
  </div>
{/if}

<style>
  .backdrop {
    position: fixed; inset: 0; z-index: 50;
    display: grid; justify-items: center; align-items: start;
    padding-top: 12vh;
    background: rgb(6 50 74 / 0.45);
  }
  .palette {
    width: min(40rem, calc(100vw - 2rem));
    max-height: 70vh;
    display: grid; grid-template-rows: auto 1fr;
    background: var(--paper);
    border-radius: var(--radius-l);
    box-shadow: 0 1.5rem 4rem rgb(6 50 74 / 0.4);
    overflow: hidden;
    animation: rise 0.18s ease-out;
  }
  .field { display: flex; align-items: center; gap: 0.7rem; padding: 1rem 1.1rem; border-bottom: 1.5px solid var(--line); }
  .field svg { width: 1.3rem; height: 1.3rem; fill: none; stroke: var(--ink-2); stroke-width: 2.4; stroke-linecap: round; }
  input { flex: 1; border: 0; background: transparent; font-size: 1.15rem; font-weight: 800; outline: none; }
  ul { list-style: none; margin: 0; padding: 0.4rem; overflow-y: auto; }
  li button {
    width: 100%; display: grid; grid-template-columns: 2.4rem 1fr auto; align-items: center; gap: 0.8rem;
    padding: 0.55rem 0.7rem; border: 0; border-radius: var(--radius-m); background: transparent; text-align: left;
  }
  li button.active { background: #fff; box-shadow: 0 1px 6px rgb(93 74 31 / 0.15); }
  .num { display: grid; place-items: center; height: 2.4rem; border-radius: 0.7rem; color: #fff; font-weight: 900; }
  .txt { display: grid; min-width: 0; }
  .name { font-weight: 900; font-size: 1rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .meta { font-size: 0.8rem; color: var(--ink-2); font-weight: 700; }
  .st { font-size: 0.85rem; color: var(--ink-2); font-weight: 800; }
  .none { padding: 1.5rem; text-align: center; color: var(--ink-2); }
  @keyframes rise { from { transform: translateY(0.6rem); opacity: 0; } }
</style>
