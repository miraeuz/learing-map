<script lang="ts">
  /**
   * Editor tab strip: the student's own file plus read-only helper files
   * (modules, CSV, JSON...) that are written next to it before the code runs.
   * `active` is -1 for the student's file, otherwise the helper index.
   */
  import type { PyFile } from '../lib/python.svelte';

  let { files, mainName, active = $bindable(-1), mainIcon = '✎' }: { files: PyFile[]; mainName: string; active?: number; mainIcon?: string } = $props();

  const icon = (n: string) => (n.endsWith('.py') ? '🐍' : n.endsWith('.csv') ? '▦' : n.endsWith('.json') ? '{}' : '▤');

  function key(e: KeyboardEvent) {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    const n = files.length + 1;
    const i = (active + 1 + (e.key === 'ArrowRight' ? 1 : n - 1)) % n;
    active = i - 1;
    (e.currentTarget as HTMLElement).querySelectorAll<HTMLButtonElement>('[role=tab]')[i]?.focus();
  }
</script>

<div class="tabs" role="tablist" tabindex="-1" aria-label="Fayllar" onkeydown={key}>
  <button role="tab" aria-selected={active === -1} tabindex={active === -1 ? 0 : -1} class:on={active === -1} onclick={() => (active = -1)}>
    <span class="i">{mainIcon}</span>{mainName}
  </button>
  {#each files as f, i (f.name)}
    <button role="tab" aria-selected={active === i} tabindex={active === i ? 0 : -1} class:on={active === i} class="ro" onclick={() => (active = i)} title="Yordamchi fayl — faqat oʻqish uchun">
      <span class="i">{icon(f.name)}</span>{f.name}<span class="lock" aria-hidden="true">🔒</span>
    </button>
  {/each}
</div>

<style>
  .tabs { display: flex; gap: 0.15rem; min-width: 0; overflow-x: auto; scrollbar-width: none; }
  .tabs::-webkit-scrollbar { display: none; }
  button {
    display: inline-flex; align-items: center; gap: 0.4rem; flex: none;
    height: 1.9rem; padding: 0 0.7rem; border: 0; border-radius: 0.45rem;
    background: none; color: #7381b4; font: 0.78rem var(--mono); white-space: nowrap;
    transition: background 0.15s, color 0.15s;
  }
  button:hover { background: rgb(255 255 255 / 0.05); color: #c3d2ff; }
  button.on { background: rgb(74 116 255 / 0.16); color: #edf1ff; box-shadow: inset 0 -2px 0 #4a74ff; }
  button.ro.on { background: rgb(247 189 70 / 0.12); box-shadow: inset 0 -2px 0 #f7bd46; }
  .i { font-size: 0.8rem; opacity: 0.85; }
  .lock { font-size: 0.62rem; opacity: 0.6; }
</style>
