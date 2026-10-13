<script lang="ts">
  import type { QuizEx } from '../lib/course';
  import { xpFor } from '../lib/course';
  import { app, markSolved, addAttempt, toast } from '../lib/store.svelte';
  import CodeEditor from './CodeEditor.svelte';

  let { ex, onNext }: { ex: QuizEx; onNext?: () => void } = $props();

  let wrong = $state<number[]>([]);
  const solved = $derived(!!app.saved.solved[ex.id]);
  let justSolved = $state(false);
  const L = ['A', 'B', 'C', 'D', 'E'];

  function pick(i: number) {
    if (solved || wrong.includes(i)) return;
    if (i === ex.answer) {
      const xp = markSolved(ex);
      justSolved = true;
      if (xp) toast(wrong.length ? 'Toʻgʻri!' : 'Birinchi urinishda toʻgʻri!', { xp, tone: 'ok' });
    } else {
      wrong = [...wrong, i];
      addAttempt(ex.id);
    }
  }

  function onKey(e: KeyboardEvent) {
    const t = e.target as HTMLElement;
    if (t.closest('input, textarea, .cm-editor') || e.ctrlKey || e.metaKey || e.altKey) return;
    const n = Number(e.key);
    if (n >= 1 && n <= ex.options.length) pick(n - 1);
    else if (e.key === 'Enter' && solved && onNext) onNext();
  }
</script>

<svelte:window onkeydown={onKey} />

<div class="quiz">
  <h3 class="q">{@html ex.q}</h3>
  {#if ex.code}
    <div class="code"><CodeEditor value={ex.code} readonly minLines={1} maxHeight="24rem" /></div>
  {/if}

  <div class="opts" class:mono={ex.mono}>
    {#each ex.options as o, i}
      {@const right = solved && i === ex.answer}
      {@const bad = wrong.includes(i)}
      <button class="opt" class:right class:bad disabled={solved || bad} onclick={() => pick(i)}>
        <span class="k">{right ? '✓' : bad ? '✕' : L[i]}</span>
        <span class="t">{o === '' ? '(hech narsa chiqmaydi)' : o}</span>
      </button>
    {/each}
  </div>

  {#if solved}
    <div class="verdict ok" class:pop={justSolved}>
      <div>
        <b>{wrong.length === 0 && justSolved ? 'Ajoyib! Birinchi urinishda.' : 'Toʻgʻri javob!'}</b>
        {#if ex.why}<p>{@html ex.why}</p>{:else if ex.code}<p>Kod ishga tushirilganda aynan shu natija chiqadi. Ishonch hosil qilish uchun uni «Kod maydoni»da sinab koʻring.</p>{/if}
      </div>
      {#if onNext}<button class="btn-primary" onclick={onNext}>Keyingisi →</button>{/if}
    </div>
  {:else if wrong.length}
    <div class="verdict no">
      <b>Notoʻgʻri — yana urinib koʻring.</b>
      <p>{ex.code ? 'Kodni qatorma-qator, xuddi kompyuterdek "bajarib" chiqing. Har bir oʻzgaruvchi qiymatini yozib boring.' : 'Savolni yana bir bor diqqat bilan oʻqing.'}</p>
    </div>
  {:else}
    <p class="hint">Javobni tanlang · klaviaturada <kbd>1</kbd>–<kbd>{ex.options.length}</kbd> · +{xpFor(ex)} XP</p>
  {/if}
</div>

<style>
  .quiz { display: grid; gap: 1.1rem; }
  .q { margin: 0; font-size: 1.2rem; font-weight: 600; line-height: 1.5; }
  .q :global(code) { font-size: 0.9em; padding: 0.1em 0.35em; border-radius: 0.3rem; background: rgb(74 116 255 / 0.14); color: #a9c0ff; }
  :global([data-theme='light']) .q :global(code) { color: var(--lapis-2); }
  .code { border-radius: var(--r-m); overflow: hidden; border: 1px solid var(--code-line); }
  .opts { display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem; }
  .opt {
    display: flex; align-items: flex-start; gap: 0.8rem; text-align: left;
    padding: 0.85rem 1rem; border-radius: var(--r-m);
    border: 1px solid var(--line-2); background: var(--surface);
    transition: border-color 0.15s, background 0.15s, transform 0.15s;
  }
  .opt:hover:not(:disabled) { border-color: var(--lapis); background: var(--surface-2); transform: translateY(-1px); }
  .opt:disabled { cursor: default; }
  .k { flex: none; display: grid; place-items: center; width: 1.8rem; height: 1.8rem; border-radius: 0.5rem; background: var(--surface-2); border: 1px solid var(--line-2); font-size: 0.82rem; font-weight: 700; color: var(--text-2); }
  .t { padding-top: 0.15rem; line-height: 1.45; white-space: pre-wrap; word-break: break-word; }
  .mono .t { font-family: var(--mono); font-size: 0.93rem; }
  .opt.right { border-color: var(--turq); background: var(--ok-bg); }
  .opt.right .k { background: var(--turq); border-color: var(--turq); color: var(--turq-ink); }
  .opt.bad { border-color: rgb(255 122 138 / 0.5); background: var(--rose-bg); opacity: 0.75; animation: shake 0.35s; }
  .opt.bad .k { background: var(--rose); border-color: var(--rose); color: #fff; }
  @keyframes shake { 25% { transform: translateX(-4px); } 75% { transform: translateX(4px); } }
  .verdict { display: flex; justify-content: space-between; align-items: center; gap: 1rem; padding: 1rem 1.2rem; border-radius: var(--r-m); }
  .verdict b { font-size: 1.02rem; }
  .verdict p { margin: 0.3rem 0 0; color: var(--text-2); line-height: 1.55; font-size: 0.95rem; }
  .verdict.ok { background: var(--ok-bg); border: 1px solid rgb(57 220 200 / 0.35); }
  .verdict.ok b { color: var(--turq); }
  .verdict.no { display: block; background: var(--rose-bg); border: 1px solid rgb(255 122 138 / 0.3); }
  .verdict.no b { color: var(--rose); }
  .pop { animation: pop 0.4s cubic-bezier(0.2, 1.4, 0.4, 1); }
  @keyframes pop { from { transform: scale(0.96); opacity: 0; } }
  .hint { margin: 0; color: var(--text-3); font-size: 0.88rem; }
  @media (max-width: 60em) { .opts { grid-template-columns: 1fr; } }
</style>
