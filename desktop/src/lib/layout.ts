import { topics, stages, type Stage } from './data';

/** Map coordinate system: a fixed-width column that the SVG scales to fit. */
export const MAP_W = 600;
const SPACING = 116;
const PAD_TOP = 230;
const PAD_BOTTOM = 160;

export interface Pt {
  x: number;
  y: number;
}

export interface Island {
  c: Pt;
  r: number;
  emoji: string;
  seed: number;
}

export interface Sign {
  c: Pt;
  stage: Stage;
  index: number;
}

const ISLAND_EMOJI = ['🏰', '🏴‍☠️', '🐚', '⛵', '🗼', '💎', '🦜', '🗺️', '⚓', '🦀', '🐙', '🛖'];

export const MAP_H = PAD_TOP + PAD_BOTTOM + (topics.length - 1) * SPACING;

export const nodes: Pt[] = topics.map((_, i) => ({
  x: MAP_W / 2 + 150 * Math.sin(i * 0.62),
  y: MAP_H - PAD_BOTTOM - i * SPACING,
}));

export const signs: Sign[] = [];
const signIdx = new Set<number>();
topics.forEach((t, i) => {
  if (i === 0 || t.stage !== topics[i - 1].stage) {
    signIdx.add(i);
    const n = nodes[i];
    const below = i === 0 ? { x: n.x, y: n.y + 72 } : { x: (n.x + nodes[i - 1].x) / 2, y: n.y + SPACING / 2 };
    const x = below.x > MAP_W / 2 ? MAP_W * 0.22 : MAP_W * 0.78;
    signs.push({ c: { x, y: below.y }, stage: stages[t.stage], index: i });
  }
});

export const islands: Island[] = [];
{
  let k = 0;
  for (let i = 1; i < topics.length; i += 3) {
    if (signIdx.has(i) || signIdx.has(i + 1)) continue;
    const n = nodes[i];
    const left = n.x > MAP_W / 2;
    islands.push({
      c: { x: left ? MAP_W * 0.13 : MAP_W * 0.87, y: n.y },
      r: 84,
      emoji: ISLAND_EMOJI[k % ISLAND_EMOJI.length],
      seed: i * 7 + 3,
    });
    k++;
  }
}

export const trophy: Pt = { x: MAP_W / 2, y: nodes[nodes.length - 1].y - 150 };

/** Cubic segment between node i and i+1. */
export function seg(i: number): [Pt, Pt, Pt, Pt] {
  const a = nodes[i];
  const b = nodes[i + 1];
  const m = (a.y + b.y) / 2;
  return [a, { x: a.x, y: m }, { x: b.x, y: m }, b];
}

export function segPoint(i: number, t: number): Pt {
  const [p0, p1, p2, p3] = seg(i);
  const u = 1 - t;
  return {
    x: u * u * u * p0.x + 3 * u * u * t * p1.x + 3 * u * t * t * p2.x + t * t * t * p3.x,
    y: u * u * u * p0.y + 3 * u * u * t * p1.y + 3 * u * t * t * p2.y + t * t * t * p3.y,
  };
}

export function routeD(): string {
  const n = nodes;
  let d = `M ${n[0].x} ${n[0].y + 150} L ${n[0].x} ${n[0].y}`;
  for (let i = 0; i < n.length - 1; i++) {
    const [, p1, p2, p3] = seg(i);
    d += ` C ${p1.x} ${p1.y} ${p2.x} ${p2.y} ${p3.x} ${p3.y}`;
  }
  return d + ` L ${trophy.x} ${trophy.y}`;
}

/** Organic island outline. */
export function blobD(c: Pt, r: number, seed: number, scale: number): string {
  const n = 16;
  const pts: Pt[] = [];
  for (let k = 0; k < n; k++) {
    const a = (k / n) * Math.PI * 2;
    const w = 0.86 + 0.14 * Math.sin(a * 3 + seed) + 0.06 * Math.cos(a * 5 + seed * 2);
    pts.push({ x: c.x + Math.cos(a) * r * 1.2 * w * scale, y: c.y + Math.sin(a) * r * 0.78 * w * scale });
  }
  const mid = (p: Pt, q: Pt) => ({ x: (p.x + q.x) / 2, y: (p.y + q.y) / 2 });
  const start = mid(pts[n - 1], pts[0]);
  let d = `M ${start.x.toFixed(1)} ${start.y.toFixed(1)}`;
  for (let k = 0; k < n; k++) {
    const p = pts[k];
    const m = mid(p, pts[(k + 1) % n]);
    d += ` Q ${p.x.toFixed(1)} ${p.y.toFixed(1)} ${m.x.toFixed(1)} ${m.y.toFixed(1)}`;
  }
  return d + ' Z';
}

/** Palm tree as a list of SVG path strings: trunk first, then leaves. */
export function palm(base: Pt, h: number, lean: number): { trunk: string; leaves: string[]; top: Pt } {
  const top = { x: base.x + lean, y: base.y - h };
  const trunk = `M ${base.x} ${base.y} Q ${base.x + lean * 0.1} ${base.y - h * 0.6} ${top.x} ${top.y}`;
  const len = h * 0.55;
  const leaves = [-160, -125, -90, -55, -20, 20, 160].map((deg) => {
    const a = (deg * Math.PI) / 180;
    const tip = { x: top.x + Math.cos(a) * len, y: top.y + Math.sin(a) * len + len * 0.35 };
    const nx = -Math.sin(a) * len * 0.22;
    const ny = Math.cos(a) * len * 0.22;
    const mid = { x: (top.x + tip.x) / 2, y: (top.y + tip.y) / 2 };
    return `M ${top.x} ${top.y} Q ${mid.x + nx} ${mid.y + ny - len * 0.15} ${tip.x} ${tip.y} Q ${mid.x - nx * 0.3} ${mid.y - ny * 0.3} ${top.x} ${top.y} Z`;
  });
  return { trunk, leaves, top };
}
