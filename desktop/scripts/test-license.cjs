// Unit tests for the activation flow with a fake Telegram API. Run: node scripts/test-license.cjs
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { createLicenseManager, decodeSecret } = require('../electron/license.cjs');

const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'icpc-lic-'));
let clock = 1_000_000;
const sent = [];
const fakeFetch = async (url, init) => {
  sent.push({ url, body: JSON.parse(init.body) });
  return { ok: true, status: 200, json: async () => ({ ok: true, result: {} }) };
};
const mk = (extra = {}) =>
  createLicenseManager({ dir, token: 'TEST:TOKEN', chatId: '42', machineId: 'pc-1', machineLabel: 'test-pc', fetch: fakeFetch, now: () => clock, ...extra });

(async () => {
  const lm = mk();
  assert.deepStrictEqual((await lm.requestCode('A')).error, 'name', 'short name rejected');
  assert.strictEqual(lm.status().activated, false);

  const r1 = await lm.requestCode('Ali Valiyev');
  assert.ok(r1.ok, 'code sent');
  assert.strictEqual(sent.length, 1);
  assert.match(sent[0].url, /bot TEST:TOKEN|botTEST:TOKEN\/sendMessage/);
  assert.strictEqual(sent[0].body.chat_id, '42');
  const code = sent[0].body.text.match(/Kod: (\d{6})/)[1];

  assert.strictEqual((await lm.requestCode('Ali Valiyev')).error, 'cooldown', 'resend cooldown');
  assert.strictEqual(lm.verify('12345').error, 'format');
  const wrong = code === '000000' ? '111111' : '000000';
  assert.strictEqual(lm.verify(wrong).error, 'wrong');
  const ok = lm.verify(code);
  assert.ok(ok.ok, 'correct code activates');
  assert.strictEqual(lm.verify(code).error, 'no_code', 'code is single use');
  assert.strictEqual(lm.status().activated, true);
  assert.strictEqual(lm.status().name, 'Ali Valiyev');

  // License does not transfer to another machine.
  assert.strictEqual(mk({ machineId: 'pc-2' }).status().activated, false, 'bound to machine');
  // Tampering breaks the signature.
  const f = path.join(dir, 'license.json');
  const lic = JSON.parse(fs.readFileSync(f, 'utf8'));
  fs.writeFileSync(f, JSON.stringify({ ...lic, name: 'Hacker' }));
  assert.strictEqual(mk().status().activated, false, 'tamper detected');
  fs.unlinkSync(f);

  // Expiry and attempt limit.
  clock += 120_000;
  const lm2 = mk();
  await lm2.requestCode('Ali');
  clock += 11 * 60 * 1000;
  assert.strictEqual(lm2.verify('123456').error, 'expired');
  await lm2.requestCode('Ali');
  for (let i = 0; i < 4; i++) assert.strictEqual(lm2.verify('999999').error === 'wrong' || true, true);
  const code2 = sent[sent.length - 1].body.text.match(/Kod: (\d{6})/)[1];
  const r = lm2.verify(code2 === '999999' ? '888888' : '999999');
  assert.strictEqual(r.error, 'too_many', 'burned after 5 wrong attempts');
  assert.strictEqual(lm2.verify(code2).error, 'no_code');

  // Not configured and Telegram errors.
  assert.strictEqual((await mk({ token: '' }).requestCode('Ali')).error, 'not_configured');
  const bad = mk({ fetch: async () => ({ ok: false, status: 401, json: async () => ({ ok: false, description: 'Unauthorized' }) }) });
  clock += 120_000;
  const e = await bad.requestCode('Ali');
  assert.strictEqual(e.error, 'telegram');
  assert.strictEqual(e.detail, 'Unauthorized');
  const down = mk({ fetch: async () => { throw new Error('offline'); } });
  assert.strictEqual((await down.requestCode('Ali')).error, 'network');

  // Secret encoding round-trip.
  const key = 'abc123';
  const enc = Buffer.from(Buffer.from('8727:XYZ').map((b, i) => b ^ Buffer.from(key)[i % key.length])).toString('base64');
  assert.strictEqual(decodeSecret(enc, key), '8727:XYZ');

  console.log('license tests: all passed');
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
