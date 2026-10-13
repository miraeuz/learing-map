/** Typed access to the verified course (built by content/build.py). */
import raw from '../data/course.json';

export type Block =
  | { t: 'p'; html: string }
  | { t: 'h'; text: string }
  | { t: 'ul'; items: string[] }
  | { t: 'tip'; html: string }
  | { t: 'warn'; html: string }
  | { t: 'table'; rows: string[][] }
  | { t: 'code'; code: string; stdin: string; norun: boolean; out: string; err: { type: string; msg: string; line: number | null } | null };

interface ExBase { id: string; lv: number }
export interface QuizEx extends ExBase { kind: 'quiz'; q: string; code: string | null; options: string[]; answer: number; mono: boolean; why: string | null }
export interface FuncEx extends ExBase { kind: 'func'; title: string; prompt: string; starter: string; tests: { call: string; expect?: string; raises?: string }[]; solution: string; hint: string | null; name: string }
export interface ProgEx extends ExBase { kind: 'prog'; title: string; prompt: string; starter: string; tests: { stdin: string; expect: string }[]; solution: string; hint: string | null }
export interface LinkEx extends ExBase { kind: 'link'; site: string; siteName: string; title: string; url: string; note: string | null }
export type Exercise = QuizEx | FuncEx | ProgEx | LinkEx;
export type CodeEx = FuncEx | ProgEx;

export interface Topic { id: string; slug: string; title: string; short: string; mins: number; level: number; blocks: Block[]; ex: Exercise[] }
export interface Section { num: number; title: string; short: string; emoji: string; topics: Topic[] }

export const course = raw as unknown as { sections: Section[]; totals: Record<string, number> };
export const sections = course.sections;
export const allTopics: Topic[] = sections.flatMap((s) => s.topics);
export const topicById = new Map(allTopics.map((t) => [t.id, t]));
export const sectionOf = (topicId: string) => sections.find((s) => s.num === Number(topicId.split('.')[0]))!;
export const totalExercises = allTopics.reduce((n, t) => n + t.ex.length, 0);

export function neighbours(topicId: string): { prev: Topic | null; next: Topic | null } {
  const i = allTopics.findIndex((t) => t.id === topicId);
  return { prev: allTopics[i - 1] ?? null, next: allTopics[i + 1] ?? null };
}

/** Difficulty band per section — the course climbs from beginner to confident. */
export const BANDS: Record<number, { label: string; tone: 'turq' | 'lapis' | 'gold' | 'rose' }> = {
  2: { label: 'Boshlangʻich', tone: 'turq' },
  3: { label: 'Boshlangʻich', tone: 'turq' },
  4: { label: 'Asosiy', tone: 'lapis' },
  5: { label: 'Oʻrta', tone: 'lapis' },
  6: { label: 'Oʻrta+', tone: 'gold' },
  7: { label: 'Ilgʻor', tone: 'rose' },
};

export const KIND_LABEL: Record<Exercise['kind'], string> = {
  quiz: 'Savol',
  func: 'Funksiya',
  prog: 'Dastur',
  link: 'Online masala',
};

/** XP for solving an exercise, by kind and difficulty. */
export function xpFor(e: Exercise): number {
  if (e.kind === 'quiz') return 5 + 5 * e.lv;
  if (e.kind === 'link') return 25;
  return 10 + 10 * e.lv;
}

export function exTitle(e: Exercise): string {
  if (e.kind === 'quiz') return e.code ? 'Natijani toping' : 'Savol';
  return e.title;
}

export const plain = (html: string) => html.replace(/<[^>]+>/g, '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
