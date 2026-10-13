<script lang="ts">
  // Mirae Academy mark: an eight-point girih star (the Samarkand tile motif) with a code caret inside.
  let { size = '2.4rem', glow = false }: { size?: string; glow?: boolean } = $props();

  const star = (R: number, cx = 50, cy = 50) => {
    const r = (R * Math.cos(Math.PI / 4)) / Math.cos(Math.PI / 8);
    const pts: string[] = [];
    for (let k = 0; k < 16; k++) {
      const a = (k * Math.PI) / 8 - Math.PI / 2;
      const rad = k % 2 === 0 ? R : r;
      pts.push(`${(cx + rad * Math.cos(a)).toFixed(2)},${(cy + rad * Math.sin(a)).toFixed(2)}`);
    }
    return pts.join(' ');
  };
  const uid = Math.random().toString(36).slice(2, 8);
</script>

<svg viewBox="0 0 100 100" width={size} height={size} class:glow aria-hidden="true">
  <defs>
    <linearGradient id="g1-{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#5b84ff" />
      <stop offset="1" stop-color="#1f3bb8" />
    </linearGradient>
    <linearGradient id="g2-{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#ffd77a" />
      <stop offset="1" stop-color="#e09a1a" />
    </linearGradient>
  </defs>
  <polygon points={star(48)} fill="url(#g1-{uid})" />
  <polygon points={star(48)} fill="none" stroke="url(#g2-{uid})" stroke-width="3" stroke-linejoin="round" />
  <polygon points={star(30)} fill="none" stroke="#39dcc8" stroke-width="2.4" stroke-linejoin="round" opacity="0.9" />
  <path d="M38 40 L28 50 L38 60 M62 40 L72 50 L62 60" fill="none" stroke="#fff" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round" />
  <path d="M54 37 L46 63" stroke="url(#g2-{uid})" stroke-width="5.5" stroke-linecap="round" />
</svg>

<style>
  svg { display: block; flex: none; }
  .glow { filter: drop-shadow(0 0 0.9rem rgb(74 116 255 / 0.55)); }
</style>
