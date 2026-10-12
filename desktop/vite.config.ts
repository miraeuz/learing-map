import { defineConfig, type Plugin } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

/**
 * Electron loads the app from file://, where module scripts and `crossorigin`
 * requests are blocked. Emit one classic deferred script instead.
 */
function fileProtocolFriendly(): Plugin {
  return {
    name: 'file-protocol-friendly',
    apply: 'build',
    transformIndexHtml: {
      order: 'post',
      handler(html) {
        return html
          .replace(/<script type="module" crossorigin/g, '<script defer')
          .replace(/ crossorigin(="[^"]*")?/g, '');
      },
    },
  };
}

import { readFileSync } from 'node:fs';

const pkg = JSON.parse(readFileSync(new URL('./package.json', import.meta.url), 'utf8'));

export default defineConfig({
  base: './',
  define: { __APP_VERSION__: JSON.stringify(pkg.version) },
  plugins: [svelte(), fileProtocolFriendly()],
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    target: 'chrome120',
    modulePreload: false,
    rollupOptions: {
      output: { format: 'iife', inlineDynamicImports: true },
    },
  },
});
