/** Tiny in-memory router: the app has a handful of screens and no URLs to share. */
import { app, save } from './store.svelte';

export type Route =
  | { name: 'home' }
  | { name: 'topic'; id: string; tab: 'dars' | 'mashq'; ex: number }
  | { name: 'playground' }
  | { name: 'exams' }
  | { name: 'exam'; sec: number }
  | { name: 'settings' };

export const nav = $state({ route: { name: 'home' } as Route, history: [] as Route[], examActive: false });

export function go(r: Route) {
  if (nav.examActive && !confirm('Imtihondan chiqasizmi? Natija saqlanmaydi.')) return;
  nav.examActive = false;
  nav.history.push(nav.route);
  if (nav.history.length > 40) nav.history.shift();
  nav.route = r;
  if (r.name === 'topic') {
    app.saved.last = { topic: r.id, tab: r.tab, ex: r.ex };
    save();
  }
  document.querySelector('main')?.scrollTo({ top: 0 });
}

export function openTopic(id: string, tab: 'dars' | 'mashq' = 'dars', ex = 0) {
  go({ name: 'topic', id, tab, ex });
}

export function back() {
  const r = nav.history.pop();
  if (r) nav.route = r;
}
