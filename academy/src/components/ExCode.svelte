<script lang="ts">
  import { untrack, tick } from 'svelte';
  import type { CodeEx } from '../lib/course';
  import { xpFor } from '../lib/course';
  import { app, markSolved, addAttempt, markRevealed, setDraft, toast } from '../lib/store.svelte';
  import { runCode, checkFunction, checkProgram, py, type PyError, type TestResult } from '../lib/python.svelte';
  import CodeEditor from './CodeEditor.svelte';
  import Output from './Output.svelte';

  let { ex, onNext }: { ex: CodeEx; onNext?: () => void } = $props();

  let code = $state(untrack(() => app.saved.drafts[ex.id] ?? ex.starter));
  const firstStdin = untrack(() => (ex.kind === 'prog' ? ex.tests[0]?.stdin ?? '' : ''));
  let stdin = $state(firstStdin.replace(/\n$/, ''));
  let busy = $state<'' | 'run' | 'check'>('');
  let run = $state<{ stdout: string; error: PyError | null; ms: number } | null>(null);
  let results = $state<TestResult[] | null>(null);
  let loadError = $state<PyError | null>(null);
  let showHint = $state(false);
  let showSol = $state(false);
  let justSolved = $state(false);
  let resultsEl = $state<HTMLElement | null>(null);

  const solved = $derived(!!app.saved.solved[ex.id]);
  const attempts = $derived(app.saved.attempts[ex.id] ?? 0);
  const revealed = $derived(!!app.saved.revealed[ex.id]);
  const passed = $derived(results ? results.filter((r) => r.ok).length : 0);
  const errLine = $derived((run?.error ?? loadError)?.line ?? null);
  const needsInput = $derived(ex.kind === 'prog' && /\binput\s*\(/.test(ex.solution));
  const examples = $derived(ex.kind === 'func' ? ex.tests.slice(0, 3) : []);

  let draftTimer: ReturnType<typeof setTimeout>;
  $effect(() => {
    const c = code;
    clearTimeout(draftTimer);
    draftTimer = setTimeout(() => untrack(() => {
      if (c !== ex.starter || app.saved.drafts[ex.id]) setDraft(ex.id, c);
    }), 400);
  });

  async function doRun() {
    if (busy) return;
    busy = 'run';
    results = null;
    loadError = null;
    const r = await runCode(code, stdin + '\n');
    run = { stdout: r.stdout, error: r.error, ms: r.ms };
    busy = '';
  }

  async function doCheck() {
    if (busy) return;
    busy = 'check';
    run = null;
    loadError = null;
    const r = ex.kind === 'func' ? await checkFunction(code, ex.tests) : await checkProgram(code, ex.tests);
    busy = '';
    if (r.error) {
      loadError = r.error;
      results = [];
      addAttempt(ex.id);
      return;
    }
    results = r.results;
    tick().then(() => resultsEl?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }));
    if (r.results.length && r.results.every((t) => t.ok)) {
      if (!solved) {
        const xp = markSolved(ex);
        justSolved = true;
        toast(xp ? 'Barcha testlar oʻtdi!' : 'Testlar oʻtdi (yechim koʻrilgani uchun XP berilmadi)', { xp: xp || undefined, tone: 'ok' });
      }
    } else addAttempt(ex.id);
  }

  function reveal() {
    if (!solved && !revealed && !confirm('Yechimni koʻrsangiz, bu mashq uchun XP berilmaydi. Davom etasizmi?')) return;
    markRevealed(ex.id);
    showSol = true;
  }

  function resetCode() {
    if (code !== ex.starter && !confirm('Kodingiz oʻchiriladi va boshlangʻich holatga qaytadi. Rozimisiz?')) return;
    code = ex.starter;
    results = null;
    run = null;
    loadError = null;
  }

  const show = (s: string) => s.replace(/\n$/, '');
</script>

<div class="wrap">
  <section class="task">
    <div class="task-head">
      <span class="kind">{ex.kind === 'func' ? 'ƒ Funksiya yozing' : '▤ Dastur yozing'}</span>
      <span class="lv" title="Qiyinlik">{'●'.repeat(ex.lv)}{'○'.repeat(Math.max(0, 3 - ex.lv))}</span>
      <span class="xp">+{xpFor(ex)} XP</span>
    </div>
    <h3>{ex.title}</h3>
    <p class="prompt">{@html ex.prompt}</p>

    {#if ex.kind === 'func'}
      <div class="ex-box">
        <div class="ex-title">Misollar</div>
        {#each examples as t}
          <div class="ex-row"><code>{t.call}</code><span>→</span><code class="exp">{t.raises ? `${t.raises} xatosi` : t.expect}</code></div>
        {/each}
        {#if ex.tests.length > examples.length}<div class="more">+ yana {ex.tests.length - examples.length} ta yashirin test</div>{/if}
      </div>
    {:else}
      <div class="ex-box">
        <div class="ex-title">Namuna</div>
        <div class="io">
          {#if needsInput}
            <div><small>Kirish</small><pre>{show(ex.tests[0].stdin)}</pre></div>
          {/if}
          <div><small>Chiqish</small><pre>{show(ex.tests[0].expect)}</pre></div>
        </div>
        {#if ex.tests.length > 1}<div class="more">Jami {ex.tests.length} ta test bilan tekshiriladi</div>{/if}
      </div>
    {/if}

    <div class="aids">
      {#if ex.hint}
        <button class="btn-ghost sm" onclick={() => (showHint = !showHint)}>💡 {showHint ? 'Maslahatni yashirish' : 'Maslahat'}</button>
      {/if}
      <button class="btn-ghost sm" class:pulse={attempts >= 3 && !solved && !showSol} onclick={() => (showSol ? (showSol = false) : reveal())}>
        👁 {showSol ? 'Yechimni yashirish' : 'Yechimni koʻrish'}
      </button>
    </div>
    {#if showHint && ex.hint}<div class="hint">{@html ex.hint}</div>{/if}
    {#if showSol}
      <div class="sol">
        <div class="sol-h">Namunaviy yechim <small>— boshqa toʻgʻri yechimlar ham boʻlishi mumkin</small></div>
        <CodeEditor value={ex.solution} readonly minLines={1} />
      </div>
    {/if}
    {#if attempts >= 3 && !solved && !showSol}
      <p class="stuck">Qiynalyapsizmi? Muammoni kichik qismlarga boʻling, <code>print()</code> bilan oraliq qiymatlarni chiqarib koʻring yoki darsga qayting.</p>
    {/if}
  </section>

  <section class="work">
    <div class="ed">
      <div class="ed-head">
        <span class="file">{ex.kind === 'func' ? `${ex.name}.py` : 'main.py'}</span>
        {#if solved}<span class="done">✓ Yechilgan</span>{/if}
        <span class="sp"></span>
        <button class="ic" onclick={resetCode} title="Boshidan boshlash">↺</button>
      </div>
      <CodeEditor bind:value={code} minLines={9} maxHeight="26rem" errorLine={errLine} onRun={doRun} onCheck={doCheck} />
      {#if needsInput}
        <label class="stdin">
          <span>Kirish:</span>
          <textarea bind:value={stdin} rows={Math.min(4, Math.max(1, stdin.split('\n').length))} spellcheck="false"></textarea>
        </label>
      {/if}
      <div class="actions">
        <button class="btn-ghost" onclick={doRun} disabled={!!busy}>{busy === 'run' ? 'Ishlamoqda…' : '▶ Ishga tushirish'}</button>
        <button class="btn-primary" onclick={doCheck} disabled={!!busy}>{busy === 'check' ? 'Tekshirilmoqda…' : '✓ Tekshirish'}</button>
        <span class="keys"><kbd>Ctrl</kbd>+<kbd>↵</kbd> ishga tushirish · <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>↵</kbd> tekshirish</span>
      </div>
      {#if py.status === 'loading' && busy}<p class="loading">Python yuklanmoqda… (birinchi marta bir necha soniya)</p>{/if}
      {#if run}
        <Output stdout={run.stdout} error={run.error} ms={run.ms} empty={ex.kind === 'func' ? 'Hech narsa chiqmadi. Funksiyani sinash uchun pastga print(...) bilan chaqiring yoki «Tekshirish»ni bosing.' : 'Kod hech narsa chiqarmadi'} />
      {/if}
      {#if loadError}
        <Output stdout="" error={loadError} label="Kod yuklanmadi" />
      {/if}
    </div>

    {#if results && results.length}
      <div class="results" class:all={passed === results.length} bind:this={resultsEl}>
        <div class="r-head">
          <b>{passed === results.length ? '🎉 Barcha testlar oʻtdi!' : `${passed} / ${results.length} test oʻtdi`}</b>
          <div class="r-bar"><i style:width={`${(passed / results.length) * 100}%`}></i></div>
        </div>
        <ul>
          {#each results as r, i}
            <li class:ok={r.ok}>
              <span class="st">{r.ok ? '✓' : '✕'}</span>
              {#if ex.kind === 'func'}
                <code class="call">{r.call}</code>
                {#if !r.ok}
                  <div class="cmp"><span>Kutilgan:</span><code>{r.expect}</code><span>Sizda:</span><code class="got">{r.got}</code></div>
                {/if}
              {:else}
                <span class="call">{i + 1}-test</span>
                {#if !r.ok}
                  <div class="cmp prog">
                    {#if needsInput}<span>Kirish:</span><pre>{show(r.stdin ?? '')}</pre>{/if}
                    <span>Kutilgan:</span><pre>{show(r.expect)}</pre>
                    <span>Sizda:</span><pre class="got">{show(r.got) || '(boʻsh)'}</pre>
                    {#if r.error}<span>Xato:</span><pre class="got">{r.error.type}: {r.error.msg}</pre>{/if}
                  </div>
                {/if}
              {/if}
            </li>
          {/each}
        </ul>
        {#if passed === results.length && onNext}
          <div class="next"><span>{justSolved ? 'Zoʻr ish! Keyingi mashqqa oʻtamizmi?' : 'Yechim toʻgʻri.'}</span><button class="btn-primary" onclick={onNext}>Keyingisi →</button></div>
        {/if}
      </div>
    {/if}
  </section>
</div>

<style>
  .wrap { display: grid; grid-template-columns: minmax(0, 0.85fr) minmax(0, 1.15fr); gap: 1.4rem; align-items: start; }
  .task { display: grid; gap: 0.9rem; position: sticky; top: 0; }
  .task-head { display: flex; align-items: center; gap: 0.8rem; font-size: 0.8rem; }
  .kind { padding: 0.25rem 0.65rem; border-radius: 2rem; background: rgb(74 116 255 / 0.15); color: #8fb0ff; font-weight: 600; }
  :global([data-theme='light']) .kind { color: var(--lapis); }
  .lv { color: var(--gold); letter-spacing: 0.1em; }
  .xp { margin-left: auto; color: var(--gold); font-weight: 700; }
  h3 { margin: 0; font-family: var(--display); font-size: 1.4rem; font-weight: 600; }
  .prompt { margin: 0; font-size: 1.04rem; line-height: 1.65; color: var(--text-2); }
  .prompt :global(code), .hint :global(code), .stuck code { font-size: 0.9em; padding: 0.1em 0.35em; border-radius: 0.3rem; background: rgb(74 116 255 / 0.13); color: #a9c0ff; }
  :global([data-theme='light']) .prompt :global(code) { color: var(--lapis-2); }
  .ex-box { border-radius: var(--r-m); background: var(--surface); border: 1px solid var(--line); padding: 0.8rem 1rem; display: grid; gap: 0.45rem; }
  .ex-title { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-3); }
  .ex-row { display: flex; align-items: baseline; gap: 0.6rem; flex-wrap: wrap; font-family: var(--mono); font-size: 0.9rem; }
  .ex-row span { color: var(--text-3); }
  .ex-row .exp { color: var(--turq); }
  .io { display: grid; grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr)); gap: 0.6rem; }
  .io small { font-size: 0.75rem; color: var(--text-3); }
  .io pre { margin: 0.25rem 0 0; padding: 0.55rem 0.7rem; border-radius: 0.5rem; background: var(--code-bg); color: #dfe6ff; font-size: 0.88rem; white-space: pre-wrap; max-height: 10rem; overflow: auto; }
  .more { font-size: 0.8rem; color: var(--text-3); }
  .aids { display: flex; gap: 0.5rem; flex-wrap: wrap; }
  .pulse { border-color: var(--gold) !important; color: var(--gold) !important; }
  .hint { padding: 0.8rem 1rem; border-radius: var(--r-m); background: rgb(247 189 70 / 0.1); border: 1px solid rgb(247 189 70 / 0.3); line-height: 1.55; }
  .sol { border-radius: var(--r-m); overflow: hidden; border: 1px solid rgb(247 189 70 / 0.4); }
  .sol-h { padding: 0.5rem 0.9rem; background: rgb(247 189 70 / 0.12); color: var(--gold); font-weight: 600; font-size: 0.86rem; }
  .sol-h small { color: var(--text-3); font-weight: 400; }
  .stuck { margin: 0; font-size: 0.9rem; color: var(--text-3); line-height: 1.55; }

  .work { display: grid; gap: 1rem; min-width: 0; }
  .ed { border-radius: var(--r-l); overflow: hidden; border: 1px solid var(--code-line); background: var(--code-bg); box-shadow: 0 1rem 2.4rem rgb(0 0 0 / 0.22); }
  .ed-head { display: flex; align-items: center; gap: 0.6rem; padding: 0.4rem 0.5rem 0.4rem 1rem; border-bottom: 1px solid var(--code-line); }
  .file { font: 0.8rem var(--mono); color: #8fa0d8; }
  .done { font-size: 0.75rem; padding: 0.15rem 0.5rem; border-radius: 1rem; background: rgb(57 220 200 / 0.15); color: #39dcc8; font-weight: 600; }
  .sp { flex: 1; }
  .ic { width: 2rem; height: 2rem; border-radius: 0.5rem; border: 0; background: none; color: #7381b4; font-size: 1.05rem; }
  .ic:hover { background: rgb(255 255 255 / 0.06); color: #edf1ff; }
  .stdin { display: flex; align-items: flex-start; gap: 0.7rem; padding: 0.6rem 1rem; border-top: 1px solid var(--code-line); font-size: 0.8rem; color: #7381b4; }
  .stdin span { padding-top: 0.35rem; }
  .stdin textarea { flex: 1; resize: vertical; padding: 0.4rem 0.6rem; border-radius: 0.45rem; border: 1px solid var(--code-line); background: #050c22; color: #f7bd46; font: 0.88rem/1.5 var(--mono); }
  .actions { display: flex; align-items: center; gap: 0.6rem; padding: 0.7rem 1rem; border-top: 1px solid var(--code-line); flex-wrap: wrap; }
  .actions .btn-ghost { color: #dfe6ff; border-color: #2a3b78; }
  .actions .btn-ghost:hover { background: rgb(255 255 255 / 0.05); }
  .keys { margin-left: auto; font-size: 0.75rem; color: #4a5a92; }
  .keys kbd { background: #0f1a42; border-color: #22346f; color: #7381b4; }
  .loading { margin: 0; padding: 0 1rem 0.7rem; font-size: 0.82rem; color: #7381b4; }

  .results { border-radius: var(--r-l); border: 1px solid rgb(255 122 138 / 0.35); background: var(--surface); overflow: hidden; }
  .results.all { border-color: rgb(57 220 200 / 0.45); animation: pop 0.4s cubic-bezier(0.2, 1.4, 0.4, 1); }
  @keyframes pop { from { transform: scale(0.97); opacity: 0; } }
  .r-head { padding: 0.9rem 1.1rem; display: grid; gap: 0.5rem; border-bottom: 1px solid var(--line); }
  .results.all .r-head b { color: var(--turq); }
  .r-bar { height: 0.35rem; border-radius: 1rem; background: rgb(255 122 138 / 0.25); overflow: hidden; }
  .r-bar i { display: block; height: 100%; background: var(--turq); transition: width 0.5s; }
  ul { list-style: none; margin: 0; padding: 0.4rem 0; max-height: 24rem; overflow: auto; }
  li { display: grid; grid-template-columns: 1.6rem 1fr; gap: 0.2rem 0.5rem; padding: 0.45rem 1.1rem; align-items: baseline; }
  li + li { border-top: 1px solid var(--line); }
  .st { font-weight: 800; color: var(--rose); }
  li.ok .st { color: var(--turq); }
  .call { font-family: var(--mono); font-size: 0.88rem; color: var(--text-2); word-break: break-all; }
  .cmp { grid-column: 2; display: grid; grid-template-columns: auto 1fr; gap: 0.25rem 0.6rem; font-size: 0.82rem; color: var(--text-3); align-items: baseline; }
  .cmp code, .cmp pre { font-family: var(--mono); font-size: 0.85rem; color: var(--turq); margin: 0; white-space: pre-wrap; word-break: break-word; }
  .cmp pre { padding: 0.35rem 0.5rem; border-radius: 0.4rem; background: var(--code-bg); max-height: 8rem; overflow: auto; }
  .cmp .got { color: var(--rose); }
  .next { display: flex; align-items: center; justify-content: space-between; gap: 1rem; padding: 0.9rem 1.1rem; border-top: 1px solid var(--line); background: var(--ok-bg); }
  .next span { font-weight: 600; color: var(--turq); }

  @media (max-width: 75em) {
    .wrap { grid-template-columns: 1fr; }
    .task { position: static; }
  }
</style>
