<script lang="ts">
  import { onMount } from 'svelte';
  import { topics } from './lib/data';
  import { app, select, currentIndex, setName } from './lib/store.svelte';
  import { hasBridge, bridge, type LicenseStatus } from './lib/license';
  import { showToast } from './lib/ui.svelte';
  import Sidebar from './components/Sidebar.svelte';
  import MapView from './components/MapView.svelte';
  import LevelPanel from './components/LevelPanel.svelte';
  import SearchPalette from './components/SearchPalette.svelte';
  import Overlays from './components/Overlays.svelte';
  import StudyModal from './components/StudyModal.svelte';
  import ConfirmReset from './components/ConfirmReset.svelte';
  import ProfileModal from './components/ProfileModal.svelte';
  import Gate from './components/Gate.svelte';

  let map = $state<MapView>();
  let panel = $state<LevelPanel>();
  let phase = $state<'checking' | 'gate' | 'ready'>('checking');
  let license = $state<LicenseStatus | null>(null);

  const jump = (i: number) => map?.scrollToLevel(i);

  onMount(async () => {
    app.selected = currentIndex();
    if (hasBridge()) {
      try {
        license = await bridge().license.status();
      } catch {
        license = null;
      }
      if (license?.activated && !app.saved.name && license.name) setName(license.name);
    }
    const activated = !hasBridge() || Boolean(license?.activated);
    if (app.saved.name && activated) {
      phase = 'ready';
      const first = app.saved.name.trim().split(/\s+/)[0];
      setTimeout(() => showToast(`Qaytganingizdan xursandmiz, ${first}!`, 'teal'), 500);
    } else {
      phase = 'gate';
    }
  });

  function gateDone() {
    phase = 'ready';
    if (!app.saved.welcomed) app.welcomeOpen = true;
  }

  function onKey(e: KeyboardEvent) {
    if (phase !== 'ready') return;
    const typing = e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement;
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      app.searchOpen = !app.searchOpen;
      return;
    }
    if (e.key === 'Escape') {
      if (app.searchOpen) app.searchOpen = false;
      else if (app.resetOpen) app.resetOpen = false;
      else if (app.profileOpen) app.profileOpen = false;
      else if (app.studyOpen) app.studyOpen = false;
      else if (app.helpOpen) app.helpOpen = false;
      else if (app.welcomeOpen) app.welcomeOpen = false;
      else app.panelOpen = false;
      return;
    }
    const modal = app.searchOpen || app.welcomeOpen || app.helpOpen || app.studyOpen || app.resetOpen || app.profileOpen;
    if (typing || modal || e.ctrlKey || e.metaKey || e.altKey) return;

    const k = e.key;
    if (k === 'ArrowRight' || k === 'ArrowLeft') {
      e.preventDefault();
      const n = Math.max(0, Math.min(topics.length - 1, app.selected + (k === 'ArrowRight' ? 1 : -1)));
      select(n);
      jump(n);
    } else if (k === 'y' || k === 'Y') {
      panel?.respond(true);
    } else if (k === 'n' || k === 'N') {
      panel?.respond(false);
    } else if (k === 'b' || k === 'B') {
      app.studyOpen = true;
    } else if (k === 'c' || k === 'C') {
      const i = currentIndex();
      select(i);
      jump(i);
    } else if (k === '/') {
      e.preventDefault();
      app.searchOpen = true;
    } else if (k === '?') {
      app.helpOpen = true;
    }
  }
</script>

<svelte:window onkeydown={onKey} />

{#if phase === 'gate'}
  <Gate status={license} onDone={gateDone} />
{:else if phase === 'ready'}
  <div class="shell" class:drawer-open={app.panelOpen}>
    <Sidebar onJump={jump} />
    <main class="main">
      <MapView bind:this={map} />
    </main>
    <div class="panel-slot">
      <LevelPanel bind:this={panel} onJump={jump} />
    </div>
  </div>

  <SearchPalette onJump={jump} />
  <StudyModal />
  <ConfirmReset />
  <ProfileModal />
{/if}
<Overlays />

<style>
  .shell {
    display: grid;
    grid-template-columns: var(--side) minmax(0, 1fr) var(--panel);
    height: 100vh;
    animation: enter 0.35s ease-out;
  }
  .main { min-width: 0; }
  .panel-slot { min-width: 0; }

  @keyframes enter { from { opacity: 0; } }

  /* Medium windows: the sidebar becomes an icon rail */
  @media (max-width: 75em) {
    .shell { --side: 5.5rem; }
  }

  /* Narrow windows: the level panel slides over the map */
  @media (max-width: 56em) {
    .shell { grid-template-columns: var(--side) minmax(0, 1fr); }
    .panel-slot {
      position: fixed; top: 0; right: 0; bottom: 0; z-index: 30;
      width: min(30rem, calc(100vw - 5.5rem));
      transform: translateX(calc(100% + 3rem));
      transition: transform 0.28s cubic-bezier(0.3, 0.8, 0.3, 1);
    }
    .drawer-open .panel-slot { transform: none; }
  }
</style>
