import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',        // fondamentale per Docker
    port: 5173,
    watch: {
      usePolling: true      // per hot-reload dentro Docker
    },
  },
});