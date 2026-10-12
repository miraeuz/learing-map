<script lang="ts">
  import { app, setName } from '../lib/store.svelte';
  import { hasBridge, bridge } from '../lib/license';
  import { showToast } from '../lib/ui.svelte';
  import Modal from './Modal.svelte';

  let name = $state('');
  $effect(() => {
    if (app.profileOpen) name = app.saved.name;
  });
  const ok = $derived(name.trim().length >= 2);
  const close = () => (app.profileOpen = false);

  async function saveName(e: Event) {
    e.preventDefault();
    if (!ok) return;
    setName(name);
    if (hasBridge()) await bridge().license.rename(name.trim());
    close();
    showToast('Ism saqlandi', 'teal');
  }
</script>

<Modal open={app.profileOpen} onClose={close} label="Profil" width="26rem" closable>
  <h2>Profil</h2>
  <form onsubmit={saveName}>
    <label for="pname">Ismingiz</label>
    <!-- svelte-ignore a11y_autofocus -->
    <input id="pname" bind:value={name} maxlength="60" autofocus />
    <button disabled={!ok}>Saqlash</button>
  </form>
</Modal>

<style>
  h2 { margin: 0 0 1rem; font-size: 1.5rem; font-weight: 900; }
  form { display: grid; gap: 0.5rem; }
  label { font-weight: 900; font-size: 0.92rem; }
  input { height: 3rem; padding: 0 1rem; border-radius: 0.9rem; border: 2px solid var(--line); background: #fff; font-size: 1.05rem; font-weight: 800; }
  input:focus { outline: none; border-color: var(--deep); }
  button { height: 3rem; margin-top: 0.5rem; border: 0; border-radius: 0.9rem; background: var(--coral); color: #fff; font-weight: 900; font-size: 1.02rem; box-shadow: 0 0.25rem 0 var(--coral-2); }
  button:disabled { background: var(--stone); box-shadow: 0 0.25rem 0 var(--stone-2); }
</style>
