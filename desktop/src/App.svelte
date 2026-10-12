<script lang="ts">
  import { onMount } from 'svelte';
  import { topics } from './lib/data';
  import { app, select, currentIndex } from './lib/store.svelte';
  import Sidebar from './components/Sidebar.svelte';
  import MapView from './components/MapView.svelte';
  import LevelPanel from './components/LevelPanel.svelte';
  import SearchPalette from './components/SearchPalette.svelte';
  import Overlays from './components/Overlays.svelte';

  let map: MapView;
  let panel: LevelPanel;

  const jump = (i: number) => map?.scrollToLevel(i);

  onMount(() => {
    app.selected = currentIndex();
    if (!app.saved.welcomed) app.welcomeOpen = true;
  });

  function onKey(e: KeyboardEvent) {
    const typing = e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement;
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      app.searchOpen = !app.searchOpen;
      return;
    }
    if (e.key === 'Escape') {
      if (app.searchOpen) app.searchOpen = false;
      else if (app.helpOpen) app.helpOpen = false;
      else if (app.welcomeOpen) app.welcomeOpen = false;
      else app.panelOpen = false;
      return;
    }
    if (typing || app.searchOpen || app.welcomeOpen || app.helpOpen || e.ctrlKey || e.metaKey || e.altKey) return;

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
<Overlays />

<style>
  .shell {
    display: grid;
    grid-template-columns: var(--side) minmax(0, 1fr) var(--panel);
    height: 100vh;
  }
  .main { min-width: 0; }
  .panel-slot { min-width: 0; }

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
