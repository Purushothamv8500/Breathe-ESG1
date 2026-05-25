/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        surface: {
          DEFAULT: '#0f1419',
          raised: '#161b22',
          overlay: '#1c2128',
          border: '#30363d',
        },
        accent: {
          DEFAULT: '#3d9eff',
          muted: '#1f6feb',
        },
      },
      fontFamily: {
        sans: ['Inter', 'Segoe UI', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      },
      boxShadow: {
        card: '0 1px 3px rgba(0,0,0,0.4), 0 0 0 1px rgba(255,255,255,0.04)',
        drawer: '-8px 0 32px rgba(0,0,0,0.5)',
      },
    },
  },
  plugins: [],
}
