import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: '../src/refast_echarts/static',
    emptyOutDir: true,
    lib: {
      entry: resolve(__dirname, 'src/index.tsx'),
      name: 'RefastEcharts',
      fileName: () => 'refast-echarts.js',  // Force .js extension
      formats: ['umd'],
    },
    rollupOptions: {
      // React and ReactDOM are provided globally by refast-client.js
      external: ['react', 'react-dom'],
      output: {
        globals: {
          // refast-client.js exposes window.React and window.ReactDOM
          react: 'React',
          'react-dom': 'ReactDOM',
        },
        // Ensure proper UMD output
        name: 'RefastEcharts',
        // Ensure CSS is extracted (if you add styles)
        assetFileNames: 'refast-echarts[extname]',
        // Force .js extension (not .cjs)
        entryFileNames: 'refast-echarts.js',
      },
    },
  },
  define: {
    'process.env': {},
  },
});
