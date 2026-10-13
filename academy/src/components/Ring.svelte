<script lang="ts">
  let { pct = 0, size = '1.6rem', stroke = 3.2, tone = 'turq', children }: {
    pct?: number; size?: string; stroke?: number; tone?: 'turq' | 'gold' | 'lapis' | 'rose'; children?: import('svelte').Snippet;
  } = $props();
  const r = $derived(16 - stroke / 2);
  const c = $derived(2 * Math.PI * r);
</script>

<span class="ring" style:width={size} style:height={size}>
  <svg viewBox="0 0 32 32" aria-hidden="true">
    <circle cx="16" cy="16" {r} class="track" stroke-width={stroke} />
    <circle cx="16" cy="16" {r} class="bar {tone}" class:full={pct >= 1} stroke-width={stroke}
      stroke-dasharray={c} stroke-dashoffset={c * (1 - Math.max(0, Math.min(1, pct)))} />
  </svg>
  {#if children}<span class="in">{@render children()}</span>{/if}
</span>

<style>
  .ring { position: relative; display: inline-grid; place-items: center; flex: none; }
  svg { position: absolute; inset: 0; transform: rotate(-90deg); }
  circle { fill: none; }
  .track { stroke: var(--line); }
  .bar { stroke-linecap: round; transition: stroke-dashoffset 0.6s cubic-bezier(0.2, 0.8, 0.2, 1); }
  .turq { stroke: var(--turq); } .gold { stroke: var(--gold); } .lapis { stroke: var(--lapis); } .rose { stroke: var(--rose); }
  .bar.full { stroke: var(--gold); }
  .in { position: relative; font-size: 0.62em; font-weight: 700; line-height: 1; }
</style>
