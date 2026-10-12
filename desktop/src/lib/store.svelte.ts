import { topics, stages } from './data';

export type Status = 'done' | 'practice';

interface Saved {
  status: Record<number, Status>;
  solved: Record<string, number>; // url -> timestamp
  notes: Record<number, string>;
  welcomed: boolean;
}

const KEY = 'icpc-yoli-v1';

function load(): Saved {
  const empty: Saved = { status: {}, solved: {}, notes: {}, welcomed: false };
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return empty;
    const v = JSON.parse(raw);
    return {
      status: v.status ?? {},
      solved: v.solved ?? {},
      notes: v.notes ?? {},
      welcomed: !!v.welcomed,
    };
  } catch {
    return empty;
  }
}

export const app = $state({
  saved: load(),
  selected: 0,
  searchOpen: false,
  welcomeOpen: false,
  helpOpen: false,
  panelOpen: false, // used on narrow windows where the panel is a drawer
});

export function save() {
  try {
    localStorage.setItem(KEY, JSON.stringify(app.saved));
  } catch {
    /* storage full or blocked: keep working in memory */
  }
}

export const statusOf = (i: number): Status | undefined => app.saved.status[i];
export const isLocked = (i: number) => i > 0 && app.saved.status[i - 1] === undefined;
export const isSolved = (url: string) => app.saved.solved[url] !== undefined;

export function solvedCount(i: number): number {
  let n = 0;
  for (const l of topics[i].links) if (app.saved.solved[l.url] !== undefined) n++;
  return n;
}

/** First unanswered open level, else the first "practice" level, else the last. */
export function currentIndex(): number {
  const st = app.saved.status;
  for (let i = 0; i < topics.length; i++) if (st[i] === undefined && !(i > 0 && st[i - 1] === undefined)) return i;
  for (let i = 0; i < topics.length; i++) if (st[i] === 'practice') return i;
  return topics.length - 1;
}

export function frontier(): number {
  for (let i = 0; i < topics.length; i++) if (app.saved.status[i] === undefined) return i;
  return topics.length;
}

export function answer(i: number, ok: boolean) {
  if (isLocked(i)) return;
  app.saved.status[i] = ok ? 'done' : 'practice';
  save();
}

export function clearAnswer(i: number) {
  delete app.saved.status[i];
  save();
}

export function toggleSolved(url: string) {
  if (app.saved.solved[url] !== undefined) delete app.saved.solved[url];
  else app.saved.solved[url] = Date.now();
  save();
}

export function setNote(i: number, text: string) {
  if (text.trim()) app.saved.notes[i] = text;
  else delete app.saved.notes[i];
  save();
}

export function select(i: number) {
  app.selected = Math.max(0, Math.min(topics.length - 1, i));
  app.panelOpen = true;
}

export function markWelcomed() {
  app.saved.welcomed = true;
  save();
}

export function resetAll() {
  app.saved = { status: {}, solved: {}, notes: {}, welcomed: true };
  app.selected = 0;
  save();
}

export function exportJson(): string {
  return JSON.stringify({ app: 'icpc-yoli', version: 1, exported: new Date().toISOString(), ...app.saved }, null, 2);
}

export function importJson(text: string): boolean {
  try {
    const v = JSON.parse(text);
    if (typeof v !== 'object' || v === null || typeof v.status !== 'object') return false;
    app.saved = { status: v.status ?? {}, solved: v.solved ?? {}, notes: v.notes ?? {}, welcomed: true };
    save();
    return true;
  } catch {
    return false;
  }
}

export interface Totals {
  levels: number;
  done: number;
  practice: number;
  problems: number;
  solved: number;
}

export function totals(): Totals {
  const all = new Set<string>();
  for (const t of topics) for (const l of t.links) all.add(l.url);
  let solved = 0;
  for (const u of all) if (app.saved.solved[u] !== undefined) solved++;
  const vals = Object.values(app.saved.status);
  return {
    levels: topics.length,
    done: vals.filter((s) => s === 'done').length,
    practice: vals.filter((s) => s === 'practice').length,
    problems: all.size,
    solved,
  };
}

export function stageTotals(stageId: number) {
  let total = 0;
  let done = 0;
  let probs = 0;
  let solved = 0;
  topics.forEach((t, i) => {
    if (t.stage !== stageId) return;
    total++;
    if (app.saved.status[i] === 'done') done++;
    probs += t.links.length;
    solved += solvedCount(i);
  });
  return { total, done, probs, solved };
}

export const stageCount = stages.length;
