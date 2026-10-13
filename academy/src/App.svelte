<script lang="ts">
  import { onMount } from 'svelte';
  import { app } from './lib/store.svelte';
  import { nav } from './lib/nav.svelte';
  import { hasBridge, bridge, type LicenseStatus } from './lib/license';
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

  onMount(async () => {
    if (hasBridge()) {
      try { status = await bridge().license.status(); } catch { status = null; }
    }
    const activated = !hasBridge() || !!status?.activated;
    phase = activated && app.saved.name ? 'app' : 'gate';
    if (phase === 'app') startPython();
  });

  function startPython() {
    // Load Python in the background so the first "Run" is instant.
    setTimeout(() => warmUp().catch(() => {}), 600);
  }

  function onKey(e: KeyboardEvent) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k' && phase === 'app') {
      e.preventDefault();
      search = !search;
    }
  }
</script>

<svelte:window onkeydown={onKey} />

{#if phase === 'boot'}
  <div class="boot"><BrandMark size="4rem" glow /></div>
{:else if phase === 'gate'}
  <Gate {status} onDone={() => { phase = 'app'; startPython(); }} />
{:else}
  <div class="shell">
    <Sidebar onSearch={() => (search = true)} />
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
  main {
    height: 100vh; overflow-y: auto; overflow-x: hidden;
    background:
      radial-gradient(60rem 30rem at 85% -10%, rgb(74 116 255 / 0.12), transparent 60%),
      radial-gradient(40rem 25rem at 0% 110%, rgb(57 220 200 / 0.06), transparent 60%),
      var(--bg);
  }
</style>
