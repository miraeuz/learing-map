import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';

// base './' so the built files load from file:// inside Electron.
export default defineConfig({
  base: './',
  plugins: [svelte()],
  build: { outDir: 'dist', emptyOutDir: true, target: 'chrome120' },
});
