<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import { EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter, drawSelection, placeholder as ph } from '@codemirror/view';
  import { EditorState, Compartment } from '@codemirror/state';
  import { defaultKeymap, history, historyKeymap, indentWithTab } from '@codemirror/commands';
  import { python } from '@codemirror/lang-python';
  import { HighlightStyle, syntaxHighlighting, indentOnInput, bracketMatching, indentUnit } from '@codemirror/language';
  import { tags as t } from '@lezer/highlight';

  let {
    value = $bindable(''),
    readonly = false,
    minLines = 4,
    maxHeight = '28rem',
    placeholder = '',
    errorLine = null,
    lang = 'py',
    onRun,
    onCheck,
  }: {
    value?: string;
    readonly?: boolean;
    minLines?: number;
    maxHeight?: string;
    placeholder?: string;
    errorLine?: number | null;
    /** 'py' — Python highlighting; anything else — plain text (shell, HTML, CSV...). */
    lang?: string;
    onRun?: () => void;
    onCheck?: () => void;
  } = $props();

  let host: HTMLDivElement;
  let view: EditorView | null = null;
  const errorComp = new Compartment();

  // Lojuvard syntax colours: turquoise keywords, gold strings, lapis functions.
  const style = HighlightStyle.define([
    { tag: [t.keyword, t.controlKeyword, t.operatorKeyword, t.definitionKeyword, t.moduleKeyword], color: '#39dcc8', fontWeight: '600' },
    { tag: [t.string, t.special(t.string)], color: '#f7bd46' },
    { tag: [t.number, t.bool, t.null], color: '#ff9e7a' },
    { tag: [t.comment, t.lineComment], color: '#7381b4', fontStyle: 'italic' },
    { tag: [t.function(t.variableName), t.function(t.propertyName)], color: '#8fb0ff' },
    { tag: [t.definition(t.variableName), t.definition(t.function(t.variableName))], color: '#c3d2ff', fontWeight: '600' },
    { tag: [t.className, t.definition(t.className)], color: '#ffd27a' },
    { tag: [t.operator, t.punctuation, t.bracket], color: '#a9b4dd' },
    { tag: t.self, color: '#ff9eb5' },
    { tag: [t.variableName, t.propertyName], color: '#edf1ff' },
  ]);

  const theme = EditorView.theme(
    {
      '&': { backgroundColor: 'var(--code-bg)', color: '#edf1ff', fontSize: '0.92rem', borderRadius: '0' },
      '.cm-content': { fontFamily: 'var(--mono)', padding: '0.75rem 0', caretColor: '#39dcc8' },
      '.cm-scroller': { fontFamily: 'var(--mono)', lineHeight: '1.6' },
      '.cm-gutters': { backgroundColor: 'transparent', color: '#4a5a92', border: 'none', paddingLeft: '0.4rem' },
      '.cm-activeLine': { backgroundColor: 'rgb(74 116 255 / 0.08)' },
      '.cm-activeLineGutter': { backgroundColor: 'transparent', color: '#a9b4dd' },
      '&.cm-focused': { outline: 'none' },
      '&.cm-focused .cm-cursor': { borderLeftColor: '#39dcc8', borderLeftWidth: '2px' },
      '.cm-selectionBackground, &.cm-focused .cm-selectionBackground, ::selection': { backgroundColor: 'rgb(57 220 200 / 0.25) !important' },
      '.cm-matchingBracket': { backgroundColor: 'rgb(247 189 70 / 0.18)', outline: 'none' },
      '.cm-placeholder': { color: '#4a5a92' },
      '.cm-error-line': { backgroundColor: 'rgb(255 122 138 / 0.14)' },
    },
    { dark: true },
  );

  onMount(() => {
    const runKeys = keymap.of([
      { key: 'Mod-Enter', run: () => { onRun?.(); return true; } },
      { key: 'Mod-Shift-Enter', run: () => { onCheck?.(); return true; } },
    ]);
    view = new EditorView({
      parent: host,
      state: EditorState.create({
        doc: value,
        extensions: [
          runKeys,
          lineNumbers(),
          highlightActiveLineGutter(),
          highlightActiveLine(),
          history(),
          drawSelection(),
          indentOnInput(),
          bracketMatching(),
          indentUnit.of('    '),
          EditorState.tabSize.of(4),
          keymap.of([indentWithTab, ...defaultKeymap, ...historyKeymap]),
          lang === 'py' ? python() : [],
          syntaxHighlighting(style),
          theme,
          ph(placeholder),
          EditorState.readOnly.of(readonly),
          EditorView.editable.of(!readonly),
          errorComp.of([]),
          EditorView.updateListener.of((u) => {
            if (u.docChanged) value = u.state.doc.toString();
          }),
        ],
      }),
    });
  });

  // Keep the editor in sync when the parent replaces the value (e.g. "reset" or a new exercise).
  $effect(() => {
    const v = value;
    if (view && v !== view.state.doc.toString()) {
      view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: v } });
    }
  });

  // Highlight the line where Python reported an error.
  $effect(() => {
    const line = errorLine;
    if (!view) return;
    const lines = view.state.doc.lines;
    const ext =
      line && line >= 1 && line <= lines
        ? EditorView.theme({ [`.cm-line:nth-child(${line})`]: { backgroundColor: 'rgb(255 122 138 / 0.16)' } })
        : [];
    view.dispatch({ effects: errorComp.reconfigure(ext) });
  });

  onDestroy(() => view?.destroy());

  export function focus() {
    view?.focus();
  }
</script>

<div class="editor" bind:this={host} style:--min={`${minLines * 1.6 + 1.5}rem`} style:--max={maxHeight}></div>

<style>
  .editor { min-height: var(--min); }
  .editor :global(.cm-editor) { min-height: var(--min); max-height: var(--max); }
  .editor :global(.cm-scroller) { min-height: var(--min); }
</style>
