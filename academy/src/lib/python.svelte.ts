/** Runs Python in a Web Worker (Pyodide). Timeouts terminate and restart the worker. */

export interface PyError { type: string; msg: string; line: number | null }
export interface RunResult { stdout: string; error: PyError | null; timedOut?: boolean; ms: number }
export interface TestResult { call?: string; stdin?: string; ok: boolean; got: string; expect: string; error?: PyError }
export interface CheckResult extends RunResult { results: TestResult[] }

export const py = $state({ status: 'idle' as 'idle' | 'loading' | 'ready' | 'error', version: '', message: '' });

let worker: Worker | null = null;
let seq = 0;
const pending = new Map<number, { resolve: (v: any) => void }>();
let readyPromise: Promise<void> | null = null;

function spawn(): Promise<void> {
  py.status = 'loading';
  worker = new Worker(new URL('./py-worker.js', document.baseURI), { type: 'module' });
  readyPromise = new Promise((resolve, reject) => {
    worker!.onmessage = (ev) => {
      const m = ev.data;
      if (m.type === 'ready') {
        py.status = 'ready';
        py.version = m.version;
        resolve();
      } else if (m.type === 'fatal') {
        py.status = 'error';
        py.message = m.message;
        reject(new Error(m.message));
      } else if (m.type === 'result') {
        pending.get(m.id)?.resolve(m.data);
        pending.delete(m.id);
      }
    };
    worker!.onerror = (e) => {
      py.status = 'error';
      py.message = e.message || 'Python yuklanmadi';
      reject(new Error(py.message));
    };
  });
  return readyPromise;
}

export function warmUp(): Promise<void> {
  if (!worker) return spawn();
  return readyPromise!;
}

function restart() {
  worker?.terminate();
  worker = null;
  for (const p of pending.values()) p.resolve(null);
  pending.clear();
  void spawn();
}

async function call<T>(op: string, payload: Record<string, unknown>, timeoutMs: number): Promise<T & { ms: number; timedOut?: boolean }> {
  await warmUp();
  const id = ++seq;
  const t0 = performance.now();
  const result = await new Promise<any>((resolve) => {
    const timer = setTimeout(() => {
      pending.delete(id);
      resolve({ __timeout: true });
      restart();
    }, timeoutMs);
    pending.set(id, {
      resolve: (v) => {
        clearTimeout(timer);
        resolve(v);
      },
    });
    worker!.postMessage({ id, op, ...payload });
  });
  const ms = Math.round(performance.now() - t0);
  if (!result || result.__timeout) {
    return {
      stdout: '',
      error: { type: 'Timeout', msg: `Kod ${Math.round(timeoutMs / 1000)} soniyada tugamadi — cheksiz sikl boʻlishi mumkin`, line: null },
      results: [],
      timedOut: true,
      ms,
    } as any;
  }
  return { ...result, ms };
}

export const runCode = (code: string, stdin = '', timeoutMs = 6000) => call<RunResult>('run', { code, stdin }, timeoutMs);

export const checkFunction = (code: string, tests: { call: string; expect?: string; raises?: string }[]) =>
  call<CheckResult>('func', { code, tests }, 8000);

export const checkProgram = (code: string, tests: { stdin: string; expect: string }[]) =>
  call<CheckResult>('prog', { code, tests }, 8000);

/** Uzbek explanations for the most common Python errors. */
export function explainError(e: PyError | null): string {
  if (!e) return '';
  const map: Record<string, string> = {
    SyntaxError: 'Sintaksis xatosi: kod Python qoidalariga mos emas (qavs, ikki nuqta yoki qoʻshtirnoq yetishmayotgan boʻlishi mumkin).',
    IndentationError: 'Chekinish xatosi: qatorlar boshidagi boʻsh joylar notoʻgʻri.',
    NameError: 'Nom topilmadi: oʻzgaruvchi yoki funksiya hali yaratilmagan yoki nomi xato yozilgan.',
    TypeError: 'Tur xatosi: amal bu turdagi qiymatlarga mos kelmaydi (masalan, satr + son).',
    ValueError: 'Qiymat xatosi: tur toʻgʻri, lekin qiymat yaroqsiz (masalan, int("abc")).',
    ZeroDivisionError: 'Nolga boʻlish mumkin emas.',
    IndexError: 'Indeks chegaradan tashqarida: roʻyxatda bunday oʻrin yoʻq.',
    KeyError: 'Kalit topilmadi: lugʻatda bunday kalit yoʻq.',
    AttributeError: 'Atribut topilmadi: bu obyektda bunday metod yoki xususiyat yoʻq.',
    EOFError: 'input() uchun kirish maʼlumoti yetmadi — "Kirish" maydoniga qiymat yozing.',
    RecursionError: 'Rekursiya juda chuqur: funksiya oʻzini toʻxtamasdan chaqiryapti.',
    Timeout: 'Vaqt tugadi: kod juda uzoq ishladi.',
  };
  return map[e.type] ?? '';
}
