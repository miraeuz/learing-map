<script lang="ts">
  import { sections, course, BANDS, allTopics, sectionOf } from '../lib/course';
  import { app, levelOf, streak, solvedCount, nextTopic, topicProgress, today, uzDate } from '../lib/store.svelte';
  import { go, openTopic } from '../lib/nav.svelte';
  import Ring from './Ring.svelte';

  const first = $derived((app.saved.name || '').split(' ')[0]);
  const hour = new Date().getHours();
  const greet = hour < 5 ? 'Xayrli tun' : hour < 11 ? 'Xayrli tong' : hour < 18 ? 'Xayrli kun' : 'Xayrli kech';
  const dateStr = uzDate(new Date(), { weekday: true });

  const lv = $derived(levelOf(app.saved.xp));
  const st = $derived(streak());
  const solved = $derived(solvedCount());
  const read = $derived(Object.keys(app.saved.read).length);
  const nt = $derived(nextTopic());
  const ntp = $derived(topicProgress(nt.id));
  const ntSec = $derived(sectionOf(nt.id));
  const fresh = $derived(solved === 0 && read === 0);

  function secStats(num: number) {
    const s = sections.find((x) => x.num === num)!;
    let d = 0, t = 0, full = 0;
    for (const tp of s.topics) {
      const p = topicProgress(tp.id);
      d += p.done; t += p.total; if (p.pct >= 1) full++;
    }
    return { pct: t ? d / t : 0, done: d, total: t, full };
  }

  // Activity heat-map: the last 20 weeks, Monday-first columns.
  const WEEKS = 30;
  const cells = $derived.by(() => {
    const out: { d: string; xp: number; future: boolean }[] = [];
    const end = new Date();
    const dow = (end.getDay() + 6) % 7;
    const start = new Date(end);
    start.setDate(end.getDate() - dow - 7 * (WEEKS - 1));
    for (let i = 0; i < WEEKS * 7; i++) {
      const d = new Date(start);
      d.setDate(start.getDate() + i);
      out.push({ d: today(d), xp: app.saved.activity[today(d)] ?? 0, future: d > end });
    }
    return out;
  });
  const heat = (xp: number) => (xp === 0 ? 0 : xp < 40 ? 1 : xp < 100 ? 2 : xp < 200 ? 3 : 4);
  const weekXp = $derived(cells.slice(-7).reduce((n, c) => n + c.xp, 0));

  const TIPS = [
    ['f-satr', 'f"{narx:,}" — sonni minglik ajratgich bilan chiqaradi: 1,250,000.'],
    ['Almashtirish', 'a, b = b, a — vaqtinchalik oʻzgaruvchisiz ikki qiymatni almashtiradi.'],
    ['Teskari', 's[::-1] — satr yoki roʻyxatni bir zumda teskari aylantiradi.'],
    ['Sanash', 'Counter(sozlar).most_common(3) — eng koʻp uchragan 3 ta soʻz.'],
    ['Kirish', 'list(map(int, input().split())) — bir qatordagi sonlarni roʻyxatga oʻqish.'],
    ['enumerate', 'for i, x in enumerate(a, 1) — indeksni 1 dan boshlab sanaydi.'],
    ['Zanjir', '0 < x < 10 — Python taqqoslashlarni zanjir qilib yozishga ruxsat beradi.'],
    ['print', 'print(*a, sep=", ") — roʻyxatni qavssiz, vergul bilan chiqaradi.'],
    ['Xatolar', 'Traceback pastdan yuqoriga oʻqiladi: avval xato turi va izohiga qarang.'],
    ['any / all', 'any(x < 0 for x in a) — birorta manfiy son bormi? Bir qatorda.'],
  ];
  const tip = TIPS[Math.floor(Date.now() / 86400000) % TIPS.length];
</script>

<div class="page">
  <header class="top">
    <div>
      <p class="date">{dateStr}</p>
      <h1>{greet}{first ? `, ${first}` : ''} <span class="wave" aria-hidden="true">👋</span></h1>
    </div>
    <div class="chips">
      <span class="chip fire" title="Ketma-ket faol kunlar"><b>🔥 {st}</b> kun</span>
      <span class="chip gold" title="Jami tajriba ochkolari"><b>⚡ {app.saved.xp.toLocaleString('ru-RU')}</b> XP</span>
    </div>
  </header>

  <section class="hero">
    <div class="cont">
      <div class="glow"></div>
      <p class="eyebrow">{fresh ? 'Birinchi qadam' : 'Davom eting'} · {ntSec.num}-boʻlim · {ntSec.title}</p>
      <h2>{nt.title}</h2>
      <p class="short">{nt.short}</p>
      <div class="pbar"><i style:width={`${ntp.pct * 100}%`}></i></div>
      <div class="meta">
        <span>{ntp.done} / {ntp.total} mashq</span>
        <span>⏱ ~{nt.mins} daqiqa</span>
        {#if ntp.read}<span class="ok">✓ dars oʻqilgan</span>{/if}
      </div>
      <div class="acts">
        <button class="btn-primary" onclick={() => openTopic(nt.id, ntp.read ? 'mashq' : 'dars')}>
          {fresh ? 'Oʻrganishni boshlash' : ntp.read ? 'Mashqlarni davom ettirish' : 'Darsni ochish'} →
        </button>
        {#if !fresh}<button class="btn-ghost" onclick={() => openTopic(nt.id, 'dars')}>Darsni takrorlash</button>{/if}
      </div>
    </div>

    <div class="stats">
      <div class="stat level">
        <Ring pct={lv.into / lv.need} size="4.2rem" stroke={3} tone="gold"><b class="lvn">{lv.level}</b></Ring>
        <div><small>Daraja</small><b>{lv.rank}</b><span>{lv.need - lv.into} XP keyingi darajagacha</span></div>
      </div>
      <div class="stat"><small>Yechilgan mashqlar</small><b>{solved}<em>/{course.totals.ex}</em></b><div class="mini"><i style:width={`${(solved / course.totals.ex) * 100}%`}></i></div></div>
      <div class="stat"><small>Oʻqilgan darslar</small><b>{read}<em>/{allTopics.length}</em></b><div class="mini t"><i style:width={`${(read / allTopics.length) * 100}%`}></i></div></div>
    </div>
  </section>

  <section class="row2">
    <div class="panel act">
      <div class="ph"><h3>Faollik</h3><span>Bu hafta: <b>{weekXp} XP</b></span></div>
      <div class="heat" style:--weeks={WEEKS}>
        {#each cells as c}
          <i class="h{heat(c.xp)}" class:future={c.future} title={`${c.d}: ${c.xp} XP`}></i>
        {/each}
      </div>
      <div class="legend">Kam <i class="h0"></i><i class="h1"></i><i class="h2"></i><i class="h3"></i><i class="h4"></i> Koʻp</div>
    </div>
    <div class="panel tip">
      <div class="ph"><h3>💡 Kun maslahati</h3><span>{tip[0]}</span></div>
      <p>{tip[1]}</p>
      <button class="btn-ghost sm" onclick={() => go({ name: 'playground' })}>Kod maydonida sinab koʻrish →</button>
    </div>
  </section>

  <div class="sh"><h3>Kurs xaritasi</h3><span>Boshlangʻichdan ilgʻor darajagacha — {sections.length} boʻlim</span></div>
  <section class="grid">
    {#each sections as s, i}
      {@const ss = secStats(s.num)}
      {@const band = BANDS[s.num]}
      {@const ex = app.saved.exams[s.num]}
      <article class="sec">
        <button class="sec-main" onclick={() => openTopic(s.topics.find((t) => topicProgress(t.id).pct < 1)?.id ?? s.topics[0].id)}>
          <div class="sec-top">
            <span class="emo" aria-hidden="true">{s.emoji}</span>
            <span class="band {band.tone}">{band.label}</span>
          </div>
          <small>{s.num}-boʻlim · {String(i + 1).padStart(2, '0')}</small>
          <h4>{s.title}</h4>
          <p>{s.short}</p>
          <div class="sec-bar"><i style:width={`${ss.pct * 100}%`}></i></div>
          <div class="sec-meta">
            <span>{s.topics.length} mavzu · {ss.total} mashq</span>
            <b>{Math.round(ss.pct * 100)}%</b>
          </div>
        </button>
        <button class="exam" class:passed={ex?.passed} onclick={() => go({ name: 'exam', sec: s.num })}>
          {#if ex?.passed}🏆 Imtihon topshirildi · {ex.best}%{:else if ex}📝 Imtihon · eng yaxshi {ex.best}%{:else}📝 Boʻlim imtihoni{/if}
        </button>
      </article>
    {/each}
  </section>
</div>

<style>
  .page { display: grid; gap: 1.5rem; padding: 2rem clamp(1.5rem, 3vw, 3rem) 3rem; max-width: 92rem; margin: 0 auto; }
  .top { display: flex; justify-content: space-between; align-items: end; gap: 1rem; flex-wrap: wrap; }
  .date { margin: 0 0 0.3rem; color: var(--text-3); font-size: 0.92rem; }
  .date::first-letter { text-transform: uppercase; }
  h1 { margin: 0; font-family: var(--display); font-size: clamp(1.6rem, 2.3vw, 2.3rem); font-weight: 600; letter-spacing: -0.01em; }
  .wave { display: inline-block; animation: wave 2.4s ease-in-out 1; transform-origin: 70% 70%; }
  @keyframes wave { 0%, 60%, 100% { transform: rotate(0); } 10%, 30% { transform: rotate(14deg); } 20%, 40% { transform: rotate(-8deg); } }
  .chips { display: flex; gap: 0.6rem; }
  .chip { padding: 0.5rem 0.9rem; border-radius: 2rem; border: 1px solid var(--line); background: var(--surface); color: var(--text-2); font-size: 0.9rem; }
  .chip b { color: var(--text); font-weight: 700; }
  .chip.gold b { color: var(--gold); }

  .hero { display: grid; grid-template-columns: minmax(0, 1.55fr) minmax(19rem, 1fr); gap: 1.2rem; }
  .cont {
    position: relative; overflow: hidden; display: grid; gap: 0.75rem; align-content: start;
    padding: 2rem; border-radius: var(--r-l);
    background: linear-gradient(135deg, #1d3aa8 0%, #142a7e 45%, #0c1a52 100%);
    border: 1px solid rgb(120 150 255 / 0.3);
    color: #fff;
    box-shadow: 0 1.2rem 3rem rgb(10 30 120 / 0.35);
  }
  :global([data-theme='light']) .cont { box-shadow: 0 1rem 2.4rem rgb(30 50 150 / 0.25); }
  .glow { position: absolute; right: -6rem; top: -6rem; width: 20rem; height: 20rem; border-radius: 50%; background: radial-gradient(circle, rgb(57 220 200 / 0.4), transparent 65%); pointer-events: none; }
  .eyebrow { margin: 0; font-size: 0.85rem; color: #a8bbff; font-weight: 500; position: relative; }
  .cont h2 { margin: 0; font-family: var(--display); font-size: clamp(1.6rem, 2.4vw, 2.3rem); font-weight: 700; line-height: 1.15; position: relative; }
  .short { margin: 0; color: #c9d4ff; font-size: 1.02rem; position: relative; }
  .pbar { height: 0.5rem; border-radius: 1rem; background: rgb(255 255 255 / 0.14); overflow: hidden; margin-top: 0.4rem; }
  .pbar i { display: block; height: 100%; border-radius: inherit; background: linear-gradient(90deg, #39dcc8, #9ff5e9); transition: width 0.6s; }
  .meta { display: flex; gap: 1.2rem; font-size: 0.88rem; color: #b8c6ff; flex-wrap: wrap; }
  .meta .ok { color: #39dcc8; }
  .acts { display: flex; gap: 0.7rem; margin-top: 0.6rem; flex-wrap: wrap; position: relative; }
  .cont .btn-primary { background: #fff; color: #10237a; box-shadow: 0 0.4rem 1.2rem rgb(0 0 0 / 0.25); }
  .cont .btn-primary:hover { background: #eef2ff; }
  .cont .btn-ghost { color: #fff; border-color: rgb(255 255 255 / 0.3); }
  .cont .btn-ghost:hover { background: rgb(255 255 255 / 0.1); }

  .stats { display: grid; gap: 0.8rem; grid-template-columns: 1fr 1fr; grid-template-rows: auto auto; }
  .stat { display: grid; gap: 0.3rem; align-content: center; padding: 1.1rem 1.2rem; border-radius: var(--r-l); background: var(--surface); border: 1px solid var(--line); }
  .stat small { color: var(--text-3); font-size: 0.82rem; }
  .stat b { font-family: var(--display); font-size: 1.6rem; font-weight: 700; }
  .stat em { font-style: normal; font-size: 0.95rem; color: var(--text-3); font-weight: 500; }
  .stat.level { grid-column: 1 / -1; display: flex; align-items: center; gap: 1.1rem; }
  .stat.level div { display: grid; gap: 0.15rem; }
  .stat.level b { font-size: 1.25rem; }
  .stat.level span { color: var(--text-3); font-size: 0.85rem; }
  .lvn { font-family: var(--display); font-size: 1.9rem; color: var(--gold); }
  .mini { height: 0.35rem; border-radius: 1rem; background: var(--line); overflow: hidden; margin-top: 0.3rem; }
  .mini i { display: block; height: 100%; background: var(--lapis); border-radius: inherit; }
  .mini.t i { background: var(--turq); }

  .row2 { display: grid; grid-template-columns: minmax(0, 1.55fr) minmax(19rem, 1fr); gap: 1.2rem; }
  .panel { padding: 1.2rem 1.4rem; border-radius: var(--r-l); background: var(--surface); border: 1px solid var(--line); display: grid; gap: 0.9rem; align-content: start; }
  .ph { display: flex; justify-content: space-between; align-items: baseline; gap: 1rem; }
  .ph h3 { margin: 0; font-size: 1.02rem; font-weight: 700; }
  .ph span { color: var(--text-3); font-size: 0.85rem; }
  .ph b { color: var(--gold); }
  .heat { display: grid; grid-template-rows: repeat(7, auto); grid-auto-flow: column; grid-auto-columns: minmax(0, 1fr); gap: 0.22rem; }
  .heat i, .legend i { aspect-ratio: 1; border-radius: 0.22rem; background: var(--line); }
  .heat i.future { opacity: 0.25; }
  .h1 { background: rgb(57 220 200 / 0.3) !important; }
  .h2 { background: rgb(57 220 200 / 0.55) !important; }
  .h3 { background: rgb(57 220 200 / 0.8) !important; }
  .h4 { background: var(--gold) !important; }
  .legend { display: flex; align-items: center; justify-content: flex-end; gap: 0.25rem; font-size: 0.75rem; color: var(--text-3); }
  .legend i { width: 0.8rem; }
  .tip p { margin: 0; font-family: var(--mono); font-size: 0.95rem; line-height: 1.6; padding: 0.9rem 1rem; border-radius: var(--r-m); background: var(--code-bg); color: #dfe6ff; border: 1px solid var(--code-line); }
  .tip .btn-ghost { justify-self: start; }

  .sh { display: flex; align-items: baseline; gap: 1rem; flex-wrap: wrap; margin-top: 0.4rem; }
  .sh h3 { margin: 0; font-family: var(--display); font-size: 1.3rem; font-weight: 600; }
  .sh span { color: var(--text-3); font-size: 0.9rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(17.5rem, 1fr)); gap: 1rem; }
  .sec { display: grid; grid-template-rows: 1fr auto; border-radius: var(--r-l); background: var(--surface); border: 1px solid var(--line); overflow: hidden; transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s; }
  .sec:hover { transform: translateY(-3px); border-color: var(--line-2); box-shadow: var(--glow); }
  .sec button { border: 0; background: none; text-align: left; }
  .sec-main { display: grid; gap: 0.45rem; align-content: start; padding: 1.2rem 1.3rem 1rem; }
  .sec-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem; }
  .emo { font-size: 1.6rem; display: grid; place-items: center; width: 2.8rem; height: 2.8rem; border-radius: 0.9rem; background: var(--surface-2); border: 1px solid var(--line); }
  .band { font-size: 0.72rem; font-weight: 700; padding: 0.25rem 0.6rem; border-radius: 2rem; letter-spacing: 0.02em; }
  .band.turq { background: rgb(57 220 200 / 0.14); color: var(--turq); }
  .band.lapis { background: rgb(74 116 255 / 0.16); color: #8fb0ff; }
  :global([data-theme='light']) .band.lapis { color: var(--lapis); }
  .band.gold { background: rgb(247 189 70 / 0.15); color: var(--gold); }
  .band.rose { background: var(--rose-bg); color: var(--rose); }
  .sec small { color: var(--text-3); font-size: 0.78rem; }
  .sec h4 { margin: 0; font-family: var(--display); font-size: 1.12rem; font-weight: 600; }
  .sec p { margin: 0; color: var(--text-2); font-size: 0.9rem; line-height: 1.45; min-height: 2.6em; }
  .sec-bar { height: 0.35rem; border-radius: 1rem; background: var(--line); overflow: hidden; margin-top: 0.4rem; }
  .sec-bar i { display: block; height: 100%; background: linear-gradient(90deg, var(--lapis), var(--turq)); border-radius: inherit; }
  .sec-meta { display: flex; justify-content: space-between; font-size: 0.82rem; color: var(--text-3); }
  .sec-meta b { color: var(--text); }
  .exam { padding: 0.75rem 1.3rem; border-top: 1px solid var(--line) !important; color: var(--text-2); font-size: 0.86rem; font-weight: 500; }
  .exam:hover { background: var(--surface-2) !important; color: var(--text); }
  .exam.passed { color: var(--gold); }

  @media (max-width: 70em) {
    .hero, .row2 { grid-template-columns: 1fr; }
  }
</style>
