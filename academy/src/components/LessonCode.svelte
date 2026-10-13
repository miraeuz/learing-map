<script lang="ts">
  import { untrack } from 'svelte';
  import CodeEditor from './CodeEditor.svelte';
  import Output from './Output.svelte';
  import { runCode, type PyError } from '../lib/python.svelte';
  import type { Block } from '../lib/course';

  let { block }: { block: Extract<Block, { t: 'code' }> } = $props();

  const orig = untrack(() => block.code);
  let code = $state(orig);
  const shownStdin = (s: string) => s.replace(/\n$/, '').split('\n').join(' | ');
  let stdin = $state(untrack(() => shownStdin(block.stdin)));
  let out = $state(untrack(() => block.out));
  let error = $state<PyError | null>(untrack(() => block.err));
  let ms = $state<number | null>(null);
  let ran = $state(false);
  let busy = $state(false);
  let copied = $state(false);
  const changed = $derived(code !== orig);
  const usesInput = $derived(/\binput\s*\(/.test(code));

  async function run() {
    if (busy || block.norun) return;
    busy = true;
    const r = await runCode(code, stdin.split('|').map((x) => x.trim()).join('\n') + '\n');
    busy = false;
    ran = true;
    out = r.stdout.replace(/\n$/, '');
    error = r.error;
    ms = r.ms;
  }

  function reset() {
    code = orig;
    stdin = shownStdin(block.stdin);
    out = block.out;
    error = block.err;
    ms = null;
    ran = false;
  }

  async function copy() {
    try {
      await navigator.clipboard.writeText(code);
      copied = true;
      setTimeout(() => (copied = false), 1200);
    } catch { /* clipboard unavailable */ }
  }
</script>

<figure class="lc" class:norun={block.norun}>
  <div class="head">
    <span class="lang">🐍 Python</span>
    {#if changed}<span class="edited">oʻzgartirilgan</span>{/if}
    <span class="sp"></span>
    <button class="ic" onclick={copy} title="Nusxalash">{copied ? '✓' : '⧉'}</button>
    {#if changed}<button class="ic" onclick={reset} title="Asl holiga qaytarish">↺</button>{/if}
    {#if !block.norun}
      <button class="run" onclick={run} disabled={busy} title="Ishga tushirish (Ctrl+Enter)">
        {busy ? '…' : '▶'} Ishga tushirish
      </button>
    {/if}
  </div>
  <CodeEditor bind:value={code} minLines={1} maxHeight="30rem" onRun={run} />
  {#if !block.norun}
    {#if usesInput}
      <label class="stdin">
        <span>Kirish (input):</span>
        <input bind:value={stdin} placeholder="Qatorlarni | bilan ajrating, masalan: Ali | 25" onkeydown={(e) => e.key === 'Enter' && run()} />
      </label>
    {/if}
    <Output stdout={out} {error} {ms} live={ran} label={ran ? 'Natija' : 'Natija (namuna)'} />
  {:else}
    <figcaption>Bu kod namuna sifatida koʻrsatilgan — u shu yerda ishga tushirilmaydi.</figcaption>
  {/if}
</figure>

<style>
  .lc { margin: 0; border-radius: var(--r-m); overflow: hidden; border: 1px solid var(--code-line); background: var(--code-bg); box-shadow: 0 0.6rem 1.6rem rgb(0 0 0 / 0.18); }
  .head { display: flex; align-items: center; gap: 0.4rem; padding: 0.35rem 0.4rem 0.35rem 0.9rem; border-bottom: 1px solid var(--code-line); background: rgb(255 255 255 / 0.02); }
  .lang { font-size: 0.75rem; font-weight: 600; color: #7381b4; }
  .edited { font-size: 0.7rem; padding: 0.1rem 0.45rem; border-radius: 1rem; background: rgb(247 189 70 / 0.15); color: #f7bd46; }
  .sp { flex: 1; }
  .ic { width: 2rem; height: 2rem; border-radius: 0.5rem; border: 0; background: none; color: #7381b4; font-size: 1rem; }
  .ic:hover { background: rgb(255 255 255 / 0.06); color: #edf1ff; }
  .run { display: flex; align-items: center; gap: 0.4rem; height: 2rem; padding: 0 0.8rem; border: 0; border-radius: 0.5rem; background: rgb(57 220 200 / 0.14); color: #39dcc8; font-size: 0.82rem; font-weight: 600; }
  .run:hover { background: rgb(57 220 200 / 0.24); }
  .stdin { display: flex; align-items: center; gap: 0.6rem; padding: 0.5rem 0.9rem; border-top: 1px solid var(--code-line); font-size: 0.8rem; color: #7381b4; }
  .stdin input { flex: 1; min-width: 0; padding: 0.35rem 0.6rem; border-radius: 0.4rem; border: 1px solid var(--code-line); background: #050c22; color: #f7bd46; font: 0.86rem var(--mono); }
  figcaption { padding: 0.55rem 0.9rem; font-size: 0.8rem; color: #7381b4; border-top: 1px solid var(--code-line); }
</style>
