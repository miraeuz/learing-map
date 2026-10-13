<script lang="ts">
  import type { Topic } from '../lib/course';
  import LessonCode from './LessonCode.svelte';

  let { topic }: { topic: Topic } = $props();
  // Lesson HTML is generated at build time from our own escaped Markdown (see content/build.py → inline()).
</script>

<article class="lesson">
  {#each topic.blocks as b, i (topic.id + ':' + i)}
    {#if b.t === 'p'}
      <p class:lead={i === 0}>{@html b.html}</p>
    {:else if b.t === 'h'}
      <h2 id={`blk-${i}`}>{b.text}</h2>
    {:else if b.t === 'ul'}
      <ul>{#each b.items as it}<li>{@html it}</li>{/each}</ul>
    {:else if b.t === 'tip'}
      <aside class="note tip"><span aria-hidden="true">💡</span><div>{@html b.html}</div></aside>
    {:else if b.t === 'warn'}
      <aside class="note warn"><span aria-hidden="true">⚠️</span><div>{@html b.html}</div></aside>
    {:else if b.t === 'table'}
      <div class="tbl">
        <table>
          <thead><tr>{#each b.rows[0] as c}<th>{@html c}</th>{/each}</tr></thead>
          <tbody>{#each b.rows.slice(1) as r}<tr>{#each r as c}<td>{@html c}</td>{/each}</tr>{/each}</tbody>
        </table>
      </div>
    {:else if b.t === 'code'}
      <LessonCode block={b} />
    {/if}
  {/each}
</article>

<style>
  .lesson { display: grid; gap: 1.05rem; font-size: 1.04rem; line-height: 1.7; color: var(--text); }
  p { margin: 0; color: var(--text-2); }
  p.lead { font-size: 1.15rem; color: var(--text); line-height: 1.65; }
  p :global(b), li :global(b) { color: var(--text); font-weight: 650; }
  h2 {
    scroll-margin-top: 1.2rem;
    margin: 1.2rem 0 -0.1rem; font-family: var(--display); font-size: 1.28rem; font-weight: 600; letter-spacing: -0.005em;
    display: flex; align-items: center; gap: 0.6rem;
  }
  h2::before { content: ''; width: 0.5rem; height: 1.3rem; border-radius: 0.2rem; background: linear-gradient(var(--turq), var(--lapis)); }
  :global(.lesson :is(p, li, td, th, .note) code) {
    font-size: 0.88em; padding: 0.12em 0.4em; border-radius: 0.35rem;
    background: rgb(74 116 255 / 0.12); color: #9fb8ff; border: 1px solid rgb(74 116 255 / 0.18);
  }
  :global([data-theme='light'] .lesson :is(p, li, td, th, .note) code) { color: var(--lapis-2); background: rgb(36 70 201 / 0.07); }
  ul { margin: 0; padding-left: 0; list-style: none; display: grid; gap: 0.45rem; color: var(--text-2); }
  li { position: relative; padding-left: 1.5rem; }
  li::before { content: ''; position: absolute; left: 0.3rem; top: 0.68em; width: 0.45rem; height: 0.45rem; transform: rotate(45deg); background: var(--turq); border-radius: 0.1rem; }
  .note { display: flex; gap: 0.8rem; padding: 0.9rem 1.1rem; border-radius: var(--r-m); line-height: 1.6; font-size: 0.98rem; }
  .note.tip { background: var(--ok-bg); border: 1px solid rgb(57 220 200 / 0.3); }
  .note.warn { background: rgb(247 189 70 / 0.1); border: 1px solid rgb(247 189 70 / 0.35); }
  .note span { font-size: 1.15rem; line-height: 1.4; }
  .tbl { overflow-x: auto; border-radius: var(--r-m); border: 1px solid var(--line); }
  table { width: 100%; border-collapse: collapse; font-size: 0.95rem; }
  th { text-align: left; padding: 0.65rem 0.9rem; background: var(--surface-2); font-weight: 650; font-size: 0.86rem; color: var(--text-2); }
  td { padding: 0.6rem 0.9rem; border-top: 1px solid var(--line); color: var(--text-2); }
  tbody tr:hover td { background: var(--surface); }
</style>
