// One-time activation codes delivered through a Telegram bot.
// Runs only in Electron's main process: the code never reaches the page,
// the page only gets "sent", "ok" or an error reason.
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const CODE_TTL_MS = 10 * 60 * 1000; // a code lives 10 minutes
const RESEND_COOLDOWN_MS = 60 * 1000; // one new code per minute
const MAX_ATTEMPTS = 5; // wrong guesses before the code is burned
const LICENSE_FILE = 'license.json';
const APP_SALT = 'icpc-yoli/license/v1';

function sha256(s) {
  return crypto.createHash('sha256').update(s).digest('hex');
}

/**
 * @param {object} opts
 * @param {string} opts.dir           folder for license.json (app userData)
 * @param {string} opts.token         Telegram bot token
 * @param {string} opts.chatId        chat that receives the codes
 * @param {string} opts.machineId     stable id of this computer
 * @param {string} opts.machineLabel  human-readable computer description for the message
 * @param {Function} [opts.fetch]     fetch implementation (injectable for tests)
 * @param {Function} [opts.now]       clock (injectable for tests)
 */
function createLicenseManager(opts) {
  const fetchImpl = opts.fetch || globalThis.fetch;
  const now = opts.now || Date.now;
  const file = path.join(opts.dir, LICENSE_FILE);
  const machineHash = sha256(`${APP_SALT}|${opts.machineId}`);
  let pending = null; // { hash, salt, expires, attempts, name }
  let lastSent = 0;

  const sign = (data) =>
    crypto.createHmac('sha256', `${APP_SALT}|${opts.machineId}`).update(JSON.stringify(data)).digest('hex');

  function readLicense() {
    try {
      const raw = JSON.parse(fs.readFileSync(file, 'utf8'));
      const { sig, ...data } = raw;
      if (data.machine !== machineHash) return null;
      if (!sig || sig !== sign(data)) return null;
      return data;
    } catch {
      return null;
    }
  }

  function status() {
    const lic = readLicense();
    return {
      configured: Boolean(opts.token && opts.chatId),
      activated: Boolean(lic),
      name: lic ? lic.name : '',
      activatedAt: lic ? lic.activatedAt : 0,
      pending: Boolean(pending && pending.expires > now()),
      expiresAt: pending ? pending.expires : 0,
      resendAt: lastSent ? lastSent + RESEND_COOLDOWN_MS : 0,
    };
  }

  async function requestCode(name) {
    const cleanName = String(name || '').trim().slice(0, 60);
    if (cleanName.length < 2) return { ok: false, error: 'name' };
    if (!opts.token || !opts.chatId) return { ok: false, error: 'not_configured' };
    const t = now();
    if (lastSent && t - lastSent < RESEND_COOLDOWN_MS) {
      return { ok: false, error: 'cooldown', retryAt: lastSent + RESEND_COOLDOWN_MS };
    }

    const code = String(crypto.randomInt(0, 1000000)).padStart(6, '0');
    const salt = crypto.randomBytes(16).toString('hex');
    const text = [
      '🎈 ICPC yoʻli — yangi faollashtirish',
      `👤 Ism: ${cleanName}`,
      `💻 Kompyuter: ${opts.machineLabel}`,
      `🔑 Kod: ${code}`,
      '⏳ 10 daqiqa amal qiladi, bir marta ishlatiladi.',
    ].join('\n');

    let res;
    try {
      res = await fetchImpl(`https://api.telegram.org/bot${opts.token}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: opts.chatId, text }),
        signal: AbortSignal.timeout(15000),
      });
    } catch {
      return { ok: false, error: 'network' };
    }
    let body = null;
    try {
      body = await res.json();
    } catch {
      /* ignore */
    }
    if (!res.ok || !body || body.ok !== true) {
      return { ok: false, error: 'telegram', detail: body && body.description ? String(body.description) : `HTTP ${res.status}` };
    }

    pending = { hash: sha256(salt + code), salt, expires: t + CODE_TTL_MS, attempts: 0, name: cleanName };
    lastSent = t;
    return { ok: true, expiresAt: pending.expires, resendAt: lastSent + RESEND_COOLDOWN_MS };
  }

  function verify(input) {
    const code = String(input || '').replace(/\D/g, '');
    if (!pending) return { ok: false, error: 'no_code' };
    if (pending.expires <= now()) {
      pending = null;
      return { ok: false, error: 'expired' };
    }
    if (code.length !== 6) return { ok: false, error: 'format' };
    const a = Buffer.from(sha256(pending.salt + code), 'hex');
    const b = Buffer.from(pending.hash, 'hex');
    if (!crypto.timingSafeEqual(a, b)) {
      pending.attempts += 1;
      if (pending.attempts >= MAX_ATTEMPTS) {
        pending = null;
        return { ok: false, error: 'too_many' };
      }
      return { ok: false, error: 'wrong', left: MAX_ATTEMPTS - pending.attempts };
    }
    const data = { name: pending.name, activatedAt: now(), machine: machineHash, v: 1 };
    pending = null; // single use
    fs.mkdirSync(opts.dir, { recursive: true });
    fs.writeFileSync(file, JSON.stringify({ ...data, sig: sign(data) }, null, 2));
    return { ok: true, name: data.name };
  }

  function rename(name) {
    const lic = readLicense();
    const cleanName = String(name || '').trim().slice(0, 60);
    if (!lic || cleanName.length < 2) return { ok: false };
    const data = { ...lic, name: cleanName };
    fs.writeFileSync(file, JSON.stringify({ ...data, sig: sign(data) }, null, 2));
    return { ok: true };
  }

  return { status, requestCode, verify, rename };
}

/** Undo the light XOR encoding the build applies so the token is not a plain string in the bundle. */
function decodeSecret(encoded, key) {
  if (!encoded) return '';
  const buf = Buffer.from(encoded, 'base64');
  const k = Buffer.from(key);
  return Buffer.from(buf.map((b, i) => b ^ k[i % k.length])).toString('utf8');
}

module.exports = { createLicenseManager, decodeSecret, CODE_TTL_MS, RESEND_COOLDOWN_MS, MAX_ATTEMPTS };
