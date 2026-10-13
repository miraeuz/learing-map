// Copies the Pyodide runtime (Python compiled to WebAssembly) into public/pyodide
// so the app can run Python fully offline.
const fs = require('fs');
const path = require('path');
const src = path.join(__dirname, '..', 'node_modules', 'pyodide');
const dst = path.join(__dirname, '..', 'public', 'pyodide');
const files = ['pyodide.mjs', 'pyodide.asm.mjs', 'pyodide.asm.wasm', 'python_stdlib.zip', 'pyodide-lock.json'];
fs.mkdirSync(dst, { recursive: true });
for (const f of files) fs.copyFileSync(path.join(src, f), path.join(dst, f));
const ver = JSON.parse(fs.readFileSync(path.join(src, 'package.json'), 'utf8')).version;
console.log(`pyodide ${ver} copied (${files.length} files)`);
