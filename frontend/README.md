## Steps to set it up

### Install Node.js & npm

1. Download Node.js LTS (includes npm) from https://nodejs.org/
   - **macOS**: use the `.pkg` installer or `brew install node`
   - **Windows**: run the `.msi` installer as admin
   - **Linux**: install via package manager (`sudo apt install nodejs npm`) or use nvm
2. Verify installation:
   ```bash
   node --version
   npm --version
   ```
   Make sure Node ≥ 18.

#### Helpful resources

- nvm (macOS/Linux): https://github.com/nvm-sh/nvm
- nvm-windows: https://github.com/coreybutler/nvm-windows
- Vite guide: https://vitejs.dev/guide/

---

1. Install project dependencies:

   ```bash
   npm install
   ```

2. Start the dev server:

   ```bash
   npm run dev
   ```

3. Open the Vite URL printed to the console (e.g. `http://localhost:5173/`) in your browser.

   - Visit `/` → full chat layout.
   - Visit `/chat-input`, `/message-bubble`, `/send-button` to inspect each teammate’s component individually (example: `http://localhost:5173/chat-input`).
