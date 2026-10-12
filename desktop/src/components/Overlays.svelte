<script lang="ts">
  import { app, markWelcomed } from '../lib/store.svelte';
  import { toast, confetti } from '../lib/ui.svelte';
  import Modal from './Modal.svelte';
  import BrandMark from './BrandMark.svelte';

  // ---------- toast ----------
  let visible = $state(false);
  let timer: ReturnType<typeof setTimeout>;
  $effect(() => {
    if (toast.id === 0) return;
    visible = true;
    clearTimeout(timer);
    timer = setTimeout(() => (visible = false), 2200);
  });

  // ---------- confetti ----------
  let canvas: HTMLCanvasElement;
  $effect(() => {
    if (confetti.id === 0 || !canvas) return;
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const ctx = canvas.getContext('2d')!;
    const dpr = devicePixelRatio || 1;
    canvas.width = innerWidth * dpr;
    canvas.height = innerHeight * dpr;
    ctx.scale(dpr, dpr);
    const colors = ['#FFC233', '#FF6B4A', '#14A38B', '#FFFFFF', '#5FCDEB'];
    const parts = Array.from({ length: 90 }, () => {
      const a = -Math.PI / 2 + (Math.random() - 0.5) * Math.PI * 1.1;
      const v = 420 + Math.random() * 560;
      return {
        x: confetti.x, y: confetti.y, vx: Math.cos(a) * v, vy: Math.sin(a) * v,
        c: colors[(Math.random() * colors.length) | 0], s: 6 + Math.random() * 7,
        r: Math.random() * Math.PI, w: (Math.random() - 0.5) * 12,
      };
    });
    let last = performance.now();
    const start = last;
    let raf = 0;
    const tick = (now: number) => {
      const dt = Math.min(0.033, (now - last) / 1000);
      last = now;
      const life = (now - start) / 1700;
      ctx.clearRect(0, 0, innerWidth, innerHeight);
      ctx.globalAlpha = Math.max(0, 1 - life);
      for (const p of parts) {
        p.vx *= 0.985; p.vy = p.vy * 0.985 + 950 * dt;
        p.x += p.vx * dt; p.y += p.vy * dt; p.r += p.w * dt;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r);
        ctx.fillStyle = p.c; ctx.fillRect(-p.s / 2, -p.s * 0.28, p.s, p.s * 0.56);
        ctx.restore();
      }
      if (life < 1) raf = requestAnimationFrame(tick);
      else ctx.clearRect(0, 0, innerWidth, innerHeight);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  });

  function closeWelcome() {
    app.welcomeOpen = false;
    markWelcomed();
  }

  const keys: [string, string][] = [
    ['← →', 'Oldingi / keyingi daraja'],
    ['Y', 'Ha, bilaman'],
    ['N', 'Hali yoʻq'],
    ['B', 'Batafsil: oʻrganish roʻyxati'],
    ['C', 'Joriy darajaga oʻtish'],
    ['Ctrl K yoki /', 'Mavzu qidirish'],
    ['Esc', 'Oynani yopish'],
    ['?', 'Shu yordam oynasi'],
  ];
</script>

<canvas bind:this={canvas} class="confetti" aria-hidden="true"></canvas>

<div class="toast {toast.tone}" class:visible role="status" aria-live="polite">{toast.text}</div>

<Modal open={app.welcomeOpen} onClose={closeWelcome} label="Xush kelibsiz">
  <div class="welcome">
    <BrandMark size="4rem" />
    <h2>ICPC yoʻliga xush kelibsiz</h2>
    <ol>
      <li><b>117 ta daraja</b> — ICPC uchun kerak boʻlgan har bir mavzu, asoslardan finalgacha.</li>
      <li>Darajani tanlang: oʻng tomonda nimani oʻrganish kerakligi va <b>15 ta masala</b> chiqadi.</li>
      <li>Yechgan masalangizni <b>katakcha</b> bilan belgilang. Darajadagi oq halqa toʻlib boradi.</li>
      <li>Mavzu oson tuyulsa <b>"Ha, bilaman"</b>, aks holda <b>"Hali yoʻq"</b>. Har qanday javob keyingi darajani ochadi.</li>
    </ol>
    <p class="hint">Hamma narsa shu kompyuterda saqlanadi. Boshqa kompyuterga oʻtkazish uchun chap pastdagi <b>Zaxira</b> tugmasidan foydalaning.</p>
    <button class="go" onclick={closeWelcome}>Yoʻlga chiqish</button>
  </div>
</Modal>

<Modal open={app.helpOpen} onClose={() => (app.helpOpen = false)} label="Klaviatura tugmalari">
  <h2 class="help-title">Klaviatura tugmalari</h2>
  <dl class="keys">
    {#each keys as [k, d]}
      <dt>{#each k.split(' ') as part}{#if part === 'yoki'}<span class="or">yoki</span>{:else}<kbd>{part}</kbd>{/if}{/each}</dt>
      <dd>{d}</dd>
    {/each}
  </dl>
  <button class="go" onclick={() => (app.helpOpen = false)}>Tushunarli</button>
</Modal>

<style>
  .confetti { position: fixed; inset: 0; width: 100vw; height: 100vh; pointer-events: none; z-index: 80; }

  .toast {
    position: fixed; left: 50%; bottom: 1.5rem; z-index: 90;
    transform: translate(-50%, 1rem);
    padding: 0.75rem 1.25rem;
    border-radius: 1rem;
    color: #fff; font-weight: 900; font-size: 1rem;
    box-shadow: var(--shadow);
    opacity: 0; pointer-events: none;
    transition: opacity 0.2s, transform 0.2s;
  }
  .toast.visible { opacity: 1; transform: translate(-50%, 0); }
  .toast.gold { background: var(--gold-2); }
  .toast.teal { background: var(--teal-2); }
  .toast.ink { background: var(--ink); }

  .welcome { display: grid; justify-items: center; text-align: center; }
  h2 { margin: 0.75rem 0 1rem; font-size: 1.6rem; font-weight: 900; }
  ol { margin: 0 0 1rem; padding: 0; list-style: none; display: grid; gap: 0.7rem; text-align: left; counter-reset: s; }
  ol li { counter-increment: s; position: relative; padding-left: 2.6rem; min-height: 1.8rem; font-weight: 700; line-height: 1.45; }
  ol li::before { content: counter(s); position: absolute; left: 0; top: -0.05rem; display: grid; place-items: center; width: 1.8rem; height: 1.8rem; border-radius: 50%; background: var(--coral); color: #fff; font-weight: 900; font-size: 0.95rem; }
  .hint { margin: 0 0 1.2rem; font-size: 0.9rem; color: var(--ink-2); line-height: 1.45; }
  .go {
    width: 100%; height: 3.1rem; border: 0; border-radius: 1rem;
    background: var(--coral); color: #fff; font-size: 1.1rem; font-weight: 900;
    box-shadow: 0 0.3rem 0 var(--coral-2);
  }
  .go:active { transform: translateY(0.25rem); box-shadow: none; }
  .help-title { margin-top: 0; }
  .keys { display: grid; grid-template-columns: auto 1fr; gap: 0.7rem 1.25rem; margin: 0 0 1.4rem; align-items: center; }
  .keys dt { display: flex; gap: 0.3rem; align-items: center; justify-content: flex-end; }
  .keys dd { margin: 0; font-weight: 700; }
  .or { font-size: 0.8rem; color: var(--ink-2); }
</style>
