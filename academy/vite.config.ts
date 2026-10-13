import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import { readFileSync } from 'node:fs';

const pkg = JSON.parse(readFileSync(new URL('./package.json', import.meta.url), 'utf8'));

// Served from the app:// protocol in Electron (see electron/main.cjs), so normal ES modules work.
export default defineConfig({
  base: './',
  define: { __APP_VERSION__: JSON.stringify(pkg.version) },
  plugins: [svelte()],
  build: { outDir: 'dist', emptyOutDir: true, target: 'chrome120', chunkSizeWarningLimit: 2000 },
  worker: { format: 'es' },
});
