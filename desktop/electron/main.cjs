// Electron shell for ICPC yoʻli: one window, activation in the main process,
// external links open in the browser.
const { app, BrowserWindow, shell, Menu, ipcMain } = require('electron');
const path = require('path');
const os = require('os');
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
}

function createWindow() {
  win = new BrowserWindow({
    width: 1440,
    height: 900,
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
  win.once('ready-to-show', () => win.show());

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
