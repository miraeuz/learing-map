<script lang="ts">
  import { app } from '../lib/store.svelte';
</script>

{#if app.toast}
  {#key app.toast.id}
    <div class="toast {app.toast.tone ?? 'info'}" role="status" aria-live="polite">
      <span>{app.toast.text}</span>
      {#if app.toast.xp}<b>+{app.toast.xp} XP</b>{/if}
    </div>
  {/key}
{/if}

<style>
  .toast {
    position: fixed; right: 1.6rem; bottom: 1.6rem; z-index: 80;
    display: flex; align-items: center; gap: 0.9rem;
    padding: 0.85rem 1.1rem 0.85rem 1.2rem; border-radius: var(--r-m);
    background: var(--raised); border: 1px solid var(--line-2); box-shadow: 0 1rem 2.6rem rgb(0 0 0 / 0.4);
    font-weight: 600; animation: rise 0.35s cubic-bezier(0.2, 1.3, 0.4, 1);
  }
  .toast.ok { border-color: rgb(57 220 200 / 0.5); }
  .toast.gold { border-color: var(--gold); background: linear-gradient(135deg, rgb(247 189 70 / 0.25), var(--raised)); }
  b { padding: 0.25rem 0.6rem; border-radius: 2rem; background: rgb(247 189 70 / 0.18); color: var(--gold); font-size: 0.88rem; }
  @keyframes rise { from { transform: translateY(1rem) scale(0.96); opacity: 0; } }
</style>
