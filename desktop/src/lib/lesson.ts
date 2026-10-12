import { topics } from './data';
import details from '../data/details.json';
import { statusOf, isOpened, solvedCount, learnedCount } from './store.svelte';

export interface Detail {
  k: string[]; // what to learn
  c: string; // complexity
  p: string[]; // pitfalls
  h: number; // estimated hours
  w: string; // when you need it
}

export const detailOf = (i: number) => details[i] as Detail;

export interface Step {
  title: string;
  hint: string;
  done: boolean;
  progress?: [number, number];
  url?: string;
}

/** The five-step lesson plan a teacher would give for one topic, with live progress. */
export function lessonSteps(i: number): Step[] {
  const d = detailOf(i);
  const t = topics[i];
  const theory = t.links.find((l) => l.title.startsWith('Nazariya: ')) ?? t.links[0];
  const learned = learnedCount(i, d.k.length);
  const solved = solvedCount(i);
  return [
    {
      title: 'Nazariyani oʻqing',
      hint: theory.title.startsWith('Nazariya: ') ? 'cp-algorithms maqolasi' : 'Birinchi manba',
      done: isOpened(theory.url),
      url: theory.url,
    },
    {
      title: 'Asosiy gʻoyalarni belgilang',
      hint: 'Har birini tushunib, oʻzingiz tushuntira olsangiz',
      done: learned === d.k.length,
      progress: [learned, d.k.length],
    },
    {
      title: '5 ta masala yeching',
      hint: 'Oson masalalardan boshlang',
      done: solved >= 5,
      progress: [Math.min(solved, 5), 5],
    },
    {
      title: '10 ta masala yeching',
      hint: 'Shablonni yoddan yozishni mashq qiling',
      done: solved >= 10,
      progress: [Math.min(solved, 10), 10],
    },
    {
      title: '"Ha, bilaman" deb belgilang',
      hint: 'Kontestda xatosiz yoza olsangiz',
      done: statusOf(i) === 'done',
    },
  ];
}

export const hoursText = (h: number) => (h <= 1 ? '~1 soat' : `~${h} soat`);
