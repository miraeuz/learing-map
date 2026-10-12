import roadmap from '../data/roadmap.json';

export interface Stage {
  id: number;
  name: string;
  emoji: string;
  tagline: string;
  color: string;
}

export interface PracticeLink {
  site: string;
  title: string;
  url: string;
}

export interface Topic {
  stage: number;
  name: string;
  info: string;
  links: PracticeLink[];
}

export const stages: Stage[] = roadmap.stages;
export const topics: Topic[] = roadmap.topics;

export const stageStart: number[] = stages.map((s) => topics.findIndex((t) => t.stage === s.id));

export interface SiteStyle {
  badge: string;
  name: string;
  color: string;
}

const S = (badge: string, name: string, color: string): SiteStyle => ({ badge, name, color });

export const sites: Record<string, SiteStyle> = {
  cf: S('CF', 'Codeforces', '#1F8ACB'),
  lc: S('LC', 'LeetCode', '#E8890C'),
  cses: S('CSES', 'CSES', '#3F4A5A'),
  acmp: S('ACMP', 'acmp.ru', '#D84315'),
  robo: S('ROBO', 'RoboContest', '#2E7D32'),
  atcoder: S('AC', 'AtCoder', '#222222'),
  ys: S('LIB', 'Library Checker', '#6A1B9A'),
  cpa: S('CPA', 'cp-algorithms', '#00897B'),
  spoj: S('SPOJ', 'SPOJ', '#3B5998'),
  uva: S('UVa', 'UVa Online Judge', '#8D6E63'),
  timus: S('TIM', 'Timus', '#5D4037'),
  kattis: S('KAT', 'Kattis', '#E53935'),
  codechef: S('CC', 'CodeChef', '#5B4638'),
  hackerrank: S('HR', 'HackerRank', '#1BA94C'),
  usaco: S('USA', 'USACO', '#1565C0'),
  vjudge: S('VJ', 'Virtual Judge', '#455A64'),
  poj: S('POJ', 'POJ', '#546E7A'),
  github: S('GH', 'GitHub', '#24292F'),
  icpc: S('ICPC', 'ICPC', '#0D47A1'),
  clist: S('CL', 'CLIST', '#00695C'),
  topcoder: S('TC', 'TopCoder', '#1E88B8'),
  lightoj: S('LOJ', 'LightOJ', '#E64A19'),
  szkopul: S('SZK', 'Szkopuł', '#C62828'),
  dmoj: S('DMOJ', 'DMOJ', '#B8860B'),
  ojuz: S('OJ', 'oj.uz', '#7B1FA2'),
  csacademy: S('CSA', 'CS Academy', '#00838F'),
  euler: S('PE', 'Project Euler', '#424242'),
  eolymp: S('EO', 'E-olymp', '#1976D2'),
  toph: S('TPH', 'Toph', '#00897B'),
  hackerearth: S('HE', 'HackerEarth', '#323754'),
  hdu: S('HDU', 'HDU', '#6D4C41'),
  baekjoon: S('BOJ', 'Baekjoon', '#0076C0'),
};

export const siteOf = (key: string): SiteStyle => sites[key] ?? S('WEB', 'Veb-sahifa', '#607D8B');

/** Lower-cases and strips Uzbek apostrophes/diacritics so search is forgiving. */
export function normalize(s: string): string {
  return s
    .toLowerCase()
    .replace(/[ʻʼ'`‘’]/g, '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '');
}
