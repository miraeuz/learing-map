<script lang="ts">
  import { app, setName, setTheme, resetProgress, exportBackup, importBackup, toast, levelOf, solvedCount, uzDate } from '../lib/store.svelte';
  import { py } from '../lib/python.svelte';
  import { course } from '../lib/course';
  import { onMount } from 'svelte';
  import { hasBridge, bridge, licenceDate, RENEW_WARN_DAYS, type LicenseStatus } from '../lib/license';

  let name = $state(app.saved.name);
  let resetStep = $state(0);
  let lic = $state<LicenseStatus | null>(null);
  onMount(async () => {
    if (hasBridge()) try { lic = await bridge().license.status(); } catch { lic = null; }
  });
  let fileInput: HTMLInputElement;
  const lv = $derived(levelOf(app.saved.xp));
  const since = uzDate(new Date(app.saved.createdAt), { year: true });

  function saveName(e: Event) {
    e.preventDefault();
    if (name.trim().length < 2) return;
    setName(name);
    toast('Ism saqlandi', { tone: 'ok' });
  }

  function download() {
    const blob = new Blob([exportBackup()], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `mirae-academy-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
    toast('Zaxira nusxa yuklab olindi', { tone: 'ok' });
  }

  async function upload(e: Event) {
    const f = (e.target as HTMLInputElement).files?.[0];
    if (!f) return;
    const ok = importBackup(await f.text());
    toast(ok ? 'Natijalar tiklandi' : 'Bu fayl Mirae Academy zaxirasi emas', { tone: ok ? 'ok' : 'info' });
    if (ok) { name = app.saved.name; setTheme(app.saved.theme); }
    (e.target as HTMLInputElement).value = '';
  }

  function doReset() {
    if (resetStep < 2) { resetStep++; return; }
    resetProgress();
    resetStep = 0;
    toast('Natijalar tozalandi', { tone: 'info' });
  }
</script>

<div class="page">
  <h1>Sozlamalar</h1>

  <section class="card profile">
    <div class="av">{(app.saved.name || 'M').split(' ').filter(Boolean).slice(0, 2).map((w) => w[0]?.toUpperCase()).join('')}</div>
    <div class="pinfo">
      <h2>{app.saved.name || 'Oʻquvchi'}</h2>
      <p>{lv.level}-daraja · {lv.rank} · {app.saved.xp} XP · {solvedCount()} / {course.totals.ex} mashq</p>
      <small>{since} dan beri oʻqiyapti</small>
    </div>
  </section>

  <section class="card">
    <h3>Profil</h3>
    <form onsubmit={saveName}>
      <label for="nm">Ism va familiya</label>
      <div class="row">
        <input id="nm" bind:value={name} maxlength="60" />
        <button class="btn-primary" disabled={name.trim().length < 2 || name.trim() === app.saved.name}>Saqlash</button>
      </div>
    </form>
  </section>

  <section class="card">
    <h3>Koʻrinish</h3>
    <div class="themes">
      <button class:on={app.saved.theme === 'dark'} onclick={() => setTheme('dark')}>
        <span class="sw dark"><i></i><i></i></span>Tungi lojuvard
      </button>
      <button class:on={app.saved.theme === 'light'} onclick={() => setTheme('light')}>
        <span class="sw light"><i></i><i></i></span>Kunduzgi qogʻoz
      </button>
    </div>
    <p class="muted">Klaviatura: <kbd>Ctrl</kbd>+<kbd>K</kbd> qidiruv · <kbd>Ctrl</kbd>+<kbd>B</kbd> yon panel · <kbd>F11</kbd> toʻliq ekran · <kbd>Ctrl</kbd>+<kbd>↵</kbd> kodni ishga tushirish · <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>↵</kbd> tekshirish</p>
  </section>

  <section class="card">
    <h3>Zaxira nusxa</h3>
    <p class="muted">Natijalar faqat shu kompyuterda saqlanadi. Boshqa kompyuterga oʻtkazish uchun zaxira faylini yuklab oling va u yerda tiklang.</p>
    <div class="row">
      <button class="btn-ghost" onclick={download}>⬇ Yuklab olish</button>
      <button class="btn-ghost" onclick={() => fileInput.click()}>⬆ Fayldan tiklash</button>
      <input type="file" accept="application/json,.json" bind:this={fileInput} onchange={upload} hidden />
    </div>
  </section>

  <section class="card danger">
    <h3>Natijalarni tozalash</h3>
    <p class="muted">Barcha yechilgan mashqlar, XP, imtihonlar va kod qoralamalari oʻchadi. Ism, rang mavzusi va qaydlaringiz saqlanadi. Bu amalni bekor qilib boʻlmaydi.</p>
    <div class="row">
      <button class="btn-danger" onclick={doReset}>
        {resetStep === 0 ? 'Natijalarni tozalash' : resetStep === 1 ? 'Ishonchingiz komilmi? Yana bosing' : 'Oxirgi tasdiq: HAMMASINI OʻCHIRISH'}
      </button>
      {#if resetStep > 0}<button class="btn-ghost" onclick={() => (resetStep = 0)}>Bekor qilish</button>{/if}
    </div>
  </section>

  <section class="card about">
    <h3>Ilova haqida</h3>
    <dl>
      <dt>Versiya</dt><dd>Mirae Academy {__APP_VERSION__}</dd>
      <dt>Python</dt><dd>{py.version ? `${py.version} (Pyodide, oflayn)` : py.status === 'loading' ? 'yuklanmoqda…' : 'birinchi ishga tushirishda yuklanadi'}</dd>
      <dt>Kurs</dt><dd>{course.totals.topics} mavzu · {course.totals.ex} mashq · {course.totals.lessonCode} ta jonli kod misoli</dd>
      <dt>Faollashtirish</dt>
      <dd>
        {#if !hasBridge()}Brauzer rejimi
        {:else if lic?.activated && lic.validUntil}
          {licenceDate(lic.validUntil)}gacha amal qiladi ·
          <span class:warn={(lic.daysLeft ?? 0) <= RENEW_WARN_DAYS}>{lic.daysLeft} kun qoldi</span>
        {:else}Bu kompyuterda faollashtirilgan{/if}
      </dd>
      <dt>Shriftlar</dt><dd>Unbounded, Onest, JetBrains Mono — SIL Open Font License</dd>
    </dl>
    <p class="muted">© 2026 Mirae Academy. Barcha mashq javoblari kod orqali avtomatik tekshirilgan.</p>
  </section>
</div>

<style>
  .page { display: grid; gap: 1rem; padding: 2rem clamp(1.5rem, 3vw, 3rem) 3rem; max-width: 52rem; margin: 0 auto; }
  h1 { margin: 0 0 0.4rem; font-family: var(--display); font-size: 2rem; font-weight: 700; }
  .warn { color: var(--gold); font-weight: 600; }
  .card { display: grid; gap: 0.8rem; padding: 1.3rem 1.5rem; border-radius: var(--r-l); background: var(--surface); border: 1px solid var(--line); }
  h3 { margin: 0; font-size: 1.05rem; }
  .profile { grid-template-columns: auto 1fr; align-items: center; gap: 1.2rem; background: linear-gradient(135deg, rgb(74 116 255 / 0.16), var(--surface) 70%); }
  .av { display: grid; place-items: center; width: 4.2rem; height: 4.2rem; border-radius: 1.2rem; background: linear-gradient(135deg, var(--lapis), var(--turq-2)); color: #fff; font-family: var(--display); font-weight: 700; font-size: 1.4rem; }
  .pinfo h2 { margin: 0; font-family: var(--display); font-size: 1.35rem; font-weight: 600; }
  .pinfo p { margin: 0.25rem 0; color: var(--text-2); }
  .pinfo small { color: var(--text-3); }
  form { display: grid; gap: 0.4rem; }
  label { font-size: 0.85rem; color: var(--text-3); }
  .row { display: flex; gap: 0.6rem; flex-wrap: wrap; }
  input { flex: 1; min-width: 12rem; height: 2.7rem; padding: 0 0.9rem; border-radius: var(--r-s); border: 1px solid var(--line-2); background: var(--bg-2); }
  input:focus { outline: none; border-color: var(--lapis); }
  .themes { display: grid; grid-template-columns: 1fr 1fr; gap: 0.8rem; }
  .themes button { display: grid; gap: 0.6rem; padding: 0.8rem; border-radius: var(--r-m); border: 2px solid var(--line); background: var(--bg-2); text-align: left; font-weight: 600; }
  .themes button.on { border-color: var(--turq); }
  .sw { display: grid; grid-template-columns: 1fr 2fr; gap: 0.3rem; height: 3.2rem; padding: 0.4rem; border-radius: 0.6rem; }
  .sw i { border-radius: 0.35rem; }
  .sw.dark { background: #060b20; } .sw.dark i:first-child { background: #0f1a42; } .sw.dark i:last-child { background: linear-gradient(135deg, #4a74ff, #39dcc8); }
  .sw.light { background: #f3efe4; } .sw.light i:first-child { background: #fffdf8; } .sw.light i:last-child { background: linear-gradient(135deg, #2446c9, #0e9f8f); }
  .muted { margin: 0; color: var(--text-3); font-size: 0.9rem; line-height: 1.6; }
  .danger { border-color: rgb(255 122 138 / 0.3); }
  .btn-danger { height: 2.6rem; padding: 0 1.1rem; border-radius: var(--r-s); border: 1px solid var(--rose); background: var(--rose-bg); color: var(--rose); font-weight: 600; }
  .btn-danger:hover { background: var(--rose); color: #fff; }
  dl { display: grid; grid-template-columns: max-content 1fr; gap: 0.45rem 1.2rem; margin: 0; font-size: 0.92rem; }
  dt { color: var(--text-3); }
  dd { margin: 0; }
</style>
