<script lang="ts">
  import type { Snippet } from 'svelte';
  let {
    open,
    onClose,
    label,
    children,
    width = '34rem',
    closable = false,
    flush = false,
  }: {
    open: boolean;
    onClose: () => void;
    label: string;
    children: Snippet;
    width?: string;
    closable?: boolean;
    flush?: boolean;
  } = $props();
</script>

{#if open}
  <!-- Clicking the dimmed backdrop closes the dialog; Esc is handled globally. -->
  <!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
  <div class="backdrop" onclick={onClose}>
    <!-- svelte-ignore a11y_click_events_have_key_events, a11y_no_static_element_interactions -->
    <div
      class="card"
      class:flush
      style:width={`min(${width}, 100%)`}
      role="dialog"
      aria-modal="true"
      aria-label={label}
      tabindex="-1"
      onclick={(e) => e.stopPropagation()}
    >
      {#if closable}
        <button class="x" onclick={onClose} aria-label="Yopish" title="Yopish (Esc)">
          <svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6 6 18" /></svg>
        </button>
      {/if}
      {@render children()}
    </div>
  </div>
{/if}

<style>
  .backdrop { position: fixed; inset: 0; z-index: 60; display: grid; place-items: center; padding: 1rem; background: rgb(6 50 74 / 0.5); animation: fade 0.15s ease-out; }
  .card {
    position: relative;
    max-height: calc(100vh - 2rem);
    overflow-y: auto;
    padding: 1.75rem 1.75rem 1.5rem;
    background: var(--paper);
    border-radius: var(--radius-l);
    box-shadow: 0 1.5rem 4rem rgb(6 50 74 / 0.4);
    animation: pop 0.22s cubic-bezier(0.2, 1.4, 0.4, 1);
  }
  .card.flush { padding: 0; }
  .x {
    position: absolute; top: 0.9rem; right: 0.9rem; z-index: 2;
    display: grid; place-items: center;
    width: 2.4rem; height: 2.4rem;
    border: 0; border-radius: 50%;
    background: rgb(255 255 255 / 0.85);
    box-shadow: 0 1px 4px rgb(6 50 74 / 0.18);
    color: var(--ink);
  }
  .x:hover { background: #fff; transform: rotate(90deg); transition: transform 0.2s; }
  .x svg { width: 1.2rem; height: 1.2rem; fill: none; stroke: currentColor; stroke-width: 2.6; stroke-linecap: round; }
  @keyframes pop { from { transform: scale(0.94); opacity: 0; } }
  @keyframes fade { from { opacity: 0; } }
</style>
