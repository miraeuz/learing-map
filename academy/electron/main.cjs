// Electron shell for Mirae Academy.
// The UI is served from a private app:// protocol (needed for the offline Python runtime),
// activation runs in this main process, and external links open in the user's browser.
const { app, BrowserWindow, shell, Menu, ipcMain, screen, protocol, net } = require('electron');
const path = require('path');
const os = require('os');
const fs = require('fs');
const { pathToFileURL } = require('url');
const { createLicenseManager, decodeSecret } = require('./license.cjs');

let config = { tokenEncoded: '', tokenKey: '', chatId: '' };
try {
  config = require('./config.cjs');
} catch {
  /* dev run without generated config: activation reports "not configured" */
}

app.setPath('userData', path.join(app.getPath('appData'), 'Mirae-Academy'));

protocol.registerSchemesAsPrivileged([
  { scheme: 'app', privileges: { standard: true, secure: true, supportFetchAPI: true, corsEnabled: true, stream: true } },
]);

if (!app.requestSingleInstanceLock()) {
  app.quit();
}

const DIST = path.join(__dirname, '..', 'dist');
let win;
let license;

function serveDist() {
  protocol.handle('app', (request) => {
    const { pathname } = new URL(request.url);
    const rel = decodeURIComponent(pathname).replace(/^\/+/, '') || 'index.html';
    const file = path.normalize(path.join(DIST, rel));
    if (!file.startsWith(DIST)) return new Response('Forbidden', { status: 403 });
    return net.fetch(pathToFileURL(file).toString());
  });
}

function setupIpc() {
  const info = os.userInfo();
  license = createLicenseManager({
    dir: app.getPath('userData'),
    token: decodeSecret(config.tokenEncoded, config.tokenKey),
    chatId: config.chatId,
    machineId: [os.hostname(), info.username, process.platform, process.arch].join('|'),
    machineLabel: `${os.hostname()} (${process.platform} ${os.release()})`,
  });
  ipcMain.handle('license:status', () => license.status());
  ipcMain.handle('license:request', (_e, name) => license.requestCode(name));
  ipcMain.handle('license:verify', (_e, code) => license.verify(code));
  ipcMain.handle('license:rename', (_e, name) => license.rename(name));
  ipcMain.handle('window:toggleFullscreen', () => {
    if (!win) return false;
    win.setFullScreen(!win.isFullScreen());
    return !win.isFullScreen();
  });
  ipcMain.handle('window:isFullscreen', () => Boolean(win && win.isFullScreen()));
}

// Window: opens maximized with normal title-bar buttons; size and position are remembered.
const stateFile = () => path.join(app.getPath('userData'), 'window-state.json');
function readWindowState() {
  try {
    const s = JSON.parse(fs.readFileSync(stateFile(), 'utf8'));
    return { maximized: s.maximized !== false, bounds: s.bounds || null };
  } catch {
    return { maximized: true, bounds: null };
  }
}
function saveWindowState() {
  if (!win) return;
  try {
    fs.mkdirSync(app.getPath('userData'), { recursive: true });
    fs.writeFileSync(stateFile(), JSON.stringify({ maximized: win.isMaximized() || win.isFullScreen(), bounds: win.getNormalBounds() }));
  } catch {
    /* not critical */
  }
}
function visibleBounds(b) {
  if (!b) return null;
  const area = screen.getDisplayMatching(b).workArea;
  const ok = b.x < area.x + area.width - 100 && b.x + b.width > area.x + 100 && b.y >= area.y - 10 && b.y < area.y + area.height - 100;
  return ok ? b : null;
}

function createWindow() {
  const state = readWindowState();
  const area = screen.getPrimaryDisplay().workArea;
  const w = Math.min(1480, area.width);
  const h = Math.min(920, area.height);
  const b = visibleBounds(state.bounds) || {
    width: w,
    height: h,
    x: area.x + Math.round((area.width - w) / 2),
    y: area.y + Math.round((area.height - h) / 2),
  };
  win = new BrowserWindow({
    ...b,
    minWidth: 900,
    minHeight: 600,
    title: 'Mirae Academy',
    backgroundColor: '#060b20',
    icon: path.join(DIST, 'icon.png'),
    autoHideMenuBar: true,
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.cjs'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      spellcheck: false,
    },
  });

  win.loadURL('app://academy/index.html');
  win.once('ready-to-show', () => {
    if (state.maximized) win.maximize();
    win.show();
  });
  win.on('close', saveWindowState);

  const sendFs = () => win.webContents.send('window:fullscreen', win.isFullScreen());
  win.on('enter-full-screen', sendFs);
  win.on('leave-full-screen', sendFs);

  win.webContents.on('before-input-event', (event, input) => {
    if (input.type === 'keyDown' && input.key === 'F11') {
      event.preventDefault();
      win.setFullScreen(!win.isFullScreen());
    }
  });

  win.webContents.setWindowOpenHandler(({ url }) => {
    if (/^https?:\/\//.test(url)) shell.openExternal(url);
    return { action: 'deny' };
  });
  win.webContents.on('will-navigate', (e, url) => {
    if (!url.startsWith('app://')) {
      e.preventDefault();
      if (/^https?:\/\//.test(url)) shell.openExternal(url);
    }
  });
}

app.on('second-instance', () => {
  if (win) {
    if (win.isMinimized()) win.restore();
    win.focus();
  }
});

app.whenReady().then(() => {
  if (process.platform !== 'darwin') Menu.setApplicationMenu(null);
  serveDist();
  setupIpc();
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
