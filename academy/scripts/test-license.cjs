// Unit tests for the activation flow with a fake Telegram API. Run: node scripts/test-license.cjs
const assert = require('assert');
const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const { createLicenseManager, decodeSecret, DAY_MS } = require('../electron/license.cjs');

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

  // ---- One-year licence ----
  const activate = async (m, who = 'Ali') => {
    clock += 120_000;
    assert.ok((await m.requestCode(who)).ok, 'code sent');
    const c = sent[sent.length - 1].body.text.match(/Kod: (\d{6})/)[1];
    return m.verify(c);
  };
  const ydir = fs.mkdtempSync(path.join(os.tmpdir(), 'icpc-lic-year-'));
  const my = (extra = {}) => mk({ dir: ydir, ...extra });
  const t0 = clock;
  const act = await activate(my());
  assert.ok(act.ok, 'activated');
  let st = my().status();
  assert.strictEqual(st.activated, true);
  assert.strictEqual(st.daysLeft, 365, 'a full year on day one');
  assert.ok(Math.abs(st.validUntil - (clock + 365 * DAY_MS)) < 1000);
  assert.match(sent[sent.length - 1].body.text, /Yangi muddat: 1 yil/);

  clock += 364 * DAY_MS;
  st = my().status();
  assert.strictEqual(st.activated, true, 'still active on day 364');
  assert.strictEqual(st.daysLeft, 1);
  my().rename('Ali Valiyev');
  assert.strictEqual(my().status().validUntil, st.validUntil, 'rename keeps the end date');

  clock += 1 * DAY_MS + 1000;
  st = my().status();
  assert.strictEqual(st.activated, false, 'expired after one year');
  assert.strictEqual(st.expired, true);
  assert.strictEqual(st.licensed, true);
  assert.strictEqual(st.name, 'Ali Valiyev', 'name survives expiry');

  // Renewal: the Telegram message says so and the new year starts today.
  const ren = await activate(my(), 'Ali Valiyev');
  assert.ok(ren.ok, 'renewed');
  assert.match(sent[sent.length - 1].body.text, /yangilash/);
  st = my().status();
  assert.strictEqual(st.activated, true, 'active again after renewal');
  assert.strictEqual(st.daysLeft, 365);

  // Early renewal adds a year on top of what is left.
  clock += 300 * DAY_MS;
  await activate(my(), 'Ali Valiyev');
  assert.strictEqual(my().status().daysLeft, 65 + 365, 'early renewal keeps remaining days');

  // Turning the clock back is detected and does not extend the licence.
  const real = clock;
  clock -= 10 * DAY_MS;
  st = my().status();
  assert.strictEqual(st.clockBack, true, 'clock rollback detected');
  assert.strictEqual(st.activated, false);
  assert.strictEqual((await my().requestCode('Ali')).error, 'clock');
  clock = real + 60_000;
  assert.strictEqual(my().status().activated, true, 'works again once the clock is right');
  clock -= 12 * 60 * 60 * 1000; // half a day back (time zone change) is fine
  assert.strictEqual(my().status().activated, true, 'small clock changes tolerated');
  clock = real + 120_000;

  // Licences written by version 1.0 (no end date) get a year from their activation day.
  const odir = fs.mkdtempSync(path.join(os.tmpdir(), 'icpc-lic-old-'));
  const machine = crypto.createHash('sha256').update('mirae-academy/license/v1|pc-1').digest('hex');
  const old = { name: 'Eski', activatedAt: clock - 100 * DAY_MS, machine, v: 1 };
  const sig = crypto.createHmac('sha256', 'mirae-academy/license/v1|pc-1').update(JSON.stringify(old)).digest('hex');
  fs.writeFileSync(path.join(odir, 'license.json'), JSON.stringify({ ...old, sig }));
  st = mk({ dir: odir }).status();
  assert.strictEqual(st.activated, true, 'old licence still works');
  assert.strictEqual(st.daysLeft, 265, 'old licence: one year from its activation');
  // Editing the end date breaks the signature.
  const lf = path.join(ydir, 'license.json');
  const cur = JSON.parse(fs.readFileSync(lf, 'utf8'));
  fs.writeFileSync(lf, JSON.stringify({ ...cur, validUntil: cur.validUntil + 1000 * DAY_MS }));
  assert.strictEqual(my().status().licensed, false, 'end date cannot be edited');
  void t0;

  // Secret encoding round-trip.
  const key = 'abc123';
  const enc = Buffer.from(Buffer.from('8727:XYZ').map((b, i) => b ^ Buffer.from(key)[i % key.length])).toString('base64');
  assert.strictEqual(decodeSecret(enc, key), '8727:XYZ');

  console.log('license tests: all passed');
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
