<script lang="ts">
  import type { LinkEx } from '../lib/course';
  import { xpFor } from '../lib/course';
  import { app, markSolved, unmarkLink, toast } from '../lib/store.svelte';

  let { ex, onNext }: { ex: LinkEx; onNext?: () => void } = $props();
  const solved = $derived(!!app.saved.solved[ex.id]);

  const SITE: Record<string, { color: string; about: string; how: string }> = {
    exercism: { color: '#7d5cf6', about: 'Exercism — bepul, mentorli mashqlar platformasi. Python treki bosqichma-bosqich tuzilgan.', how: 'Saytda roʻyxatdan oʻting, Python trekiga qoʻshiling va mashqni brauzerdagi muharrirda yeching.' },
    lc: { color: '#f7a21b', about: 'LeetCode — dunyodagi eng mashhur algoritmik masalalar bazasi. Ish suhbatlariga tayyorgarlikda ishlatiladi.', how: 'Tilni «Python3» qilib tanlang. Funksiya shablonini toʻldiring va «Submit» bosing.' },
    cses: { color: '#39dcc8', about: 'CSES — Finlyandiya universiteti tuzgan klassik olimpiada masalalari toʻplami.', how: 'Kirish standart oqimdan (input()) oʻqiladi, natija print() bilan chiqariladi. Tilni Python3 qilib yuboring.' },
    acmp: { color: '#ff7a8a', about: 'acmp.ru — maktab olimpiadalari uchun mashhur rus tilidagi masalalar arxivi.', how: 'Masala sharti rus tilida. Kirish/chiqish odatda standart oqim orqali. Tilni Python qilib yuboring.' },
  };
  const s = $derived(SITE[ex.site] ?? SITE.exercism);

  function toggle() {
    if (solved) {
      unmarkLink(ex.id);
      return;
    }
    const xp = markSolved(ex);
    toast('Online masala belgilandi', { xp: xp || undefined, tone: 'ok' });
  }
</script>

<div class="link" style:--site={s.color}>
  <div class="card">
    <div class="top">
      <span class="site">{ex.siteName}</span>
      <span class="xp">+{xpFor(ex)} XP</span>
    </div>
    <h3>{ex.title}</h3>
    {#if ex.note}<p class="note">💡 {@html ex.note}</p>{/if}
    <p class="about">{s.about}</p>
    <div class="how"><b>Qanday yechiladi:</b> {s.how}</div>
    <div class="acts">
      <a class="btn-primary" href={ex.url} target="_blank" rel="noopener noreferrer">Masalani ochish ↗</a>
      <button class={solved ? 'btn-ghost done' : 'btn-ghost'} onclick={toggle}>
        {solved ? '✓ Yechildi (bekor qilish)' : 'Yechdim — belgilash'}
      </button>
    </div>
    <p class="url">{ex.url}</p>
  </div>
  <aside class="side">
    <h4>Online masalalarni yechish odatlari</h4>
    <ol>
      <li>Shartni <b>ikki marta</b> oʻqing, kirish va chiqish formatini yozib oling.</li>
      <li>Avval namunaviy testni qoʻlda hisoblang.</li>
      <li>Yechimni «Kod maydoni»da sinab koʻring, keyin yuboring.</li>
      <li>«Wrong Answer» — chegaraviy holatlarni tekshiring: 0, 1, boʻsh roʻyxat, juda katta son.</li>
    </ol>
    {#if onNext}<button class="btn-ghost sm" onclick={onNext}>Keyingi mashq →</button>{/if}
  </aside>
</div>

<style>
  .link { display: grid; grid-template-columns: minmax(0, 1.3fr) minmax(16rem, 0.7fr); gap: 1.2rem; align-items: start; }
  .card {
    display: grid; gap: 0.9rem; padding: 1.6rem 1.7rem; border-radius: var(--r-l);
    background: linear-gradient(145deg, color-mix(in srgb, var(--site) 14%, var(--surface)), var(--surface) 60%);
    border: 1px solid color-mix(in srgb, var(--site) 40%, var(--line));
  }
  .top { display: flex; justify-content: space-between; align-items: center; }
  .site { padding: 0.3rem 0.75rem; border-radius: 2rem; background: color-mix(in srgb, var(--site) 22%, transparent); color: var(--site); font-weight: 700; font-size: 0.82rem; }
  .xp { color: var(--gold); font-weight: 700; font-size: 0.85rem; }
  h3 { margin: 0; font-family: var(--display); font-size: 1.6rem; font-weight: 600; }
  .note { margin: 0; padding: 0.7rem 0.9rem; border-radius: var(--r-s); background: rgb(247 189 70 / 0.1); line-height: 1.5; }
  .note :global(code) { font-size: 0.9em; color: var(--gold); }
  .about { margin: 0; color: var(--text-2); line-height: 1.6; }
  .how { font-size: 0.93rem; color: var(--text-2); line-height: 1.55; padding: 0.75rem 0.9rem; border-radius: var(--r-s); background: var(--bg-2); border: 1px solid var(--line); }
  .how b { color: var(--text); }
  .acts { display: flex; gap: 0.7rem; flex-wrap: wrap; margin-top: 0.3rem; }
  .acts a { text-decoration: none; }
  .done { border-color: var(--turq) !important; color: var(--turq) !important; }
  .url { margin: 0; font: 0.78rem var(--mono); color: var(--text-3); word-break: break-all; }
  .side { padding: 1.3rem 1.4rem; border-radius: var(--r-l); background: var(--surface); border: 1px solid var(--line); display: grid; gap: 0.7rem; }
  .side h4 { margin: 0; font-size: 0.98rem; }
  ol { margin: 0; padding-left: 1.2rem; display: grid; gap: 0.5rem; color: var(--text-2); font-size: 0.92rem; line-height: 1.5; }
  ol b { color: var(--text); }
  .side .btn-ghost { justify-self: start; }
  @media (max-width: 70em) { .link { grid-template-columns: 1fr; } }
</style>
