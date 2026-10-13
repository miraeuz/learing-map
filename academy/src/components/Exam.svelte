<script lang="ts">
  import { onDestroy } from 'svelte';
  import { sections, type QuizEx, type CodeEx } from '../lib/course';
  import { app, recordExam, toast } from '../lib/store.svelte';
  import { nav, go, openTopic } from '../lib/nav.svelte';
  import { checkFunction, checkProgram } from '../lib/python.svelte';
  import CodeEditor from './CodeEditor.svelte';

  let { sec }: { sec: number } = $props();

  const QUIZ_N = 14;
  const CODE_N = 2;
  const CODE_PTS = 3;
  const MINUTES = 30;
  const PASS = 70;

  const section = $derived(sections.find((s) => s.num === sec)!);
  const rec = $derived(app.saved.exams[sec]);

  type Q = { kind: 'quiz'; ex: QuizEx; topic: string; pick: number | null }
    | { kind: 'code'; ex: CodeEx; topic: string; code: string; passed: number; total: number; checked: boolean; busy: boolean };

  let phase = $state<'intro' | 'run' | 'done'>('intro');
  let qs = $state<Q[]>([]);
  let at = $state(0);
  let endsAt = $state(0);
  let now = $state(Date.now());
  let tick: ReturnType<typeof setInterval> | null = null;
  onDestroy(() => { if (tick) clearInterval(tick); nav.examActive = false; });

  function shuffle<T>(a: T[]): T[] {
    const b = [...a];
    for (let i = b.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [b[i], b[j]] = [b[j], b[i]];
    }
    return b;
  }

  /** Spread the picks across topics: one per topic per round. */
  function spread<T extends { topic: string }>(items: T[], n: number): T[] {
    const byTopic = new Map<string, T[]>();
    for (const it of shuffle(items)) byTopic.set(it.topic, [...(byTopic.get(it.topic) ?? []), it]);
    const out: T[] = [];
    while (out.length < n && [...byTopic.values()].some((l) => l.length)) {
      for (const l of shuffle([...byTopic.values()])) {
        if (l.length && out.length < n) out.push(l.shift()!);
      }
    }
    return out;
  }

  function start() {
    const quizzes = section.topics.flatMap((t) => t.ex.filter((e): e is QuizEx => e.kind === 'quiz').map((ex) => ({ ex, topic: t.id })));
    const allCodes = section.topics.flatMap((t) =>
      t.ex.filter((e): e is CodeEx => e.kind === 'func' || e.kind === 'prog').map((ex) => ({ ex, topic: t.id })),
    );
    // Prefer harder tasks; early sections have mostly level-1 tasks, so fall back to those.
    const harder = allCodes.filter((x) => x.ex.lv >= 2);
    const codes = harder.length >= CODE_N * 2 ? harder : allCodes;
    qs = [
      ...spread(quizzes, QUIZ_N).map((x) => ({ kind: 'quiz' as const, ...x, pick: null })),
      ...spread(codes, CODE_N).map((x) => ({ kind: 'code' as const, ...x, code: x.ex.starter, passed: 0, total: x.ex.tests.length, checked: false, busy: false })),
    ];
    at = 0;
    now = Date.now();
    endsAt = now + MINUTES * 60_000;
    phase = 'run';
    nav.examActive = true;
    tick = setInterval(() => {
      now = Date.now();
      if (now >= endsAt) finish(true);
    }, 500);
  }

  const left = $derived(Math.max(0, Math.ceil((endsAt - now) / 1000)));
  const mmss = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
  const answered = $derived(qs.filter((q) => (q.kind === 'quiz' ? q.pick !== null : q.checked)).length);

  function points(q: Q) {
    if (q.kind === 'quiz') return q.pick === q.ex.answer ? 1 : 0;
    return q.total && q.passed === q.total ? CODE_PTS : 0;
  }
  const totalPts = $derived(qs.reduce((n, q) => n + (q.kind === 'quiz' ? 1 : CODE_PTS), 0) || 1);
  const score = $derived(Math.round((qs.reduce((n, q) => n + points(q), 0) / totalPts) * 100));
  let firstPass = $state(false);

  async function check(q: Extract<Q, { kind: 'code' }>) {
    q.busy = true;
    const r = q.ex.kind === 'func' ? await checkFunction(q.code, q.ex.tests) : await checkProgram(q.code, q.ex.tests);
    q.busy = false;
    q.checked = true;
    q.passed = r.error ? 0 : r.results.filter((t) => t.ok).length;
  }

  function finish(auto = false) {
    if (phase !== 'run') return;
    if (!auto && answered < qs.length && !confirm(`${qs.length - answered} ta savolga javob berilmagan. Imtihonni yakunlaysizmi?`)) return;
    if (tick) clearInterval(tick);
    nav.examActive = false;
    phase = 'done';
    firstPass = recordExam(sec, score, score >= PASS);
    if (firstPass) toast('Boʻlim imtihoni topshirildi!', { xp: 200, tone: 'gold' });
    document.querySelector('main')?.scrollTo({ top: 0 });
  }

  const cur = $derived(qs[at]);
  const L = ['A', 'B', 'C', 'D', 'E'];
</script>

<div class="page">
  {#if phase === 'intro'}
    <div class="intro">
      <span class="emo">{section.emoji}</span>
      <p class="eyebrow">{sec}-boʻlim imtihoni</p>
      <h1>{section.title}</h1>
      <p class="lead">Boʻlimdagi barcha mavzular boʻyicha bilimingizni sinang. Savollar har safar tasodifiy tanlanadi.</p>
      <div class="rules">
        <div><b>{QUIZ_N}</b><span>test savoli · 1 ball</span></div>
        <div><b>{CODE_N}</b><span>kod yozish · {CODE_PTS} ball</span></div>
        <div><b>{MINUTES}</b><span>daqiqa</span></div>
        <div><b>{PASS}%</b><span>oʻtish bali</span></div>
      </div>
      <ul class="notes">
        <li>Test savollarida javob darhol koʻrsatilmaydi — natijalar oxirida chiqadi.</li>
        <li>Kod topshiriqlarini istalgancha tekshirishingiz mumkin; barcha testlar oʻtsa — toʻliq ball.</li>
        <li>Birinchi marta topshirsangiz <b class="gold">+200 XP</b> va boʻlim kubogi 🏆.</li>
      </ul>
      {#if rec}<p class="prev">Oldingi natija: eng yaxshisi <b>{rec.best}%</b> · {rec.tries} marta urinilgan {rec.passed ? '· 🏆 topshirilgan' : ''}</p>{/if}
      <div class="acts">
        <button class="btn-primary big" onclick={start}>Imtihonni boshlash</button>
        <button class="btn-ghost" onclick={() => go({ name: 'exams' })}>Ortga</button>
      </div>
    </div>
  {:else if phase === 'run' && cur}
    <div class="run">
      <header class="bar">
        <div><small>{section.emoji} {sec}-boʻlim imtihoni</small><b>{at + 1} / {qs.length}</b></div>
        <div class="prog"><i style:width={`${(answered / qs.length) * 100}%`}></i></div>
        <span class="timer" class:low={left < 120}>⏱ {mmss(left)}</span>
        <button class="btn-primary sm" onclick={() => finish()}>Yakunlash</button>
      </header>
      <nav class="dots" aria-label="Savollar">
        {#each qs as q, i}
          <button class:on={i === at} class:ans={q.kind === 'quiz' ? q.pick !== null : q.checked} class:code={q.kind === 'code'} onclick={() => (at = i)}>{q.kind === 'code' ? '⌨' : i + 1}</button>
        {/each}
      </nav>

      <section class="qcard">
        {#if cur.kind === 'quiz'}
          {@const q = cur}
          <h3>{@html q.ex.q}</h3>
          {#if q.ex.code}<div class="code"><CodeEditor value={q.ex.code} readonly minLines={1} /></div>{/if}
          <div class="opts" class:mono={q.ex.mono}>
            {#each q.ex.options as o, i}
              <button class:sel={q.pick === i} onclick={() => (q.pick = i)}><span>{L[i]}</span><span class="t">{o === '' ? '(hech narsa)' : o}</span></button>
            {/each}
          </div>
        {:else}
          {@const q = cur}
          <h3>⌨ {q.ex.title} <small>· {CODE_PTS} ball</small></h3>
          <p class="prompt">{@html q.ex.prompt}</p>
          {#if q.ex.kind === 'func'}
            <div class="ex">{#each q.ex.tests.slice(0, 2) as t}<code>{t.call} → {t.raises ? t.raises + ' xatosi' : t.expect}</code>{/each}</div>
          {:else}
            <div class="ex"><code>Chiqish namunasi: {q.ex.tests[0].expect.trim().split('\n').slice(0, 3).join(' ⏎ ')}</code></div>
          {/if}
          <div class="ed">
            {#key q.ex.id}<CodeEditor bind:value={q.code} minLines={8} onCheck={() => check(q)} onRun={() => check(q)} />{/key}
            <div class="ed-foot">
              <button class="btn-primary sm" onclick={() => check(q)} disabled={q.busy}>{q.busy ? 'Tekshirilmoqda…' : '✓ Tekshirish'}</button>
              {#if q.checked}
                <span class:ok={q.passed === q.total}>{q.passed === q.total ? `✓ Barcha ${q.total} test oʻtdi` : `${q.passed} / ${q.total} test oʻtdi`}</span>
              {/if}
            </div>
          </div>
        {/if}
        <div class="qnav">
          <button class="btn-ghost" disabled={at === 0} onclick={() => at--}>← Oldingi</button>
          {#if at < qs.length - 1}
            <button class="btn-ghost" onclick={() => at++}>Keyingi →</button>
          {:else}
            <button class="btn-primary" onclick={() => finish()}>Imtihonni yakunlash</button>
          {/if}
        </div>
      </section>
    </div>
  {:else if phase === 'done'}
    {@const ok = score >= PASS}
    <div class="result">
      <div class="score" class:ok>
        <span class="big">{ok ? '🏆' : '📘'}</span>
        <div>
          <p class="eyebrow">{section.title} · natija</p>
          <h1>{score}%</h1>
          <p>{ok ? (firstPass ? 'Tabriklaymiz! Boʻlim imtihoni topshirildi. +200 XP' : 'Ajoyib — imtihon topshirildi!') : `Oʻtish uchun ${PASS}% kerak. Xatolarni koʻrib chiqing va yana urinib koʻring.`}</p>
        </div>
        <div class="acts">
          <button class="btn-primary" onclick={() => { phase = 'intro'; }}>Qayta topshirish</button>
          <button class="btn-ghost" onclick={() => go({ name: 'exams' })}>Barcha imtihonlar</button>
        </div>
      </div>
      <h3 class="rh">Javoblar tahlili</h3>
      <ol class="review">
        {#each qs as q, i}
          {@const p = points(q)}
          <li class:ok={p > 0}>
            <span class="st">{p > 0 ? '✓' : '✕'}</span>
            <div>
              {#if q.kind === 'quiz'}
                <b>{@html q.ex.q}</b>
                {#if q.ex.code}<pre>{q.ex.code}</pre>{/if}
                <p>Toʻgʻri javob: <code>{q.ex.options[q.ex.answer] || '(hech narsa)'}</code>
                  {#if q.pick !== q.ex.answer} · Sizniki: <code class="bad">{q.pick === null ? 'javob berilmagan' : q.ex.options[q.pick] || '(hech narsa)'}</code>{/if}</p>
              {:else}
                <b>⌨ {q.ex.title}</b>
                <p>{q.checked ? `${q.passed} / ${q.total} test oʻtdi` : 'Tekshirilmagan'}</p>
              {/if}
              {#if p === 0}<button class="link" onclick={() => openTopic(q.topic, 'dars')}>Mavzuni takrorlash: {q.topic} →</button>{/if}
            </div>
          </li>
        {/each}
      </ol>
    </div>
  {/if}
</div>

<style>
  .page { padding: 2rem clamp(1.5rem, 3vw, 3rem) 3rem; max-width: 64rem; margin: 0 auto; }
  .intro { display: grid; gap: 1rem; justify-items: start; }
  .emo { font-size: 2.6rem; display: grid; place-items: center; width: 4.4rem; height: 4.4rem; border-radius: 1.3rem; background: var(--surface); border: 1px solid var(--line); }
  .eyebrow { margin: 0; color: var(--text-3); font-size: 0.88rem; }
  h1 { margin: 0; font-family: var(--display); font-size: 2.3rem; font-weight: 700; }
  .lead { margin: 0; color: var(--text-2); font-size: 1.05rem; max-width: 40rem; line-height: 1.6; }
  .rules { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0.8rem; width: 100%; margin-top: 0.4rem; }
  .rules div { display: grid; gap: 0.2rem; padding: 1rem 1.1rem; border-radius: var(--r-m); background: var(--surface); border: 1px solid var(--line); }
  .rules b { font-family: var(--display); font-size: 1.6rem; color: var(--turq); }
  .rules span { color: var(--text-3); font-size: 0.85rem; }
  .notes { margin: 0.3rem 0 0; padding-left: 1.2rem; color: var(--text-2); line-height: 1.75; }
  .gold { color: var(--gold); }
  .prev { margin: 0; color: var(--text-3); }
  .prev b { color: var(--text); }
  .acts { display: flex; gap: 0.7rem; flex-wrap: wrap; margin-top: 0.4rem; }
  .big { height: 3.2rem; padding: 0 1.8rem; font-size: 1.05rem; }

  .run { display: grid; gap: 1rem; }
  .bar { position: sticky; top: 0; z-index: 2; display: flex; align-items: center; gap: 1rem; padding: 0.8rem 1.1rem; border-radius: var(--r-m); background: var(--surface); border: 1px solid var(--line); box-shadow: var(--glow); }
  .bar div:first-child { display: grid; }
  .bar small { color: var(--text-3); font-size: 0.78rem; }
  .bar b { font-family: var(--display); }
  .prog { flex: 1; height: 0.4rem; border-radius: 1rem; background: var(--line); overflow: hidden; }
  .prog i { display: block; height: 100%; background: var(--turq); transition: width 0.3s; }
  .timer { font: 600 1rem var(--mono); color: var(--text-2); }
  .timer.low { color: var(--rose); animation: blink 1s infinite; }
  @keyframes blink { 50% { opacity: 0.5; } }
  .dots { display: flex; gap: 0.35rem; flex-wrap: wrap; }
  .dots button { width: 2.3rem; height: 2.3rem; border-radius: 0.6rem; border: 1px solid var(--line); background: var(--surface); color: var(--text-3); font-size: 0.85rem; font-weight: 600; }
  .dots button.ans { background: rgb(74 116 255 / 0.18); border-color: rgb(74 116 255 / 0.4); color: var(--text); }
  .dots button.code { color: var(--gold); }
  .dots button.on { border-color: var(--turq); box-shadow: 0 0 0 3px rgb(57 220 200 / 0.2); }
  .qcard { display: grid; gap: 1rem; padding: 1.5rem 1.6rem; border-radius: var(--r-l); background: var(--surface); border: 1px solid var(--line); }
  .qcard h3 { margin: 0; font-size: 1.2rem; line-height: 1.5; }
  .qcard h3 small { color: var(--gold); font-weight: 500; font-size: 0.85rem; }
  .qcard :global(code) { font-family: var(--mono); font-size: 0.9em; }
  .code, .ed { border-radius: var(--r-m); overflow: hidden; border: 1px solid var(--code-line); background: var(--code-bg); }
  .opts { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; }
  .opts button { display: flex; gap: 0.8rem; align-items: flex-start; text-align: left; padding: 0.8rem 1rem; border-radius: var(--r-m); border: 1px solid var(--line-2); background: var(--bg-2); }
  .opts button:hover { border-color: var(--lapis); }
  .opts button > span:first-child { flex: none; display: grid; place-items: center; width: 1.7rem; height: 1.7rem; border-radius: 0.45rem; border: 1px solid var(--line-2); font-size: 0.8rem; font-weight: 700; }
  .opts .t { white-space: pre-wrap; padding-top: 0.1rem; }
  .opts.mono .t { font-family: var(--mono); font-size: 0.92rem; }
  .opts button.sel { border-color: var(--lapis); background: rgb(74 116 255 / 0.16); }
  .opts button.sel > span:first-child { background: var(--lapis); border-color: var(--lapis); color: #fff; }
  .prompt { margin: 0; color: var(--text-2); line-height: 1.6; }
  .ex { display: grid; gap: 0.3rem; }
  .ex code { color: var(--turq); }
  .ed-foot { display: flex; align-items: center; gap: 1rem; padding: 0.6rem 0.9rem; border-top: 1px solid var(--code-line); color: #ff9aa6; font-size: 0.88rem; }
  .ed-foot .ok { color: #39dcc8; }
  .qnav { display: flex; justify-content: space-between; }

  .result { display: grid; gap: 1.2rem; }
  .score { display: flex; align-items: center; gap: 1.4rem; flex-wrap: wrap; padding: 1.6rem 1.8rem; border-radius: var(--r-l); background: var(--rose-bg); border: 1px solid rgb(255 122 138 / 0.35); }
  .score.ok { background: linear-gradient(135deg, rgb(247 189 70 / 0.2), rgb(57 220 200 / 0.08)); border-color: rgb(247 189 70 / 0.45); }
  .score .big { font-size: 3.2rem; height: auto; padding: 0; }
  .score > div:nth-child(2) { flex: 1; min-width: 16rem; }
  .score h1 { font-size: 3rem; }
  .score.ok h1 { color: var(--gold); }
  .score p { margin: 0.2rem 0 0; color: var(--text-2); }
  .rh { margin: 0.6rem 0 0; font-family: var(--display); font-weight: 600; }
  .review { list-style: none; margin: 0; padding: 0; display: grid; gap: 0.6rem; }
  .review li { display: flex; gap: 0.9rem; padding: 0.9rem 1.1rem; border-radius: var(--r-m); background: var(--surface); border: 1px solid var(--line); border-left: 3px solid var(--rose); }
  .review li.ok { border-left-color: var(--turq); }
  .review .st { font-weight: 800; color: var(--rose); }
  .review li.ok .st { color: var(--turq); }
  .review div { display: grid; gap: 0.35rem; min-width: 0; }
  .review b { font-weight: 600; }
  .review pre { margin: 0; padding: 0.5rem 0.7rem; border-radius: 0.5rem; background: var(--code-bg); color: #dfe6ff; font-size: 0.85rem; overflow-x: auto; }
  .review p { margin: 0; color: var(--text-2); font-size: 0.92rem; }
  .review code { font-family: var(--mono); color: var(--turq); white-space: pre-wrap; }
  .review code.bad { color: var(--rose); }
  .link { justify-self: start; border: 0; background: none; padding: 0; color: var(--lapis); font-weight: 600; font-size: 0.88rem; }
  @media (max-width: 60em) { .opts, .rules { grid-template-columns: 1fr 1fr; } }
</style>
