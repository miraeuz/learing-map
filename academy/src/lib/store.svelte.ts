/** Learner progress, saved in localStorage on this computer only. */
import { allTopics, topicById, xpFor, type Exercise } from './course';

const KEY = 'mirae-academy:v1';
const VERSION = 1;

export interface ExamRecord { best: number; passed: boolean; at: number; tries: number }
export interface Saved {
  v: number;
  name: string;
  theme: 'dark' | 'light';
  solved: Record<string, number>;      // exercise id → time solved
  revealed: Record<string, number>;    // solution was opened before solving
  attempts: Record<string, number>;
  drafts: Record<string, string>;
  read: Record<string, number>;        // topic id → lesson finished
  xp: number;
  activity: Record<string, number>;    // yyyy-mm-dd → xp earned that day
  exams: Record<string, ExamRecord>;
  last: { topic: string; tab: 'dars' | 'mashq'; ex: number } | null;
  playground: string;
  notes: Record<string, string>;       // topic id → the learner's own notes
  sideCollapsed: boolean;
  createdAt: number;
}

function fresh(): Saved {
  return {
    v: VERSION, name: '', theme: 'dark', solved: {}, revealed: {}, attempts: {}, drafts: {}, read: {},
    xp: 0, activity: {}, exams: {}, last: null, notes: {}, sideCollapsed: false,
    playground: '# Bu yerda erkin tajriba qiling\nism = input("Ismingiz: ")\nfor i in range(3):\n    print(f"{i + 1}. Salom, {ism}!")\n',
    createdAt: Date.now(),
  };
}

function load(): Saved {
  try {
    const s = JSON.parse(localStorage.getItem(KEY) ?? 'null');
    if (s && typeof s === 'object' && s.v === VERSION) return { ...fresh(), ...s };
  } catch { /* storage unavailable or corrupt — start fresh */ }
  return fresh();
}

export const app = $state({ saved: load(), toast: null as null | { text: string; xp?: number; tone?: 'ok' | 'info' | 'gold'; id: number } });

let timer: ReturnType<typeof setTimeout> | null = null;
export function save() {
  if (timer) clearTimeout(timer);
  timer = setTimeout(() => {
    try { localStorage.setItem(KEY, JSON.stringify(app.saved)); } catch { /* ignore quota */ }
  }, 250);
}

const UZ_MONTHS = ['yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun', 'iyul', 'avgust', 'sentabr', 'oktabr', 'noyabr', 'dekabr'];
const UZ_DAYS = ['yakshanba', 'dushanba', 'seshanba', 'chorshanba', 'payshanba', 'juma', 'shanba'];
/** "seshanba, 13-oktabr" — Intl has no reliable Uzbek locale in every runtime. */
export function uzDate(d: Date, opts: { weekday?: boolean; year?: boolean } = {}) {
  const s = `${d.getDate()}-${UZ_MONTHS[d.getMonth()]}${opts.year ? ` ${d.getFullYear()}-yil` : ''}`;
  return opts.weekday ? `${UZ_DAYS[d.getDay()]}, ${s}` : s;
}

export const today = (d = new Date()) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;

let toastSeq = 0;
export function toast(text: string, opts: { xp?: number; tone?: 'ok' | 'info' | 'gold'; ms?: number } = {}) {
  const id = ++toastSeq;
  const { ms = 2600, ...rest } = opts;
  app.toast = { text, id, ...rest };
  setTimeout(() => { if (app.toast?.id === id) app.toast = null; }, ms);
}

function addXp(n: number) {
  if (n <= 0) return;
  const before = levelOf(app.saved.xp).level;
  app.saved.xp += n;
  const d = today();
  app.saved.activity[d] = (app.saved.activity[d] ?? 0) + n;
  const after = levelOf(app.saved.xp).level;
  if (after > before) setTimeout(() => toast(`Yangi daraja: ${after} — ${levelOf(app.saved.xp).rank}!`, { tone: 'gold' }), 900);
}

export function markSolved(e: Exercise) {
  const s = app.saved;
  if (s.solved[e.id]) return false;
  s.solved[e.id] = Date.now();
  const xp = s.revealed[e.id] ? 0 : xpFor(e);
  addXp(xp);
  save();
  return xp;
}

export function unmarkLink(id: string) {
  delete app.saved.solved[id];
  save();
}

export function markRevealed(id: string) {
  if (!app.saved.solved[id]) app.saved.revealed[id] = Date.now();
  save();
}

export function addAttempt(id: string) {
  app.saved.attempts[id] = (app.saved.attempts[id] ?? 0) + 1;
  save();
}

export function markRead(topicId: string) {
  if (app.saved.read[topicId]) return;
  app.saved.read[topicId] = Date.now();
  addXp(20);
  save();
  toast('Dars oʻqildi', { xp: 20, tone: 'ok' });
}

export function setDraft(id: string, code: string) {
  app.saved.drafts[id] = code;
  save();
}

export function recordExam(sec: number, score: number, passed: boolean) {
  const prev = app.saved.exams[sec];
  const firstPass = passed && !prev?.passed;
  app.saved.exams[sec] = {
    best: Math.max(prev?.best ?? 0, score),
    passed: passed || !!prev?.passed,
    at: Date.now(),
    tries: (prev?.tries ?? 0) + 1,
  };
  if (firstPass) addXp(200);
  save();
  return firstPass;
}

export function setName(name: string) {
  app.saved.name = name.trim().replace(/\s+/g, ' ').slice(0, 60);
  save();
  window.mirae?.license.rename(app.saved.name).catch(() => {});
}

export function setTheme(t: 'dark' | 'light') {
  app.saved.theme = t;
  document.documentElement.dataset.theme = t;
  save();
}

export function resetProgress() {
  const keep = { name: app.saved.name, theme: app.saved.theme, notes: app.saved.notes, sideCollapsed: app.saved.sideCollapsed };
  app.saved = { ...fresh(), ...keep };
  try { localStorage.setItem(KEY, JSON.stringify(app.saved)); } catch { /* ignore */ }
}

export function exportBackup(): string {
  return JSON.stringify({ app: 'mirae-academy', exported: new Date().toISOString(), data: app.saved }, null, 2);
}

export function importBackup(text: string): boolean {
  try {
    const j = JSON.parse(text);
    const d = j?.app === 'mirae-academy' ? j.data : null;
    if (!d || d.v !== VERSION || typeof d.solved !== 'object') return false;
    app.saved = { ...fresh(), ...d };
    save();
    return true;
  } catch {
    return false;
  }
}

// ---------- derived numbers ----------
const RANKS = ['Yangi boshlovchi', 'Qiziquvchi', 'Oʻquvchi', 'Izlanuvchi', 'Kod yozuvchi', 'Dasturchi', 'Tajribali', 'Usta', 'Ekspert', 'Mirae ustozi'];

/** Level n needs 50·n·(n+1) XP in total: 100, 300, 600, 1000, … */
export function levelOf(xp: number) {
  let level = 0;
  while (50 * (level + 1) * (level + 2) <= xp) level++;
  const base = 50 * level * (level + 1);
  const next = 50 * (level + 1) * (level + 2);
  return { level: level + 1, into: xp - base, need: next - base, rank: RANKS[Math.min(RANKS.length - 1, Math.floor(level / 2))] };
}

export function topicProgress(topicId: string) {
  const t = topicById.get(topicId);
  if (!t) return { done: 0, total: 0, pct: 0, read: false };
  const done = t.ex.reduce((n, e) => n + (app.saved.solved[e.id] ? 1 : 0), 0);
  return { done, total: t.ex.length, pct: done / t.ex.length, read: !!app.saved.read[topicId] };
}

export function streak(): number {
  const act = app.saved.activity;
  let n = 0;
  const d = new Date();
  if (!act[today(d)]) d.setDate(d.getDate() - 1); // today not started yet — streak still alive
  while (act[today(d)]) {
    n++;
    d.setDate(d.getDate() - 1);
  }
  return n;
}

export function solvedCount() {
  return Object.keys(app.saved.solved).length;
}

/** First topic that is not finished — where "Davom etish" goes. */
export function nextTopic() {
  const last = app.saved.last && topicById.get(app.saved.last.topic);
  if (last && topicProgress(last.id).pct < 1) return last;
  return allTopics.find((t) => topicProgress(t.id).pct < 1) ?? allTopics[allTopics.length - 1];
}
