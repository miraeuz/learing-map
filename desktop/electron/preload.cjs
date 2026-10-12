// Exposes a tiny, typed bridge to the page. No Node APIs leak into the renderer.
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('icpc', {
  license: {
    status: () => ipcRenderer.invoke('license:status'),
    request: (name) => ipcRenderer.invoke('license:request', String(name)),
    verify: (code) => ipcRenderer.invoke('license:verify', String(code)),
    rename: (name) => ipcRenderer.invoke('license:rename', String(name)),
  },
});
