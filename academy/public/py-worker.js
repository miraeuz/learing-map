// Web Worker that hosts Python (Pyodide). The page can terminate it at any time,
// which is how infinite loops are stopped.
import { loadPyodide } from './pyodide/pyodide.mjs';

let py = null;
let fns = null;

async function init() {
  const base = new URL('./pyodide/', self.location.href).href;
  py = await loadPyodide({ indexURL: base });
  const harness = await (await fetch(new URL('./harness.py', self.location.href))).text();
  py.runPython(harness);
  fns = {
    run: py.globals.get('run_program'),
    func: py.globals.get('check_function'),
    prog: py.globals.get('check_program'),
  };
  const version = py.runPython('import sys; sys.version.split()[0]');
  self.postMessage({ type: 'ready', version });
}

const ready = init().catch((e) => {
  self.postMessage({ type: 'fatal', message: String(e && e.message ? e.message : e) });
  throw e;
});

self.onmessage = async (ev) => {
  const { id, op, code, stdin, tests } = ev.data;
  try {
    await ready;
    let raw;
    if (op === 'run') raw = fns.run(code, stdin || '');
    else if (op === 'func') raw = fns.func(code, JSON.stringify(tests));
    else if (op === 'prog') raw = fns.prog(code, JSON.stringify(tests));
    else throw new Error('unknown op ' + op);
    self.postMessage({ type: 'result', id, data: JSON.parse(raw) });
  } catch (e) {
    self.postMessage({ type: 'result', id, data: { stdout: '', error: { type: 'InternalError', msg: String(e), line: null } } });
  }
};
