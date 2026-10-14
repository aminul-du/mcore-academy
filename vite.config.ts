import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({
  plugins: [react()],
  server: { host: true, port: 5182 },
  preview: { host: true, port: 4182 },
  build: { target: 'es2022', sourcemap: true, outDir: 'dist' },
});
