<script lang="ts">
  import { app, totals, resetAll, exportJson } from '../lib/store.svelte';
  import { showToast } from '../lib/ui.svelte';
  import Modal from './Modal.svelte';

  const WORD = 'TOZALASH';
  let step = $state<1 | 2>(1);
  let typed = $state('');
  const t = $derived(totals());
  const notes = $derived(Object.keys(app.saved.notes).length);
  const ready = $derived(typed.trim().toUpperCase() === WORD);

  $effect(() => {
    if (app.resetOpen) {
      step = 1;
      typed = '';
    }
  });

  const close = () => (app.resetOpen = false);

  function backup() {
    const blob = new Blob([exportJson()], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `icpc-yoli-zaxira-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(a.href);
    showToast('Zaxira nusxa saqlandi', 'teal');
  }

  function confirmFinal() {
    if (!ready) return;
    resetAll();
    close();
    showToast('Natijalar tozalandi. Yoʻlni qaytadan boshlaymiz!', 'ink');
  }
</script>

<Modal open={app.resetOpen} onClose={close} label="Natijalarni tozalash" width="30rem" closable>
  {#if step === 1}
    <div class="icon" aria-hidden="true">🗑️</div>
    <h2>Natijalarni tozalaysizmi?</h2>
    <p>Quyidagilar butunlay oʻchiriladi:</p>
    <ul>
      <li><b>{t.done + t.practice}</b> ta javob berilgan daraja</li>
      <li><b>{t.solved}</b> ta belgilangan masala</li>
      <li><b>{notes}</b> ta eslatma va oʻrganish roʻyxatidagi belgilar</li>
    </ul>
    <button class="backup" onclick={backup}>Avval zaxira nusxa olish</button>
    <div class="actions">
      <button class="soft" onclick={close}>Bekor qilish</button>
      <button class="danger" onclick={() => (step = 2)}>Davom etish</button>
    </div>
  {:else}
    <div class="icon" aria-hidden="true">⚠️</div>
    <h2>Oxirgi tasdiq</h2>
    <p>Bu amalni qaytarib boʻlmaydi. Tasdiqlash uchun quyiga <b>{WORD}</b> deb yozing.</p>
    <!-- svelte-ignore a11y_autofocus -->
    <input
      bind:value={typed}
      placeholder={WORD}
      aria-label={`Tasdiqlash uchun ${WORD} deb yozing`}
      autofocus
      onkeydown={(e) => e.key === 'Enter' && confirmFinal()}
    />
    <div class="actions">
      <button class="soft" onclick={() => (step = 1)}>Orqaga</button>
      <button class="danger" disabled={!ready} onclick={confirmFinal}>Hammasini tozalash</button>
    </div>
  {/if}
</Modal>

<style>
  .icon { font-size: 2.4rem; }
  h2 { margin: 0.4rem 0 0.5rem; font-size: 1.5rem; font-weight: 900; }
  p { margin: 0 0 0.75rem; color: var(--ink-2); font-weight: 700; line-height: 1.5; }
  ul { margin: 0 0 1rem; padding: 0 0 0 1.2rem; display: grid; gap: 0.3rem; font-weight: 700; }
  .backup { width: 100%; height: 2.8rem; margin-bottom: 1rem; border-radius: 0.9rem; border: 1.5px dashed var(--teal); background: #effaf6; color: var(--teal-2); font-weight: 900; }
  input { width: 100%; height: 3rem; margin-bottom: 1rem; padding: 0 1rem; border-radius: 0.9rem; border: 2px solid var(--line); background: #fff; font-size: 1.1rem; font-weight: 900; letter-spacing: 0.08em; }
  input:focus { outline: none; border-color: var(--coral-2); }
  .actions { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; }
  .soft, .danger { height: 3rem; border-radius: 0.9rem; font-weight: 900; font-size: 1rem; }
  .soft { border: 1.5px solid var(--line); background: #fff; }
  .danger { border: 0; background: #d63b1f; color: #fff; box-shadow: 0 0.25rem 0 #9e2812; }
  .danger:disabled { background: var(--stone); box-shadow: 0 0.25rem 0 var(--stone-2); cursor: default; }
</style>
