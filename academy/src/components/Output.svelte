<script lang="ts">
  import { explainError, type PyError } from '../lib/python.svelte';

  let { stdout = '', error = null, ms = null, label = 'Natija', live = true, empty = 'Kod hech narsa chiqarmadi' }: {
    stdout?: string; error?: PyError | null; ms?: number | null; label?: string; live?: boolean; empty?: string;
  } = $props();
  const why = $derived(explainError(error));
</script>

<div class="out" class:err={!!error}>
  <div class="bar">
    <span class="lbl"><i class:live></i>{label}</span>
    {#if ms != null}<span class="ms">{ms} ms</span>{/if}
  </div>
  {#if stdout}<pre>{stdout}</pre>{:else if !error}<p class="empty">{empty}</p>{/if}
  {#if error}
    <div class="error">
      <b>{error.type}{error.line ? ` · ${error.line}-qator` : ''}</b>
      <code>{error.msg}</code>
      {#if why}<p>💡 {why}</p>{/if}
    </div>
  {/if}
</div>

<style>
  .out { background: #050c22; border-top: 1px solid var(--code-line); color: #dfe6ff; }
  .bar { display: flex; justify-content: space-between; align-items: center; padding: 0.45rem 0.9rem; border-bottom: 1px dashed rgb(74 116 255 / 0.2); }
  .lbl { display: flex; align-items: center; gap: 0.5rem; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #7381b4; }
  .lbl i { width: 0.45rem; height: 0.45rem; border-radius: 50%; background: #4a5a92; }
  .lbl i.live { background: #39dcc8; box-shadow: 0 0 0.5rem #39dcc8; }
  .out.err .lbl i { background: #ff7a8a; box-shadow: 0 0 0.5rem #ff7a8a; }
  .ms { font: 0.75rem var(--mono); color: #4a5a92; }
  pre { margin: 0; padding: 0.75rem 0.9rem; font: 0.92rem/1.55 var(--mono); white-space: pre-wrap; word-break: break-word; max-height: 22rem; overflow: auto; }
  .empty { margin: 0; padding: 0.75rem 0.9rem; font-size: 0.85rem; color: #4a5a92; font-style: italic; }
  .error { margin: 0.6rem 0.8rem 0.8rem; padding: 0.7rem 0.85rem; border-radius: 0.6rem; background: rgb(255 122 138 / 0.1); border: 1px solid rgb(255 122 138 / 0.3); display: grid; gap: 0.3rem; }
  .error b { color: #ff9aa6; font-size: 0.88rem; }
  .error code { font-size: 0.86rem; color: #ffd0d6; white-space: pre-wrap; }
  .error p { margin: 0.15rem 0 0; color: #c9d1f0; font-size: 0.86rem; line-height: 1.45; }
</style>
