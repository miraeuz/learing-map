<script lang="ts">
  import { onDestroy, untrack } from 'svelte';
  import { app, setName } from '../lib/store.svelte';
  import { hasBridge, bridge, errorText, licenceDate, type LicenseStatus } from '../lib/license';
  import { course, sections } from '../lib/course';
  import BrandMark from './BrandMark.svelte';

  let { status, onDone }: { status: LicenseStatus | null; onDone: () => void } = $props();

  const init = untrack(() => status);
  const needsCode = hasBridge() && !init?.activated;
  // The year is over (or the clock was turned back): same code flow, renewal wording.
  const renewing = needsCode && Boolean(init?.licensed);
  const clockBack = Boolean(init?.clockBack);
  let step = $state<'name' | 'code'>(app.saved.name && needsCode ? 'code' : 'name');
  let name = $state(app.saved.name || init?.name || '');
  let digits = $state(['', '', '', '', '', '']);
  let boxes: HTMLInputElement[] = $state([]);
  let sent = $state(Boolean(init?.pending));
  let expiresAt = $state(init?.expiresAt ?? 0);
  let resendAt = $state(init?.resendAt ?? 0);
  let busy = $state(false);
  let error = $state('');
  let success = $state(false);
  let now = $state(Date.now());
  const tick = setInterval(() => (now = Date.now()), 1000);
  onDestroy(() => clearInterval(tick));

  const nameOk = $derived(name.trim().length >= 2);
  const code = $derived(digits.join(''));
  const resendIn = $derived(Math.max(0, Math.ceil((resendAt - now) / 1000)));
  const expiresIn = $derived(Math.max(0, Math.ceil((expiresAt - now) / 1000)));
  const mmss = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;

  async function submitName(e: Event) {
    e.preventDefault();
    if (!nameOk) return;
    setName(name);
    if (!needsCode) return onDone();
    step = 'code';
    if (!sent) await send();
  }

  async function send() {
    busy = true;
    error = '';
    const r = await bridge().license.request(name.trim());
    busy = false;
    if (r.ok) {
      sent = true;
      expiresAt = r.expiresAt ?? 0;
      resendAt = r.resendAt ?? 0;
      digits = ['', '', '', '', '', ''];
      queueMicrotask(() => boxes[0]?.focus());
    } else {
      if (r.retryAt) resendAt = r.retryAt;
      error = errorText(r.error, { detail: r.detail });
    }
  }

  async function verify() {
    if (code.length !== 6 || busy) return;
    busy = true;
    error = '';
    const r = await bridge().license.verify(code);
    busy = false;
    if (r.ok) {
      success = true;
      setTimeout(onDone, 1000);
    } else {
      error = errorText(r.error, { left: r.left });
      if (r.error === 'too_many' || r.error === 'expired') sent = false;
      digits = ['', '', '', '', '', ''];
      queueMicrotask(() => boxes[0]?.focus());
    }
  }

  function onDigit(k: number, e: Event) {
    const el = e.target as HTMLInputElement;
    const v = el.value.replace(/\D/g, '');
    if (v.length > 1) {
      const all = v.slice(0, 6 - k).split('');
      all.forEach((d, j) => (digits[k + j] = d));
      boxes[Math.min(5, k + all.length)]?.focus();
    } else {
      digits[k] = v;
      if (v && k < 5) boxes[k + 1]?.focus();
    }
    el.value = digits[k];
    if (digits.every((d) => d)) verify();
  }

  function onKey(k: number, e: KeyboardEvent) {
    if (e.key === 'Backspace' && !digits[k] && k > 0) {
      digits[k - 1] = '';
      boxes[k - 1]?.focus();
      e.preventDefault();
    } else if (e.key === 'ArrowLeft' && k > 0) boxes[k - 1]?.focus();
    else if (e.key === 'ArrowRight' && k < 5) boxes[k + 1]?.focus();
    else if (e.key === 'Enter') verify();
  }

  function onPaste(e: ClipboardEvent) {
    const v = (e.clipboardData?.getData('text') ?? '').replace(/\D/g, '').slice(0, 6);
    if (!v) return;
    e.preventDefault();
    digits = Array.from({ length: 6 }, (_, j) => v[j] ?? '');
    boxes[Math.min(5, v.length)]?.focus();
    if (v.length === 6) verify();
  }

  const fmt = (n: number) => n.toLocaleString('ru-RU').replace(/ /g, ' ');
  const demo = [
    ['kw', 'def '], ['fn', 'salom'], ['p', '('], ['v', 'ism'], ['p', '):'], ['nl', ''],
    ['sp', '    '], ['kw', 'return '], ['st', 'f"Salom, {ism}!"'], ['nl', ''], ['nl', ''],
    ['fn', 'print'], ['p', '('], ['fn', 'salom'], ['p', '('], ['st', '"Mirae"'], ['p', '))'],
  ];
</script>

<div class="gate">
  <section class="hero" aria-hidden="true">
    <div class="pattern"></div>
    <div class="hero-in">
      <div class="brand"><BrandMark size="3rem" glow /><span>Mirae <b>Academy</b></span></div>
      <h2>Python'ni <em>amalda</em> oʻrganing</h2>
      <p>Har bir mavzu — qisqa dars, jonli kod va 20 ta mashq. Kod shu yerning oʻzida, internetsiz ishlaydi.</p>
      <div class="term">
        <div class="term-bar"><i></i><i></i><i></i><span>dars.py</span></div>
        <pre>{#each demo as [k, t]}{#if k === 'nl'}{'\n'}{:else}<span class={k}>{t}</span>{/if}{/each}</pre>
        <div class="term-out"><span>›</span> Salom, Mirae!</div>
      </div>
      <ul class="stats">
        <li><b>{sections.length}</b><span>boʻlim</span></li>
        <li><b>{course.totals.topics}</b><span>mavzu</span></li>
        <li><b>{fmt(course.totals.ex)}</b><span>mashq</span></li>
      </ul>
    </div>
  </section>

  <section class="side">
    <div class="card">
      {#if needsCode}
        <ol class="steps" aria-label="Qadamlar">
          <li class:on={step === 'name'} class:done={step === 'code'}><span>{step === 'code' ? '✓' : '1'}</span>Ism</li>
          <li class="bar" class:done={step === 'code'}></li>
          <li class:on={step === 'code'} class:done={success}><span>{success ? '✓' : '2'}</span>{renewing ? 'Yangilash' : 'Faollashtirish'}</li>
        </ol>
      {/if}

      {#if step === 'name'}
        <h1>Xush kelibsiz!</h1>
        <p class="lead">Boshlash uchun ismingizni kiriting — ilova sizga shu ism bilan murojaat qiladi.</p>
        <form onsubmit={submitName}>
          <label for="name">Ism va familiya</label>
          <!-- svelte-ignore a11y_autofocus -->
          <input id="name" bind:value={name} maxlength="60" autocomplete="name" placeholder="Masalan: Madina Karimova" autofocus />
          <button class="btn-primary big" disabled={!nameOk || busy}>{needsCode ? 'Davom etish' : 'Boshlash'} <span aria-hidden="true">→</span></button>
        </form>
      {:else}
        <h1>{success ? 'Tayyor!' : clockBack ? 'Sanani tekshiring' : renewing ? 'Muddat tugadi' : 'Faollashtirish'}</h1>
        {#if success}
          <p class="lead ok">{renewing ? 'Litsenziya yana 1 yilga yangilandi' : 'Ilova 1 yilga faollashtirildi'}. Omad, {name.trim().split(' ')[0]}! 🚀</p>
        {:else if clockBack}
          <p class="lead">Kompyuterdagi sana avval koʻrilgan sanadan oldinga qaytarilgan. Sana va vaqtni toʻgʻri qoʻyib, ilovani qayta oching.</p>
          <div class="notice">🕒 Natijalaringiz, qaydlaringiz va kodlaringiz saqlangan — hech narsa oʻchmaydi.</div>
        {:else if !sent}
          {#if renewing}
            <div class="notice">📅 Bir yillik foydalanish muddati <b>{licenceDate(init?.validUntil ?? 0)}</b> kuni tugadi. Natijalaringiz, XP va qaydlaringiz saqlangan — yangilagach hammasi joyida boʻladi.</div>
          {/if}
          <p class="lead">Bir martalik kod Mirae Academy Telegram botiga yuboriladi. Kodni ustozingizdan oling va shu yerga kiriting. Faollashtirish <b>1 yil</b> amal qiladi.</p>
          <button class="btn-primary big" onclick={send} disabled={busy || resendIn > 0}>
            {busy ? 'Yuborilmoqda…' : resendIn > 0 ? `Kod yuborish (${mmss(resendIn)})` : 'Kod yuborish'}
          </button>
        {:else}
          <p class="lead">6 xonali kod yuborildi. Ustozingizdan olib, kiriting.</p>
          <div class="code" role="group" aria-label="Faollashtirish kodi">
            {#each digits as dg, k}
              <input
                bind:this={boxes[k]}
                value={dg}
                inputmode="numeric"
                autocomplete="one-time-code"
                maxlength="6"
                aria-label={`${k + 1}-raqam`}
                class:filled={dg}
                oninput={(e) => onDigit(k, e)}
                onkeydown={(e) => onKey(k, e)}
                onpaste={onPaste}
                disabled={busy}
              />
            {/each}
          </div>
          <div class="meta">
            <span class:late={expiresIn === 0}>{expiresIn > 0 ? `Kod ${mmss(expiresIn)} amal qiladi` : 'Kod muddati tugadi'}</span>
            <button class="link" onclick={send} disabled={busy || resendIn > 0}>
              {resendIn > 0 ? `Qayta yuborish · ${mmss(resendIn)}` : 'Qayta yuborish'}
            </button>
          </div>
          <button class="btn-primary big" onclick={verify} disabled={code.length !== 6 || busy}>{busy ? 'Tekshirilmoqda…' : 'Faollashtirish'}</button>
        {/if}
        {#if !success && !clockBack}
          <button class="back" onclick={() => { step = 'name'; error = ''; }}>← Ismni oʻzgartirish</button>
        {/if}
      {/if}

      {#if error}<p class="error" role="alert">{error}</p>{/if}
    </div>
    <p class="foot">🔒 Natijalaringiz faqat shu kompyuterda saqlanadi.</p>
  </section>
</div>

<style>
  .gate {
    position: fixed; inset: 0; z-index: 100;
    display: grid;
    grid-template-columns: minmax(0, 1.15fr) minmax(27rem, 0.85fr);
    background: var(--bg);
  }
  .hero {
    position: relative; overflow: hidden;
    display: grid; align-items: center;
    padding: clamp(2rem, 5vw, 5rem);
    background: radial-gradient(120% 90% at 0% 0%, #1b2f86 0%, #0a1240 45%, #050a22 100%);
    color: #edf1ff;
  }
  .pattern {
    position: absolute; inset: -20%;
    background-image:
      radial-gradient(circle at 50% 50%, rgb(57 220 200 / 0.16) 0 1.5px, transparent 2px),
      linear-gradient(45deg, rgb(74 116 255 / 0.07) 1px, transparent 1px),
      linear-gradient(-45deg, rgb(74 116 255 / 0.07) 1px, transparent 1px);
    background-size: 3rem 3rem, 3rem 3rem, 3rem 3rem;
    mask-image: radial-gradient(70% 70% at 70% 40%, #000 0%, transparent 75%);
    animation: drift 40s linear infinite;
  }
  @keyframes drift { to { transform: translate(3rem, 3rem); } }
  .hero-in { position: relative; display: grid; gap: 1.4rem; max-width: 36rem; }
  .brand { display: flex; align-items: center; gap: 0.8rem; font-family: var(--display); font-size: 1.15rem; font-weight: 500; letter-spacing: 0.02em; }
  .brand b { color: var(--gold); font-weight: 700; }
  h2 { margin: 0.6rem 0 0; font-family: var(--display); font-size: clamp(2.2rem, 3.6vw, 3.6rem); line-height: 1.05; font-weight: 700; letter-spacing: -0.02em; }
  h2 em { font-style: normal; background: linear-gradient(90deg, #39dcc8, #8fb0ff); -webkit-background-clip: text; background-clip: text; color: transparent; }
  .hero p { margin: 0; font-size: 1.12rem; line-height: 1.55; color: #b8c3ee; max-width: 32rem; }
  .term { border-radius: 1rem; background: rgb(4 9 30 / 0.85); border: 1px solid rgb(74 116 255 / 0.3); box-shadow: 0 1.5rem 4rem rgb(0 0 0 / 0.45); overflow: hidden; max-width: 30rem; }
  .term-bar { display: flex; align-items: center; gap: 0.4rem; padding: 0.6rem 0.9rem; border-bottom: 1px solid rgb(74 116 255 / 0.18); }
  .term-bar i { width: 0.65rem; height: 0.65rem; border-radius: 50%; background: #ff7a8a; }
  .term-bar i:nth-child(2) { background: #f7bd46; }
  .term-bar i:nth-child(3) { background: #39dcc8; }
  .term-bar span { margin-left: 0.5rem; font: 0.8rem var(--mono); color: #7381b4; }
  .term pre { margin: 0; padding: 1rem 1.1rem; font: 0.95rem/1.65 var(--mono); }
  .kw { color: #39dcc8; font-weight: 600; } .fn { color: #8fb0ff; } .st { color: #f7bd46; } .p { color: #a9b4dd; } .v { color: #edf1ff; }
  .term-out { padding: 0.7rem 1.1rem; border-top: 1px dashed rgb(74 116 255 / 0.25); font: 0.95rem var(--mono); color: #39dcc8; }
  .term-out span { color: #7381b4; margin-right: 0.4rem; }
  .stats { list-style: none; margin: 0.4rem 0 0; padding: 0; display: flex; gap: 2.4rem; }
  .stats li { display: grid; }
  .stats b { font-family: var(--display); font-size: 2rem; font-weight: 700; line-height: 1.1; color: #fff; }
  .stats span { color: #8f9bc8; font-size: 0.92rem; }

  .side { display: grid; align-content: center; justify-items: center; gap: 1.2rem; padding: 2rem; background: var(--bg); }
  .card { width: min(26rem, 100%); display: grid; gap: 1rem; }
  .steps { list-style: none; margin: 0 0 0.6rem; padding: 0; display: flex; align-items: center; gap: 0.7rem; }
  .steps li { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; font-weight: 600; color: var(--text-3); }
  .steps span { display: grid; place-items: center; width: 1.8rem; height: 1.8rem; border-radius: 50%; border: 1px solid var(--line-2); font-size: 0.85rem; }
  .steps li.on { color: var(--text); }
  .steps li.on span { background: var(--lapis); border-color: var(--lapis); color: #fff; box-shadow: 0 0 0 4px rgb(74 116 255 / 0.2); }
  .steps li.done span { background: var(--turq); border-color: var(--turq); color: var(--turq-ink); }
  .steps .bar { flex: 1; height: 2px; background: var(--line); border-radius: 2px; }
  .steps .bar.done { background: var(--turq); }
  h1 { margin: 0; font-family: var(--display); font-size: 2rem; font-weight: 700; letter-spacing: -0.01em; }
  .lead { margin: 0; color: var(--text-2); font-size: 1.02rem; line-height: 1.55; }
  .lead.ok { color: var(--turq); font-weight: 600; }
  .lead b { color: var(--text); }
  .notice { padding: 0.8rem 1rem; border-radius: var(--r-m); background: rgb(247 189 70 / 0.1); border: 1px solid rgb(247 189 70 / 0.35); color: var(--text-2); line-height: 1.55; font-size: 0.95rem; }
  .notice b { color: var(--gold); }
  form { display: grid; gap: 0.6rem; margin-top: 0.3rem; }
  label { font-weight: 600; font-size: 0.9rem; color: var(--text-2); }
  #name {
    height: 3.3rem; padding: 0 1.1rem; border-radius: var(--r-m);
    border: 1px solid var(--line-2); background: var(--surface);
    font-size: 1.1rem; font-weight: 500;
    transition: border-color 0.15s, box-shadow 0.15s;
  }
  #name:focus { outline: none; border-color: var(--lapis); box-shadow: 0 0 0 4px rgb(74 116 255 / 0.18); }
  .big { height: 3.3rem; font-size: 1.05rem; margin-top: 0.3rem; }
  .code { display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.55rem; }
  .code input {
    width: 100%; aspect-ratio: 0.82; text-align: center;
    border-radius: var(--r-m); border: 1px solid var(--line-2); background: var(--surface);
    font: 600 1.8rem var(--mono); font-variant-numeric: tabular-nums;
    transition: border-color 0.15s, box-shadow 0.15s, transform 0.15s;
  }
  .code input:focus { outline: none; border-color: var(--lapis); box-shadow: 0 0 0 4px rgb(74 116 255 / 0.2); transform: translateY(-2px); }
  .code input.filled { border-color: var(--turq); }
  .meta { display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; font-size: 0.88rem; color: var(--text-2); }
  .meta .late { color: var(--rose); }
  .link { border: 0; background: none; color: var(--lapis); font-weight: 600; padding: 0; }
  .link:disabled { color: var(--text-3); cursor: default; }
  .back { justify-self: start; border: 0; background: none; padding: 0.2rem 0; color: var(--text-3); font-weight: 500; }
  .back:hover { color: var(--text); }
  .error { margin: 0; padding: 0.75rem 0.95rem; border-radius: var(--r-s); background: var(--rose-bg); color: var(--rose); font-weight: 500; font-size: 0.92rem; line-height: 1.45; border: 1px solid rgb(255 122 138 / 0.3); }
  .foot { margin: 0; font-size: 0.85rem; color: var(--text-3); }

  @media (max-width: 64em) {
    .gate { grid-template-columns: 1fr; }
    .hero { display: none; }
  }
</style>
