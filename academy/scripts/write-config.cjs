// Writes electron/config.cjs from environment variables at build time.
// The bot token comes from the TELEGRAM_BOT_TOKEN secret and is never committed.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const token = (process.env.TELEGRAM_BOT_TOKEN || '').trim();
const chatId = (process.env.TELEGRAM_CHAT_ID || '8795480827').trim();
const strict = process.argv.includes('--strict');

if (strict && !token) {
  console.error('TELEGRAM_BOT_TOKEN is not set. Add it as a repository secret before building installers.');
  process.exit(1);
}

const key = crypto.randomBytes(24).toString('hex');
const encoded = token
  ? Buffer.from(Buffer.from(token).map((b, i) => b ^ Buffer.from(key)[i % key.length])).toString('base64')
  : '';

const out = path.join(__dirname, '..', 'electron', 'config.cjs');
fs.writeFileSync(
  out,
  `// GENERATED at build time by scripts/write-config.cjs — do not commit.\n` +
    `module.exports = ${JSON.stringify({ tokenEncoded: encoded, tokenKey: key, chatId }, null, 2)};\n`,
);
console.log(`wrote ${path.relative(process.cwd(), out)} (token ${token ? 'set' : 'MISSING'}, chat ${chatId})`);
