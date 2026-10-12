<script lang="ts">
  import type { Snippet } from 'svelte';
  let { open, onClose, label, children }: { open: boolean; onClose: () => void; label: string; children: Snippet } = $props();
</script>

{#if open}
  <!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
  <div class="backdrop" onclick={onClose}>
    <!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
    <div class="card" role="dialog" aria-modal="true" aria-label={label} tabindex="-1" onclick={(e) => e.stopPropagation()}>
      {@render children()}
    </div>
  </div>
{/if}

<style>
  .backdrop { position: fixed; inset: 0; z-index: 60; display: grid; place-items: center; padding: 1rem; background: rgb(6 50 74 / 0.5); }
  .card {
    width: min(34rem, 100%);
    max-height: calc(100vh - 2rem);
    overflow-y: auto;
    padding: 1.75rem 1.75rem 1.5rem;
    background: var(--paper);
    border-radius: var(--radius-l);
    box-shadow: 0 1.5rem 4rem rgb(6 50 74 / 0.4);
    animation: pop 0.22s cubic-bezier(0.2, 1.4, 0.4, 1);
  }
  @keyframes pop { from { transform: scale(0.94); opacity: 0; } }
</style>
