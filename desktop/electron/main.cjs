// Electron shell for ICPC yoʻli: one window, activation in the main process,
// external links open in the browser.
const { app, BrowserWindow, shell, Menu, ipcMain, screen } = require('electron');
const path = require('path');
const os = require('os');
const fs = require('fs');
const { createLicenseManager, decodeSecret } = require('./license.cjs');

let config = { tokenEncoded: '', tokenKey: '', chatId: '' };
try {
  config = require('./config.cjs');
} catch {
  /* dev run without generated config: activation reports "not configured" */
}

if (!app.requestSingleInstanceLock()) {
  app.quit();
}

let win;
let license;

function setupLicense() {
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
  ipcMain.handle('window:toggleFullscreen', () => toggleFullscreen());
  ipcMain.handle('window:isFullscreen', () => Boolean(win && win.isFullScreen()));
}

// Window state: opens maximized (with the normal title bar and taskbar),
// remembers size, position and maximized state between launches.
// F11 is an optional distraction-free full screen; the app never starts in it.
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
    fs.writeFileSync(
      stateFile(),
      JSON.stringify({ maximized: win.isMaximized() || win.isFullScreen(), bounds: win.getNormalBounds() }),
    );
  } catch {
    /* not critical */
  }
}
/** Only reuse saved bounds if they are still visible on a connected screen. */
function visibleBounds(b) {
  if (!b) return null;
  const area = screen.getDisplayMatching(b).workArea;
  const visible = b.x < area.x + area.width - 100 && b.x + b.width > area.x + 100 && b.y >= area.y - 10 && b.y < area.y + area.height - 100;
  return visible ? b : null;
}

function toggleFullscreen() {
  if (!win) return false;
  win.setFullScreen(!win.isFullScreen());
  return !win.isFullScreen();
}

function createWindow() {
  const state = readWindowState();
  const area = screen.getPrimaryDisplay().workArea;
  const b = visibleBounds(state.bounds) || {
    width: Math.min(1440, area.width),
    height: Math.min(900, area.height),
    x: area.x + Math.max(0, Math.round((area.width - Math.min(1440, area.width)) / 2)),
    y: area.y + Math.max(0, Math.round((area.height - Math.min(900, area.height)) / 2)),
  };
  win = new BrowserWindow({
    ...b,
    minWidth: 760,
    minHeight: 560,
    title: 'ICPC yoʻli',
    backgroundColor: '#2BB3D9',
    icon: path.join(__dirname, '..', 'dist', 'icon.png'),
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

  win.loadFile(path.join(__dirname, '..', 'dist', 'index.html'));
  win.once('ready-to-show', () => {
    if (state.maximized) win.maximize();
    win.show();
  });
  win.on('close', saveWindowState);

  const sendFs = () => win.webContents.send('window:fullscreen', win.isFullScreen());
  win.on('enter-full-screen', sendFs);
  win.on('leave-full-screen', sendFs);

  // F11 toggles full screen (there is no menu bar to provide the shortcut).
  win.webContents.on('before-input-event', (event, input) => {
    if (input.type === 'keyDown' && input.key === 'F11') {
      event.preventDefault();
      toggleFullscreen();
    }
  });

  // Problem links open in the user's normal browser, never inside the app.
  win.webContents.setWindowOpenHandler(({ url }) => {
    if (/^https?:\/\//.test(url)) shell.openExternal(url);
    return { action: 'deny' };
  });
  win.webContents.on('will-navigate', (e, url) => {
    if (!url.startsWith('file://')) {
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
  setupLicense();
  createWindow();
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
