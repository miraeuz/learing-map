<script lang="ts">
  import { onDestroy, untrack } from 'svelte';
  import { app, setName } from '../lib/store.svelte';
  import { hasBridge, bridge, errorText, type LicenseStatus } from '../lib/license';
  import BrandMark from './BrandMark.svelte';

  let { status, onDone }: { status: LicenseStatus | null; onDone: () => void } = $props();

  // The gate reads the activation status once, when it opens.
  const init = untrack(() => status);
  const needsCode = hasBridge() && !init?.activated;
  let step = $state<'name' | 'code'>(app.saved.name ? 'code' : 'name');
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
    if (!needsCode) return finish();
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
      setTimeout(finish, 900);
    } else {
      error = errorText(r.error, { left: r.left });
      if (r.error === 'too_many' || r.error === 'expired') sent = false;
      digits = ['', '', '', '', '', ''];
      queueMicrotask(() => boxes[0]?.focus());
    }
  }

  function finish() {
    onDone();
  }

  function onDigit(k: number, e: Event) {
    const el = e.target as HTMLInputElement;
    const v = el.value.replace(/\D/g, '');
    if (v.length > 1) {
      // Pasted or autofilled several digits.
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

  // Island preview path for the left panel.
  const pts = Array.from({ length: 9 }, (_, i) => ({ x: 200 + 110 * Math.sin(i * 0.8), y: 560 - i * 62 }));
  const d = pts.slice(1).reduce((acc, b, i) => {
    const a = pts[i], m = (a.y + b.y) / 2;
    return `${acc} C ${a.x} ${m} ${b.x} ${m} ${b.x} ${b.y}`;
  }, `M ${pts[0].x} ${pts[0].y}`);
</script>

<div class="gate">
  <section class="hero" aria-hidden="true">
    <svg viewBox="0 0 400 620" class="route">
      <path {d} class="channel" />
      <path {d} class="wake" />
      {#each pts as p, i}
        <circle cx={p.x} cy={p.y} r="17" class="node {i < 4 ? 'done' : i === 4 ? 'cur' : 'next'}" />
        <text x={p.x} y={p.y + 6} text-anchor="middle" class="num">{i + 1}</text>
      {/each}
      <text x={pts[4].x - 66} y={pts[4].y + 12} font-size="34">⛵</text>
    </svg>
    <div class="hero-text">
      <h2>Asoslardan World Finals gacha</h2>
      <p>Har bir mavzu — orol. Har bir yechilgan masala — oldinga bir qadam.</p>
      <ul>
        <li><b>117</b><span>daraja</span></li>
        <li><b>1 755</b><span>mashq havolasi</span></li>
        <li><b>11</b><span>bosqich</span></li>
      </ul>
    </div>
  </section>

  <section class="side">
    <div class="card">
      <BrandMark size="3.5rem" />
      {#if needsCode}
        <ol class="steps" aria-label="Qadamlar">
          <li class:on={step === 'name'} class:done={step === 'code'}><span>1</span>Ism</li>
          <li class:on={step === 'code'} class:done={success}><span>2</span>Faollashtirish</li>
        </ol>
      {/if}

      {#if step === 'name'}
        <h1>Xush kelibsiz!</h1>
        <p class="lead">Boshlash uchun ismingizni kiriting. Ilova sizga shu ism bilan murojaat qiladi.</p>
        <form onsubmit={submitName}>
          <label for="name">Ismingiz</label>
          <!-- svelte-ignore a11y_autofocus -->
          <input id="name" bind:value={name} maxlength="60" autocomplete="name" placeholder="Masalan: Ali Valiyev" autofocus />
          <button class="primary" disabled={!nameOk || busy}>{needsCode ? 'Davom etish' : 'Boshlash'}</button>
        </form>
      {:else}
        <h1>{success ? 'Tayyor!' : 'Faollashtirish'}</h1>
        {#if success}
          <p class="lead ok">Ilova faollashtirildi. Omad, {name.trim().split(' ')[0]}!</p>
        {:else if !sent}
          <p class="lead">Bir martalik kod ICPC yoʻli Telegram botiga yuboriladi. Kodni administratordan olib, shu yerga kiriting.</p>
          <button class="primary" onclick={send} disabled={busy || resendIn > 0}>
            {busy ? 'Yuborilmoqda…' : resendIn > 0 ? `Kod yuborish (${mmss(resendIn)})` : 'Kod yuborish'}
          </button>
        {:else}
          <p class="lead">6 xonali kod Telegram botga yuborildi. Uni shu yerga kiriting.</p>
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
            <span>{expiresIn > 0 ? `Kod ${mmss(expiresIn)} davomida amal qiladi` : 'Kod muddati tugadi'}</span>
            <button class="link" onclick={send} disabled={busy || resendIn > 0}>
              {resendIn > 0 ? `Qayta yuborish (${mmss(resendIn)})` : 'Qayta yuborish'}
            </button>
          </div>
          <button class="primary" onclick={verify} disabled={code.length !== 6 || busy}>{busy ? 'Tekshirilmoqda…' : 'Faollashtirish'}</button>
        {/if}
        {#if !success}
          <button class="back" onclick={() => { step = 'name'; error = ''; }}>← Ismni oʻzgartirish</button>
        {/if}
      {/if}

      {#if error}<p class="error" role="alert">{error}</p>{/if}
    </div>
    <p class="foot">Natijalaringiz faqat shu kompyuterda saqlanadi.</p>
  </section>
</div>

<style>
  .gate {
    position: fixed; inset: 0; z-index: 100;
    display: grid;
    grid-template-columns: minmax(0, 1.1fr) minmax(26rem, 0.9fr);
    background: var(--paper);
  }
  .hero {
    position: relative;
    display: grid;
    grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
    align-items: center;
    gap: 1rem;
    padding: 3rem clamp(1.5rem, 4vw, 4rem);
    background: var(--lagoon);
    overflow: hidden;
  }
  .route { width: 100%; max-height: 80vh; }
  .channel { fill: none; stroke: rgb(11 95 134 / 0.22); stroke-width: 60; stroke-linecap: round; }
  .wake { fill: none; stroke: var(--gold); stroke-width: 5; stroke-dasharray: 10 12; stroke-linecap: round; }
  .node { stroke: #fff; stroke-width: 3; }
  .node.done { fill: var(--gold); }
  .node.cur { fill: var(--coral); }
  .node.next { fill: var(--stone); }
  .num { fill: #fff; font-weight: 900; font-size: 15px; font-family: Nunito, sans-serif; }
  .hero-text { color: #fff; }
  .hero-text h2 { margin: 0 0 1rem; font-size: clamp(2rem, 3.4vw, 3.4rem); line-height: 1.02; font-weight: 900; letter-spacing: -0.02em; text-wrap: balance; }
  .hero-text p { margin: 0 0 2rem; font-size: 1.15rem; line-height: 1.5; max-width: 26rem; color: rgb(255 255 255 / 0.92); }
  .hero-text ul { list-style: none; margin: 0; padding: 0; display: flex; gap: 2rem; flex-wrap: wrap; }
  .hero-text li { display: grid; }
  .hero-text b { font-size: 2rem; font-weight: 900; line-height: 1; }
  .hero-text span { font-size: 0.9rem; color: rgb(255 255 255 / 0.85); }

  .side { display: grid; align-content: center; justify-items: center; gap: 1rem; padding: 2rem; }
  .card { width: min(26rem, 100%); display: grid; gap: 0.9rem; }
  .steps { list-style: none; margin: 0.5rem 0 0; padding: 0; display: flex; gap: 1.2rem; }
  .steps li { display: flex; align-items: center; gap: 0.45rem; font-size: 0.9rem; font-weight: 800; color: var(--stone-2); }
  .steps span { display: grid; place-items: center; width: 1.6rem; height: 1.6rem; border-radius: 50%; background: var(--paper-2); color: var(--ink-2); font-size: 0.85rem; }
  .steps li.on { color: var(--ink); }
  .steps li.on span { background: var(--coral); color: #fff; }
  .steps li.done span { background: var(--teal); color: #fff; }
  h1 { margin: 0.3rem 0 0; font-size: 2.1rem; font-weight: 900; letter-spacing: -0.01em; }
  .lead { margin: 0; color: var(--ink-2); font-size: 1.02rem; line-height: 1.5; font-weight: 700; }
  .lead.ok { color: var(--teal-2); }
  form { display: grid; gap: 0.5rem; margin-top: 0.4rem; }
  label { font-weight: 900; font-size: 0.92rem; }
  #name {
    height: 3.2rem; padding: 0 1rem;
    border-radius: 1rem; border: 2px solid var(--line); background: #fff;
    font-size: 1.1rem; font-weight: 800;
  }
  #name:focus { outline: none; border-color: var(--deep); }
  .primary {
    height: 3.2rem; margin-top: 0.4rem; border: 0; border-radius: 1rem;
    background: var(--coral); color: #fff; font-size: 1.08rem; font-weight: 900;
    box-shadow: 0 0.3rem 0 var(--coral-2);
  }
  .primary:active:not(:disabled) { transform: translateY(0.25rem); box-shadow: none; }
  .primary:disabled { background: var(--stone); box-shadow: 0 0.3rem 0 var(--stone-2); cursor: default; }
  .code { display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.5rem; margin-top: 0.3rem; }
  .code input {
    width: 100%; aspect-ratio: 0.85; text-align: center;
    border-radius: 0.9rem; border: 2px solid var(--line); background: #fff;
    font-size: 1.7rem; font-weight: 900; font-variant-numeric: tabular-nums;
  }
  .code input:focus { outline: none; border-color: var(--deep); box-shadow: 0 0 0 3px rgb(11 95 134 / 0.15); }
  .code input.filled { border-color: var(--teal); }
  .meta { display: flex; justify-content: space-between; align-items: center; gap: 0.5rem; font-size: 0.88rem; color: var(--ink-2); font-weight: 700; }
  .link { border: 0; background: none; color: var(--deep); font-weight: 900; padding: 0; }
  .link:disabled { color: var(--stone-2); cursor: default; }
  .back { justify-self: start; border: 0; background: none; padding: 0.2rem 0; color: var(--ink-2); font-weight: 800; }
  .back:hover { color: var(--ink); }
  .error { margin: 0; padding: 0.7rem 0.9rem; border-radius: 0.8rem; background: #fde8e3; color: #9a2a12; font-weight: 800; font-size: 0.92rem; line-height: 1.4; }
  .foot { margin: 0; font-size: 0.82rem; color: var(--ink-2); }

  @media (max-width: 62em) {
    .gate { grid-template-columns: 1fr; }
    .hero { display: none; }
  }
</style>
