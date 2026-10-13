<script lang="ts">
  import { onMount } from 'svelte';
  import { app, save, toast } from './lib/store.svelte';
  import { nav } from './lib/nav.svelte';
  import { hasBridge, bridge, licenceDate, RENEW_WARN_DAYS, type LicenseStatus } from './lib/license';
  import { warmUp } from './lib/python.svelte';
  import Gate from './components/Gate.svelte';
  import Sidebar from './components/Sidebar.svelte';
  import Home from './components/Home.svelte';
  import Topic from './components/Topic.svelte';
  import Playground from './components/Playground.svelte';
  import Exams from './components/Exams.svelte';
  import Exam from './components/Exam.svelte';
  import Settings from './components/Settings.svelte';
  import SearchPalette from './components/SearchPalette.svelte';
  import Toast from './components/Toast.svelte';
  import BrandMark from './components/BrandMark.svelte';

  document.documentElement.dataset.theme = app.saved.theme;

  let phase = $state<'boot' | 'gate' | 'app'>('boot');
  let status = $state<LicenseStatus | null>(null);
  let search = $state(false);

  onMount(() => {
    boot();
    // The app may stay open for days: re-check the licence every half hour.
    const timer = hasBridge() ? setInterval(recheck, 30 * 60 * 1000) : null;
    return () => { if (timer) clearInterval(timer); };
  });

  async function boot() {
    if (hasBridge()) {
      try { status = await bridge().license.status(); } catch { status = null; }
    }
    const activated = !hasBridge() || !!status?.activated;
    phase = activated && app.saved.name ? 'app' : 'gate';
    if (phase === 'app') {
      startPython();
      remind();
    }
  }

  async function recheck() {
    if (phase !== 'app') return;
    try {
      const s = await bridge().license.status();
      if (!s.activated && !nav.examActive) {
        status = s;
        phase = 'gate';
      }
    } catch { /* keep working; checked again later */ }
  }

  /** Gentle reminder during the last month of the licence. */
  function remind() {
    const d = status?.daysLeft ?? 0;
    if (!status?.activated || !status.validUntil || d > RENEW_WARN_DAYS) return;
    setTimeout(() => toast(`Litsenziya ${d} kundan keyin tugaydi (${licenceDate(status!.validUntil!)}). Yangilash uchun ustozingizga murojaat qiling.`, { tone: 'gold', ms: 9000 }), 2500);
  }

  function startPython() {
    // Load Python in the background so the first "Run" is instant.
    setTimeout(() => warmUp().catch(() => {}), 600);
  }

  function toggleSide() {
    app.saved.sideCollapsed = !app.saved.sideCollapsed;
    save();
  }

  function onKey(e: KeyboardEvent) {
    if (!(e.ctrlKey || e.metaKey) || phase !== 'app') return;
    const k = e.key.toLowerCase();
    if (k === 'k') {
      e.preventDefault();
      search = !search;
    } else if (k === 'b' && !(e.target as HTMLElement)?.closest?.('.cm-editor, input, textarea')) {
      e.preventDefault();
      toggleSide();
    }
  }
</script>

<svelte:window onkeydown={onKey} />

{#if phase === 'boot'}
  <div class="boot"><BrandMark size="4rem" glow /></div>
{:else if phase === 'gate'}
  {#key status}
    <Gate {status} onDone={async () => {
      if (hasBridge()) {
        try { status = await bridge().license.status(); } catch { /* keep previous */ }
      }
      phase = 'app';
      startPython();
    }} />
  {/key}
{:else}
  <div class="shell" class:collapsed={app.saved.sideCollapsed}>
    {#if app.saved.sideCollapsed}
      <button class="reopen" onclick={toggleSide} title="Yon panelni ochish (Ctrl+B)" aria-label="Yon panelni ochish">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16" /></svg>
      </button>
    {:else}
      <Sidebar onSearch={() => (search = true)} onCollapse={toggleSide} />
    {/if}
    <main>
      {#if nav.route.name === 'home'}
        <Home />
      {:else if nav.route.name === 'topic'}
        <Topic id={nav.route.id} tab={nav.route.tab} ex={nav.route.ex} />
      {:else if nav.route.name === 'playground'}
        <Playground />
      {:else if nav.route.name === 'exams'}
        <Exams />
      {:else if nav.route.name === 'exam'}
        {#key nav.route.sec}<Exam sec={nav.route.sec} />{/key}
      {:else if nav.route.name === 'settings'}
        <Settings />
      {/if}
    </main>
  </div>
  {#if search}<SearchPalette onClose={() => (search = false)} />{/if}
  <Toast />
{/if}

<style>
  .boot { position: fixed; inset: 0; display: grid; place-items: center; background: var(--bg); animation: breathe 1.4s ease-in-out infinite; }
  @keyframes breathe { 50% { opacity: 0.6; transform: scale(0.97); } }
  .shell { display: grid; grid-template-columns: var(--side) minmax(0, 1fr); height: 100vh; }
  .shell.collapsed { grid-template-columns: minmax(0, 1fr); }
  .reopen {
    position: fixed; z-index: 20; top: 0.9rem; left: 0.9rem; width: 2.5rem; height: 2.5rem; display: grid; place-items: center;
    border-radius: 0.75rem; border: 1px solid var(--line); background: color-mix(in srgb, var(--surface) 88%, transparent);
    backdrop-filter: blur(8px); color: var(--text-2); box-shadow: 0 0.5rem 1.4rem rgb(0 0 0 / 0.2);
  }
  .reopen:hover { color: var(--text); border-color: var(--lapis); }
  .reopen svg { width: 1.2rem; height: 1.2rem; fill: none; stroke: currentColor; stroke-width: 2; stroke-linecap: round; }
  main {
    height: 100vh; overflow-y: auto; overflow-x: hidden;
    background:
      radial-gradient(60rem 30rem at 85% -10%, rgb(74 116 255 / 0.12), transparent 60%),
      radial-gradient(40rem 25rem at 0% 110%, rgb(57 220 200 / 0.06), transparent 60%),
      var(--bg);
  }
</style>
