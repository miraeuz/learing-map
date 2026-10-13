<script lang="ts">
  import { untrack } from 'svelte';
  import { app, save } from '../lib/store.svelte';
  import { runCode, py, type PyError } from '../lib/python.svelte';
  import CodeEditor from './CodeEditor.svelte';
  import Output from './Output.svelte';

  let code = $state(untrack(() => app.saved.playground));
  let stdin = $state('Mirae');
  let busy = $state(false);
  let res = $state<{ stdout: string; error: PyError | null; ms: number } | null>(null);

  $effect(() => {
    const c = code;
    untrack(() => { app.saved.playground = c; save(); });
  });

  async function run() {
    if (busy) return;
    busy = true;
    const r = await runCode(code, stdin + '\n', 10000);
    res = { stdout: r.stdout, error: r.error, ms: r.ms };
    busy = false;
  }

  const SNIPPETS: [string, string, string][] = [
    ['👋 Salomlashish', 'ism = input("Ismingiz: ")\nprint(f"Salom, {ism}! Mirae Academy ga xush kelibsiz.")\n', 'Ali'],
    ['🔢 Karra jadvali', 'n = 9\nfor i in range(1, n + 1):\n    qator = [f"{i * j:3}" for j in range(1, n + 1)]\n    print(" ".join(qator))\n', ''],
    ['🧮 Tub sonlar', 'def tubmi(n):\n    if n < 2:\n        return False\n    i = 2\n    while i * i <= n:\n        if n % i == 0:\n            return False\n        i += 1\n    return True\n\nprint([x for x in range(2, 60) if tubmi(x)])\n', ''],
    ['📊 Soʻz chastotasi', 'from collections import Counter\n\nmatn = """python oddiy python kuchli\npython bilan dasturlash qiziqarli"""\nfor soz, n in Counter(matn.split()).most_common(3):\n    print(f"{soz:<12}{\'█\' * n} {n}")\n', ''],
    ['🎲 Son topish oʻyini', 'import random\n\nsir = random.randint(1, 100)\nurinish = 0\nfor taxmin in [50, 25, 75, 12, 88, 37, 63]:\n    urinish += 1\n    if taxmin == sir:\n        print("Topdingiz!", urinish, "urinishda")\n        break\n    print(taxmin, "→", "kattaroq" if sir > taxmin else "kichikroq")\nelse:\n    print("Sir son:", sir)\n', ''],
    ['🛡️ Xavfsiz kirish', 'def son_oqi(matn):\n    try:\n        return int(matn)\n    except ValueError:\n        return None\n\nfor s in ["42", "qirq", "-7", "3.5"]:\n    print(repr(s), "→", son_oqi(s))\n', ''],
  ];

  function load(i: number) {
    if (code.trim() && code !== SNIPPETS[i][1] && !confirm('Joriy kod almashtiriladi. Davom etasizmi?')) return;
    code = SNIPPETS[i][1];
    stdin = SNIPPETS[i][2];
    res = null;
  }
</script>

<div class="page">
  <header>
    <div>
      <h1>Kod maydoni</h1>
      <p>Erkin tajriba uchun joy. Kod kompyuteringizda, internetsiz ishlaydi{py.version ? ` — Python ${py.version}` : ''}.</p>
    </div>
  </header>

  <div class="snips">
    {#each SNIPPETS as s, i}<button class="snip" onclick={() => load(i)}>{s[0]}</button>{/each}
  </div>

  <div class="grid">
    <div class="ed">
      <div class="ed-head">
        <span class="file">playground.py</span>
        <span class="sp"></span>
        <button class="btn-primary sm" onclick={run} disabled={busy}>{busy ? 'Ishlamoqda…' : '▶ Ishga tushirish'}</button>
      </div>
      <CodeEditor bind:value={code} minLines={20} maxHeight="calc(100vh - 17rem)" errorLine={res?.error?.line ?? null} onRun={run} />
    </div>
    <div class="side">
      <div class="box">
        <div class="bh">Kirish (input)</div>
        <textarea bind:value={stdin} rows="5" spellcheck="false" placeholder="Har bir input() uchun alohida qator"></textarea>
      </div>
      <div class="box out">
        {#if res}
          <Output stdout={res.stdout} error={res.error} ms={res.ms} />
        {:else}
          <div class="ph">
            <span>▶</span>
            <p>Natija shu yerda chiqadi.<br /><kbd>Ctrl</kbd> + <kbd>↵</kbd> — ishga tushirish</p>
          </div>
        {/if}
      </div>
    </div>
  </div>
</div>

<style>
  .page { display: grid; gap: 1.1rem; padding: 1.8rem clamp(1.5rem, 3vw, 3rem) 2rem; max-width: 100rem; margin: 0 auto; }
  h1 { margin: 0; font-family: var(--display); font-size: 1.9rem; font-weight: 700; }
  header p { margin: 0.4rem 0 0; color: var(--text-2); }
  .snips { display: flex; gap: 0.5rem; flex-wrap: wrap; }
  .snip { padding: 0.45rem 0.85rem; border-radius: 2rem; border: 1px solid var(--line); background: var(--surface); color: var(--text-2); font-size: 0.86rem; }
  .snip:hover { border-color: var(--lapis); color: var(--text); }
  .grid { display: grid; grid-template-columns: minmax(0, 1.5fr) minmax(18rem, 1fr); gap: 1.1rem; align-items: start; }
  .ed { border-radius: var(--r-l); overflow: hidden; border: 1px solid var(--code-line); background: var(--code-bg); }
  .ed-head { display: flex; align-items: center; padding: 0.45rem 0.5rem 0.45rem 1rem; border-bottom: 1px solid var(--code-line); }
  .file { font: 0.8rem var(--mono); color: #8fa0d8; }
  .sp { flex: 1; }
  .side { display: grid; gap: 1rem; }
  .box { border-radius: var(--r-l); overflow: hidden; border: 1px solid var(--code-line); background: var(--code-bg); }
  .bh { padding: 0.5rem 0.9rem; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #7381b4; border-bottom: 1px solid var(--code-line); }
  textarea { display: block; width: 100%; border: 0; resize: vertical; padding: 0.7rem 0.9rem; background: transparent; color: #f7bd46; font: 0.9rem/1.55 var(--mono); }
  textarea:focus { outline: none; }
  .ph { display: grid; place-items: center; gap: 0.5rem; padding: 3rem 1rem; text-align: center; color: #4a5a92; }
  .ph span { font-size: 2rem; }
  .ph p { margin: 0; line-height: 1.8; font-size: 0.9rem; }
  .ph kbd { background: #0f1a42; border-color: #22346f; color: #7381b4; }
  @media (max-width: 70em) { .grid { grid-template-columns: 1fr; } }
</style>
