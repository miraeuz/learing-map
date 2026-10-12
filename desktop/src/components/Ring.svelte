<script lang="ts">
  let {
    value,
    size = '4rem',
    stroke = 7,
    color = 'var(--gold)',
    track = 'var(--paper-2)',
    label = '',
  }: { value: number; size?: string; stroke?: number; color?: string; track?: string; label?: string } = $props();

  const r = 26;
  const c = 2 * Math.PI * r;
</script>

<div class="ring" style:width={size} style:height={size}>
  <svg viewBox="0 0 64 64" aria-hidden="true">
    <circle cx="32" cy="32" {r} fill="none" stroke={track} stroke-width={stroke} />
    <circle
      cx="32" cy="32" {r} fill="none" stroke={color} stroke-width={stroke} stroke-linecap="round"
      stroke-dasharray={c} stroke-dashoffset={c * (1 - Math.max(0, Math.min(1, value)))}
      transform="rotate(-90 32 32)"
    />
  </svg>
  {#if label}<span>{label}</span>{/if}
</div>

<style>
  .ring { position: relative; display: grid; place-items: center; flex: none; }
  svg { position: absolute; inset: 0; width: 100%; height: 100%; }
  circle { transition: stroke-dashoffset 0.6s cubic-bezier(0.2, 0.8, 0.2, 1); }
  span { position: relative; font-weight: 900; font-size: 1rem; color: var(--ink); }
</style>
