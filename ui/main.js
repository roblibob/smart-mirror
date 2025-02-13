import { app, BrowserWindow } from "electron";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const isDev = process.env.NODE_ENV === "development"; // Detect dev mode

function createWindow() {
    const win = new BrowserWindow({
        width: 1280,
        height: 720,
        webPreferences: {
            nodeIntegration: true,
        },
    });
    win.maximize();
    win.setFullScreen(true);
    win.show();

    if (isDev) {
        // Load Vite dev server
        win.webContents.openDevTools();
        win.loadURL("http://localhost:5173"); // Default Vite dev server port
    } else {
        // Load built production files
        win.loadURL(`file://${path.join(__dirname, "dist", "index.html")}`);
    }
}

app.whenReady().then(createWindow);